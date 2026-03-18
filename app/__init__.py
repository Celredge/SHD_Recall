from flask import Flask
from .database import db
from .models import user

def create_app():
	app = Flask(__name__)

	app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
	
	@app.route("/health")
	def health():
		return {"status":"ok"}
	
	db.init_app(app)

	return app


