import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
CREDENTIALS = {"email": "test", "password": "test"}  # Replace with valid credentials
VALID_USER_ID = 4  # Replace with a valid userID
INVALID_USER_ID = 999  # An assumed invalid userID for negative test

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to get groups for a user
def get_groups_for_user(token, user_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/users_in_groups/{user_id}/", headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(CREDENTIALS)

# Positive Test: Fetch groups for a valid user
print("Positive Test - Fetch groups for a valid user:")
response = get_groups_for_user(token, VALID_USER_ID)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Negative Test: Fetch groups for an invalid user
print("\nNegative Test - Fetch groups for an invalid user:")
response = get_groups_for_user(token, INVALID_USER_ID)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
