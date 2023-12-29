# Filename: app.py

from datetime import datetime
import re
from functools import wraps

from flask import Flask, jsonify, render_template, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager, create_access_token, get_jwt, get_jwt_identity, jwt_required, verify_jwt_in_request
)
from sqlalchemy.orm.exc import NoResultFound
import dateutil.parser
from dotenv import load_dotenv
import os
from werkzeug.utils import secure_filename
from flask import send_file
import json
import logging
from flask import request


load_dotenv()

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['UPLOAD_FOLDER'] = './userdata/pictures/profilepicture'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['MAX_CONTENT_LENGTH'] = 3 * 1024 * 1024  # 3 M


jwt = JWTManager(app)
db = SQLAlchemy(app)

BLACKLIST_FILE_PATH = './static/blacklist.txt'
BANNED_EMAILS_FILE_PATH = './static/banned_emails.txt'


# Allowed file types for profile pictures
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Database Models
class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    profile_picture = db.Column(db.String(255))  # Path to profile picture

class UsersInGroups(db.Model):
    userID = db.Column(db.Integer, db.ForeignKey('user.userID'), primary_key=True)
    groupID = db.Column(db.Integer, db.ForeignKey('group.groupID'), primary_key=True)
    startingDate = db.Column(db.DateTime, nullable=False)

