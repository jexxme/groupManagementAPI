import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Modify if your server runs on a different URL

# Function to add a new user
def add_user(user_data):
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    return response

# Test data for new user
new_user_data = {
    "email": "newuser@example.com",
    "firstName": "New",
    "password": "newpassword",
    "isAdmin": False  # Change to True if you want to create an admin user
}

# Test adding a new user
print("Testing add new user:")
response = add_user(new_user_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
