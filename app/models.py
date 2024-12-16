from datetime import datetime
from flask_login import LoginManager,UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

db = SQLAlchemy()
login_manager = LoginManager()

class SoftDeleteMixin:
    deleted_at = db.Column(db.DateTime, nullable=True)
    created_at =  db.Column(db.DateTime, default=datetime.now(timezone.utc)) #meta
    updated_at =  db.Column(db.DateTime, onupdate=datetime.now(timezone.utc)) #meta

    def soft_delete(self):
        self.deleted_at = datetime.now(timezone.utc)
        self.updated_at = datetime.now(timezone.utc)

    def undelete(self):
        self.deleted_at = None
        self.updated_at = datetime.now(timezone.utc)

    @classmethod
    def get_deleted(cls, session):
        return session.query(cls).filter(cls.deleted_at != None).all()

    @classmethod
    def get_all(cls, session, include_deleted=False):
        if include_deleted:
            return session.query(cls).all()
        else:
            return session.query(cls).filter(cls.deleted_at == None).all()

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