class Group(db.Model):
    groupID = db.Column(db.Integer, primary_key=True)
    ownerID = db.Column(db.Integer, db.ForeignKey('user.userID'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    maxUsers = db.Column(db.Integer)

class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    groupID = db.Column(db.Integer, db.ForeignKey('group.groupID'), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    place = db.Column(db.String(100), nullable=False)
    maxUsers = db.Column(db.Integer)


# Custom decorator for admin-only routes
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return jsonify({'message':"Administratorrechte erforderlich!"}), 403
        else:
            return fn(*args, **kwargs)
    return wrapper


# Configure the main logger for Flask (optional)
logging.basicConfig(filename='flask.log', level=logging.INFO)

# Configure a separate logger for API access logs
api_logger = logging.getLogger('api_access_logger')
api_handler = logging.FileHandler('api_access.log')
api_formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
api_handler.setFormatter(api_formatter)
api_logger.addHandler(api_handler)
api_logger.setLevel(logging.INFO)

# Log decorator
def log_access(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity() if verify_jwt_in_request(optional=True) else 'Anonymous'
        log_data = {
            "user_id": user_id,
            "time": datetime.now().isoformat(),
            "route": request.path,
            "method": request.method,
            "data": request.json if request.method == 'POST' else 'N/A'
        }
        api_logger.info(json.dumps(log_data))  # Use the separate logger for API access logs
        return func(*args, **kwargs)
    return wrapper

# Apply the decorator to every REST method
for rule in app.url_map.iter_rules():
    if rule.endpoint != 'static':
        view_func = app.view_functions[rule.endpoint]
        app.view_functions[rule.endpoint] = log_access(view_func)

@app.route('/api_logs', methods=['GET'])
@admin_required
@log_access
def get_api_logs():
    try:
        with open('api_access.log', 'r') as file:
            logs = file.readlines()
        return jsonify({'logs': logs}), 200
    except FileNotFoundError:
        return jsonify({'message': 'API-Zugriffsprotokolldatei nicht gefunden'}), 404
    except Exception as e:
        return jsonify({'message': str(e)}), 500



# / route for dashboard
@app.route('/')
@log_access
def hello_world():
    users = User.query.all()
    groups = Group.query.all()
    return render_template('index.html', users=users, groups=groups)



# ROUTES FOR AUTHENTICATION
# Login route for GET (Login page)
@app.route('/login', methods=['GET'])
@log_access
def login_page():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
@log_access
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Validate user credentials
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"message": "Bad username or password"}), 401

    # Create JWT token with additional user information
    user_claims = {
        "is_admin": user.isAdmin,
        "user_id": user.userID,
        "email": user.email,
        # You can add more user-specific information here if needed
    }
    access_token = create_access_token(identity=user.userID, additional_claims=user_claims)
    return jsonify(access_token=access_token)


# Protected route for users
@app.route('/whoami', methods=['GET'])
@jwt_required()
@log_access
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    
    # Get the user object from the database
    user = db.session.query(User).get(current_user)
    
    # Return the "Vorname" (first name) instead of "logged_in_as"
    return jsonify(Vorname=user.firstName), 200

# Protected route for admins
@app.route('/admin-only', methods=['GET'])
@admin_required
@log_access
def admin_only_route():
    # Admin-only logic
    return jsonify(msg="Welcome, admin!")



# Dashboard route 
@app.route('/dashboard')
@log_access
def dashboard():
    users = User.query.all()
    groups = Group.query.all()
    return render_template('index.html', users=users, groups=groups)




@app.route('/upload_profile_picture', methods=['POST'])
@jwt_required()
@log_access
def upload_profile_picture():
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    user_id_from_request = request.form.get('user_id')

    # Stellen Sie sicher, dass user_id_from_request nicht None ist, bevor Sie es in eine Ganzzahl umwandeln
    if user_id_from_request is None:
        return jsonify({'message': 'Benutzer-ID fehlt'}), 400

    if not is_admin and current_user_id != int(user_id_from_request):
        return jsonify({'message': 'Nicht berechtigt, das Profilbild dieses Benutzers zu ändern'}), 403

    if 'file' not in request.files:
        return jsonify({'message': 'Kein Dateiteil vorhanden'}), 400
    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'Keine ausgewählte Datei'}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_specific_path = os.path.join(app.config['UPLOAD_FOLDER'], str(current_user_id))
        
        # Create a directory for the user if it doesn't exist
        if not os.path.exists(user_specific_path):
            os.makedirs(user_specific_path)

        file_path = os.path.join(user_specific_path, filename)
        file.save(file_path)

        # Normalize the file path for cross-platform compatibility
        normalized_file_path = os.path.normpath(file_path)

        # Update user profile to include the picture path
        update_user_profile_picture_path(current_user_id, normalized_file_path)

        return jsonify({'message': 'Profilbild erfolgreich hochgeladen'}), 200
    else:
        return jsonify({'message': 'Ungültiger Dateityp oder Größe'}), 400




# Profile picture download route
@app.route('/profile_picture/<int:user_id>')
@log_access
def get_profile_picture(user_id):
    user_picture_path = get_user_profile_picture_path(user_id)
    if user_picture_path and os.path.exists(user_picture_path):
        return send_file(user_picture_path)
    else:
        return jsonify({'message': 'Profilbild nicht gefunden'}), 404

    
def get_user_profile_picture_path(user_id):
    user = User.query.get(user_id)
    if user and user.profile_picture:
        return user.profile_picture
    else:
        return None


def update_user_profile_picture_path(user_id, path):
    user = User.query.get(user_id)
    user.profile_picture = path
    db.session.commit()




@app.route('/blacklist', methods=['GET'])
@admin_required
@log_access
def get_blacklist():
    try:
        with open(BLACKLIST_FILE_PATH, 'r') as file:
            blacklist = file.read().splitlines()
        return jsonify(blacklist=blacklist), 200
    except FileNotFoundError:
        return jsonify(message='Blacklist-Datei nicht gefunden'), 404
    
@app.route('/blacklist', methods=['PUT'])
@admin_required
@log_access
def update_blacklist():
    if not request.json or 'blacklist' not in request.json:
        abort(400, description="Bitte geben Sie eine 'blacklist' Nutzlast an.")
    
    new_blacklist = request.json['blacklist']
    if not isinstance(new_blacklist, list):
        abort(400, description="Die 'blacklist' muss eine Liste von Wörtern sein.")
    
    try:
        with open(BLACKLIST_FILE_PATH, 'w') as file:
            file.write('\n'.join(new_blacklist))
        return jsonify(message='Blacklist erfolgreich aktualisiert'), 200
    except IOError as e:
        return jsonify(message='Beim Aktualisieren der Blacklist ist ein Fehler aufgetreten'), 500



@app.route('/banned_emails', methods=['GET'])
@log_access
def get_banned_emails():
    try:
        with open(BANNED_EMAILS_FILE_PATH, 'r') as file:
            banned_emails = file.read().splitlines()
        return jsonify(banned_emails=banned_emails), 200
    except FileNotFoundError:
        return jsonify(message='Datei mit gesperrten E-Mails nicht gefunden'), 404


@app.route('/banned_emails', methods=['PUT'])
@log_access
def update_banned_emails():
    if not request.json or 'banned_emails' not in request.json:
        abort(400, description="Bitte geben Sie eine 'banned_emails' Nutzlast an.")
    
    new_banned_emails = request.json['banned_emails']
    if not isinstance(new_banned_emails, list):
        abort(400, description="Die 'banned_emails' muss eine Liste von E-Mails sein.")
    
    try:
        with open(BANNED_EMAILS_FILE_PATH, 'w') as file:
            file.write('\n'.join(new_banned_emails))
        return jsonify(message='Gesperrte E-Mails erfolgreich aktualisiert'), 200
    except IOError as e:
        return jsonify(message='Beim Aktualisieren der gesperrten E-Mails ist ein Fehler aufgetreten'), 500


# CRUD Routes for Users
# Create new user
@app.route('/users', methods=['POST'])
@log_access
def create_user():
    data = request.get_json()

    # Email pattern check
    if not re.search(r"@[gG][sS][oO]\.schule\.koeln$", data['email']):
        return jsonify({'message': 'Es sind nur E-Mails von @gso.schule.koeln erlaubt'}), 400

    # Check if email already exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'message': 'Ein Benutzer mit dieser E-Mail-Adresse existiert bereits'}), 409  # 409 Conflict

    new_user = User(email=data['email'], firstName=data['firstName'],
                    password=data['password'], isAdmin=False)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Neuer Benutzer erstellt'}), 201


# Create new admin user
@app.route('/admin', methods=['POST'])
@admin_required
@log_access
def create_admin():
    data = request.get_json()

    # Check if email already exists
    existing_admin = User.query.filter_by(email=data['email'], isAdmin=True).first()
    if existing_admin:
        return jsonify({'message': 'Ein Admin mit dieser E-Mail-Adresse existiert bereits'}), 409  # 409 Conflict

    new_user = User(email=data['email'], firstName=data['firstName'],
                    password=data['password'], isAdmin=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Neuer Admin erstellt'}), 201

# Read all users
@app.route('/users', methods=['GET'])
@admin_required
@log_access
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'userID': user.userID, 'email': user.email, 
                     'firstName': user.firstName, 'password': user.password,
                     'isAdmin': user.isAdmin}
        output.append(user_data)
    return jsonify(output)

# Read a single user by userID
@app.route('/users/<id>', methods=['GET'])
@log_access
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'userID': user.userID, 'email': user.email, 
                    'firstName': user.firstName, 'isAdmin': user.isAdmin})


