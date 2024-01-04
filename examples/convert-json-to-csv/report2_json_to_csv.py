# Python script to convert JSON to CSV
import os
import json
import pandas as pd

# Define the directory containing the JSON files and the output CSV file path
json_directory = '/path/to/json/files'
output_csv = '/path/to/output/cloud_report.csv'
dataframes = []

# Iterate over each file in the directory
for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            # Convert the JSON data to a DataFrame
            df = pd.DataFrame(data)
            # Add a column with the filename including the .json extension
            df['aws_account_number'] = filename
            # Append the DataFrame to the list of DataFrames
            dataframes.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a CSV file
combined_df.to_csv(output_csv, index=False)
print("CSV file generated with .json extensions.")

# Read the CSV file, remove the .json extension from the 'aws_account_number' column, and save it again
df = pd.read_csv(output_csv)
df['aws_account_number'] = df['aws_account_number'].str.replace('.json', '')
df.to_csv(output_csv, index=False)
print("Completed", output_csv)