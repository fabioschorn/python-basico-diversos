import os
import csv
import requests
import json

# Clear current working directory
output_directory = 'json_results' # Update this if you want to use a different directory

# Get the list of files in the directory and show the list of files
files = os.listdir(output_directory)
print("The following files are in the directory:", files)

# After showing the list of files, remove the files the directory and ignore what is not a json file
for filename in os.listdir(output_directory):
    if filename.endswith(".json"):
        file_path = os.path.join(output_directory, filename)
        os.remove(file_path)

# Show the new status of the directory and the list of files that were removed
files = os.listdir(output_directory)
print("The following files were removed from the directory:", files)

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
                    file_name = f'{output_directory}/{external_account_number}.json'
                    with open(file_name, 'w') as json_file:
                        json.dump(response.json(), json_file)
                        print(f'File written: {file_name}')
                else:
                    print(f'Failed to fetch data for cloudAccountId: {cloud_account_id}')

# Example usage
product_name = input("Enter the product name: ")
user_token_file = input("Enter the path to the user token file: ")
csv_file_path = 'product_list.csv'  # Update this if your CSV file is in a different directory

fetch_and_save_data(product_name, user_token_file, csv_file_path, output_directory)