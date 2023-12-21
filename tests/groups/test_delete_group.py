import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
ADMIN_CREDENTIALS = {"email": "admin", "password": "admin"}
OWNER_CREDENTIALS = {"email": "test", "password": "test"}
NON_OWNER_CREDENTIALS = {"email": "petermurller@mail.com", "password": "peterspw"}

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to create a group
def create_group(token, owner_id=3):
    group_data = {"ownerID": owner_id, "title": "Test Group", "description": "A test group", "maxUsers": 10}
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{BASE_URL}/groups", json=group_data, headers=headers)
    return response.json().get('groupID')

# Function to delete a group
def delete_group(token, group_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f"{BASE_URL}/groups/{group_id}", headers=headers)
    return response

# Positive test: Delete as owner
owner_token = get_jwt_token(OWNER_CREDENTIALS)
group_id_for_owner_test = create_group(owner_token)
print("Positive Test - Delete as Owner:")
response = delete_group(owner_token, group_id_for_owner_test)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Negative test: Delete as non-owner
non_owner_token = get_jwt_token(NON_OWNER_CREDENTIALS)
group_id_for_non_owner_test = create_group(owner_token)  # Create a new group for this test
print("\nNegative Test - Delete as Non-Owner:")
response = delete_group(non_owner_token, group_id_for_non_owner_test)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Negative test: Delete as admin
admin_token = get_jwt_token(ADMIN_CREDENTIALS)
group_id_for_admin_test = create_group(owner_token)  # Create a new group for this test
print("\nNegative Test - Delete as Admin:")
response = delete_group(admin_token, group_id_for_admin_test)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
