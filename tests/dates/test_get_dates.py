import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
CREDENTIALS = {"email": "test", "password": "test"}  # Replace with valid credentials

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to get all dates with JWT token
def get_all_dates(token):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/dates", headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(CREDENTIALS)

# Get all dates with authentication
response = get_all_dates(token)
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
