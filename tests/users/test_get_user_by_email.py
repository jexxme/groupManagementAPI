import requests

def test_get_user_by_email():
    # Constants
    BASE_URL = "http://127.0.0.1:5000"  # Modify if your server runs on a different URL
    email_to_test = "admin@admin.admin"

    # Making a GET request to fetch the user by email
    response = requests.get(f"{BASE_URL}/users/email/{email_to_test}")
    
    # Assertions to verify the response
    assert response.status_code == 200, "Expected status code 200, got {}".format(response.status_code)
    data = response.json()
    assert data['email'] == email_to_test, f"Expected email {email_to_test}, got {data.get('email')}"

    # Additional checks can be added here based on the expected response structure
    # For example, checking if the firstName or isAdmin fields are present
    assert 'firstName' in data, "firstName field is missing in the response"
    assert 'isAdmin' in data, "isAdmin field is missing in the response"

    print("Test passed - User fetched successfully!")

# Running the test function
test_get_user_by_email()
