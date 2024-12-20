structure = {
    "AppName": {
        ".env": "SECRET_KEY=your_secret_key\nDATABASE_URL=sqlite:///app.db\n",
        "app": {
            "__init__.py": "from flask import Flask\nfrom flask_sqlalchemy import SQLAlchemy\nfrom flask_migrate import Migrate\n\ndb = SQLAlchemy()\nmigrate = Migrate()\n\ndef create_app():\n    app = Flask(__name__)\n    app.config.from_object('config.Config')\n    \n    db.init_app(app)\n    migrate.init_app(app, db)\n\n    with app.app_context():\n        from .routes import main\n        app.register_blueprint(main)\n        db.create_all()\n        \n    return app\n",
            "forms.py": "",
            "models.py": "from . import db\n\nclass ExampleModel(db.Model):\n    id = db.Column(db.Integer, primary_key=True)\n    name = db.Column(db.String(128), nullable=False)\n    created_at = db.Column(db.DateTime, default=db.func.now())\n    \nclass User(db.Model, UserMixin, SoftDeleteMixin):\n    id = db.Column(db.Integer, primary_key=True)\n    name = db.Column(db.String(128), nullable=False)\n    email= db.Column(db.String(100), nullable=False)\n    contact= db.Column(db.Integer, nullable=False)\n    \n    def __repr__(self):\n        return f'<User {self.name}>'\n    \n    @login_manager.user_loader\n    def load_user(user_id):\n        return User.query.get(int(user_id)) \n    \n\nclass StructureHistory(db.Model, SoftDeleteMixin):\n    id = db.Column(db.Integer, primary_key=True)\n    version = db.Column(db.Integer, nullable=False)\n    structure_data = db.Column(db.JSON, nullable=False)  # Store the structure as JSON\n    created_at = db.Column(db.DateTime, default=datetime.utcnow)\n\n    def __init__(self, version, structure_data):\n        self.version = version\n        self.structure_data = structure_data\n\n    def __repr__(self):\n        return f\"<StructureHistory(version={self.version}, created_at={self.created_at})>\"\n\nclass Broker(db.Model):\n    id = db.Column(db.Integer, primary_key=True, nullable=False)\n    name = db.Column(db.String(200), nullable=False)\n    email = db.Column(db.String(300), nullable=False)\n",
            "routes.py": "from flask import Blueprint, render_template\n\nmain = Blueprint('main', __name__)\n\n@main.route('/')\ndef index():\n    return render_template('index.html')\n",
            "static": {
                "css": {},
                "images": {},
                "js": {}
            },
            "templates": {
                "base.html": "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n    <meta charset=\"UTF-8\">\n    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">\n    <title>{% block title %}Flask App{% endblock %}</title>\n    <link rel=\"stylesheet\" href=\"{{ url_for('static', filename='css/style.css') }}\">\n</head>\n<body>\n    <header>\n        <h1>Flask App Boilerplate</h1>\n    </header>\n    <main>\n        {% block content %}{% endblock %}\n    </main>\n    <footer>\n        <p>&copy; 2024 Flask App</p>\n    </footer>\n</body>\n</html>\n",
                "index.html": "{% extends 'base.html' %}\n\n{% block title %}Home{% endblock %}\n\n{% block content %}\n<h2>Welcome to the Flask App!</h2>\n<p>This is a starter boilerplate for a Flask application.</p>\n{% endblock %}\n"
            }
        },
        "config.py": "import os\n\nclass Config:\n    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')\n    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///app.db')\n    SQLALCHEMY_TRACK_MODIFICATIONS = False\n",
        "migrations": {},
        "requirements.txt": "Flask==2.3.3\nFlask-SQLAlchemy==3.0.4\nFlask-Migrate==4.0.0\npython-dotenv==1.0.0\n",
        "run.py": "from app import create_app\n\napp = create_app()\n\nif __name__ == \"__main__\":\n    app.run(debug=True)\n"
    }
}