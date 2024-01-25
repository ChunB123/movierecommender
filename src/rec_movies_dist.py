import matplotlib.pyplot as plt

# Data for the graph
movies = [
    'Rain Man 1988', 'Rear Window 1954', 'Rebecca 1940', '101 Dalmatians 1996', 'Rat Race 2001',
    'Reality Bites 1994', 'Red Corner 1997', 'Red Firecracker, Green Firecracker 1994', 'The Shawshank Redemption 1994',
    'Red Eye 2005', 'Inception 2010', 'Remember the Titans 2000', 'The Lord of the Rings: The Fellowship of the Ring 2001',
    'Interstellar 2014', 'Seven Samurai 1954', 'Star Wars 1977', 'The Godfather 1972', 'The Dark Knight 2008',
    'Forrest Gump 1994', 'The Lord of the Rings: The Two Towers 2002'
]
recommendations = [2541, 1794, 1217, 908, 587, 536, 236,
                   158, 125, 104, 104, 93, 81, 71, 67, 64, 63, 60, 59, 59]

# Create a horizontal bar chart
plt.figure(figsize=(12, 10))
plt.barh(movies, recommendations, color='purple')
plt.xlabel('Number of Recommendations')
plt.title('Recommended Movies Distribution')
plt.gca().invert_yaxis()  # Invert y-axis to have the largest number at the top
plt.show()
