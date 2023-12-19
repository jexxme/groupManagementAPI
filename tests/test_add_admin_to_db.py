from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime

# Assuming you are using SQLite as per your Flask app configuration
DATABASE_URI = 'sqlite:///data.db'  # Update if your database URI is different

# SQLAlchemy engine
engine = create_engine(DATABASE_URI)

# Create a new session
Session = sessionmaker(bind=engine)
session = Session()

# Assuming this is how your User model is defined
class User:
    def __init__(self, email, firstName, password, isAdmin):
        self.email = email
        self.firstName = firstName
        self.password = password  # In a real application, hash this password
        self.isAdmin = isAdmin

# Replace these details with the admin user's details
admin_email = "admin@example.com"
admin_firstName = "Admin"
admin_password = "adminpassword"  # You should hash the password
admin_isAdmin = True

# Create an admin user instance
admin_user = User(email=admin_email, firstName=admin_firstName, password=admin_password, isAdmin=admin_isAdmin)

# Add the admin user to the session and commit
session.add(admin_user)
session.commit()

print("Admin user inserted into the database.")

# Close the session
session.close()
