import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
CREDENTIALS = {"email": "test", "password": "test"}  # Replace with valid credentials
DATE_ID = 1  # Replace with a valid dateID

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to get a specific date
def get_specific_date(token, date_id):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.get(f"{BASE_URL}/dates/{date_id}", headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(CREDENTIALS)

# Get specific date
response = get_specific_date(token, DATE_ID)
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
