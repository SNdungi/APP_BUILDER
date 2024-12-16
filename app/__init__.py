from flask import Flask
from app.models import db, login_manager
from flask_migrate import Migrate
from app.database.admin import create_admin
from app.routes import update, view


migrate = Migrate()

def create_app():
	app = Flask(__name__)
	app.config.from_object('config.Config')
	
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)

	with app.app_context():
		app.register_blueprint(update.update_bp)
		app.register_blueprint(view.view_bp)
		create_admin(app)
		
	return app