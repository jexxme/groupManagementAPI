import requests
import json

# Constants
BASE_URL = "http://127.0.0.1:5000"  # Update with your Flask app's URL
GROUP_ID = 1  # Replace with an actual groupID from your database

# Send a GET request to retrieve a single group by groupID
response = requests.get(f"{BASE_URL}/groups/{GROUP_ID}")

# Print the response from the server
print(f"Status Code: {response.status_code}")
print(f"Response: {json.dumps(response.json(), indent=4)}")
