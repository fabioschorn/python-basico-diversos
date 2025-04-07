# Data Wrangling Example: Handling Missing Values in a Car Dataset
# This script demonstrates how to read a CSV file from a URL, assign column headers,
# handle missing values, and visualize the data using a histogram.
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

# Define the URL of the dataset
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

# Define the column headers
headers = [
    "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
    "num-of-doors", "body-style", "drive-wheels", "engine-location",
    "wheel-base", "length", "width", "height", "curb-weight",
    "engine-type", "num-of-cylinders", "engine-size", "fuel-system",
    "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
    "city-mpg", "highway-mpg", "price"
]

# Step 1: Load the dataset
df = pd.read_csv(url, names=headers)

# Step 2: Replace "?" with NaN
df.replace("?", np.nan, inplace=True)

# Step 3: Convert selected numeric columns to proper types
numeric_cols = [
    "normalized-losses", "bore", "stroke",
    "horsepower", "peak-rpm", "price"
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# Step 4: Handle missing values by replacing with column means
for col in numeric_cols:
    df[col].fillna(df[col].mean(), inplace=True)

# Optional: Fill missing 'num-of-doors' with most common value (mode)
df["num-of-doors"].fillna(df["num-of-doors"].mode()[0], inplace=True)

# Step 5: Show missing data summary
print("Missing values per column:")
print(df.isnull().sum())
print("\nFirst 5 rows after cleaning:")
print(df.head())

# Step 6: Plot histogram of car prices
df["price"].dropna().hist()
plt.title("Histogram of Car Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()