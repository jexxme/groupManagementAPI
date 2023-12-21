import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
ADMIN_CREDENTIALS = {"email": "admin", "password": "admin"}
OWNER_CREDENTIALS = {"email": "test", "password": "test"}
NON_OWNER_CREDENTIALS = {"email": "petermurller@mail.com", "password": "peterspw"}
DATE_ID = 4  # Replace with a valid dateID


# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to delete a date and handle the response
def delete_date(token, date_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.delete(f"{BASE_URL}/dates/{date_id}", headers=headers)
    try:
        response_data = response.json()
    except requests.exceptions.JSONDecodeError:
        response_data = 'No content'
    return response.status_code, response_data

# Test as the owner
owner_token = get_jwt_token(OWNER_CREDENTIALS)
print("Testing delete date as the owner:")
status_code, response_data = delete_date(owner_token, DATE_ID)
print(f"Status Code: {status_code}, Response: {response_data}")

# Test as an admin user
admin_token = get_jwt_token(ADMIN_CREDENTIALS)
print("\nTesting delete date as an admin:")
response = delete_date(admin_token, DATE_ID)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test as a non-owner
non_owner_token = get_jwt_token(NON_OWNER_CREDENTIALS)
print("\nTesting delete date as a non-owner:")
response = delete_date(non_owner_token, DATE_ID)
print(f"Status Code: {response.status_code}, Response: {response.json()}")