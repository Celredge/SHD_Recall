from flask import Flask
from .database import db
from .models import user

#Configs and registers the app with the SQLAlchemy instance
def create_app():
	"""Creates and configures the Flask application, including setting up the database connection and defining a health check route.
	   Necessary to keep the execution and the creation of the app seperate, as dictated by the structure of the project and the use of SQLAlchemy. (App factory)
	
	Returns:
		Flask: The configured Flask application instance.	
    """
	app = Flask(__name__)

	#Configures the database URI and disables track modifications to save resources.
	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	
	#Test route to check if the app is running.
	@app.route("/health")
	def health():
		return {"status":"ok"}
	
	
	#Connects the database to the app.
	db.init_app(app)

	return app


