import requests

# Constants
BASE_URL = "http://127.0.0.1:5000"

# Function to get all dates
def get_all_dates():
    response = requests.get(f"{BASE_URL}/dates")
    return response

# Get all dates
response = get_all_dates()
print(f"Response Status Code: {response.status_code}, Response: {response.json()}")