@app.route('/users/<id>', methods=['PUT'])
@jwt_required()
@log_access
def update_user(id):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    # Check if the user is updating their own account or if they are an admin
    if str(current_user_id) != id and not is_admin:
        return jsonify({'message': 'Sie sind nicht authorisiert um diesen Benutzer zu bearbeiten!'}), 403

    user = User.query.get_or_404(id)
    data = request.get_json()

    # Allow users to update their own email and first name. Admins can update everything.
    if str(current_user_id) == id:
        user.email = data.get('email', user.email)
        user.firstName = data.get('firstName', user.firstName)

    # Only admins can change the 'isAdmin' field and passwords
    if is_admin:
        user.email = data.get('email', user.email)
        user.firstName = data.get('firstName', user.firstName)
        user.password = data.get('password', user.password)  # Consider hashing the password
        user.isAdmin = data.get('isAdmin', user.isAdmin)

    db.session.commit()
    return jsonify({'message': 'Benutzer aktualisiert'})

# Delete a user
@app.route('/users/<id>', methods=['DELETE'])
@admin_required
@log_access
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Benutzer gelöscht'})



# CRUD Routes for Groups 

# Create a new group
@app.route('/groups', methods=['POST'])
@jwt_required()
@log_access
def create_group():
    data = request.get_json()
    new_group = Group(ownerID=data['ownerID'], title=data['title'],
                      description=data['description'], maxUsers=data['maxUsers'])
    db.session.add(new_group)
    db.session.commit()

    new_user_in_group = UsersInGroups(userID=data['ownerID'], groupID=new_group.groupID,
                                      startingDate=datetime.utcnow())
    db.session.add(new_user_in_group)
    db.session.commit()

    # Retrieve the groupID of the newly created group
    groupID = new_group.groupID

    # Return the groupID and a message
    return jsonify({'message': 'Neue Gruppe erstellt', 'groupID': groupID}), 201


