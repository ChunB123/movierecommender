import unittest
from datetime import datetime, timedelta, date
from read_kafka import read_kafka
import os
import json
from utils import curl_req
from json2csv import json2csv 
# from unittest.mock import patch, MagicMock
import tempfile
from model.train import train
import ast  # for converting string representation of list to actual list
import pandas as pd
import coverage



def isValid(id, type="user", link = "http://fall2023-comp585.cs.mcgill.ca:8080/"):
    #this is the exact function used in checking kafka logs in read_kafka.py    
    if type == "user":
        try:
            it_id = int(id)
        except:
            return False
    try:
        info = curl_req(f"{link}{type}/{id}")
        return not ("message" in info) # validate user id
    except Exception as e:
        print(e)
        return False

def validate_kafkaData(input_data):
        if isinstance(input_data, str):
            try:
                input_data = json.loads(input_data)
            except json.JSONDecodeError:
                return False

        if not isinstance(input_data, dict):
            return False

        for key, value in input_data.items():
            if not isinstance(value, dict):
                return False

            if 'duration' not in value or 'rating' not in value:
                return False

            if not isinstance(value['duration'], dict) or not isinstance(value['rating'], dict):
                return False

            if len(value['rating']) > len(value['duration']):
                return False

        return True



class Test(unittest.TestCase):  
    def setUp(self):
         
         #get serial number
        DATE_TEMPLATE = "%Y-%m-%d"
        # begin_date = date.today.strftime(DATE_TEMPLATE)
        begin_date = "2023-10-03"
        self.userids_file = f"data/users@{begin_date}.csv"
        self.outfile_user_movies = f"data/user_movies@{begin_date}.csv"
        self.outfile_common_movies = f"data/common_movies@{begin_date}.csv"
        # self.userids_file = f"data/users.csv"
        # self.outfile_user_movies = f"data/user_movies.csv"
        # self.outfile_common_movies = f"data/common_movies.csv"

        
        ddl_date = "2023-10-04"
        old_kafka_path = f"data/user_movie_new.json"
        # begin_datetime = datetime.strptime(f"{begin_date}",DATE_TEMPLATE)
        # ddl_datetime = datetime.strptime(f"{ddl_date}",DATE_TEMPLATE)
            
        # Collect Kafka logs
        print(f"Collecting kafka logs from {begin_date} to {ddl_date}")
        
        self.input_data = read_kafka(begin_date=begin_date,ddl_date=ddl_date,
                            infile=old_kafka_path,
                            return_json=True)

    def test_valid_dict(self):
        # test_dict_type
        # test_missing_field
        # test_ratings_length_less_than_duration
       
        self.assertTrue(validate_kafkaData(self.input_data))

    def test_invalid_user_id_negative(self):
        self.assertFalse(isValid("-1", "user"))

    
    def test_invalid_user_id_nonnumeric(self):
        self.assertFalse(isValid("aaa", "user"))

    
    def test_invalid_movie_id_numeric(self):
        self.assertFalse(isValid("-1", "movie"))
        self.assertFalse(isValid("10000", "movie"))
    
    def test_nonexisting_movie_id(self):
        self.assertFalse(isValid("asdfghjkl", "movie"))
    
    def test_returned_dataframe(self):
        df = json2csv(self.input_data)
        self.assertIn('userid', df.columns)
        self.assertIn('movieid', df.columns)
        self.assertIn('watchtime', df.columns)
        self.assertIn('movie_duration', df.columns)
        self.assertIn('watchtime_percentage', df.columns)
        self.assertTrue((df['watchtime_percentage'] <= 1.0).all())

    def test_train_function(self):
        #get serial number
        DATE_TEMPLATE = "%Y-%m-%d"
        begin_date = datetime.today().strftime(DATE_TEMPLATE)
        # model serialziation
        outfile_similarity = f"{self.HOME}/data/user_similarity_new@{begin_date}.csv"
        outfile_utility = f"{self.HOME}/data/user_watchtime_utility_new@{begin_date}.csv"
        outfile_users = f"{self.HOME}/data/users@{begin_date}.csv"
        outfile_movies = f"{self.HOME}/data/movies@{begin_date}.csv"
        # outfile_similarity = f"data/user_similarity_new.csv"
        # outfile_utility = f"data/user_watchtime_utility_new.csv"
        # outfile_users = f"data/users.csv"
        # outfile_movies = f"data/movies.csv"
        # Check if files exist
        self.assertTrue(os.path.exists(outfile_similarity))
        self.assertTrue(os.path.exists(outfile_utility))
        self.assertTrue(os.path.exists(outfile_users))
        self.assertTrue(os.path.exists(outfile_movies))

        # Check that all entries in outfile_similarity are <= 1.0
        similarity_df = pd.read_csv(outfile_similarity, index_col=0)
        self.assertTrue((similarity_df.iloc[1:, 1:] <= 1.0).all().all())

        # Check that all entries (except the first row or column) in user_watchtime_utility_new.csv are <= 100.0
        utility_df = pd.read_csv(outfile_utility)
        
        utility_df=utility_df.fillna(0)
        # remove the first row
        utility_df = utility_df.iloc[1:]
        
       
        # check if all entries are less than or equal to 100
        check = utility_df.map(lambda x: x <= 100.0 if isinstance(x, (int, float)) else True)
        self.assertTrue(check.all().all())

        with tempfile.TemporaryDirectory() as temp_dir:
            home = os.path.join(temp_dir, 'test_data')
            os.makedirs(os.path.join(home, 'data'))
            
            train(self, home)

            self.assertTrue(os.path.exists(os.path.join(home, 'data', 'user_similarity_new.csv')))
            self.assertTrue(os.path.exists(os.path.join(home, 'data', 'user_watchtime_utility_new.csv')))
            self.assertTrue(os.path.exists(os.path.join(home, 'data', 'users.csv')))
            self.assertTrue(os.path.exists(os.path.join(home, 'data', 'movies.csv')))

            # Check that all entries in user_similarity_new.csv are <= 1.0
            similarity_file = os.path.join(home, 'data', 'user_similarity_new.csv')
            similarity_df = pd.read_csv(similarity_file, index_col=0)
            self.assertTrue((similarity_df.iloc[1:, 1:] <= 1.0).all().all())

            # Check that all entries in user_watchtime_utility_new.csv are <= 100.0
            utility_file = os.path.join(home, 'data', 'user_similarity_new.csv')
            utility_df = pd.read_csv(utility_file, index_col=0)
            self.assertTrue((utility_df.iloc[1:, 1:] <= 100.0).all().all())
    
    def test_generateCSV(self):
        # Check if users.csv file exists
        self.assertTrue(os.path.exists(self.userids_file), msg="users.csv does not exist")

        # Check if user_movies.csv and common_movies.csv files are created
        self.assertTrue(os.path.exists(self.outfile_user_movies), msg="user_movies.csv was not created")
        self.assertTrue(os.path.exists(self.outfile_common_movies), msg="common_movies.csv was not created")

        # Check the contents of user_movies.csv
        user_movies_df = pd.read_csv(self.outfile_user_movies, index_col=0)
        self.assertFalse(user_movies_df.empty, msg="user_movies.csv is empty")

        # Check the contents of common_movies.csv
        common_movies_df = pd.read_csv(self.outfile_common_movies, index_col=0)
        self.assertFalse(common_movies_df.empty, msg="common_movies.csv is empty")
    
    def test_user_movies_content(self):
        user_movies_df = pd.read_csv(self.outfile_user_movies, index_col=0)
        
        # Check if userid column is int and userid > 0
        self.assertTrue(user_movies_df['userid'].dtype == int, msg="userid column is not int")
        self.assertTrue((user_movies_df['userid'] > 0).all(), msg="userid contains values less than 0")
        
        # Check if movies column is a list of strings
        for movies_str in user_movies_df['movies']:
            try:
                movies_list = ast.literal_eval(movies_str)
                self.assertTrue(isinstance(movies_list, list), msg="movies column is not a list")
                self.assertTrue(all(isinstance(movie, str) for movie in movies_list), msg="movies list contains non-string elements")
            except:
                self.fail(msg="movies column could not be converted to list")
    
    def test_movies_column(self):
        DATE_TEMPLATE = "%Y-%m-%d"
        begin_date = datetime.today().strftime(DATE_TEMPLATE)
        # outfile_users = f"{self.HOME}/data/users@{begin_date}.csv"
        outfile_users = f"data/user_movies.csv"
        df = pd.read_csv(outfile_users)

        for index, row in df.iterrows():
            movies_str = row['movies']
            try:
                movies_list = ast.literal_eval(movies_str)
                self.assertIsInstance(movies_list, list)
                self.assertLessEqual(len(movies_list), 20)
                for movie in movies_list:
                    self.assertIsInstance(movie, str)
            except ValueError:
                self.fail(f"Row index {index} has invalid movies string format")

        
        
if __name__ == '__main__':
    cov = coverage.Coverage(source=['src/'])
    cov.start()

    unittest.main(exit=False)

    cov.stop()
    cov.save()
    cov.report()