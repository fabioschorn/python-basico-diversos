# This script demonstrates how to read a CSV file from a URL, assign column headers,
# and visualize the data using a histogram.
# Import necessary libraries
import pandas as pd
import matplotlib.pylab as plt

# Define the URL of the dataset
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

# Define the column headers based on dataset documentation
headers = [
    "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
    "num-of-doors", "body-style", "drive-wheels", "engine-location",
    "wheel-base", "length", "width", "height", "curb-weight",
    "engine-type", "num-of-cylinders", "engine-size", "fuel-system",
    "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
    "city-mpg", "highway-mpg", "price"
]

# Read the dataset directly from the URL
df = pd.read_csv(url, names=headers)

# Show the first 5 rows of the dataset
print("First 5 rows of the dataset:")
print(df.head())

# Optional: convert 'price' column to numeric (to enable plotting)
df["price"] = pd.to_numeric(df["price"], errors='coerce')

# Plot a histogram of car prices
df["price"].dropna().hist()
plt.title("Histogram of Car Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()