import requests
from getpass import getpass
import json

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
    # Save the token JSON to a file
    with open('token.json', 'w') as file:
        json.dump(token_data, file)
    print("Token saved to token.json")
else:
    print("Failed to generate token: ", response.status_code)