import requests
import json

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Update with your Flask app's URL

# Login and get JWT token
login_data = {"email": "admin", "password": "admin"}
login_response = requests.post(f"{BASE_URL}/login", json=login_data)
token = login_response.json().get('access_token')

# Check if token is received
if not token:
    print("Failed to login")
    exit()

# Group data to be sent
group_data = {
    "ownerID": 3,  # Update with an appropriate owner ID
    "title": "Einführung in die Informatik",
    "description": "Wr programmieren in Python!",
    "maxUsers": 10,
}

# Headers with JWT token
headers = {'Authorization': f'Bearer {token}'}

# Send a POST request to create a new group
response = requests.post(f"{BASE_URL}/groups", json=group_data, headers=headers)

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=4)}")
