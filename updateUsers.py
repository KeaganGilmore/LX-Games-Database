import requests
import json
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

# Get the necessary credentials from environment variables
login_url = os.getenv('LOGIN_URL')
email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')

# Function to log in and get a new Bearer token
def get_bearer_token(login_url, email, password):
    # Define the payload for the POST request
    payload = {
        'email': email,
        'password': password
    }

    # Send the POST request to log in and get the Bearer token
    response = requests.post(login_url, json=payload)

    # Check if the request was successful
    if response.status_code == 200:
        bearer_token = response.text.strip()
        return bearer_token
    else:
        print(f'Failed to log in. Status code: {response.status_code}')
        print("Response content:", response.text)
        raise Exception('Failed to log in.')

# Main script execution
if __name__ == '__main__':
    try:
        # Log in and get a new Bearer token
        bearer_token = get_bearer_token(login_url, email, password)
        
        # Define the URL for the GET request
        url = 'https://lxlibrary.online/api/v2/student'

        # Define the headers
        headers = {
            'Authorization': f'Bearer {bearer_token}'
        }

        # Send the GET request
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            # Get the response content
            response_json = response.json()
            
            # Convert the response content to a JSON string
            response_str = json.dumps(response_json, indent=4)
            
            # Define the filename
            filename = 'users.json'
            
            # Write the JSON string to a file
            with open(filename, 'w') as file:
                file.write(response_str)
            
            print(f'Successfully saved the response to {filename}')
        else:
            print(f'Failed to get a valid response. Status code: {response.status_code}')
            print(response.text)
    except Exception as e:
        print(f'Error: {e}')