import sys
import os
import re
import time
import json
import pickle
import requests
import subprocess
import pandas as pd
import numpy as np
from datetime import datetime
from kafka import KafkaConsumer
from collections import OrderedDict
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.email_util import send_email


def _removeLabels(df):
    df.columns.name = None
    df.index.names = ['']
    return df

def is_valid(id, type):
    link = "http://fall2023-comp585.cs.mcgill.ca:8080/"
    try:
        data = requests.get(f"{link}{type}/{id}").json()
    except:
        return False, None
    
    if not ("message" in data):
        if type == "movie":
            return True, data["runtime"]
        else:
            return True, data
        
    return False, None

def process_log(log_line):
    context = log_line.decode('utf-8')
    match = re.search(r',(\d+),GET /data/m/(.+)/(\d+).mpg', context)

    if match:
        user_ID = match.group(1)
        movie_title = match.group(2)
        watch_time = match.group(3)

        return user_ID, movie_title, watch_time
    else:
        return "Invalid log line format"

def read_kafka(max_messages=1000):
    format_string = "%Y-%m-%dT%H:%M:%S"
    consumer = KafkaConsumer(
        'movielog2',
        bootstrap_servers='fall2023-comp585.cs.mcgill.ca:9092',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    # in_out_info = "./data/info/info.json"
    in_out_info = "./data/info/info.pkl"
    # in_out_users = "./data/info/users_info.json"
    # in_out_users_advanced = "./data/info/users_info_advanced.json"
    in_out_users = "./data/info/users_info.pkl"
    in_out_users_advanced = "./data/info/users_info_advanced.pkl"
    # in_out_logs = "./data/logs/logs.csv"
    # in_out_logs_advanced = "./data/logs/logs_advanced.csv"
    in_out_logs = "./data/logs/logs.pkl"
    in_out_logs_advanced = "./data/logs/logs_advanced.pkl"
    
    info = {}
    user_movie_dict = {}
    user_movie_dict_advanced = {}

    # with open(in_out_info, 'r') as file:
    #     info = json.load(file)
    with open(in_out_info, 'rb') as file:
        info = pickle.load(file)

    # with open(in_out_users, 'r') as file:
    #     user_movie_dict = json.load(file)
    with open(in_out_users, 'rb') as file:
        user_movie_dict = pickle.load(file)

    # df = pd.read_csv(in_out_logs, header=None, names=['userID', 'movieID', 'rating'])
    df = pd.read_pickle(in_out_logs)
    # df.drop_duplicates(subset=['userID', 'movieID'], inplace=True)
    # df_advanced = pd.read_csv(in_out_logs_advanced, header=None, names=['userID', 'movieID', 'rating'])
    df_advanced = pd.DataFrame(columns=['userID', 'movieID', 'rating'])

    count = 0
    start_flag = False
    counter = 0

    for message in consumer:
        print(count)
        print(message.value)
        match_duration = re.search(r'(.+),(\d+),GET /data/m/(.+)/(\d+).mpg', message.value.decode('utf-8'))
        match_rating = re.search(r'(.+),(\d+),GET /rate/(.+)=(\d)', message.value.decode('utf-8'))

        if match_duration:
            time_stamp = match_duration.group(1)
            user_ID = match_duration.group(2)
            movie_ID = match_duration.group(3)
            watch_time = match_duration.group(4)
            rating = 0

            if start_flag == False:
                try:
                    old_end_time = datetime.strptime(info["log"]["end_time"], format_string)
                    current_start_time = datetime.strptime(time_stamp, format_string)
                    if current_start_time > old_end_time:
                        start_flag = True
                except:
                    continue
            
            if start_flag == True:
                if count == max_messages - 1:
                    try:
                        current_end_time = datetime.strptime(time_stamp, format_string)
                        info["log"]["end_time"] = time_stamp
                    except:
                        continue

                flag, information = is_valid(user_ID, "user")
                if flag == False:
                    continue

                flag, duration = is_valid(movie_ID, "movie")                    
                if flag == False:
                    continue
                
                if duration == 0:
                    continue

                rating = round(float(int(watch_time) / int(duration)) * 5, 2)
                rating = max(rating, 1)

                if not user_ID in user_movie_dict.keys():
                    user_movie_dict[user_ID] = {
                        "user_info": information,
                        "ratings": {
                            movie_ID: rating
                        }
                    }
                    counter += 1
                else:
                    if movie_ID in user_movie_dict[user_ID]["ratings"].keys():
                        counter += 1
                        if rating > float(user_movie_dict[user_ID]["ratings"][movie_ID]):
                            user_movie_dict[user_ID]["ratings"][movie_ID] = rating   
                    else:
                        user_movie_dict[user_ID]["ratings"][movie_ID] = rating

                mask = (df['userID'] == user_ID) & (df['movieID'] == movie_ID)

                if mask.any():
                    # if float(rating) > float(df.loc[mask, 'rating'].iat[0]):
                    df.loc[mask, 'rating'] = rating
                else:
                    new_row = {'userID': user_ID, 'movieID': movie_ID, 'rating': rating}
                    df.loc[len(df)] = new_row

                count += 1

            if count >= max_messages:
                break

            continue

        if match_rating:
            time_stamp = match_rating.group(1)
            user_ID = match_rating.group(2)
            movie_ID = match_rating.group(3)
            rating = match_rating.group(4)

            if start_flag == False:
                try:
                    old_end_time = datetime.strptime(info["log"]["end_time"], format_string)
                    current_start_time = datetime.strptime(time_stamp, format_string)
                    if current_start_time > old_end_time:
                        start_flag = True
                except:
                    continue
             
            if start_flag == True:
                if count == max_messages - 1:
                    try:
                        current_end_time = datetime.strptime(time_stamp, format_string)
                        info["log"]["end_time"] = time_stamp
                    except:
                        continue

                flag, duration = is_valid(user_ID, "user")
                if flag == False:
                    continue

                flag, duration = is_valid(movie_ID, "movie")                    
                if flag == False:
                    continue
                
                if not user_ID in user_movie_dict.keys():
                    user_movie_dict[user_ID] = {
                        "user_info": information,
                        "ratings": {
                            movie_ID: rating
                        }
                    }
                else:
                    if movie_ID in user_movie_dict[user_ID]["ratings"].keys():
                        counter += 1
                        if float(rating) > float(user_movie_dict[user_ID]["ratings"][movie_ID]):
                            user_movie_dict[user_ID]["ratings"][movie_ID] = rating
                    else:
                        user_movie_dict[user_ID]["ratings"][movie_ID] = rating

                mask = (df['userID'] == user_ID) & (df['movieID'] == movie_ID)

                if mask.any():
                    # if float(rating) > float(df.loc[mask, 'rating'].iat[0]):
                    df.loc[mask, 'rating'] = rating
                else:
                    new_row = {'userID': user_ID, 'movieID': movie_ID, 'rating': rating}
                    df.loc[len(df)] = new_row

                count += 1
        
        if count >= max_messages:
            break
    
    print(counter)
    df['userID'] = df['userID'].astype(int)
    df = df.sort_values(by='userID')
    df.drop_duplicates(subset=['userID', 'movieID'], inplace=True)
    # df.to_csv(in_out_logs, header=False, index=False)
    df.reset_index(drop=True, inplace=True)
    df.to_pickle(in_out_logs)

    for id in df['userID'].unique():
        if df[df['userID'] == int(id)].shape[0] > 1:
            df_advanced = df_advanced._append(df[df['userID'] == int(id)])

    df_advanced['userID'] = df_advanced['userID'].astype(int)
    df_advanced = df_advanced.sort_values(by='userID')
    # df_advanced.to_csv(in_out_logs_advanced, header=False, index=False)
    df_advanced.reset_index(drop=True, inplace=True)
    df_advanced.to_pickle(in_out_logs_advanced)

    for key, value in user_movie_dict.items():
        if len(value["ratings"].keys()) > 1:
            user_movie_dict_advanced[key] = value

    user_movie_dict = OrderedDict(sorted(user_movie_dict.items()))
    user_movie_dict_advanced = OrderedDict(sorted(user_movie_dict_advanced.items()))

    # with open(in_out_users, 'w') as file:
    #     json.dump(user_movie_dict, file, indent=2)
    with open(in_out_users, 'wb') as file:
        pickle.dump(user_movie_dict, file)
    
    # with open(in_out_users_advanced, 'w') as file:
    #     json.dump(user_movie_dict_advanced, file, indent=2)
    with open(in_out_users_advanced, 'wb') as file:
        pickle.dump(user_movie_dict_advanced, file)
    
    # with open(in_out_info, 'w') as file:
    #     json.dump(info, file, indent=2)
    with open(in_out_info, 'wb') as file:
        pickle.dump(info, file)

def preprocess_data(flag):
    data_path = "../data/logs/logs_advanced.pkl"
    df = pd.read_pickle(data_path)
    df['rating'] = df['rating'].astype(float)
    inout_info = "../data/info/info.pkl"
    info = {}
    with open(inout_info, 'rb') as file:
        info = pickle.load(file)
    
    training_data_version = str(int(info["training_data_version"]) + 1)
    # training_data_version = str(int(info["training_data_version"]))
    outfile_training_data = "../data/training_data_versions/data_" + training_data_version + ".txt"
    outfile_users = "../data/training_data_versions/users_" + training_data_version + ".txt"
    outfile_movies = "../data/training_data_versions/movies_" + training_data_version + ".txt"
    
    data_df = df.pivot(index='userID', columns='movieID', values='rating')
    data_df = data_df.fillna(-1)
    data_df = _removeLabels(data_df)

    matrix_ratings = data_df.to_numpy()
    np.savetxt(outfile_training_data, matrix_ratings, fmt='%.2f', delimiter=' ')
    users = np.array(list(data_df.index.values), dtype = int)
    np.savetxt(outfile_users, users, fmt='%d', delimiter=' ')
    print("Number of users: ", len(users))
    movies = np.array(list(data_df.columns.values), dtype = str)
    np.savetxt(outfile_movies, movies, fmt='%s', delimiter=' ')
    print("Number of movies: ", len(movies))

    info["training_data_version"] = int(training_data_version)

    if flag:
        info["pipeline_version"] += 1
        
    with open(inout_info, 'wb') as file:
        pickle.dump(info, file)

    print("Data preprocess finished.")

def train():
    script_file = "../model/train_user.js"
    result = subprocess.run(['node', script_file], stdout=subprocess.PIPE)
    print(result.stdout.decode())

    inout_info = "../data/info/info.pkl"
    info = {}
    with open(inout_info, 'rb') as file:
        info = pickle.load(file)
    
    in_recommendation = "../data/recommendation_versions/recommendation_user_" + str(info["training_data_version"]) + ".json"
    out_recommendation = "../data/recommendation_versions/recommendation_user_" + str(info["training_data_version"]) + ".pkl"
    recommendations = {}
    with open(in_recommendation, 'r') as file:
        recommendations = json.load(file)
    with open(out_recommendation, "wb") as file:
        pickle.dump(recommendations, file)

def main():
    read_kafka(20000)
    preprocess_data(False)
    train()
    send_email("Model training completed.")

if __name__ == "__main__":
    main()
    # preprocess_data()
    # train()