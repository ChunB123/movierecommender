import os
import pandas as pd  
import numpy as np  
from copy import deepcopy
from scipy.spatial.distance import pdist, squareform

def calculate_user_rating(userid, similarity_mtx, utility):
    user_rating = utility.iloc[:,userid]
    pred_rating = deepcopy(user_rating)
    
    default_rating = user_rating[user_rating>0].mean()
    numerate = np.dot(similarity_mtx, user_rating)
    corr_sim = similarity_mtx[:, user_rating >0]
    for i,ix in enumerate(pred_rating):
        temp = 0
        if ix < 1:
            w_r = numerate[i]
            sum_w = corr_sim[i,:].sum()
            if w_r == 0 or sum_w == 0:
                temp = default_rating
            else:
                temp = w_r / sum_w
            pred_rating.iloc[i] = temp
    return pred_rating

def recommendation_to_user(userid, top_n, similarity_mtx, utility):
    user_rating = utility.iloc[:,userid-1]
    pred_rating = calculate_user_rating(userid, similarity_mtx, utility)

    top_item = sorted(range(1,len(pred_rating)), key = lambda i: -1*pred_rating.iloc[i])
    top_item = list(filter(lambda x: user_rating.iloc[x]==0, top_item))[:top_n]
    res = []
    for i in top_item:
        res.append(tuple([i, pred_rating.iloc[i]]))
    
    return res

def train(df):
    HOME  = os.path.expanduser("~")
    HOME  = '..'
    outfile_similarity = f"{HOME}/data/user_similarity_new.csv"
    outfile_utility = f"{HOME}/data/user_watchtime_utility_new.csv"
    outfile_users = f"{HOME}/data/users.csv"
    outfile_movies = f"{HOME}/data/movies.csv"
    
    df["watchtime_percentage"] = df["watchtime_percentage"]*100 
    
    utility = df.pivot(index = 'movieid', columns = 'userid', values = 'watchtime_percentage')
    similarity_mtx = utility.fillna(0).corr()
    utlity = _removeLabels(utility)
    similarity_mtx = _removeLabels(similarity_mtx)
    
    utility["mean"] = utility.mean(axis=1,skipna=True)
    utility.to_csv(outfile_utility)
    similarity_mtx.to_csv(outfile_similarity)

    #Generate userid csv and movie csv, remove the duplicates
    df = df.drop(['watchtime', 'movie_duration'], axis=1)
    merged_df = df.pivot(index='userid', columns='movieid', values='watchtime_percentage')
    userIDs = list(merged_df.index.values)
    movieIDs = list(merged_df.columns.values)

    users_df = pd.DataFrame({'userid':userIDs})
    movies_df = pd.DataFrame({'movieid':movieIDs})

    users_df.to_csv(outfile_users)
    movies_df.to_csv(outfile_movies)


def _removeLabels(df):
    df.columns.name = None
    df.index.names = ['']
    return df

def main():
    HOME  = os.path.expanduser("~")
    HOME  = '..'
    outfile_similarity = f"{HOME}/data/user_similarity_new.csv"
    outfile_utility = f"{HOME}/data/user_watchtime_utility_new.csv"
    outfile_users = f"{HOME}/data/users.csv"
    outfile_movies = f"{HOME}/data/movies.csv"
    data_path = f"{HOME}/data/user_watchtime.csv" 
    
    df = pd.read_csv(data_path, 
                     names = ['userid', 'movieid', 'watchtime','movie_duration','watchtime_percentage'])
    
    df["watchtime_percentage"] = df["watchtime_percentage"]*100 
    
    utility = df.pivot(index = 'movieid', columns = 'userid', values = 'watchtime_percentage')
    similarity_mtx = utility.fillna(0).corr()
    utlity = _removeLabels(utility)
    similarity_mtx = _removeLabels(similarity_mtx)
    
    utility["mean"] = utility.mean(axis=1,skipna=True)
    utility.to_csv(outfile_utility)
    similarity_mtx.to_csv(outfile_similarity)

    #Generate userid csv and movie csv, remove the duplicates
    df = df.drop(['watchtime', 'movie_duration'], axis=1)
    merged_df = df.pivot(index='userid', columns='movieid', values='watchtime_percentage')
    userIDs = list(merged_df.index.values)
    movieIDs = list(merged_df.columns.values)

    users_df = pd.DataFrame({'userid':userIDs})
    movies_df = pd.DataFrame({'movieid':movieIDs})

    users_df.to_csv(outfile_users)
    movies_df.to_csv(outfile_movies)
    

if __name__ == "__main__":
    main()