import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
CREDENTIALS = {"email": "test", "password": "test"}  # Replace with valid credentials
DATE_ID = 3  # Replace with a valid dateID

# Update data (modify as needed)
UPDATE_DATA = {
    "groupID": 2,  # New group ID
    "date": "2023-12-31 15:00:00",  # New date and time
    "place": "New Place",  # New place
    "maxUsers": 25  # New max users
}

# Function to get JWT token
def get_jwt_token(credentials):
    response = requests.post(f"{BASE_URL}/login", json=credentials)
    return response.json().get('access_token')

# Function to update a specific date
def update_specific_date(token, date_id, update_data):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.put(f"{BASE_URL}/dates/{date_id}", json=update_data, headers=headers)
    return response

# Acquire JWT token
token = get_jwt_token(CREDENTIALS)

# Update the specific date
response = update_specific_date(token, DATE_ID, UPDATE_DATA)
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
