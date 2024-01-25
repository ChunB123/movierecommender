import os
import math
import random
import collections
import json
from itertools import islice
import requests  
import pandas as pd
import numpy as np
import pickle

import tqdm
import spacy


LINK = "http://fall2023-comp585.cs.mcgill.ca:8080/"
with open(f"{os.path.dirname(__file__)}/../data/occupation_similarity.json","r") as infile:
    occupation_similarity = json.load(infile)
    
def curl_req(link:str): 
    response = requests.get(link)   
    return response.json()

# THIS FUNCTION COMPUTES THE COVERAGE AND DIVERSITY OF OUR MODEL  
# FIRST, IT CALCULATES THE PROPORTION OF OF RECOMMENDED MOVIES WITH RESPECT TO THE TOTAL NUMBER OF MOVIES  
# THEN, IT QUANTIFIES THE DIVERSITY OF OUR MODEL BY CALCUATING THE PROPORTION OF MOVIE GENRES WITH RESPECT TO TOTAL NUMBER OF MOVIE IN ITS OWN GENRE,
#       AND WITH RESPECT TO THE TOTAL NUMBER OF MOVIES
# Calculate the proportion of movie genres in all the movie. Then we calculate such proportion in the recommeded movies
def collect_movie_genres(movies:list):
    total_genres = dict()
    for movie in  tqdm.tqdm(movies,desc='Collecting Movie Genre'):
        movie_info = curl_req(f"{LINK}movie/{movie}")
        genres = movie_info['genres']
        for genre in genres:
            if genre['name'] in total_genres:
                total_genres[genre['name']] += 1
            else: 
                total_genres[genre['name']] = 1
    return total_genres
def check_coverage(input_file=f"{os.path.dirname(__file__)}/../data/user_movies.csv",movie_file=f"{os.path.dirname(__file__)}/../data/movies.csv"):
    # Compute what is the proportion of movies that are recommended to user
    recommended_movies = []
    # df = pd.read_csv(input_file)
    # movie_df = pd.read_csv(movie_file)
    df,movie_df,_ = load_pickel_file()
    for idx, row in df.iterrows():
        # recommended_movies += row['movies'].strip("][").replace("'","").split(",")
        recommended_movies += row['movies']
    num_total_movies = len(movie_df.index)
    recommended_movies = [movie.strip() for movie in recommended_movies]
    recommended_movies = list(dict.fromkeys(recommended_movies))
    print("Ratio of recommended films to the entire movies collected: ", len(recommended_movies)/num_total_movies)
    
    collected_genres = collect_movie_genres(movie_df["movieid"])
    print("Total number of movies in each genre")
    print(json.dumps(collected_genres,indent=2)) 
    recommended_genres = collect_movie_genres(recommended_movies)
    recommended_genres_vs_total = dict()
    for genre in recommended_genres:
        recommended_genres[genre] = round(recommended_genres[genre] / collected_genres[genre] * 100,2)
        recommended_genres_vs_total[genre] = round(recommended_genres[genre] / num_total_movies * 100,2)
    print("Ratio of recommended films to the entire movies collected")
    print(json.dumps(recommended_genres,indent=2)) 
    print("Proportion of recommended movies within each genre compared to the sum of all collected movies")
    print(json.dumps(recommended_genres_vs_total,indent=2)) 
    
