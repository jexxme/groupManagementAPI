# Filename: app.py

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify
from flask_restx import Api
from flask_restx import Resource, fields

app = Flask(__name__)

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

# CRUD Routes for Users

# Create a new user
@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(email=data['email'], firstName=data['firstName'],
                    password=data['password'], isAdmin=data.get('isAdmin', False))
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'New user created'}), 201

# Read all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    output = []
    for user in users:
        user_data = {'userID': user.userID, 'email': user.email, 
                     'firstName': user.firstName, 'isAdmin': user.isAdmin}
        output.append(user_data)
    return jsonify({'users': output})

# Read a single user by userID
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify({'userID': user.userID, 'email': user.email, 
                    'firstName': user.firstName, 'isAdmin': user.isAdmin})

# Update a user
@app.route('/users/<id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.email = data.get('email', user.email)
    user.firstName = data.get('firstName', user.firstName)
    user.password = data.get('password', user.password)
    user.isAdmin = data.get('isAdmin', user.isAdmin)
    db.session.commit()
    return jsonify({'message': 'User updated'})

# Delete a user
@app.route('/users/<id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted'})


# CRUD Routes for UsersInGroups

# Create a new user in group
@app.route('/users_in_groups', methods=['POST'])
def create_user_in_group():
    data = request.get_json()
    new_user_in_group = UsersInGroups(userID=data['userID'], groupID=data['groupID'],
                                      startingDate=data['startingDate'])
    db.session.add(new_user_in_group)
    db.session.commit()
    return jsonify({'message': 'New user added to the group'}), 201

# Read all users in groups
@app.route('/users_in_groups', methods=['GET'])
def get_users_in_groups():
    users_in_groups = UsersInGroups.query.all()
    output = []
    for user_in_group in users_in_groups:
        user_in_group_data = {'userID': user_in_group.userID, 'groupID': user_in_group.groupID, 
                              'startingDate': user_in_group.startingDate}
        output.append(user_in_group_data)
    return jsonify({'users_in_groups': output})

# Read a single user in group by userID and groupID
@app.route('/users_in_groups/<userID>/<groupID>', methods=['GET'])
def get_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    return jsonify({'userID': user_in_group.userID, 'groupID': user_in_group.groupID, 
                    'startingDate': user_in_group.startingDate})

# Update a user in group
@app.route('/users_in_groups/<userID>/<groupID>', methods=['PUT'])
def update_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    data = request.get_json()
    user_in_group.startingDate = data.get('startingDate', user_in_group.startingDate)
    db.session.commit()
    return jsonify({'message': 'User in group updated'})

# Delete a user in group
@app.route('/users_in_groups/<userID>/<groupID>', methods=['DELETE'])
def delete_user_in_group(userID, groupID):
    user_in_group = UsersInGroups.query.filter_by(userID=userID, groupID=groupID).first()
    db.session.delete(user_in_group)
    db.session.commit()
    return jsonify({'message': 'User in group deleted'})






# CRUD Routes for Groups 

# Create a new group
@app.route('/groups', methods=['POST'])
def create_group():
    data = request.get_json()
    new_group = Group(ownerID=data['ownerID'], title=data['title'],
                      description=data['description'], maxUsers=data['maxUsers'])
    db.session.add(new_group)
    db.session.commit()
    return jsonify({'message': 'New group created'}), 201


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
    return jsonify({'groups': output})

# Read a single group by groupID
@app.route('/groups/<groupID>', methods=['GET'])
def get_group(groupID):
    group = Group.query.get_or_404(groupID)
    return jsonify({'groupID': group.groupID, 'ownerID': group.ownerID, 
                    'title': group.title, 'description': group.description,
                    'maxUsers': group.maxUsers})

# Update a group
@app.route('/groups/<groupID>', methods=['PUT'])
def update_group(groupID):
    group = Group.query.get_or_404(groupID)
    data = request.get_json()
    group.ownerID = data.get('ownerID', group.ownerID)
    group.title = data.get('title', group.title)
    group.description = data.get('description', group.description)
    group.maxUsers = data.get('maxUsers', group.maxUsers)
    db.session.commit()
    return jsonify({'message': 'Group updated'})


# Delete a group
@app.route('/groups/<groupID>', methods=['DELETE'])
def delete_group(groupID):
    group = Group.query.get_or_404(groupID)
    db.session.delete(group)
    db.session.commit()
    return jsonify({'message': 'Group deleted'})


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
@app.route('/dates/<dateID>', methods=['DELETE'])
def delete_date(dateID):
    date = Date.query.get_or_404(dateID)
    db.session.delete(date)
    db.session.commit()
    return jsonify({'message': 'Date deleted'})



if __name__ == '__main__':
    app.run(debug=True)
