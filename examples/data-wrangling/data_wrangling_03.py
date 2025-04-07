# Data Wrangling with Pandas
# This script cleans up a dataset of automobiles, handling missing data and converting data types.
# Importing required libraries
# Importing required libraries
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

# Dataset URL
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

# Define column headers
headers = [
    "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
    "num-of-doors", "body-style", "drive-wheels", "engine-location",
    "wheel-base", "length", "width", "height", "curb-weight",
    "engine-type", "num-of-cylinders", "engine-size", "fuel-system",
    "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
    "city-mpg", "highway-mpg", "price"
]

# Step 1: Load dataset from URL
df = pd.read_csv(url, names=headers)

# Step 2: Replace "?" with NaN for proper missing data handling
df.replace("?", np.nan, inplace=True)

# Step 3: Evaluate missing data using .isnull()
missing_data = df.isnull()
print("📋 Missing data flags (first 5 rows):")
print(missing_data.head(5))

# Step 4: Display total missing values per column
print("\n📊 Total missing values per column:")
print(missing_data.sum())

# Step 5: Convert relevant columns to numeric
numeric_cols = [
    "normalized-losses", "bore", "stroke",
    "horsepower", "peak-rpm", "price"
]
df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

# Step 6: Fill missing numeric values with the mean of each column
for col in numeric_cols:
    df[col].fillna(df[col].mean(), inplace=True)

# Step 7: Fill missing categorical values (e.g., 'num-of-doors') with the mode
df["num-of-doors"].fillna(df["num-of-doors"].mode()[0], inplace=True)

# Step 8: Final check for remaining missing values
print("\n✅ Remaining missing values after cleanup:")
print(df.isnull().sum())

# Step 9: Display first 5 rows of cleaned data
print("\n📌 Cleaned data preview (first 5 rows):")
print(df.head())

# Step 10: Plot histogram of car prices
df["price"].dropna().hist()
plt.title("Histogram of Car Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# Step 11: Save cleaned dataset to ./data/cleaned_auto.csv
output_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "cleaned_auto.csv")
df.to_csv(output_path, index=False)

print(f"\n✅ Cleaned data saved to: '{output_path}'")