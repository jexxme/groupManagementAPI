import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Modify this if your server is running on a different URL

# Helper function to login and get token
def get_token(email, password):
    response = requests.post(f"{BASE_URL}/login", json={"email": email, "password": password})
    return response.json().get('access_token')

# Testing admin access
def test_admin_route(email, password):
    token = get_token(email, password)
    if token:
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(f"{BASE_URL}/admin-only", headers=headers)
        print(f"Status Code: {response.status_code}, Response: {response.json()}")
    else:
        print("Failed to authenticate")

# Replace with the credentials of an admin user
admin_email = "admin@admin.admin"
admin_password = "admin"

# Replace with the credentials of a regular user
user_email = "user"
user_password = "password123"

print("Testing with Admin User:")
test_admin_route(admin_email, admin_password)

print("\nTesting with Regular User:")
test_admin_route(user_email, user_password)