# THIS FUNCTION COMPUTE THE SIMILARITY BETWEEN OCCUPATIONS USING "SPACY" PYTHON PACKAGE
def compute_occupation_sim(input_file=f"{os.path.dirname(__file__)}/../data/user_movies.csv"):
    users = pd.read_csv(input_file)['userid'].tolist()
    occupations = "" 
    # GET ALL OCCUPATIONS   
    for user in users:        
        info = curl_req(f"{LINK}user/{user}")
        age,occupation, gender = info['age'], info['occupation'] ,info['gender'],
        occupation =  "other" if "other" in occupation else occupation  
        occupation = occupation.replace("/","_").replace(" ","_").replace("-","_")
        if occupation not in occupations: occupations += occupation + " "
    print(occupations)
    occupations  = occupations.strip()
    # LOAD EMBEDDING IN SPACY
    nlp = spacy.load('en_core_web_sm') 
    tokens = nlp(occupations)
    sim = dict()
    # CALCULATE SIMILARITY
    for i in range(0,len(tokens)):
        sim[str(tokens[i])] = dict()
        for j in range(0,len(tokens)):
            if j == i: 
                sim[str(tokens[i])][str(tokens[j])] = 1.0
            else:
                sim[str(tokens[i])][str(tokens[j])] = tokens[i].similarity(tokens[j])
            
    print(sim)
    with open(f"{os.path.dirname(__file__)}/../data/occupation_similarity.json","w") as outfile:
        json.dump(sim,outfile,indent=2)
        
# THIS FUNCTION RETURNS THE AGE, OCCUPATION, & GENDER OF A GIVEN USER
def get_user_info(user_id):
    info = curl_req(f"{LINK}user/{user_id}")
    age,occupation, gender = info['age'], info['occupation'] ,info['gender'],
    occupation =  "other" if "other" in occupation else occupation  
    occupation = occupation.replace("/","_").replace(" ","_").replace("-","_")
    # print("UserId Age Occupation Gender: ", user_id, age, occupation, gender)
    return age, occupation, gender
def get_users_info(userids:list):
    ages, occupations, genders = [], [], []
    for userid in tqdm.tqdm(userids,desc='Collecting user info'):
        age, occupation, gender = get_user_info(userid)
        ages.append(age)
        occupations.append(occupation)
        genders.append(gender)
    return ages, occupations, genders

# THIS FUNCTION COMPUTES THE DISTANCE BETWEEN USERS BASED ON THEIR GENDER, OCCUPATION, & GENDER, USING "compute_occupation_sim" FUNCTION
def compute_user_dist(user_1,user_2):

    age_1,occupation_1, gender_1 = get_user_info(user_1)
    age_2,occupation_2, gender_2 = get_user_info(user_2)
    dist = (abs(age_2-age_1)/100)  + (1-occupation_similarity[occupation_1][occupation_2])  + (0 if gender_1 == gender_2 else 0.5) 
    print(f"distance between users {user_1}, {user_2}: ",dist)

# THIS FUNCTION COMPUTE THE OVERLAP OF RECOMMENDED MOVIES BETWEEN 2 USERS
# COMBINING WITH "compute_user_dist", WE CAN QUANTIFY WHETHER THE MODEL'S OUTPUT IS REASONABLE  
# SPECIFICALLY, IF 2 USERS ARE "CLOSE" ENOUGH, THE MOVIES RECOMMENDED TO THEM SHOULD HAVE A CERTAIN AMOUNT OF OVERLAP;
# ON THE OTHER HAND, IF 2 USERS ARE REALLY "FAR" AWAY, THE MOVIES RECOMMENDED TO THEM SHOULD HAVE CLOSE TO ZERO OVERLAP
def compute_recommedation_overlap(user_1, user_2, input_file=f"{os.path.dirname(__file__)}/../data/user_movies.csv"):
    recommeded_movies = []
    df = pd.read_csv(input_file)
    user_1_movies = df.loc[df['userid']==user_1]['movies'].tolist()[0].strip("][").replace("'","").split(", ")
    
    user_2_movies = df.loc[df['userid']==user_2]['movies'].tolist()[0].strip("][").replace("'","").split(", ")
    
    print("Overlap: ", list(set(user_1_movies) & set(user_2_movies)))
    
