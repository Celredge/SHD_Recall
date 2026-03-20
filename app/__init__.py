from flask import Flask
from .database import db
from .models import user

#Configs and registers the app with the SQLAlchemy instance
def create_app():
	app = Flask(__name__)

	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	
	@app.route("/health")
	def health():
		return {"status":"ok"}
	
	
	#Connects the database to the app.
	db.init_app(app)

	return app


