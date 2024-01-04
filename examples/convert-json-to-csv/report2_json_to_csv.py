# Python script to convert JSON to CSV
import os
import json
import pandas as pd
import re

def sanitize_filename(filename):
    """Remove special characters and return a clean filename."""
    # Remove the file extension and any non-alphanumeric characters (excluding underscores and dashes)
    return re.sub(r'[^a-zA-Z0-9_-]', '', os.path.splitext(filename)[0])

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
            # Sanitize the filename to remove special characters
            clean_filename = sanitize_filename(filename)
            # Add a column with the sanitized filename, named 'aws_account_number'
            df['aws_account_number'] = clean_filename
            # Append the DataFrame to the list of DataFrames
            dataframes.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a CSV file
combined_df.to_csv(output_csv, index=False)
print("Completed", output_csv)