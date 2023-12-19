import requests
import json

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Update with your Flask app's URL
ADMIN_CREDENTIALS = {"email": "admin", "password": "admin"}
OWNER_CREDENTIALS = {"email": "test", "password": "test"}
GROUP_ID = 4  # Replace with a valid groupID

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to update group
def update_group(token, group_id, update_data):
    headers = {'Authorization': f'Bearer {token}'} if token else {}
    response = requests.put(f"{BASE_URL}/groups/{group_id}", json=update_data, headers=headers)
    return response

# Test Data
update_data = {
    "ownerID": 2,  # New owner ID
    "title": "Updated Study Group for Math",
    "description": "Updated description",
    "maxUsers": 20
}

# Test as a not logged in user
response = update_group(None, GROUP_ID, update_data)
print("Not Logged In User Test:")
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as an admin user
admin_token = get_jwt_token(ADMIN_CREDENTIALS)
response = update_group(admin_token, GROUP_ID, update_data)
print("\nAdmin User Test:")
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as the owner of the group
owner_token = get_jwt_token(OWNER_CREDENTIALS)
response = update_group(owner_token, GROUP_ID, update_data)
print("\nGroup Owner Test:")
print(f"Status Code: {response.status_code}, Response: {response.json()}")
