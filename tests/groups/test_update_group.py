import requests
import json

# Constants
BASE_URL = "http://127.0.0.1:5000"
ADMIN_CREDENTIALS = {"email": "admin", "password": "admin"}
OWNER_CREDENTIALS = {"email": "test", "password": "test"}
NON_OWNER_CREDENTIALS = {"email": "petermurller@mail.com", "password": "peterspw"}

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    print("logged in as " + credentials.get('email'))
    return response.json().get('access_token')

# Function to create a group
def create_group(token, group_data):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{BASE_URL}/groups", json=group_data, headers=headers)
    return response.json().get('groupID')

# Function to update a group
def update_group(token, group_id, update_data):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.put(f"{BASE_URL}/groups/{group_id}", json=update_data, headers=headers)
    return response

# Setup a mock group
owner_token = get_jwt_token(OWNER_CREDENTIALS)
group_data = {"ownerID": 3, "title": "Test Group", "description": "A test group", "maxUsers": 10}
group_id = create_group(owner_token, group_data)

# Update Data
update_data = {"title": "Updated Test Group", "description": "An updated test group", "maxUsers": 15}

# Test as the owner
print("Testing update as the owner:")
response = update_group(owner_token, group_id, update_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as a non-owner
non_owner_token = get_jwt_token(NON_OWNER_CREDENTIALS)
print("\nTesting update as a non-owner:")
response = update_group(non_owner_token, group_id, update_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as an admin
admin_token = get_jwt_token(ADMIN_CREDENTIALS)
print("\nTesting update as an admin:")
response = update_group(admin_token, group_id, update_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
