import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
ADMIN_CREDENTIALS = {"email": "admin", "password": "admin"}
OWNER_CREDENTIALS = {"email": "test", "password": "test"}
UNAUTHORIZED_CREDENTIALS = {"email": "petermurller@mail.com", "password": "peterspw"}
GROUP_ID = 14  # Replace with a valid groupID

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to create a date
def create_date(token, group_id, date_data):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.post(f"{BASE_URL}/dates", json=date_data, headers=headers)
    return response

# Date data to be sent
date_data = {
    "groupID": GROUP_ID,
    "date": "2023-12-25 14:00:00",
    "place": "Study Hall",
    "maxUsers": 20
}

# Test as the owner
owner_token = get_jwt_token(OWNER_CREDENTIALS)
print("Testing create date as the owner:")
response = create_date(owner_token, GROUP_ID, date_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as an admin user
admin_token = get_jwt_token(ADMIN_CREDENTIALS)
print("\nTesting create date as an admin:")
response = create_date(admin_token, GROUP_ID, date_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as an unauthorized user
unauthorized_token = get_jwt_token(UNAUTHORIZED_CREDENTIALS)
print("\nTesting create date as an unauthorized user:")
response = create_date(unauthorized_token, GROUP_ID, date_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
