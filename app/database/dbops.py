from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from models import db

class DBOperations:
    @staticmethod
    def create_entry(model, data):
        """Create a single entry in the database."""
        try:
            entry = model(**data)
            db.session.add(entry)
            db.session.commit()
            return {"success": True, "entry": entry}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def read_entries(model, filters=None):
        """Read entries from the database."""
        try:
            query = model.query
            if filters:
                query = query.filter_by(**filters)
            return {"success": True, "entries": query.all()}
        except Exception as e:
            return {"success": False, "error": str(e)}

    @staticmethod
    def update_entry(model, filters, updates):
        """Update a single entry in the database."""
        try:
            entry = model.query.filter_by(**filters).first()
            if not entry:
                return {"success": False, "error": "Entry not found"}
            for key, value in updates.items():
                setattr(entry, key, value)
            db.session.commit()
            return {"success": True, "entry": entry}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def delete_entry(model, filters):
        """Delete a single entry from the database."""
        try:
            entry = model.query.filter_by(**filters).first()
            if not entry:
                return {"success": False, "error": "Entry not found"}
            db.session.delete(entry)
            db.session.commit()
            return {"success": True}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def bulk_insert(model, data_list):
        """Insert multiple entries at once."""
        try:
            db.session.bulk_insert_mappings(model, data_list)
            db.session.commit()
            return {"success": True, "count": len(data_list)}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def bulk_update(model, update_data, key_field):
        """
        Perform bulk updates.
        update_data: List of dictionaries with updated fields and `key_field` to identify entries.
        key_field: The field used to match rows for updates.
        """
        try:
            db.session.bulk_update_mappings(model, update_data)
            db.session.commit()
            return {"success": True, "count": len(update_data)}
        except Exception as e:
            db.session.rollback()
            return {"success": False, "error": str(e)}

    @staticmethod
    def process_csv(file_path, model):
        """Process a CSV file and insert entries into the database."""
        try:
            df = pd.read_csv(file_path)
            data_list = df.to_dict(orient='records')
            return DBOperations.bulk_insert(model, data_list)
        except Exception as e:
            return {"success": False, "error": str(e)}
