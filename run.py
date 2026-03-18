from app import create_app
from app.database import db



app = create_app()

#Make a custom Command Line Interface command
@app.cli.command("init-db")
def init_db():
	db.create_all()
	print("Database initialized!")

if __name__ == "__main__":
	app.run(debug=True)
