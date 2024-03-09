import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Modify if your server runs on a different URL

# Helper function to login and get token
def get_token(email, password):
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    return response.json().get('access_token')

# Function to update user details
def update_user(user_id, token, updated_data):
    headers = {'Authorization': f'Bearer {token}'}
    response = requests.put(f"{BASE_URL}/users/{user_id}", headers=headers, json=updated_data)
    return response

# Test data
admin_email = "admin@admin.admin"  # Replace with actual admin email
admin_password = "admin"   # Replace with actual admin password
user_email = "newstuff@example.com"    # Replace with actual user email
user_password = "newpassword"     # Replace with actual user password
user_id_to_update = "3"            # ID of the user to update
updated_data = {"email": "newstuff@example.com", "firstName": "NewSTuName"}

# Get tokens
admin_token = get_token(admin_email, admin_password)
user_token = get_token(user_email, user_password)

# Test updating as admin
print("Testing update as admin:")
response = update_user(user_id_to_update, admin_token, updated_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Test updating as user
print("\nTesting update as regular user:")
response = update_user(user_id_to_update, user_token, updated_data)
print(f"Status Code: {response.status_code}, Response: {response.json()}")
