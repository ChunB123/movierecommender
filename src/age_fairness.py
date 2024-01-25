import matplotlib.pyplot as plt
import numpy as np

import matplotlib.pyplot as plt

# Data for each group
groups = ['young', 'middle_aged', 'aged']
total_movies_genre = {
    "young": {
        "Comedy": 292, "Family": 99, "Drama": 362, "Action": 195, "Crime": 119, "Thriller": 208, "Romance": 150,
        "Science Fiction": 116, "Mystery": 80, "Adventure": 162, "Horror": 61, "Fantasy": 102, "Animation": 44,
        "Western": 17, "Music": 28, "History": 26, "War": 27, "Foreign": 2, "Documentary": 5
    },
    # Same structure for 'middle_aged' and 'aged'
}

proportion_recommended = {
    "young": {
        "Horror": 3.14, "Comedy": 5.38, "Music": 4.1,  # and so on...
    },
    # Same structure for 'middle_aged' and 'aged'
}

# Combining the first three graphs (Total Number of Movies in Each Genre) into one figure
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

for i, group in enumerate(groups):
    genres = list(total_movies_genre[group].keys())
    values = list(total_movies_genre[group].values())
    average = sum(values) / len(values)

    axes[i].bar(genres, values, color='skyblue')
    axes[i].axhline(y=average, color='r', linestyle='--')
    axes[i].set_title(f'Total Number of Movies in Each Genre for {group}')
    axes[i].set_xlabel('Genres')
    axes[i].set_ylabel('Total Number of Movies')
    axes[i].set_xticklabels(genres, rotation=45, ha='right')

plt.tight_layout()

# Combining the last three graphs (Proportion of Recommended Movies within Each Genre) into one figure
fig, axes = plt.subplots(3, 1, figsize=(12, 18))

for i, group in enumerate(groups):
    genres = list(proportion_recommended[group].keys())
    proportions = list(proportion_recommended[group].values())
    average = sum(proportions) / len(proportions)

    axes[i].bar(genres, proportions, color='purple')
    axes[i].axhline(y=average, color='r', linestyle='--')
    axes[i].set_title(
        f'Proportion of Recommended Movies within Each Genre for {group}')
    axes[i].set_xlabel('Genres')
    axes[i].set_ylabel('Proportion of Recommended Movies')
    axes[i].set_xticklabels(genres, rotation=45, ha='right')

plt.tight_layout()
plt.show()
