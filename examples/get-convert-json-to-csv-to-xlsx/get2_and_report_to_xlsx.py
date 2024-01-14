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

def add_environment_column(output_csv, product_list_csv):
    df = pd.read_csv(output_csv)
    product_list_df = pd.read_csv(product_list_csv)
    environment_map = dict(zip(product_list_df.externalAccountNumber, product_list_df.environment))
    df['environment'] = df['aws_account_number'].map(environment_map)
    new_csv = output_csv.replace('.csv', '_updated.csv')
    df.to_csv(new_csv, index=False)
    return new_csv

def csv_to_excel(output_csv, output_excel):
    df = pd.read_csv(output_csv)
    # Reorder columns to make 'aws_account_number' first and 'environment' second
    reordered_columns = ['aws_account_number', 'environment'] + [col for col in df.columns if col not in ['aws_account_number', 'environment']]
    df = df[reordered_columns]
    # Set the sheet name to 'report_automated'
    df.to_excel(output_excel, index=False, sheet_name='report_automated')
    print("Excel file created!!!", output_excel)
    os.remove(output_csv)
    print("CSV file deleted!", output_csv)

def display_product_menu(csv_file_path):
    print("Menu Products:")  # Displaying the menu title
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        products = sorted(set(row[0] for row in reader))  # Unique product names

    for i, product in enumerate(products, 1):
        print(f"{i} - {product}")

    # Add the 'Press to skip!' option
    skip_option_number = len(products) + 1
    print(f"{skip_option_number} - Press to skip!")
    products.append('Press to skip!')  # Append to the product list for selection handling

    return products

# Main script starts here - change the values below
output_directory = 'json_results' # Change this to the path of your output directory
output_csv = '/path/to/output/cloud_report.csv' # Change this to the path of your output CSV file
csv_file_path = 'product_list.csv'  # Change this to the path of your product list CSV file

products = display_product_menu(csv_file_path)

selected_product_index = int(input("Select a product number: ")) - 1

# Check if the user selected the 'Press to skip!' option
if selected_product_index >= len(products) - 1:
    print("You chose to skip.")
    # Handle the skip action here (e.g., exit the program or continue with a default action)

else:
    product_name = products[selected_product_index]
    user_token_file = input("Enter the path to the user token file: ")

    fetch_and_save_data(product_name, user_token_file, csv_file_path, output_directory)
    json_to_csv(output_directory, output_csv)

    # Block to add environment column and replace old file
    updated_csv = add_environment_column(output_csv, csv_file_path)
    os.remove(output_csv)
    os.rename(updated_csv, output_csv)

    # Modify output_excel to include the selected product name
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_excel = f'/path/to/output/{product_name}_cloud_report_{current_time}.xlsx' # Change this to the path of your output Excel file

    csv_to_excel(output_csv, output_excel)