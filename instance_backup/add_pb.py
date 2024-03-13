import requests
import sqlite3
from os.path import join, dirname, abspath
from time import sleep
import random

# Assuming your SQLite DB is in the same directory as your script
DATABASE_PATH = join(dirname(abspath(__file__)), 'data.db')

def login():
    """Log in to the API and return the JWT token."""
    url = "https://lbv.digital/login"
    credentials = {
        "email": "admin@admin.admin",
        "password": "admin"
    }
    response = requests.post(url, json=credentials)
    response.raise_for_status()  # This will raise an exception for HTTP error codes
    return response.json()['access_token']

def get_users_without_profile_picture():
    """Query the database for users without a profile picture."""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT userID FROM user;")
    users = cursor.fetchall()
    conn.close()
    return [user[0] for user in users]

def get_random_picture():
    """Get a random picture from picsum.photos."""
    response = requests.get(f'https://api.dicebear.com/7.x/personas/png?seed={random.randint(1, 1000)}', allow_redirects=True)
    return response.content

def upload_profile_picture(user_id, picture, token):
    """Upload a profile picture for a given user."""
    url = 'https://lbv.digital/upload_profile_picture'
    files = {'file': ('profile.jpg', picture, 'image/jpeg')}
    data = {'user_id': user_id}
    headers = {'Authorization': f'Bearer {token}'}
    
    response = requests.post(url, files=files, data=data, headers=headers)
    print(f"User {user_id}: {response.json()}")
    sleep(1)  # Sleep for 1 second to avoid rate limiting

def main():
    token = login()  # Log in to get the JWT token
    users = get_users_without_profile_picture()
    for user_id in users:
        picture = get_random_picture()
        upload_profile_picture(user_id, picture, token)

if __name__ == "__main__":
    main()
