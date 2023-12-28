import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import os

# Constants
BASE_URL = "http://127.0.0.1:5000"
ADMIN_CREDENTIALS = {"email": "jerome@admin.admin", "password": "jerome28092000"}
IMAGE_PATH = os.path.join(os.getcwd(), 'jerome.jpg')

# Authenticate and get JWT token
def authenticate():
    response = requests.post(f"{BASE_URL}/login", json=ADMIN_CREDENTIALS)
    return response.json().get('access_token')

# Upload profile picture
def upload_profile_picture(token, user_id, image_path):
    multipart_data = MultipartEncoder(
        fields={
            'user_id': str(user_id),
            'file': ('profilepicture.jpg', open(image_path, 'rb'), 'image/jpeg')
        }
    )

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': multipart_data.content_type
    }

    response = requests.post(f"{BASE_URL}/upload_profile_picture", headers=headers, data=multipart_data)
    return response

# Download profile picture
def download_profile_picture(user_id):
    response = requests.get(f"{BASE_URL}/profile_picture/{user_id}")
    return response

# Test the upload and download process
def test_profile_picture_upload_and_download():
    token = authenticate()
    if not token:
        print("Authentication failed.")
        return

    # Assuming admin user's ID is 1
    upload_response = upload_profile_picture(token, 1, IMAGE_PATH)
    print(f"Upload Response: {upload_response.status_code}, {upload_response.json()}")

    download_response = download_profile_picture(5)
    if download_response.status_code == 200:
        with open('downloaded_image_admin.jpg', 'wb') as f:
            f.write(download_response.content)
        print("Downloaded profile picture saved as downloaded_image.jpg")
    else:
        print(f"Download Response: {download_response.status_code}, {download_response.json()}")

# Run the test
test_profile_picture_upload_and_download()
