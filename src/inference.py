import os
import pandas as pd
import json

HOME  = os.path.expanduser("~")
HOME  = '..'  
def inference(user_to_predict:str = '4070', top_n:int = 20) -> list:
    outfile_similarity = f"{HOME}/data/user_similarity_new.csv"
    outfile_utility = f"{HOME}/data/user_watchtime_utility_new.csv"
    
    utility = pd.read_csv(outfile_utility,index_col=0)
    utility.index = utility.index.astype(str)
    
    similarity_mtx = pd.read_csv(outfile_similarity,index_col=0)
    similarity_mtx.index = similarity_mtx.index.astype(str)
    
    common_movies = utility.sort_values(by="mean",ascending=False).head(top_n).index.to_list()
    # First check if the user is new  
    if user_to_predict not in similarity_mtx.columns:
        # recommendation_list = utility.sort_values(by="mean",ascending=False).head(top_n).index.to_list()
        return common_movies
    
    n = 10
    similarity_mtx.drop(user_to_predict, axis = 0, inplace=True)
    
    # User similarity threashold
    similarity_mtx_threshold = 0.0

    # Get top n similar users
    similar_users = similarity_mtx[similarity_mtx[user_to_predict]>similarity_mtx_threshold][user_to_predict].sort_values(ascending=False)[:n]

    # Print out top n similar users
    # print(f'The similar users for user {user_to_predict} are\n\t', similar_users.head(n).index.to_list())
    
    picked_userid_watched = utility[user_to_predict].dropna(axis=0, how='all')
    # print(picked_userid_watched.head(10))
    
    # print(similar_users.index)
    similar_user_movies = utility[similar_users.index].dropna(axis=0, how='all')
    
    similar_user_movies.drop(picked_userid_watched.index,axis=0, inplace=True, errors='ignore')
    
    # A dictionary to store item scores
    item_score = {}
    similar_user_movies = similar_user_movies.T
    # Loop through items
    for i in similar_user_movies.columns:
        # Get the ratings for movie i
        movie_rating = similar_user_movies[i]
        # Create a variable to store the score
        total = 0
        # Create a variable to store the number of scores
        count = 0
        # Loop through similar users
        for u in similar_users.index:
            # If the movie has rating
            if pd.isna(movie_rating[u]) == False:
                # Score is the sum of user similarity score multiply by the movie rating
                score = similar_users[u] * movie_rating[u]
                # Add the score to the total score for the movie so far
                total += score
                # Add 1 to the count
                count +=1
        # Get the average score for the item
        item_score[i] = total / count

    # Convert dictionary to pandas dataframe
    item_score = pd.DataFrame(item_score.items(), columns=['movie', 'movie_score'])

    # Sort the movies by score
    # print(item_score.head())
    ranked_item_score = item_score.sort_values(by='movie_score', ascending=False)

    # Select top m movies
    m = 20
    # print(f"\n\nRecommend {m} movies for user {user_to_predict}:")
    recommendation_list = ranked_item_score['movie'].head(m).to_list()
    if(len(recommendation_list)) <= 5:
        return common_movies
    else:
        return recommendation_list


def generateCSV():
    userids_file = f"{HOME}/data/users.csv"
    outfile_user_movies = f"{HOME}/data/user_movies.csv"
    outfile_common_movies = f"{HOME}/data/common_movies.csv"

    userids = pd.read_csv(userids_file,index_col=0)

    
    userid_list = userids["userid"].tolist()
    print(userid_list)
    print(len(userid_list))

    recommend_movies = []
    for i in range(0,len(userid_list)):
        movies = inference(user_to_predict=str(userid_list[i]))
        print(f'Recommed 20 movies for user {userid_list[i]}:\n\t',movies)
        recommend_movies.append(movies)
    
    dict = {'userid': userid_list, 'movies': recommend_movies}
    df = pd.DataFrame(dict)
    df.to_csv(outfile_user_movies)

    common_movies = inference(user_to_predict='-1')
    print(f'Top common 20 movies:\n\t', common_movies)
    dict = {'movies': [common_movies]}
    df = pd.DataFrame(dict)
    df.to_csv(outfile_common_movies)

if __name__ == "__main__":
    generateCSV()