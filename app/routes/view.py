from flask import  flash, Blueprint, render_template, request, jsonify, send_file,json
from app.construct import structure
from app.models import StructureHistory,db
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
    """Extract the model names and column data types from SQLAlchemy models."""
    def resolve_column_type(arg):
        """Resolve the actual type from an AST node."""
        if isinstance(arg, ast.Attribute):
            return f"{arg.value.id}.{arg.attr}" if isinstance(arg.value, ast.Name) else arg.attr
        elif isinstance(arg, ast.Name):
            return arg.id
        elif isinstance(arg, ast.Call):
            return resolve_column_type(arg.func)
        elif isinstance(arg, ast.Constant):
            return str(arg.value)
        else:
            return str(arg)

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
                            # Extract the column type and additional info
                            if stmt.value.func.attr == "Column":
                                args = stmt.value.args
                                type_name = resolve_column_type(args[0]) if args else None
                                kwargs = {
                                    kw.arg: resolve_column_type(kw.value) for kw in stmt.value.keywords
                                }
                                columns.append({'name': column_name, 'type': type_name, 'kwargs': kwargs})
                if columns:
                    models[model_name] = columns  # Add model and its columns to the dictionary
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
        # Get latest structure from database first
        latest_structure = StructureHistory.query.order_by(StructureHistory.id.desc()).first()
        print(f"Latest structure: {latest_structure}")
        
        if latest_structure:
            # Use structure from database
            model_code = latest_structure.structure_data.get('AppName',{}).get('app', {}).get('models.py', '')
            print(f"Latest structure: {latest_structure.structure_data}")
        else:
            # Fallback to imported structure if no database records exist
            model_code = structure.get('AppName',{}).get('app', {}).get('models.py', '')
        
        # Parse models and return template
        models = extract_models_info(model_code)
        return render_template('index.html', models=models)
        
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

@view_bp.route('/remove-model/<class_name>', methods=['POST'])
def remove_model(class_name):
    """Remove specified model class from structure."""
    try:
        # Get latest structure from database
        latest_structure = StructureHistory.query.order_by(StructureHistory.id.desc()).first()
        
        if latest_structure:
            # Get the models.py content
            model_code = latest_structure.structure_data['AppName']['app']['models.py']
            
            # Parse the code into lines
            lines = model_code.split('\n')
            
            # Find and remove the class definition and its columns
            new_lines = []
            skip_lines = False
            for line in lines:
                if line.startswith(f"class {class_name}"):
                    skip_lines = True
                    continue
                elif skip_lines and line.startswith('class '):
                    skip_lines = False
                
                if not skip_lines:
                    new_lines.append(line)
            
            # Update structure with modified code
            latest_structure.structure_data['AppName']['app']['models.py'] = '\n'.join(new_lines)
            
            # Create new version in database
            new_version = latest_structure.version + 1
            new_structure = StructureHistory(
                version=new_version, 
                structure_data=latest_structure.structure_data
            )
            db.session.add(new_structure)
            db.session.commit()
            
            return jsonify({
                'status': 'success',
                'message': f'Model {class_name} removed successfully'
            })
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Failed to remove model: {str(e)}'
        })



#____________________________

# HTML SECTION: Creating HTML DOMs for data capture

#____________________________


import os

def generate_html_document(model_name, model_columns, output_dir="templates"):
    """
    Generate an HTML document for CRUD operations for a given model.

    Args:
        model_name (str): Name of the model (e.g., "User").
        model_columns (list): List of tuples containing column names and types (e.g., [("id", "Integer"), ("name", "String")]).
        output_dir (str): Directory to save the generated HTML document (default: "templates").
    """
    # Sanitize and lowercase the model name for URLs
    url_model_name = model_name.lower()
    
    # Basic HTML layout
    html_template = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{model_name} Management</title>
        <link rel="stylesheet" href="{{{{ url_for('static', filename='styles.css') }}}}">
    </head>
    <body>
        <div class="container">
            <h1>{model_name} Management</h1>
            <nav>
                <ul>
                    <li><a href="/{url_model_name}/create">Create New {model_name}</a></li>
                    <li><a href="/{url_model_name}/">View All {model_name}s</a></li>
                </ul>
            </nav>
            <div class="content">
                {{{{ block content }}}}
                <!-- Content will be injected here -->
                {{{{ endblock }}}}
            </div>
        </div>
    </body>
    </html>
    """
    
    # CRUD templates
    templates = {
        "create.html": f"""
        {{{{% extends "{url_model_name}/layout.html" %}}}}
        {{{{% block content %}}}}
        <h2>Create New {model_name}</h2>
        <form action="/{url_model_name}/create" method="POST">
            {"".join([f'<label for="{col[0]}">{col[0].capitalize()}</label><input type="text" name="{col[0]}" id="{col[0]}"><br>' for col in model_columns if col[0] != 'id'])}
            <button type="submit">Create</button>
        </form>
        {{{{% endblock %}}}}
        """,
        "read.html": f"""
        {{{{% extends "{url_model_name}/layout.html" %}}}}
        {{{{% block content %}}}}
        <h2>All {model_name}s</h2>
        <table>
            <thead>
                <tr>
                    {"".join([f'<th>{col[0].capitalize()}</th>' for col in model_columns])}
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {{{{ for record in records }}}}
                <tr>
                    {"".join([f'<td>{{{{ record.{col[0]} }}}}</td>' for col in model_columns])}
                    <td>
                        <a href="/{url_model_name}/update/{{{{ record.id }}}}">Edit</a> | 
                        <a href="/{url_model_name}/delete/{{{{ record.id }}}}">Delete</a>
                    </td>
                </tr>
                {{{{ endfor }}}}
            </tbody>
        </table>
        {{{{% endblock %}}}}
        """,
        "update.html": f"""
        {{{{% extends "{url_model_name}/layout.html" %}}}}
        {{{{% block content %}}}}
        <h2>Update {model_name}</h2>
        <form action="/{url_model_name}/update/{{{{ record.id }}}}" method="POST">
            {"".join([f'<label for="{col[0]}">{col[0].capitalize()}</label><input type="text" name="{col[0]}" id="{col[0]}" value="{{{{ record.{col[0]} }}}}"><br>' for col in model_columns if col[0] != 'id'])}
            <button type="submit">Update</button>
        </form>
        {{{{% endblock %}}}}
        """,
        "delete.html": f"""
        {{{{% extends "{url_model_name}/layout.html" %}}}}
        {{{{% block content %}}}}
        <h2>Delete {model_name}</h2>
        <p>Are you sure you want to delete this {model_name}?</p>
        <form action="/{url_model_name}/delete/{{{{ record.id }}}}" method="POST">
            <button type="submit">Delete</button>
        </form>
        {{{{% endblock %}}}}
        """
    }

    # Create output directories
    model_dir = os.path.join(output_dir, url_model_name)
    os.makedirs(model_dir, exist_ok=True)

    # Save the layout HTML
    with open(os.path.join(model_dir, "layout.html"), "w") as layout_file:
        layout_file.write(html_template)

    # Save each CRUD template
    for filename, content in templates.items():
        with open(os.path.join(model_dir, filename), "w") as template_file:
            template_file.write(content)

    print(f"HTML templates for {model_name} created in {model_dir}")
