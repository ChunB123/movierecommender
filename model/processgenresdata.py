import requests  
import os
import pandas as pd 
import json


def curl_req(link:str): 
    response = requests.get(link)   
    return response.json()


def generatecsv():

    curdir = os.getcwd()
    moviesdf = pd.read_csv(curdir + '/../data/movies.csv')
    movie_ids = moviesdf['movieid'].to_list()
    genredict = {}
    moviegenredict = {}

    for movie in movie_ids:
        url = ""
        
        movie_info = curl_req(url)

        genre_list = [genre["name"] for genre in movie_info["genres"]]
        moviegenredict[movie] = genre_list

        for genre in genre_list:
            if genre in genredict:
                genredict[genre].append(movie)
            else:
                genredict[genre] = [movie]


    genrejson = json.dumps(genredict, indent=4)

    with open(f'{curdir}/../data/genre_movies.json', 'w') as jsonfile:
        jsonfile.write(genrejson)


    moviegenrejson = json.dumps(moviegenredict, indent=4)

    with open(f'{curdir}/../data/movies_genres.json', 'w') as jsonfile:
        jsonfile.write(moviegenrejson)


    usersdf = pd.read_csv(curdir + '/../data/users.csv')
    userids = usersdf['userid'].to_list()
    usergenresdict = {}

    for userid in userids:
        jsonfilepath = curdir + "/../data/user_movie_080623_090623.json"
        movieswatched = []
        usergenres = {}
        durationmovies = []
        ratingmovies = []

        with open(jsonfilepath, 'r') as json_file:
            json_data = json.load(json_file)

            if str(userid) in json_data:
                movieswatched = json_data[str(userid)]
            else:
                continue
        
        if 'duration' in movieswatched:
            durationmovies = list(movieswatched["duration"].keys())
        if 'rating' in movieswatched:
            ratingmovies = list(movieswatched["rating"].keys())

        moviesbyusers = list(set(durationmovies).union(set(ratingmovies)))

        for movie in moviesbyusers:
            if movie in moviegenredict:
                for mgenre in moviegenredict[movie]:
                    if mgenre in usergenres:
                        usergenres[mgenre] += 1
                    else :
                        usergenres[mgenre] = 1
                usergenres = dict(sorted(usergenres.items(), key=lambda item: item[1], reverse=True))

        usergenresdict[str(userid)] = usergenres

    usergenrejson = json.dumps(usergenresdict, indent=4)
    
    with open(f'{curdir}/../data/users_genres.json', 'w') as jsonfile:
        jsonfile.write(usergenrejson)

def main():
    generatecsv()



if __name__ == "__main__":
    main()



    



    


        
    


