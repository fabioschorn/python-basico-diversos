# Data Wrangling Example: Handling Missing Values in a Car Dataset
# This script demonstrates how to handle missing values in a dataset using pandas.
# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
import os

# Dataset URL
url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/auto.csv"

# Define headers
headers = [
    "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
    "num-of-doors", "body-style", "drive-wheels", "engine-location",
    "wheel-base", "length", "width", "height", "curb-weight",
    "engine-type", "num-of-cylinders", "engine-size", "fuel-system",
    "bore", "stroke", "compression-ratio", "horsepower", "peak-rpm",
    "city-mpg", "highway-mpg", "price"
]

# Step 1: Load data
df = pd.read_csv(url, names=headers)

# Step 2: Replace "?" with NaN
df.replace("?", np.nan, inplace=True)

# Step 3: Identify missing data
missing_data = df.isnull()

print("📋 Missing data flags (first 5 rows):")
print(missing_data.head())

print("\n📊 Missing value summary per column:")
for column in missing_data.columns.values.tolist():
    print(column)
    print(missing_data[column].value_counts())
    print("")

# Step 4: Handle missing data based on type

# Replace by mean
columns_mean = ["normalized-losses", "bore", "stroke", "horsepower", "peak-rpm"]
for col in columns_mean:
    df[col] = df[col].astype("float")
    mean_val = df[col].mean()
    print(f"Average of {col}: {mean_val}")
    df[col].replace(np.nan, mean_val, inplace=True)

# Replace by frequency
most_common_doors = "four"
df["num-of-doors"].replace(np.nan, most_common_doors, inplace=True)

# Drop rows where price is missing
initial_row_count = df.shape[0]
df.dropna(subset=["price"], axis=0, inplace=True)
df.reset_index(drop=True, inplace=True)
rows_dropped = initial_row_count - df.shape[0]
print(f"\n🗑️ Dropped {rows_dropped} rows due to missing 'price' values.")

# Convert price to float
df["price"] = df["price"].astype("float")

# Step 5: Final missing value check
print("\n✅ Remaining missing values after cleanup:")
print(df.isnull().sum())

# Step 6: Display first 5 cleaned rows
print("\n📌 Cleaned data preview (first 5 rows):")
print(df.head())

# Step 7: Plot histogram of prices
df["price"].dropna().hist()
plt.title("Histogram of Car Prices")
plt.xlabel("Price")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()

# Step 8: Save cleaned dataset
output_dir = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "cleaned_auto.csv")
df.to_csv(output_path, index=False)

print(f"\n✅ Cleaned data saved to: '{output_path}'")