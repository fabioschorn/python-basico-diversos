# Python script to convert JSON to CSV
import os
import json
import pandas as pd

# Get current working directory
json_directory = '/path/to/json/files'
output_csv = '/path/to/output/cloud_report.csv'
dataframes = []

for filename in os.listdir(json_directory):
    if filename.endswith('.json'):
        file_path = os.path.join(json_directory, filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            # Convert data to DataFrame
            df = pd.DataFrame(data)
            # Add a new column for the filename
            df['source_file'] = filename
            # Append the DataFrame to the list
            dataframes.append(df)

# Combine all DataFrames
combined_df = pd.concat(dataframes, ignore_index=True)
# Save to CSV
combined_df.to_csv(output_csv, index=False)
print("Completed", output_csv)