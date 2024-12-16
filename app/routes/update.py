from flask import  flash, Blueprint, render_template, request, jsonify, json
from app.construct import structure
import os
import zipfile
from dotenv import load_dotenv
from app.models import db, StructureHistory
from datetime import datetime



load_dotenv()

update_bp = Blueprint('update_bp', __name__)
year_now=datetime.today().year
print(year_now)



@update_bp.route('/')
def home():
    """Render the home page with the input form."""
    return render_template('index.html')

#_____________________________

#UPDATE BOILERPLATE

#_____________________________

@update_bp.route('/update-models', methods=['POST'])
def update_models():
    model_json = request.json

    # Generate new model class code
    new_model_code = f"\n\nclass {model_json['class_name']}(db.Model):\n"

    # Add columns
    for column in model_json['columns']:
        column_def = f"    {column['name']} = db.Column("
    
        # Handle data type
        if column['length']:
            column_def += f"db.{column['data_type']}({column['length']}"
        else:
            column_def += f"db.{column['data_type']}"
    
        # Add constraints
        constraints = []
        if column['primary_key']:
            constraints.append("primary_key=True")
        if not column['nullable']:
            constraints.append("nullable=False")
        
        if constraints:
            column_def += ", " + ", ".join(constraints)
        
        column_def += ")\n"
        new_model_code += column_def

    # Update the structure dictionary
    structure['app']['models.py'] = structure['app']['models.py'].rstrip() + new_model_code

    # Increment version and save the structure in the database
    latest_version = StructureHistory.query.order_by(StructureHistory.version.desc()).first()
    new_version = latest_version.version + 1 if latest_version else 1

    # Save the current structure into the database
    structure_history_record = StructureHistory(version=new_version, structure_data=structure)
    db.session.add(structure_history_record)
    db.session.commit()

    # Write updated structure back to construct.py (optional)
    construct_path = os.path.join(os.path.dirname(__file__), 'construct.py')
    with open(construct_path, 'w') as f:
        f.write(f"structure = {json.dumps(structure, indent=4)}")

    return jsonify({'status': 'success', 'message': 'Models updated and versioned successfully'})


#______________________________

#HISTORY

#______________________________

@update_bp.route('/rollback', methods=['POST'])
def rollback_structure():
    version = request.json.get('version')

    if not version:
        return jsonify({'status': 'error', 'message': 'Version not provided'})

    # Retrieve the structure from the specified version
    structure_record = StructureHistory.query.filter_by(version=version).first()

    if structure_record:
        global structure
        structure = structure_record.structure_data

        # Write the reverted structure back to construct.py (optional)
        construct_path = os.path.join(os.path.dirname(__file__), 'construct.py')
        with open(construct_path, 'w') as f:
            f.write(f"structure = {json.dumps(structure, indent=4)}")

        return jsonify({'status': 'success', 'message': f'Structure rolled back to version {version}'})
    else:
        return jsonify({'status': 'error', 'message': f'No structure found for version {version}'})





#_____________________________

#CREATE BOILERPLATE

#_____________________________

@update_bp.route('/create-boilerplate', methods=['POST'])
def create_boilerplate():
    """Create Flask boilerplate project."""
    
    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, "w") as file:
                    file.write(content)
    
    project_path = request.form.get('project_path')
    project_name = request.form.get('project_name')
    target_dir = os.path.join(project_path, project_name)

    try:
        # Create project directory and structure
        os.makedirs(target_dir, exist_ok=True)
        create_structure(target_dir, structure)

        # Create a zip file of the project
        zip_path = f"{target_dir}.zip"
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(target_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, target_dir)
                    zipf.write(file_path, arcname)

        return jsonify({"message": "Boilerplate created successfully.", "zip_path": zip_path}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

