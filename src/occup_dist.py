import matplotlib.pyplot as plt

# Data for the graph
occupation_data = {
    'College Grad Student': 2375, 'Executive/Managerial': 1886, 'Sales/Marketing': 1271, 'Scientist': 935,
    'Self Employed': 698, 'Other': 685, 'Academic/Educator': 403, 'K-12 Student': 310, 'Homemaker': 288,
    'Artist': 213, 'Retired': 168, 'Clerical/Admin': 147, 'Technician/Engineer': 146, 'Programmer': 105,
    'Tradesman/Craftsman': 61, 'Doctor/Health Care': 39, 'Writer': 37, 'Lawyer': 35, 'Unemployed': 24,
    'Customer Service': 22, 'Farmer': 2
}
labels = occupation_data.keys()
sizes = occupation_data.values()

# Create a bar chart
plt.figure(figsize=(10, 8))
plt.barh(list(labels), list(sizes))
plt.xlabel('Number of People')
plt.title('Occupation Distribution')
plt.gca().invert_yaxis()  # Invert y-axis to have the highest number at the top
plt.show()