def calculate_sparsity(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Replace NaN with 0 for sparsity calculation
    df.fillna(0, inplace=True)
    
    # Count total elements
    total_elements = df.size

    # Count non-zero elements
    non_zero_elements = df.astype(bool).sum().sum()

    # Compute sparsity
    sparsity = 1 - (non_zero_elements / total_elements)

    return sparsity
def get_num_people_by_age_category(df,age_lists):
    df["age_group"] = pd.cut(x=df['age'], bins=[0,age_lists[0][-1],age_lists[1][-1],age_lists[2][-1]], labels=["young","middle_aged","aged"])
    return df

def load_pickel_file(input_file=f"{os.path.dirname(__file__)}/../data/recommendation_user_1.pkl", 
                     movie_file = f"{os.path.dirname(__file__)}/../data/logs_advanced.pkl"):
    # with open (input_file,"rb") as file:
    #     recommendation_lists = pickle.load(file)
    with open (f"{os.path.dirname(__file__)}/../data/new_model/recommendation_user_1.json") as infile:
        recommendation_lists = json.load(infile)
    userids  = recommendation_lists.keys()
    recommendation_list = recommendation_lists.values()
    movies = pd.read_pickle(movie_file)
    movie_temp = {}
    movie_total = []
    for movie in movies['movieID']:
            movie_temp[movie.strip()] = ''
            movie_total.append(movie.strip())
    distinct_movie = list(movie_temp.keys())
    movie_df = pd.DataFrame(distinct_movie, columns=['movieid'])
    df = pd.DataFrame(list(zip(userids,recommendation_list)),columns=['userid','movies'])
    
    return df,movie_df,movie_total
        
def measure_bias(movies:list, genres:dict):
    counter = collections.Counter(movies)
    print("Top 20 most frequently movie:\n", counter.most_common(20))
    sorted_collected_genres = dict(sorted(genres.items(), key=lambda item: item[1],reverse=True))
    print("Most frequently genres")
    print(sorted_collected_genres)

def measure_fairness(input_file=f"{os.path.dirname(__file__)}/../data/user_movies.csv",group='gender',movie_file=f"{os.path.dirname(__file__)}/../data/movies.csv"):
    # group can either be age, occupation, or gender
    if group not in ['age','occupation','gender']:
        raise Exception("Invalid group name. Please choose a group among 'age', 'occupation', 'gender'")
    # df = pd.read_csv(input_file)
    # movie_df = pd.read_csv(movie_file)
    df,movie_df,movie_total = load_pickel_file()
    
    userids = df['userid']
    ages, occupations, genders = get_users_info(userids)
        
    df['age'] = ages
    df['occupation'] = occupations
    df['gender'] = genders
    
    if group == "age":
        age_lists = np.array_split(list(set(sorted(ages))),3)
        print("Age groups: ", age_lists)
        df = get_num_people_by_age_category(df,age_lists)
        group = 'age_group'
    gb = df.groupby(group)
    groups = [gb.get_group(x) for x in gb.groups]
    group_names = list(gb.groups.keys())
    print("Groups:\n", group_names)
    num_total_movies = len(movie_df.index)
    collected_genres = collect_movie_genres(movie_df["movieid"])
    
    # print("Bias of all groups")
    # measure_bias(movie_total,collect_movie_genres(movie_total))
    
    for idx, group_df in enumerate(groups):
        recommended_movies = []
        print("Group: ", group_names[idx])
        for i, row in group_df.iterrows():
            # recommended_movies += row['movies'].strip("][").replace("'","").split(",")
            recommended_movies += row['movies']
        
        # Count movies WITH duplicates, measure bias
        recommended_movies = [movie.strip() for movie in recommended_movies]
        collected_genres_group = collect_movie_genres(recommended_movies)
        measure_bias(recommended_movies,collected_genres_group)
        
        # Count movies WITHOUT duplicates, measure fairness
        recommended_movies = list(dict.fromkeys(recommended_movies))
        recommended_genres = collect_movie_genres(recommended_movies)
        print("Ratio of recommended films to the entire movies collected: ", len(recommended_movies)/num_total_movies)
        print("Total number of movies in each genre")
        print(json.dumps(recommended_genres,indent=2)) 
        
        
        recommended_genres_vs_total = dict()
        for genre in recommended_genres:
            recommended_genres[genre] = round(recommended_genres[genre] / collected_genres[genre] * 100,2)
            recommended_genres_vs_total[genre] = round(recommended_genres[genre] / num_total_movies * 100,2)
            
        print("Ratio of recommended films within each genre to the entire movies collected within each genre")
        print(json.dumps(recommended_genres,indent=2)) 
        print("Proportion of recommended movies within each genre compared to the sum of all collected movies")
        print(json.dumps(recommended_genres_vs_total,indent=2)) 
        
        
    
    # df.loc[df[group]]
    
    # print(df.head())
    
def measure_training_bias(in_file = f"{os.path.dirname(__file__)}/../data/logs_advanced.pkl",df=None):
    if df is None: df = pd.read_pickle(in_file)
    movies = df['movieID']
    counter = collections.Counter(movies)
    print(counter.most_common(20))
    
    log_genres = collect_movie_genres(movies)
    sorted_log_genres = dict(sorted(log_genres.items(), key=lambda item: item[1],reverse=True))
    print("Genre distribution of ALL movie:\n",sorted_log_genres)
    
    log_genres = collect_movie_genres(list(dict.fromkeys(movies)))
    sorted_log_genres = dict(sorted(log_genres.items(), key=lambda item: item[1],reverse=True))
    print("Genre distribution of unique movies:\n",sorted_log_genres)

    
    
    userids = df['userID']
    userids = list(dict.fromkeys(userids))
    ages, occupations, genders = get_users_info(userids)
    ages_counter = collections.Counter(ages)
    occupations_counter = collections.Counter(occupations)
    genders_counter = collections.Counter(genders)
    
    print("Age Distribution:\n",dict(ages_counter.most_common()))
    print("Occupation Distribution:\n",dict(occupations_counter.most_common()))
    print("Gender Distribution:\n",dict(genders_counter.most_common()))
    
def measure_movie_bias_per_genre(train_file = f"{os.path.dirname(__file__)}/../data/logs_advanced.pkl",):
    recommendation_df,movie_df,_ = load_pickel_file()
    recommended_movies = []
    for idx, row in recommendation_df.iterrows():
        # recommended_movies += row['movies'].strip("][").replace("'","").split(",")
        recommended_movies += row['movies']
    # recommended_movies = list(dict.fromkeys(recommended_movies))
    
    train_df = pd.read_pickle(train_file)
    train_movie = train_df['movieID']
    
    def count_movie_frequency(movies:list,n=10):
        result,result_temp = {},{}
        for movie in tqdm.tqdm(movies,desc="Counting movie and genre frequency"):
            movie_info = curl_req(f"{LINK}movie/{movie}")
            genres = movie_info['genres']
            for genre_name in genres:
                genre_name = genre_name['name']
                if genre_name in result_temp:
                    if movie in result_temp[genre_name]:
                        result_temp[genre_name][movie] += 1
                    else:
                        result_temp[genre_name][movie] = 1
                else: 
                    result_temp[genre_name] = {}
                    result_temp[genre_name][movie] = 1
        for genre in result_temp:
            result[genre] = list(islice(dict(sorted(result_temp[genre].items(), key=lambda item: item[1],reverse=True)).items(),n))
        return result
    
    recommended_movie_genre_dist = count_movie_frequency(recommended_movies)
    print("Top 10 popular movies in each gennre in model's prediction")
    print(recommended_movie_genre_dist)
    
    print("Top 10 popular movies in each gennre in training data")
    train_movie_genre_dist = count_movie_frequency(train_movie)
    print(train_movie_genre_dist)
    
def traning_data_balancer(group = 'gender',in_file = f"{os.path.dirname(__file__)}/../data/logs_advanced.pkl",):
    df = pd.read_pickle(in_file)
    userids = df['userID']
    ages, occupations, genders = get_users_info(userids)
        
    df['age'] = ages
    df['occupation'] = occupations
    df['gender'] = genders
    
    if group == 'gender':
        # df_1 needs to be reduced
        # df_2 needs to have more
        # df_1 : df_2 = 1:4
        df_1 = df.loc[df['gender']=='M']
        df_2 = df.loc[df['gender']=='F']
    elif group == 'age':
        df_1 = df.loc[(df['age'] < 36) & (df['age'] > 24)]
        df_2 = df.loc[(df['age']) > 35 | (df['age'] < 25)]
        
    num_df2_log = len(df_2.index)
    num_df1_log = len(df_1.index)
    
    expected_num_df1_log = math.floor(num_df2_log * 1/4)
    random_anchor = random.randrange(0,num_df1_log - expected_num_df1_log,2)
    
    df_1 = df_1.iloc[random_anchor:random_anchor+expected_num_df1_log]
    
    print('Group 1 final counts: ', len(df_1.index))
    print('Group 2 final count: ', len(df_2.index))
    result_df = pd.concat([df_2,df_1],ignore_index=True)
    return result_df
        
        # for idx, group_df in enumerate(groups):
            
        #     print("Group: ", group_names[idx])
        #     percentage = percentages[group_names[idx]]
        #     print(len(group_df.index))
        
def measure_overlap(seed=42,):
    df,movie_df,movie_total = load_pickel_file()
    userids = df['userid']
    ages, occupations, genders = get_users_info(userids)
        
    df['age'] = ages
    df['occupation'] = occupations
    df['gender'] = genders
    df_new = df.loc[(df['gender'] == 'M') & (df['age'] == 25)]
    recommendation_lists = df_new['movies']        
    num_sim_users = len(recommendation_lists.index)
    print("Similar users: ", num_sim_users)
    N = num_sim_users//2
    
    total_num_overlap = 0
    for i in range(N):
        # Sample users
        random.seed(seed + i)
        recommendation_lists_sampled = random.sample(list(recommendation_lists),2)
        # Measure overlap
        
        overlap = set.intersection(*map(set,recommendation_lists_sampled))
        print(overlap)
        total_num_overlap += len(overlap)
    print("Average overlap between two 25-year-old male users: ",round(total_num_overlap / N,1))
        
if __name__ == "__main__":
    # load_pickel_file()
    # measure_training_bias()
    # recommendation_df,movie_df,_ = load_pickel_file()
    # df = pd.read_pickle(f"{os.path.dirname(__file__)}/../data/new_model/users_info_advanced.pkl")
    # print(df)
    # with open (f"{os.path.dirname(__file__)}/../data/new_model/recommendation_user_1.json") as infile:
    #     recommendations = json.load(infile)
    # print(len(recommendations.keys()))
    # measure_overlap(seed=2023585)
    measure_movie_bias_per_genre()
    exit()
    result_df = traning_data_balancer(group='age')
    measure_training_bias(df = result_df)
    exit()
    measure_fairness(group='age')
    exit()
    recommended_movies = []
    for idx, row in recommendation_df.iterrows():
        # recommended_movies += row['movies'].strip("][").replace("'","").split(",")
        recommended_movies += row['movies']
    # recommended_movies = list(dict.fromkeys(recommended_movies))
    # recommended_genres = collect_movie_genres(recommended_movies)
    # recommended_movies = [movie.strip() for movie in recommended_movies]
    collected_genres_group = collect_movie_genres(recommended_movies)
    measure_bias(recommended_movies,collected_genres_group)
    # measure_movie_bias_per_genre()
    exit()
    
    
    file_path = '/home/tyang30/data/user_watchtime_utility_new.csv'
    sparsity = calculate_sparsity(file_path)
    print(f"The sparsity of the CSV file is: {sparsity}")
    
    check_coverage()
    
    compute_user_dist(35723,32880)
    compute_recommedation_overlap(35723,32880)
    
    compute_user_dist(175634,137114)
    compute_recommedation_overlap(175634,137114)
