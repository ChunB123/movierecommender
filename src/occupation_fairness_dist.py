import matplotlib.pyplot as plt
import numpy as np

# Data for the total number of movies in each genre
genres = ["Comedy", "Family", "Drama", "Action", "Crime", "Thriller", "Romance",
          "Science Fiction", "Mystery", "Adventure", "Horror", "Fantasy", "Animation",
          "Western", "Music", "History", "War", "Foreign", "Documentary"]
total_movies = [292, 99, 362, 195, 119, 208, 150,
                116, 80, 162, 61, 102, 44, 17, 28, 26, 27, 2, 5]

# Creating a bar chart
plt.figure(figsize=(15, 8))
plt.bar(genres, total_movies, color='skyblue')
plt.xlabel('Genre', fontsize=14)
plt.ylabel('Total Number of Movies', fontsize=14)
plt.title('Total Number of Movies in Each Genre', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.show()


# Ratios of recommended films to the entire movies collected for each group
ratios = {
    "K_12_student": 0.0511,
    "academic_educator": 0.0677,
    "artist": 0.0345,
    "clerical_admin": 0.0255,
    "college_grad_student": 0.3538,
    "doctor_health_care": 0.0255,
    "executive_managerial": 0.3078,
    "homemaker": 0.0945,
    "other": 0.2797,
    "programmer": 0.0255,
    "retired": 0.0255,
    "sales_marketing": 0.2695,
    "scientist": 0.2925,
    "self_employed": 0.1111,
    "technician_engineer": 0.0255,
    "tradesman_craftsman": 0.0255,
    "writer": 0.0255
}

groups = list(ratios.keys())
average_ratios = list(ratios.values())

# Creating a bar chart for average ratios
plt.figure(figsize=(15, 8))
plt.bar(groups, average_ratios, color='lightgreen')
plt.xlabel('Group', fontsize=14)
plt.ylabel('Average Ratio of Recommended Films', fontsize=14)
plt.title('Average Ratio of Recommended Films to Total Films Collected for Each Group', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.show()



# Calculate the average ratio of recommended films for each group
average_ratio = df['Ratio of recommended films to the entire movies collected'].mean()

# Create a bar chart for the ratio of recommended films for each group
plt.figure(figsize=(14, 6))
plt.bar(df['Group'], df['Ratio of recommended films to the entire movies collected'],
        color='lightgreen')
plt.axhline(y=average_ratio, color='r', linestyle='-',
            label=f'Average Ratio ({average_ratio:.2f})')
plt.xlabel('Professional Group')
plt.ylabel('Ratio of Recommended Films')
plt.title('Ratio of Recommended Films to Total Films Collected for Each Group')
plt.xticks(rotation=45)
plt.legend()
plt.grid(True)
plt.show()


# # Function to calculate the average proportion for each group
# def calculate_average(proportion_dict):
#     return sum(proportion_dict.values()) / len(proportion_dict)


# # Calculating average proportions for each group
# avg_proportions = {group: calculate_average(
#     proportions[group]) for group in proportions}

# # Creating a combined plot with an average line for each group's chart
# fig, axes = plt.subplots(4, 1, figsize=(14, 24))

# # Plotting each group's proportions with their average line
# for i, (group, prop) in enumerate(proportions.items()):
#     axes[i].bar(prop.keys(), prop.values(), color=plt.cm.Paired(i))
#     axes[i].axhline(y=avg_proportions[group], color='r', linestyle='-',
#                     label=f'Average ({avg_proportions[group]:.2f})')
#     axes[i].set_title(
#         f'Proportion of Recommended Movies Within Each Genre for {group.replace("_", " ").title()}')
#     axes[i].set_xlabel('Movie Genres')
#     axes[i].set_ylabel('Proportion of Recommended Movies')
#     axes[i].legend()
#     axes[i].tick_params(axis='x', rotation=45)

# plt.tight_layout()
# plt.show()
