import requests
from getpass import getpass
import json
import os
import hashlib

# Directory where token files are stored
token_directory = '/YOUR-PATH'

# Clean up the directory at the start of the program
for file_name in os.listdir(token_directory):
    file_path = os.path.join(token_directory, file_name)
    if os.path.isfile(file_path):
        os.remove(file_path)

# URL of the API endpoint that generates the token
token_generation_url = 'https://api.fs.com.br/token'

# Headers
headers = {'Accept': 'application/json', 'Content-Type': 'application/x-www-form-urlencoded'}

# Prompt user for their username and password
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Payload with user-provided credentials to be sent to the API endpoint
payload = {
    'grant_type': 'password',  # This is typically a fixed value for this grant type
    'username': username,
    'password': password,
    'client_id': '',  # Fill in if required
    'client_secret': ''  # Fill in if required
}

# Send a POST request to the API endpoint
response = requests.post(token_generation_url, headers=headers, data=payload)

# Check if the request was successful
if response.status_code == 200:
    token_data = response.json()
    # Save the token JSON to a file for later use
    with open(os.path.join(token_directory, 'token.json'), 'w') as token_file:
        json.dump(token_data, token_file)

    # Create a hash of the access token and save it to another file
    token_hash = hashlib.sha256(token_data['access_token'].encode()).hexdigest()
    with open(os.path.join(token_directory, 'token.file'), 'w') as hash_file:
        hash_file.write(token_hash)

    # Print the token hash
    print(f"Your token hash is: {token_hash}")
else:
    print(f"Failed to generate token: {response.text}")