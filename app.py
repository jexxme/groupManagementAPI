# Filename: app.py

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import render_template
import re
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request
from flask import jsonify, request
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'secretXYZ'  # Change this to a random secret key
jwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    userID = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    firstName = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)

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
            return jsonify(msg="Administratorrechte erforderlich!"), 403
        else:
            return fn(*args, **kwargs)
    return wrapper

# / route for dashboard
@app.route('/')
def hello_world():
    users = User.query.all()
    groups = Group.query.all()
    return render_template('index.html', users=users, groups=groups)


@app.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    # Validate user credentials
    user = User.query.filter_by(email=email, password=password).first()
    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Create JWT token with additional user information
    user_claims = {
        "is_admin": user.isAdmin,
        "user_id": user.userID,
        "email": user.email,
        # You can add more user-specific information here if needed
    }
    access_token = create_access_token(identity=user.userID, additional_claims=user_claims)
    return jsonify(access_token=access_token)



# TEST ROUTES FOR AUTHENTICATION
# Protected route for users
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Protected route for admins
@app.route('/admin-only', methods=['GET'])
@admin_required
def admin_only_route():
    # Admin-only logic
    return jsonify(msg="Welcome, admin!")





# CRUD Routes for Users
# Create new user
@app.route('/users', methods=['POST'])
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
def create_admin():
    data = request.get_json()
    new_user = User(email=data['email'], firstName=data['firstName'],
                    password=data['password'], isAdmin=True)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Neuer Admin erstellt'}), 201

# Read all users
@app.route('/users', methods=['GET'])
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
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'userID': user.userID, 'email': user.email, 
                    'firstName': user.firstName, 'isAdmin': user.isAdmin})


@app.route('/users/<id>', methods=['PUT'])
@jwt_required()
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
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Benutzer gelöscht'})



# CRUD Routes for Groups 

# Create a new group
@app.route('/groups', methods=['POST'])
@jwt_required()
def create_group():
    data = request.get_json()
    new_group = Group(ownerID=data['ownerID'], title=data['title'],
                      description=data['description'], maxUsers=data['maxUsers'])
    db.session.add(new_group)
    db.session.commit()

    #  TODO: Add the owner to the group

    # Retrieve the groupID of the newly created group
    groupID = new_group.groupID

    # Return the groupID and a message
    return jsonify({'message': 'Neue Gruppe erstellt', 'groupID': groupID}), 201


# Read all groups
@app.route('/groups', methods=['GET'])
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
def get_group(groupID):
    group = Group.query.get_or_404(groupID)
    return jsonify({'groupID': group.groupID, 'ownerID': group.ownerID, 
                    'title': group.title, 'description': group.description,
                    'maxUsers': group.maxUsers})


@app.route('/groups/<groupID>', methods=['PUT'])
@jwt_required()
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

# CRUD Routes for UsersInGroups
# Create a new user in group
@app.route('/users_in_groups', methods=['POST'])
@jwt_required()
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
def get_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    return jsonify({'userID': user_in_group.userID, 'groupID': user_in_group.groupID, 
                    'startingDate': user_in_group.startingDate})

# TODO: Document this route
@app.route('/users_in_groups/<int:userID>/', methods=['GET'])
@jwt_required()
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


# Update a user in group
@app.route('/users_in_groups/<userID>/<groupID>', methods=['PUT'])
def update_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    data = request.get_json()
    user_in_group.startingDate = data.get('startingDate', user_in_group.startingDate)
    db.session.commit()
    return jsonify({'message': 'User in group updated'})

# Delete a user in group
@admin_required
@app.route('/users_in_groups/<userID>/<groupID>', methods=['DELETE'])
def delete_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    db.session.delete(user_in_group)
    db.session.commit()
    return jsonify({'message': 'User in group deleted'})

# View all members of a group
@app.route('/users_in_groups/<groupID>', methods=['GET'])
def get_users_in_group(groupID):
    users_in_group = UsersInGroups.query.filter_by(groupID=groupID).all()
    output = []
    for user_in_group in users_in_group:
        user_in_group_data = {'userID': user_in_group.userID, 'groupID': user_in_group.groupID, 
                              'startingDate': user_in_group.startingDate}
        output.append(user_in_group_data)
    return jsonify({'users_in_group': output})



# CRUD Routes for Dates
# Create a new date
@app.route('/dates', methods=['POST'])
def create_date():
    data = request.get_json()
    new_date = Date(groupID=data['groupID'], date=data['date'],
                    place=data['place'], maxUsers=data['maxUsers'])
    db.session.add(new_date)
    db.session.commit()
    return jsonify({'message': 'New date created'}), 201

# Read all dates
@app.route('/dates', methods=['GET'])
def get_dates():
    dates = Date.query.all()
    output = []
    for date in dates:
        date_data = {'id': date.id, 'groupID': date.groupID,
                     'date': date.date, 'place': date.place,
                     'maxUsers': date.maxUsers}
        output.append(date_data)
    return jsonify({'dates': output})

# Read a single date by dateID
@app.route('/dates/<dateID>', methods=['GET'])
def get_date(dateID):
    date = Date.query.get_or_404(dateID)
    return jsonify({'id': date.id, 'groupID': date.groupID,
                    'date': date.date, 'place': date.place,
                    'maxUsers': date.maxUsers})

# Update a date
@app.route('/dates/<dateID>', methods=['PUT'])
def update_date(dateID):
    date = Date.query.get_or_404(dateID)
    data = request.get_json()
    date.groupID = data.get('groupID', date.groupID)
    date.date = data.get('date', date.date)
    date.place = data.get('place', date.place)
    date.maxUsers = data.get('maxUsers', date.maxUsers)
    db.session.commit()
    return jsonify({'message': 'Date updated'})

# Delete a date
@admin_required
@app.route('/dates/<dateID>', methods=['DELETE'])
def delete_date(dateID):
    date = Date.query.get_or_404(dateID)
    db.session.delete(date)
    db.session.commit()
    return jsonify({'message': 'Date deleted'})
















if __name__ == '__main__':
    app.run(debug=True)
