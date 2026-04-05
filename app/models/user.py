from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone
from typing import Tuple
from math import isfinite

#Defines in Python an abstraction for a User table. This is the model that SQLAlchemy will use to create the database and interact with it.
class User(db.Model):
    """Model class representing a user in the database. Defines the structure of the tables, fields, and methods for password management and data representation.

    Args:
        db (SQLAlchemy): The SQLAlchemy database instance used for defining the model and interacting with the database.
    """

    def __init__(self, **kwargs):
        """Initializes a User object with the provided keyword arguments.
        Python's default constructor does not work with the models, so
        a super() is used to call the db.Model default constructor instead.

        Args:
            **kwargs: Arbitrary keyword arguments representing the fields of the User model. These can include badge_num, name, and password_hash, among others.
        """

        super().__init__(**kwargs)

        # Ensure Python-level defaults
        if "admin" not in kwargs:
            self.admin = False
        if "status" not in kwargs:
            self.status = "Offline"
        if "last_seen" not in kwargs:
            from datetime import datetime, timezone
            self.last_seen = datetime.now(timezone.utc)

    #Note: last_seen needs to use lambdas because datetime.now is evaluated once at runtime, not per instance. Using a lambda ensures that a new
    #timestamp is generated each time a User instance is created or updated, rather than all instances sharing the same timestamp.
    id =db.Column(db.Integer, primary_key=True)
    badge_num = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    last_seen = db.Column(db.DateTime, default=lambda:datetime.now(timezone.utc), onupdate=lambda:datetime.now(timezone.utc))
    status = db.Column(db.String(20), default="Offline", nullable=False)

    #Unchanging Checks
    APPROVED_STATUS = ["Online","Offline","Away"]

    #User Attributes
    def set_password(self,password) -> Tuple[bool,str | None]:
        """Encrypts using werkzeug.security's generate_password_hash function and stores the hash in the password_hash field.

        Args:
            password (str): The plaintext password to be hashed and stored.
        
        Returns:
            Tuple[bool, str | None]: A tuple where the first element is a boolean indicating
            success (True if the password was set successfully, False otherwise), and the second element is an optional error message
             (None if the password was set successfully, or a string describing the error if it was not).
        """
        
        self.password_hash = generate_password_hash(password)
        return (True,None)
    
    def check_password(self,password) -> Tuple[bool,str | None]:
        """Checks if the provided password matches the stored password hash using werkzeug.security's check_password_hash function.

        Args:
            password (str): The password to be checked against the stored password hash.
        
        Returns:
            Tuple[bool, str | None]: A tuple where the first element is a boolean indicating 
            success (True if the password matches the hash, False otherwise), and the second element is an optional error message 
            (None if the password matches, or a string describing the error if it does not).
        
        """

        #Type
        if self.is_string(password) == False:
            return (False,"Password must be a non-empty string.")

        #Length
        if len(password) < 8 or len(password) > 128:
            return (False,"Password must be between 8 and 128 characters long.")
        
        #Actual Check
        if check_password_hash(self.password_hash,password):
            return (True,None)
        else:
            return (False,"Incorrect password.")
    
    def to_dict(self) ->dict:
        """Converts the User object into a dictionary format.

        Returns:
            dict: A dictionary representation of the User object, excluding the password hash for security reasons.
        
        """
        return {
            "id": self.id,
            "badge_num": self.badge_num,
            "name": self.name,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "last_seen": self.last_seen.isoformat(),
            "status": self.status,
            "admin": self.admin
        }
    
    def set_admin(self) -> None:
        """Toggles the admin status of the user.
            Needed because we cannot access attributes outside of the class
            without assigning all to "self".
        """
    
        if self.admin == False: 
            self.admin = True 
        else: 
            self.admin = False

    #User State
    def update_status(self,new_status:str) -> Tuple[bool,str | None]:
        """Updates the user's status to one of the approved statuses.

        Args:
            new_status (str): The new status to be set for the user. Must be one of "Online", "Offline", or "Away".

        Returns:
            Tuple[bool, str | None]: A tuple where the first element is a boolean indicating success (True if the status was updated successfully, False otherwise), 
            and the second element is an optional error message (None if the update was successful, or a string describing the error if it was not).
        """
        if new_status not in self.APPROVED_STATUS or not self.is_string(new_status):
            return (False,f"Status must be one of {self.APPROVED_STATUS}")
        
        self.status = new_status
        return (True,None)
    
    def set_location(self,latitude:float,longitude:float) -> Tuple[bool,str | None]:
        """Sets the user's location by updating the latitude and longitude fields.

        Args:
            latitude (float): The latitude value to be set for the user's location. Must be between -90 and 90.
            longitude (float): The longitude value to be set for the user's location. Must be between -180 and 180.

        Returns:
            Tuple[bool, str | None]: A tuple where the first element is a boolean indicating success (True if the location was updated successfully, False otherwise), 
            and the second element is an optional error message (None if the update was successful, or a string describing the error if it was not).
        """

        #Type
        if self.is_float(latitude) == False or self.is_float(longitude) == False:
            return (False,"Latitude and Longitude must be decimals.")
        
        #Range
        if latitude < -90 or latitude > 90:
            return (False,"Latitude must be between -90 and 90.")
        
        if longitude < -180 or longitude > 180:
            return (False,"Longitude must be between -180 and 180.")
        
        self.latitude = latitude
        self.longitude = longitude
        return (True,None)



    #Helper Methods
    def is_string(self,value) -> bool:
        """Checks if the provided value is a string.

        Args:
            value: The value to be checked.
        
        Returns:
            bool: True if the value is a string, False otherwise.
        """
    
        if not isinstance(value,str) or value.strip() == "":
            return False
    
        return True

    def is_int(self,value) -> bool:
        """Checks if the provided value is an integer.

        Args:
            value: The value to be checked.
        
        Returns:
            bool: True if the value is an integer, False otherwise.
        """

        if not isinstance(value,int):
            return False
        
        return True
    
    def is_float(self,value) -> bool:
        """Checks if the provided value is a float.

        Args:
            value: The value to be checked.
        
        Returns:
            bool: True if the value is a float, False otherwise.
        """
        if not isinstance(value,float) or not isfinite(value):
            return False
        
        return True