from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash

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


    id =db.Column(db.Integer, primary_key=True)
    badge_num = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean, default=False)

    def set_password(self,password):
        """Encrypts using werkzeug.security's generate_password_hash function and stores the hash in the password_hash field.

        Args:
            password (str): The plaintext password to be hashed and stored.
        """
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        """Checks if the provided password matches the stored password hash using werkzeug.security's check_password_hash function.

        Args:
            password (str): The password to be checked against the stored password hash.
        
        Returns:
            bool: True if the password matches the stored hash, False otherwise.
        
        """
        
        return check_password_hash(self.password_hash,password)
    
    def to_dict(self):
        """Converts the User object into a dictionary format.

        Returns:
            dict: A dictionary representation of the User object, excluding the password hash for security reasons.
        
        """
        return {
            "id": self.id,
            "badge_num": self.badge_num,
            "name": self.name
        }
    
    def set_admin(self):
        """Toggles the admin status of the user.
            Needed because we cannot access attributes outside of the class
            without assigning all to "self".
        """
        if self.admin == False: 
            self.admin = True 
        else: self.admin = False