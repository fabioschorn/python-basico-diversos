# Python script to convert JSON to CSV
import os
import json
import pandas as pd
from datetime import datetime

# Get current working directory
output_directory = '/path/to/json/files' # Update this if you want to use a different directory
output_csv = '/path/to/output/cloud_report.csv' # Update this if you want to use a different directory
dataframes = []

for filename in os.listdir(output_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(output_directory, filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            # Add a new column for the filename
            df['aws_account_number'] = filename
            # Append the DataFrame to the list
            dataframes.append(df)

# Combine all DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)

# Save to CSV
combined_df.to_csv(output_csv, index=False)
print("Part 1: CSV file created!", output_csv)

# Read the CSV file, remove the .json extension from the 'aws_account_number' colum's values
df = pd.read_csv(output_csv)
df['aws_account_number'] = df['aws_account_number'].str.replace('.json', '')

# Save to CSV
df.to_csv(output_csv, index=False)
print("Part 2: CSV change column created!", output_csv)

# Change the column order, move the 'aws_account_number' column to the first position
cols = df.columns.tolist()
cols = cols[-1:] + cols[:-1]
df = df[cols]

# Save to CSV
df.to_csv(output_csv, index=False)
print("Part 3: CSV change column order created!", output_csv)

# Generate timestamp
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")

# Define the path for the Excel file with timestamp
output_excel = f'/path/to/output/cloud_report_{current_time}.xlsx' # Update this if you want to use a different directory

# Convert CSV to Excel
df.to_excel(output_excel, index=False)
print("Part 4: Excel file created!", output_excel)

# Delete the Original CSV File
if os.path.exists(output_csv):
    os.remove(output_csv)
    print("Part 5: CSV file deleted!", output_csv)