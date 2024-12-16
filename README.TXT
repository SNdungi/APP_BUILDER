APP FOR DEVELOPING APPS
APP folder contains main __init__ file, which is the main file for the app.
models are sqlalchemy classes for creating database tables.
database is sqlite persisted as a file in the instance folder
routes contains blueprints for views and updated
update routes allow create, update and delete
view routes allow for reading
construct is the dictionary containing app design folders and files
flask admin and login are implemented for db admin and login tasks 
database contains dbops utils for CRUD and admin for implementing flask-admin
the rest is as usual i.e. static, config, .env and templates
run.py is the app endpoint