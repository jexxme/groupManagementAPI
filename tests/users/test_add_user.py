import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Modify if your server runs on a different URL

# Function to add a new user
def add_user(user_data):
    response = requests.post(f"{BASE_URL}/users", json=user_data)
    return response

# Positive test data for new user (with correct email pattern)
positive_user_data = {
    "email": "positiveuser@gso.schule.koeln",
    "firstName": "Positive",
    "password": "password123",
    "isAdmin": False
}

# Negative test data for new user (with incorrect email pattern)
negative_user_data = {
    "email": "negativeuser@example.com",
    "firstName": "Negative",
    "password": "password123",
    "isAdmin": False
}

# Test adding a new user with correct email pattern
print("Testing add new user with correct email pattern:")
response = add_user(positive_user_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test adding a new user with incorrect email pattern
print("\nTesting add new user with incorrect email pattern:")
response = add_user(negative_user_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