# Read all groups
@app.route('/groups', methods=['GET'])
@log_access
def get_groups():
    groups = Group.query.all()
    output = []
    for group in groups:
        group_data = {'groupID': group.groupID, 'ownerID': group.ownerID, 
                      'title': group.title, 'description': group.description,
                      'maxUsers': group.maxUsers}
        output.append(group_data)
    return jsonify(output)

# Read a single group by groupID
@app.route('/groups/<groupID>', methods=['GET'])
@log_access
def get_group(groupID):
    group = Group.query.get_or_404(groupID)
    return jsonify({'groupID': group.groupID, 'ownerID': group.ownerID, 
                    'title': group.title, 'description': group.description,
                    'maxUsers': group.maxUsers})


@app.route('/groups/<groupID>', methods=['PUT'])
@jwt_required()
@log_access
def update_group(groupID):
    # Get the current user's identity and claims
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    # Fetch the group
    group = Group.query.get_or_404(groupID)

    # Check if the user is the owner or an admin
    if str(current_user_id) != str(group.ownerID) and not is_admin:
        return jsonify({'message': 'Sie sind nicht authorisiert um diese Gruppe zu bearbeiten!'}), 403

    # Update group details
    data = request.get_json()
    group.ownerID = data.get('ownerID', group.ownerID)
    group.title = data.get('title', group.title)
    group.description = data.get('description', group.description)
    group.maxUsers = data.get('maxUsers', group.maxUsers)
    db.session.commit()

    return jsonify({'message': 'Gruppe aktualisiert'})

# Delete a group
@app.route('/groups/<groupID>', methods=['DELETE'])
@jwt_required()
@log_access
def delete_group(groupID):

    # Get the current user's identity and claims
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    # Fetch the group
    group = Group.query.get_or_404(groupID)

    # Check if the user is the owner or an admin
    if str(current_user_id) != str(group.ownerID) and not is_admin:
        return jsonify({'message': 'Sie sind nicht authorisiert um diese Gruppe zu löschen!'}), 403

    db.session.delete(group)
    db.session.commit()
    return jsonify({'message': 'Gruppe gelöscht'})


# Read all members of a group
@app.route('/groups/<groupID>/members', methods=['GET'])
@jwt_required()
@log_access
def get_members(groupID):
    members = UsersInGroups.query.filter_by(groupID=groupID).all()
    output = []
    for member in members:
        member_data = {'userID': member.userID, 'groupID': member.groupID, 
                       'startingDate': member.startingDate}
        output.append(member_data)
    return jsonify(output)

# CRUD Routes for UsersInGroups
# Create a new user in group
@app.route('/users_in_groups', methods=['POST'])
@jwt_required()
@log_access
def create_user_in_group():
    data = request.get_json()

    # Check if the user exists
    try:
        user = User.query.filter_by(userID=data['userID']).one()
    except NoResultFound:
        return jsonify({'message': 'Benutzer nicht gefunden'}), 404

    # Check if the group exists
    try:
        group = Group.query.filter_by(groupID=data['groupID']).one()
    except NoResultFound:
        return jsonify({'message': 'Gruppe nicht gefunden'}), 404

    # Check if the group is full
    current_members_count = UsersInGroups.query.filter_by(groupID=group.groupID).count()
    if current_members_count >= group.maxUsers:
        return jsonify({'message': 'Gruppe ist bereits voll'}), 400

    # Add the user to the group with the current date as the starting date
    new_user_in_group = UsersInGroups(userID=data['userID'], groupID=data['groupID'],
                                      startingDate=datetime.utcnow())
    db.session.add(new_user_in_group)
    db.session.commit()
    return jsonify({'message': 'Benutzer wurde der Gruppe hinzugefügt'}), 201


# Read all users in all groups
@app.route('/users_in_groups', methods=['GET'])
@jwt_required()
@log_access
def get_users_in_groups():
    users_in_groups = UsersInGroups.query.all()
    output = []
    for user_in_group in users_in_groups:
        user_in_group_data = {'userID': user_in_group.userID, 'groupID': user_in_group.groupID, 
                              'startingDate': user_in_group.startingDate}
        output.append(user_in_group_data)
    return jsonify(output)

