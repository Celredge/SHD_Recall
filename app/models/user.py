from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash

#Defines in Python an abstraction for a User table. This is the model that SQLAlchemy will use to create the database and interact with it.
class User(db.Model):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    id =db.Column(db.Integer, primary_key=True)
    badge_num = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
    def to_dict(self):
        return {
            "id": self.id,
            "badge_num": self.badge_num,
            "name": self.name
        }
    