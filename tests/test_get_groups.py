import requests
import json

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Update with your Flask app's URL

# Send a GET request to retrieve all groups
response = requests.get(f"{BASE_URL}/groups")

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=4)}")