# Read a single user in group by userID and groupID
@app.route('/users_in_groups/<userID>/<groupID>', methods=['GET'])
@jwt_required()
@log_access
def get_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    return jsonify({'userID': user_in_group.userID, 'groupID': user_in_group.groupID, 
                    'startingDate': user_in_group.startingDate})

# Get all groups for a user
@app.route('/users_in_groups/<int:userID>/', methods=['GET'])
@jwt_required()
@log_access
def get_groups_for_user(userID):
    user_groups = UsersInGroups.query.filter_by(userID=userID).all()
    output = []
    for user_group in user_groups:
        group_data = {
            'userID': user_group.userID,
            'groupID': user_group.groupID,
            'startingDate': user_group.startingDate
        }
        output.append(group_data)
    return jsonify(output)


# Delete a user in group
@app.route('/users_in_groups/<userID>/<groupID>', methods=['DELETE'])
@jwt_required()
@log_access
def delete_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    db.session.delete(user_in_group)
    db.session.commit()
    return jsonify({'message': 'Benutzer wurde aus der Gruppe entfernt'})


# CRUD Routes for Dates
@app.route('/dates', methods=['POST'])
@jwt_required()
@log_access
def create_date():
    data = request.get_json()
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    # Convert the date string to a datetime object
    try:
        parsed_date = dateutil.parser.parse(data['date'])
    except ValueError as e:
        return jsonify({'message': str(e)}), 400


    # Fetch the group
    group = Group.query.get_or_404(data['groupID'])

    # Check if the user is the owner or an admin
    if str(current_user_id) != str(group.ownerID) and not is_admin:
        return jsonify({'message': 'Sie sind nicht authorisiert einen Termin für diese Gruppe zu erstellen'}), 403

    # Create the new date
    new_date = Date(groupID=data['groupID'], date=parsed_date,
                    place=data['place'], maxUsers=data['maxUsers'])
    db.session.add(new_date)
    db.session.commit()
    return jsonify({'message': 'Neuer Termin erstellt'}), 201


# Read all dates
@app.route('/dates', methods=['GET'])
@jwt_required()
@log_access
def get_dates():
    dates = Date.query.all()
    output = []
    for date in dates:
        date_data = {'id': date.id, 'groupID': date.groupID,
                     'date': date.date, 'place': date.place,
                     'maxUsers': date.maxUsers}
        output.append(date_data)
    return jsonify(output)

# Read a single date by dateID
@app.route('/dates/<dateID>', methods=['GET'])
@jwt_required()
@log_access
def get_date(dateID):
    date = Date.query.get_or_404(dateID)
    return jsonify({'id': date.id, 'groupID': date.groupID,
                    'date': date.date, 'place': date.place,
                    'maxUsers': date.maxUsers})


@app.route('/dates/<dateID>', methods=['PUT'])
@jwt_required()
@log_access
def update_date(dateID):
    date = Date.query.get_or_404(dateID)
    data = request.get_json()

    # Check if 'date' is in data and convert it to datetime object
    if 'date' in data:
        try:
            data['date'] = dateutil.parser.parse(data['date'])
        except ValueError as e:
            return jsonify({'message': str(e)}), 400

    date.groupID = data.get('groupID', date.groupID)
    date.date = data.get('date', date.date)
    date.place = data.get('place', date.place)
    date.maxUsers = data.get('maxUsers', date.maxUsers)
    
    db.session.commit()
    return jsonify({'message': 'Termin bearbeitet'})


@app.route('/dates/<dateID>', methods=['DELETE'])
@jwt_required()
@log_access
def delete_date(dateID):
    current_user_id = get_jwt_identity()
    claims = get_jwt()
    is_admin = claims.get('is_admin', False)

    date = Date.query.get_or_404(dateID)
    group = Group.query.get_or_404(date.groupID)

    # Check if the user is the owner of the group or an admin
    if str(current_user_id) != str(group.ownerID) and not is_admin:
        return jsonify({'message': 'Sie sind nicht authorisiert diesen Termin zu löschen!'}), 403

    db.session.delete(date)
    db.session.commit()
    return jsonify({'message': 'Termin gelöscht'})


if __name__ == '__main__':
    app.run(debug=True)
