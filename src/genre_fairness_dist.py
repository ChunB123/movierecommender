import matplotlib.pyplot as plt

# Data
genres = ["Comedy", "Family", "Drama", "Action", "Crime", "Thriller", "Romance",
          "Science Fiction", "Mystery", "Adventure", "Horror", "Fantasy",
          "Animation", "Western", "Music", "History", "War", "Foreign", "Documentary"]

total_movies_f = [292, 99, 362, 195, 119, 208, 150,
                  116, 80, 162, 61, 102, 44, 17, 28, 26, 27, 2, 5]
ratio_recommended_f = [33.85, 33.33, 31.51, 36.21, 41.18, 37.25, 33.43, 43.75,
                       34.62, 34.62, 40.98, 50.0, 60.0, 30.67, 30.25, 29.55, 48.15, 26.26, 21.43]
proportion_recommended_f = [4.32, 4.26, 4.02, 4.62, 5.26, 4.76, 4.27,
                            5.59, 4.42, 4.42, 5.23, 6.39, 7.66, 3.92, 3.86, 3.77, 6.15, 3.35, 2.74]

# Assuming the data for Group M is the same as Group F for demonstration purposes
total_movies_m = total_movies_f
ratio_recommended_m = ratio_recommended_f
proportion_recommended_m = proportion_recommended_f

def add_average_line(ax, data, color):
    # Calculate the average
    average = sum(data) / len(data)
    # Add a horizontal line for the average
    ax.axhline(y=average, color=color, linestyle='--',
               label=f'Average: {average:.2f}')
    # Add legend
    ax.legend()


# Recreating the graphs with average lines
fig, axs = plt.subplots(3, 2, figsize=(15, 18))

# Total Number of Movies in Each Genre
axs[0, 0].bar(genres, total_movies_f, color='skyblue')
axs[0, 0].set_title('Group F: Total Number of Movies in Each Genre')
axs[0, 0].tick_params(labelrotation=45)
axs[0, 0].set_ylabel('Total Movies')
add_average_line(axs[0, 0], total_movies_f, 'blue')

axs[0, 1].bar(genres, total_movies_m, color='lightgreen')
axs[0, 1].set_title('Group M: Total Number of Movies in Each Genre')
axs[0, 1].tick_params(labelrotation=45)
axs[0, 1].set_ylabel('Total Movies')
add_average_line(axs[0, 1], total_movies_m, 'green')

# Ratio of Recommended Films to Total Films Collected
axs[1, 0].bar(genres, ratio_recommended_f, color='skyblue')
axs[1, 0].set_title('Group F: Ratio of Recommended Films to Total Films')
axs[1, 0].tick_params(labelrotation=45)
axs[1, 0].set_ylabel('Ratio (%)')
add_average_line(axs[1, 0], ratio_recommended_f, 'blue')

axs[1, 1].bar(genres, ratio_recommended_m, color='lightgreen')
axs[1, 1].set_title('Group M: Ratio of Recommended Films to Total Films')
axs[1, 1].tick_params(labelrotation=45)
axs[1, 1].set_ylabel('Ratio (%)')
add_average_line(axs[1, 1], ratio_recommended_m, 'green')

# Proportion of Recommended Movies Within Each Genre
axs[2, 0].bar(genres, proportion_recommended_f, color='skyblue')
axs[2, 0].set_title(
    'Group F: Proportion of Recommended Movies Within Each Genre')
axs[2, 0].tick_params(labelrotation=45)
axs[2, 0].set_ylabel('Proportion (%)')
add_average_line(axs[2, 0], proportion_recommended_f, 'blue')

axs[2, 1].bar(genres, proportion_recommended_m, color='lightgreen')
axs[2, 1].set_title(
    'Group M: Proportion of Recommended Movies Within Each Genre')
axs[2, 1].tick_params(labelrotation=45)
axs[2, 1].set_ylabel('Proportion (%)')
add_average_line(axs[2, 1], proportion_recommended_m, 'green')

# Adjust layout for better visibility
plt.tight_layout()
plt.show()
