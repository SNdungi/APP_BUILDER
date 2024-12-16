from flask import  flash, Blueprint, render_template, request, jsonify, send_file,json
from app.construct import structure
from dotenv import load_dotenv
from datetime import datetime
import ast



load_dotenv()

view_bp = Blueprint('view_bp', __name__)
year_now=datetime.today().year
print(year_now)

# HOME PAGE __________________

@view_bp.route('/')
def home():
    """Render the home page with the input form."""
    return render_template('index.html')


#_____________________________

#HELPERS HTML CREATION & STUCTURE VIEW

#_____________________________

def render_folder_structure(data, level=0):
        """Recursively render folder structure as nested divs."""
        html = '<div style="margin-left:{}px;">'.format(level * 20)
        for key, value in data.items():
            if isinstance(value, dict):
                # Key represents a folder
                html += f'<div><strong>{key}/</strong></div>'
                html += render_folder_structure(value, level + 1)
            else:
                # Key represents a file
                html += f'<div>{key}</div>'
        html += '</div>'
        return html

def get_structure_items(d):
    """Recursively retrieve keys and values from a dictionary."""
    items = []
    for key, value in d.items():
        if isinstance(value, dict):
            # Recursively call for nested dictionaries
            items.extend(get_structure_items(value))
            print(f"Key: {key}")
        else:
            items.append((key, value))
    
    return items

def extract_models_info(model_code):
    """Extract the model names and columns from SQLAlchemy models."""
    try:
        tree = ast.parse(model_code)
        models = {}

        for node in tree.body:
            if isinstance(node, ast.ClassDef):  # Look for class definitions
                model_name = node.name
                columns = []
                for stmt in node.body:
                    if isinstance(stmt, ast.Assign) and hasattr(stmt.targets[0], 'id'):
                        column_name = stmt.targets[0].id
                        if isinstance(stmt.value, ast.Call) and hasattr(stmt.value.func, 'attr'):
                            column_type = stmt.value.func.attr
                            columns.append({'name': column_name, 'type': column_type})
                if columns:
                    models[model_name] = columns  # Add model and its columns to the dictionary
        print(f"Models: {models}")
        return models
    except Exception as e:
        print(f"Error parsing model code: {e}")
        return {}


#_____________________________

#VIEW MODELS & STRUCTURE

#_____________________________

@view_bp.route('/view-models', methods=['GET', 'POST'])
def view_models():
    """View and extract created models."""
    print("Accessing View models route")
    try:
        # Retrieve the model code from the dictionary
        model_code = structure['AppName']['app']['models.py']
        print(f"Retrieved Model Code: \n{model_code}")

        # Parse the model code to extract multiple models and their columns
        models = extract_models_info(model_code)
        if not models:
            raise ValueError("No valid models found or unable to parse model details.")

        print(f"Extracted Models: {models}")
        
        return render_template(
            'index.html',
            models=models
        )

    except KeyError:
        print("View models. Model not found in structure.")
        return jsonify({"error": "Model not found in structure."}), 404
    except Exception as e:
        print(f"Error in view_models: {e}")
        return jsonify({"error": str(e)}), 500


@view_bp.route('/view-structure', methods=['GET', 'POST'])
def view_structure():
    """Display structure keys and their contents."""
    print("Accessing Structure View")
    
    if request.method == 'POST':
        # Extract key-value pairs from the nested structure
        structure_items = get_structure_items(structure['AppName'])
            # Generate structure for `AppName`
        structure_html = render_folder_structure(structure['AppName'])
    else:
        structure_items = []
        structure_html=None# Initialize with an empty list for GET requests

    return render_template(
        'index.html', 
        structure_items=structure_items, 
        structure_html=structure_html,
        structure=json.dumps(structure, indent=4)
    )
