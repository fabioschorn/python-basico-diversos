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
                response = requests.get(
                    f'https://api.fs.com.br/api/v2/cloud/{cloud_account_id}/assessments/failures',
                    headers={'accept': 'application/json', 'Authorization': f'Bearer {user_token}'}
                )
                if response.status_code == 200:
                    with open(f'{output_directory}/{external_account_number}.json', 'w') as json_file:
                        json.dump(response.json(), json_file)
                else:
                    print(f'Failed to fetch data for cloudAccountId: {cloud_account_id}')

def get_multi_line_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)
    return '\n'.join(lines)

# Example usage
product_name = input("Enter the product name: ")
print("Enter your user token (Type 'END' on a new line when finished):")
user_token = get_multi_line_input("Enter your user token:")
csv_file_path = 'product_list.csv'  # Update this if your CSV file is in a different directory
output_directory = 'json_results'  # Update this if you want to save JSON files in a different directory

fetch_and_save_data(product_name, user_token, csv_file_path, output_directory)