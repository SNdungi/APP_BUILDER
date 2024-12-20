
structure = {
    "AppName": {
        "app": {
            "__init__.py": """\
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        from .routes import main
        app.register_blueprint(main)
        db.create_all()
        
    return app
""",
            "routes.py": """\
from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')
    
    
""",
            "models.py": """\
from . import db

class ExampleModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now())
    
class User(db.Model, UserMixin, SoftDeleteMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email= db.Column(db.String(100), nullable=False)
    contact= db.Column(db.Integer, nullable=False)
    
    def __repr__(self):
        return f'<User {self.name}>'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id)) 
    

class StructureHistory(db.Model, SoftDeleteMixin):
    id = db.Column(db.Integer, primary_key=True)
    version = db.Column(db.Integer, nullable=False)
    structure_data = db.Column(db.JSON, nullable=False)  # Store the structure as JSON
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, version, structure_data):
        self.version = version
        self.structure_data = structure_data

    def __repr__(self):
        return f"<StructureHistory(version={self.version}, created_at={self.created_at})>"    
    
""",
            "forms.py": "",
            "templates": {
                "base.html": """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Flask App{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
</head>
<body>
    <header>
        <h1>Flask App Boilerplate</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
    <footer>
        <p>&copy; 2024 Flask App</p>
    </footer>
</body>
</html>
""",
                "index.html": """\
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
<h2>Welcome to the Flask App!</h2>
<p>This is a starter boilerplate for a Flask application.</p>
{% endblock %}
"""
            },
            "static": {
                "css": {},
                "js": {},
                "images": {}
            },
        },
        "migrations": {},
        ".env": "SECRET_KEY=your_secret_key\nDATABASE_URL=sqlite:///app.db\n",
        "config.py": """\
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
""",
        "run.py": """\
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
""",
        "requirements.txt": """\
Flask==2.3.3
Flask-SQLAlchemy==3.0.4
Flask-Migrate==4.0.0
python-dotenv==1.0.0
"""
    }
}


    