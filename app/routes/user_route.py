from flask import Blueprint, request, jsonify
from ..schemas.user import UserSchema
from ..models.user import User
from sqlalchemy import select
from app.database import db
from marshmallow import ValidationError
from typing import TypedDict, cast

user_bp = Blueprint('users', __name__, url_prefix='/users')

schema = UserSchema()

#Without this, the static type checker complains alter on, because "it could be None". 
#Schema.load can *never* be none, just error, so this is a safe assertion to make.
class UserPayload(TypedDict):
    badge_num: str
    name: str
    password: str
    latitude: float | None
    longitude: float | None
    status: str 


@user_bp.route('/', methods=['GET'])
def get_users():
    """Endpoint to retrieve all users from the database. Queries the User model for all user records, serializes them using the UserSchema, and returns the data as a JSON response.

    Returns:
        Response: A Flask response object containing a JSON representation of all users in the database, along with an HTTP status code of 200 (OK).
    """

    #Select * from User
    stmt = select(User)

    #Run the query on the statement,scalar() returns actual user objects, all() makes a python list.
    result = db.session.execute(stmt).scalars().all()

    #Make all of the objects in the list into a dict, then jsonify the list of dicts and return it with a 200 status code.
    return jsonify([u.to_dict() for u in result]), 200

@user_bp.route('/', methods=['POST'])
def create_user():

    data = request.get_json()

    if not data:
        return jsonify({"error": "No input data provided"}), 400



    try:
        validated_data = cast(UserPayload, schema.load(data))
    except ValidationError as err:
        return jsonify({"error": err.messages}), 400
    


    new_user = User(
        badge_num=validated_data['badge_num'],
        name=validated_data['name'],
        admin=False,
        latitude=None,
        longitude=None,
        status="Offline")
    

    
    ok, err = new_user.set_password(validated_data['password'])

    if not ok:
        return jsonify({"error": err}), 400
    
    #Add to database
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: " + str(e)}), 500
    
        
    return jsonify(new_user.to_dict()), 201
    

    
    
    

    


