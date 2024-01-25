import matplotlib.pyplot as plt

# Data for the graph
genre_data_all_movies = {
    'Drama': 12809, 'Thriller': 4821, 'Comedy': 4579, 'Mystery': 3956, 'Adventure': 3600, 'Action': 3193,
    'Family': 2654, 'Crime': 2100, 'Romance': 1842, 'Fantasy': 1841, 'Science Fiction': 1618, 'Animation': 1314,
    'Horror': 832, 'History': 614, 'Documentary': 607, 'War': 576, 'Music': 373, 'Western': 285, 'Foreign': 223,
    'TV Movie': 62
}
genres_all_movies = genre_data_all_movies.keys()
counts_all_movies = genre_data_all_movies.values()

# Create a horizontal bar chart
plt.figure(figsize=(12, 10))
plt.barh(list(genres_all_movies), list(counts_all_movies), color='green')
plt.xlabel('Number of Movies')
plt.title('Genre Distribution of All Movies')
plt.gca().invert_yaxis()  # Invert y-axis to have the largest number at the top
plt.show()
