import os
import csv
import requests
import json
import pandas as pd
from datetime import datetime

def clear_directory(directory):
    files = os.listdir(directory)
    print("The following files are in the directory:", files)
    for filename in files:
        if filename.endswith(".json"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
    print("The following files were removed from the directory:", os.listdir(directory))

def fetch_and_save_data(product_name, user_token_file, csv_file_path, output_directory):
    with open(user_token_file, 'r') as token_file:
        user_token = token_file.read()
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['productName'] == product_name:
                cloud_account_id = row['cloudAccountId']
                external_account_number = row['externalAccountNumber']
                response = requests.get(
                    f'https://api.fs.com.br/api/v2/cloud/{cloud_account_id}/assessments/failures',
                    headers={'accept': 'application/json', 'Authorization': f'Bearer {user_token}'}
                )
                if response.status_code == 200:
                    file_name = f'{output_directory}/{external_account_number}.json'
                    with open(file_name, 'w') as json_file:
                        json.dump(response.json(), json_file)
                        print(f'File written: {file_name}')
                else:
                    print(f'Failed to fetch data for cloudAccountId: {cloud_account_id}')

def json_to_csv(output_directory, output_csv):
    dataframes = []
    for filename in os.listdir(output_directory):
        if filename.endswith('.json'):
            file_path = os.path.join(output_directory, filename)
            with open(file_path) as json_file:
                data = json.load(json_file)
                df = pd.DataFrame(data)
                df['aws_account_number'] = filename.replace('.json', '')
                dataframes.append(df)
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df.to_csv(output_csv, index=False)
    print("CSV file created!", output_csv)

def csv_to_excel(output_csv, output_excel):
    df = pd.read_csv(output_csv)
    cols = df.columns.tolist()
    cols = cols[-1:] + cols[:-1]
    df = df[cols]
    df.to_excel(output_excel, index=False)
    print("Excel file created!", output_excel)
    os.remove(output_csv)
    print("CSV file deleted!", output_csv)

# Main script starts here - update the variables below
output_directory = 'json_results'  # Update this if you want to use a different directory
output_csv = '/path/to/output/cloud_report.csv'  # Update this for the CSV file
current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
output_excel = f'/path/to/output/cloud_report_{current_time}.xlsx'  # Update this for the Excel file

clear_directory(output_directory) # Clear the directory before running the script

product_name = input("Enter the product name: ")
user_token_file = input("Enter the path to the user token file: ")
csv_file_path = 'product_list.csv'  # Update this if your CSV file is in a different directory
fetch_and_save_data(product_name, user_token_file, csv_file_path, output_directory)
json_to_csv(output_directory, output_csv)
csv_to_excel(output_csv, output_excel)