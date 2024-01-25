import matplotlib.pyplot as plt
import re
import pandas as pd
import tqdm
import json


def check_coverage(user_log_df, movie_details_df):
    # Assuming 'user_log_df' is a DataFrame similar to 'df_log'
    # and 'movie_details_df' is a DataFrame with movie details including genres

    # Calculate the ratio of recommended films to the total number of movies
    recommended_movies = user_log_df['Movie'].unique()
    num_total_movies = len(movie_details_df)
    print("Ratio of recommended films to the entire movies collected: ",
          len(recommended_movies) / num_total_movies)

    # Function to collect movie genres (placeholder, needs actual implementation or API call)
    def collect_movie_genres(movies):
        total_genres = dict()
        # Placeholder loop - replace with actual data collection logic
        for movie in tqdm.tqdm(movies):
            # movie_info = curl_req(f"{link}movie/{movie}") # Replace with actual data fetching
            genres = movie_info['genres']  # Placeholder
            for genre in genres:
                if genre['name'] in total_genres:
                    total_genres[genre['name']] += 1
                else:
                    total_genres[genre['name']] = 1
        return total_genres

    # Collecting genres
    collected_genres = collect_movie_genres(movie_details_df["movieid"])
    print("Total number of movies in each genre")
    print(json.dumps(collected_genres, indent=2))

    recommended_genres = collect_movie_genres(recommended_movies)
    recommended_genres_vs_total = dict()
    for genre in recommended_genres:
        recommended_genres[genre] = round(
            recommended_genres[genre] / collected_genres[genre] * 100, 2)
        recommended_genres_vs_total[genre] = round(
            recommended_genres[genre] / num_total_movies * 100, 2)

    print("Ratio of recommended films to the entire movies collected")
    print(json.dumps(recommended_genres, indent=2))
    print("Proportion of recommended movies within each genre compared to the sum of all collected movies")
    print(json.dumps(recommended_genres_vs_total, indent=2))

# Example call (replace with actual DataFrame names)
# check_coverage(df_log, df_movies)


def check_fairness():# Reading the log file
    log_file_path = '09-26_get_trainingData.log'
    with open(log_file_path, 'r') as file:
        log_data = file.read()

    # Regular expression for parsing the log data
    log_pattern = re.compile(
        r"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}).*?(\d+).*?GET /data/m/(.+)/(\d+).mpg")

    # Parsing the log file using the pattern
    log_entries = log_pattern.findall(log_data)

    # Converting the parsed data into a DataFrame for analysis
    df_log = pd.DataFrame(log_entries, columns=[
                        'Timestamp', 'UserID', 'Movie', 'Duration'])

    # Converting data types
    df_log['Timestamp'] = pd.to_datetime(df_log['Timestamp'])
    df_log['Duration'] = pd.to_numeric(df_log['Duration'])
    df_log['UserID'] = pd.to_numeric(df_log['UserID'])

    # Analysis for Feedback Loops
    # Counting how frequently each movie is accessed
    movie_access_frequency = df_log['Movie'].value_counts()

    # Analysis for Fairness Issues
    # Counting unique movies and users for a basic fairness analysis
    unique_movies = df_log['Movie'].nunique()
    unique_users = df_log['UserID'].nunique()

    # Preparing results for presentation
    feedback_loop_analysis = movie_access_frequency.head(
        10)  # Top 10 most accessed movies
    user_diversity_analysis = {
        "Total Unique Movies Accessed": unique_movies,
        "Total Unique Users": unique_users
    }

    # Displaying the results of the analysis
    print("Feedback Loop Analysis:\n", feedback_loop_analysis)
    print("\nFairness Issue Analysis:\n", user_diversity_analysis)

    feedback_loop_analysis.plot(kind='barh', color='skyblue', figsize=(12, 6))
    plt.xlabel('Access Counts')
    plt.ylabel('Movies')
    plt.title('Top 10 Most Accessed Movies')
    plt.gca().invert_yaxis()  # To display the highest value on top
    plt.show()

if __name__ == "__main__":
    check_fairness()


# Data for the top 10 most accessed movies
movies = [
    "Dances with Wolves",
    "Schindler's List",
    "Jurassic Park",
    "Pulp Fiction",
    "The Godfather",
    "Star Wars",
    "Terminator 2",
    "The Godfather II",
    "Forrest Gump",
    "The Matrix"
]
access_counts = [1715, 961, 956, 915, 867, 855, 847, 784, 781, 741]

# Creating a bar plot
plt.figure(figsize=(12, 6))
plt.barh(movies, access_counts, color='skyblue')
plt.xlabel('Access Counts')
plt.ylabel('Movies')
plt.title('Top 10 Most Accessed Movies')
plt.gca().invert_yaxis()  # To display the highest value on top
plt.show()
