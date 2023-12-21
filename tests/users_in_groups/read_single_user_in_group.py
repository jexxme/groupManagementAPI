import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"
# Test Parameters (replace with actual values from your database)
TEST_USER_ID = 6
TEST_GROUP_ID = 14

# Function to get a single user in a group
def get_user_in_group(user_id, group_id):
    response = requests.get(f"{BASE_URL}/users_in_groups/{user_id}/{group_id}")
    return response

# Get user in group
response = get_user_in_group(TEST_USER_ID, TEST_GROUP_ID)
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
