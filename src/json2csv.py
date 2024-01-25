import json
import csv
import pandas as pd
from utils import curl_req

def json2csv(data):
    col_names = ['userid', 'movieid', 'watchtime','movie_duration','watchtime_percentage']
    df = pd.DataFrame(columns=col_names)  
    for key,value in data.items():
        user_id = key
            
        for movie,val in value["duration"].items():
            movie_info = curl_req(f"http://fall2023-comp585.cs.mcgill.ca:8080/movie/{movie}")
            runtime = movie_info["runtime"]
            try:
                df.loc[len(df)] = [user_id,movie,val,runtime,round(min(1.0, val/runtime),4)]
            except Exception as e:
                print(e)
    return df

def main(infile_path = "/home/tyang30/data/user_movie_080623_090623.json",outfile_path="/home/tyang30/data/user_watchtime.csv"):
       
    with open(infile_path,'r') as infile:
        data = json.load(infile) 
    with open(outfile_path,"w+") as outfile:
        # user_id, movie_id, duration  
        writer = csv.writer(outfile,delimiter=',')          
        for key,value in data.items():
            user_id = key
            
            # if "rating" not in value: continue
                
            for movie,val in value["duration"].items():
                movie_info = curl_req(f"http://fall2023-comp585.cs.mcgill.ca:8080/movie/{movie}")
                runtime = movie_info["runtime"]
                try:
                    writer.writerow([user_id,movie,val,runtime,round(min(1.0, val/runtime),4)])
                except Exception as e:
                    print(e)
                    print(f"Movie: {movie}, Movie duration: {runtime}, user watchtime: {val}")
        

if __name__ == "__main__":
    main()
