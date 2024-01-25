import matplotlib.pyplot as plt

# Data for the graph
gender_data = {'Male': 8151, 'Female': 1699}
labels = gender_data.keys()
sizes = gender_data.values()

# Create a pie chart
plt.figure(figsize=(8, 6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.title('Gender Distribution')
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.show()
