from app import create_app
from app.database import db
from app.models.user import User as user
import inspect


#Gets the function from __init__.py and creates the app
app = create_app()

with app.app_context():
    #Creates the database and tables based on the models defined in app/models
	db.create_all()	
