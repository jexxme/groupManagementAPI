import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
OWNER_CREDENTIALS = {"email": "test", "password": "test"}
GROUP_ID = 14  # Group ID for testing

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to add a user to a group
def add_user_to_group(token, user_id, group_id):
    data = {"userID": user_id, "groupID": group_id}
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{BASE_URL}/users_in_groups", json=data, headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(OWNER_CREDENTIALS)

# Assuming userID 1 for testing - replace with an actual userID from your system
user_id = 6

# Add user to group
response = add_user_to_group(token, user_id, GROUP_ID)
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
