import csv
import requests
import json

def fetch_and_save_data(product_name, user_token, csv_file_path, output_directory):
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row['productName'] == product_name:
                cloud_account_id = row['cloudAccountId']
                external_account_number = row['externalAccountNumber']
                url = f'https://api.cloudcheckr.com/api/v2/cloud/{cloud_account_id}/assessments/failures'
                headers = {
                    'accept': 'application/json',
                    'Authorization': f'Bearer {user_token}'
                }
                response = requests.get(url, headers=headers)
                json_data = response.json()
                file_name = f'{external_account_number}.json'
                file_path = f'{output_directory}/{file_name}'
                with open(file_path, mode='w', encoding='utf-8') as json_file:
                    json.dump(json_data, json_file, indent=4)

if __name__ == '__main__':
    product_name = input('Product Name: ')
    user_token = input('User Token: ')
    csv_file_path = input('CSV File Path: ')
    output_directory = input('Output Directory: ')
    fetch_and_save_data(product_name, user_token, csv_file_path, output_directory)