import matplotlib.pyplot as plt

# Data for the graph
genre_data = {
    'Drama': 3579, 'Comedy': 1922, 'Thriller': 1243, 'Romance': 1210, 'Action': 1098, 'Crime': 820,
    'Adventure': 705, 'Horror': 501, 'Documentary': 489, 'Science Fiction': 469, 'Mystery': 439,
    'Fantasy': 431, 'Family': 425, 'History': 334, 'Animation': 294, 'War': 278, 'Music': 258,
    'Foreign': 190, 'Western': 151, 'TV Movie': 49
}
genres = genre_data.keys()
counts = genre_data.values()

# Create a horizontal bar chart
plt.figure(figsize=(12, 10))
plt.barh(list(genres), list(counts), color='skyblue')
plt.xlabel('Number of Movies')
plt.title('Genre Distribution of Unique Movies')
plt.gca().invert_yaxis()  # Invert y-axis to have the largest number at the top
plt.show()
