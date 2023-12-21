import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
CREDENTIALS = {"email": "test", "password": "test"}  # Replace with valid credentials
USER_ID = 3  # Replace with a valid userID
GROUP_ID = 13  # Replace with a valid groupID

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to add a user to a group (assuming you have this functionality)
def add_user_to_group(token, user_id, group_id):
    data = {"userID": user_id, "groupID": group_id}
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{BASE_URL}/users_in_groups", json=data, headers=headers)
    return response

# Function to delete a user from a group
def delete_user_from_group(token, user_id, group_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f"{BASE_URL}/users_in_groups/{user_id}/{group_id}", headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(CREDENTIALS)

# Add user to group for testing
add_response = add_user_to_group(token, USER_ID, GROUP_ID)
print(f"Add User to Group Response Status Code: {add_response.status_code}, Response: {add_response.json()}")

# Delete user from group
delete_response = delete_user_from_group(token, USER_ID, GROUP_ID)
print(f"Delete User from Group Response Status Code: {delete_response.status_code}, Response: {delete_response.json()}")
