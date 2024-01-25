from flask import Flask
import pandas as pd
import ast
import requests

app = Flask(__name__)

def curl_req(link:str):
    response = requests.get(link)
    return response.json()

@app.route('/recommend/<string:user_id>')
def recommendation_route(user_id):
    user_movies_file = "../data/user_movie_u.csv"
    # user_movies_file = "../data/user_movie_i.csv"
    common_movies_file = "../data/common_movies.csv"

    url = ""

    response = curl_req(url+str(user_id))
    #print(response)
    if 'message' in response:
        return "Invalid user"
    
    common_movies_df = None
    common_movies = None
    user_movies_df = None
    movies = []

    try:
        common_movies_df = pd.read_csv(common_movies_file)
        common_movies_df['movies'] = common_movies_df['movies'].apply(ast.literal_eval)
        common_movies = common_movies_df['movies'].tolist()[0]

        user_movies_df = pd.read_csv(user_movies_file,index_col=0)
        user_movies_df.index = user_movies_df.index.astype(str)
        user_movies_df['movies'] = user_movies_df['movies'].apply(ast.literal_eval)
    except OSError as e:
        print("OSError found")
        return e
    except:
        return "server Error"
    
    if int(user_id) in user_movies_df['userid'].tolist():
        movies = user_movies_df[user_movies_df['userid'] == int(user_id)]['movies'].tolist()[0]
        if len(movies) == 0:
            movies = common_movies
        else:
            movies = [x[1] for x in movies]
    else:
        movies = common_movies
        
    # response
    response = movies
    response = ",".join(response)
    
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8082)
