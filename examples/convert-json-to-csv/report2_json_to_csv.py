# Python script to convert JSON to CSV
import os
import json
import pandas as pd

# Get current working directory
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
            # Remove the '.json' extension from the filename
            filename_without_extension = os.path.splitext(filename)[0]
            # Add a column with the filename without the extension
            df['aws_account_number'] = filename_without_extension
            # Append the DataFrame to the list of DataFrames
            dataframes.append(df)

# Combine all DataFrames into a single DataFrame
combined_df = pd.concat(dataframes, ignore_index=True)

# Write the combined DataFrame to a CSV file
combined_df.to_csv(output_csv, index=False)
print("Completed", output_csv)