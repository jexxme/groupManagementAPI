# Filename: run.py

from app import app, db

# Create tables and start the application
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run()
