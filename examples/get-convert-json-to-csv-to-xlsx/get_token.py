import requests
import json
from getpass import getpass

# URL of the API endpoint that generates the token
token_generation_url = 'https://api.fs.com.br/docs#/Auth/post_auth_token'
# Any necessary headers
headers = {'Content-Type': 'application/json'}

# Prompt user for their username and password
username = input("Enter your username: ")
password = getpass("Enter your password: ")

# Payload with user-provided credentials
payload = {'username': username, 'password': password}

# Send a POST request to the API endpoint
response = requests.post(token_generation_url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    token_data = response.json()
    # Save the token JSON to a file
    with open('token.json', 'w') as file:
        json.dump(token_data, file)
    print("Token saved to token.json")
else:
    print("Failed to generate token: ", response.status_code)