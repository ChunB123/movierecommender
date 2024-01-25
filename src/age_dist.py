import matplotlib.pyplot as plt

# Data for the graph
age_data = {
    25: 864, 31: 841, 30: 837, 27: 835, 33: 835, 29: 833, 34: 823, 26: 819, 32: 798, 28: 797, 18: 229, 21: 159,
    19: 90, 24: 85, 22: 83, 23: 77, 20: 68, 36: 40, 35: 39, 43: 38, 42: 36, 38: 33, 44: 32, 41: 32, 40: 29, 39: 26,
    37: 25, 54: 20, 53: 18, 46: 16, 14: 16, 15: 16, 55: 16, 10: 16, 69: 15, 50: 14, 52: 14, 51: 14, 16: 14, 17: 12,
    49: 11, 58: 10, 59: 10, 13: 10, 47: 9, 73: 9, 75: 9, 8: 9, 12: 9, 78: 9, 80: 8, 45: 8, 9: 8, 77: 7, 83: 6, 62: 6,
    71: 6, 84: 6, 72: 6, 67: 6, 81: 5, 61: 5, 74: 5, 11: 5, 48: 5, 89: 5, 70: 5, 63: 5, 60: 4, 64: 4, 66: 4, 68: 4,
    85: 4, 65: 3, 87: 3, 57: 3, 76: 3, 88: 3, 82: 3, 79: 2, 90: 2, 56: 2
}
ages = sorted(age_data.keys())
counts = [age_data[age] for age in ages]

# Create a bar chart
plt.figure(figsize=(12, 8))
plt.bar(ages, counts, color='blue')
plt.xlabel('Age')
plt.ylabel('Number of People')
plt.title('Age Distribution')
plt.xticks(rotation=90)
plt.show()
