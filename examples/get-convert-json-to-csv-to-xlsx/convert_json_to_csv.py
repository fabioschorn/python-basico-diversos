# Python script to convert JSON to CSV
import os
import json
import pandas as pd

# Get current working directory
json_directory = '/path/to/json/files'
output_csv = '/path/to/output/cloud_report.csv'
combined_data = []
for filename in os.listdir(json_directory):
    if filename.endswith('json'):
        file_path = os.path.join(json_directory, filename)
        with open(file_path) as json_file:
            data = json.load(json_file)
            combined_data.extend(data)
df = pd.DataFrame(combined_data)
df.to_csv(output_csv, index=False)
print("completed", output_csv)