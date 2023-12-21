import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
CREDENTIALS = {"email": "test", "password": "test"}  # Replace with valid credentials
GROUP_ID = 15  # Group ID for testing

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to get members of a group
def get_group_members(token, group_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/groups/{group_id}/members", headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(CREDENTIALS)

# Get members of the group
response = get_group_members(token, GROUP_ID)
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
