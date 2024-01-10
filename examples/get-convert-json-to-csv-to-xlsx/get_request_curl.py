import os
import csv
import requests
import json

def clear_directory(directory):
    files_to_remove = [f for f in os.listdir(directory) if f.endswith(".json")]
    print("The following files are in the directory:", files_to_remove)
    for filename in files_to_remove:
        os.remove(os.path.join(directory, filename))
    print("The following files were removed from the directory:", files_to_remove)

def fetch_and_save_data(product_name, user_token_file, csv_file_path, output_directory):
    # Read the user token from the specified file
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
                    with open(f'{output_directory}/{external_account_number}.json', 'w') as json_file:
                        json.dump(response.json(), json_file)
                else:
                    print(f'Failed to fetch data for cloudAccountId: {cloud_account_id}')

# Clear the directory first
json_directory = 'json_results'
clear_directory(json_directory)

# Then fetch and save data
product_name = input("Enter the product name: ")
user_token_file = input("Enter the path to the user token file: ")
csv_file_path = 'product_list.csv'  # Update this if your CSV file is in a different directory
fetch_and_save_data(product_name, user_token_file, csv_file_path, json_directory)