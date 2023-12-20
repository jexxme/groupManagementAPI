import requests

# URL for login endpoint
login_url = "http://127.0.0.1:5000/login"

# User's credentials
credentials = {
    "email": "user",
    "password": "password123"
}

# Send a POST request to login and get the access token
response = requests.post(login_url, json=credentials)
access_token = response.json().get("access_token")

# URL for the protected endpoint
protected_url = "http://127.0.0.1:5000/protected"

# Set the Authorization header with the received token
headers = {
    'Authorization': f'Bearer {access_token}'
}

# Send a GET request to the protected endpoint
protected_response = requests.get(protected_url, headers=headers)

# Process the response from the protected endpoint
print(protected_response.json())
