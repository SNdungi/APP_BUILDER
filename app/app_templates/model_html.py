
import ast

def extract_models_and_columns(models_py_str):
    """
    Extract model names and columns from a Python source string.

    Args:
        models_py_str (str): A string representing the content of models.py.

    Returns:
        dict: A dictionary where keys are model names and values are lists of column attributes.
    """
    models = {}

    # Parse the string into an AST
    tree = ast.parse(models_py_str)

    # Iterate over all top-level nodes in the AST
    for node in tree.body:
        # Check if the node is a class definition
        if isinstance(node, ast.ClassDef):
            model_name = node.name
            columns = []

            # Iterate over the class body to find assignments
            for class_body_item in node.body:
                if isinstance(class_body_item, ast.Assign):
                    for target in class_body_item.targets:
                        if isinstance(target, ast.Name):
                            column_name = target.id
                            # Optionally extract column details (e.g., type) from the value
                            if isinstance(class_body_item.value, ast.Call):
                                column_details = class_body_item.value.func.attr  # Extract db.Column or similar
                                columns.append((column_name, column_details))
                            else:
                                columns.append((column_name, None))
            
            # Store the model and its columns
            models[model_name] = columns

    return models


# Example usage
models_py_str = """\
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
"""

# Extract models and columns
models = extract_models_and_columns(models_py_str)

# Output the result
for model, columns in models.items():
    print(f"Model: {model}")
    for column_name, column_type in columns:
        print(f"  Column: {column_name}, Type: {column_type}")



def generate_html_from_models(models_py_str):
    """
    Generate HTML templates dynamically for models defined in a module.
    
    Args:
        models_module: The Python module containing SQLAlchemy models.
    
    Returns:
        dict: A dictionary where keys are model names and values are tuples (html_fstring, rendered_html).
    """
    html_templates = {}
    
    models = extract_models_and_columns(models_py_str)
    # Iterate through all attributes in the module
    for model_name, columns in models.items():
      print(f"Model: {model}")
      for col_name, col_type in columns:
        print(f"  Column: {col_name}, Type: {col_type}")
        

            
            # Generate the HTML f-string template for the model
        html_template = f"""
            {{% extends "base.html" %}}
            {{% block content %}}
            <section id="section_{model_name}" class="main-wrapper">
                <div class="row my-4 p-3">
                    <div class="col-12">
                        <div class="custom-block bg-white">
                            <ul class="nav nav-tabs" id="myTab" role="tablist">
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link active" id="create-tab" data-bs-toggle="tab" 
                                            data-bs-target="#create-tab-pane" type="button" role="tab" 
                                            aria-controls="create-tab-pane" aria-selected="true">Create</button>
                                </li>
                                <li class="nav-item" role="presentation">
                                    <button class="nav-link" id="view-tab" data-bs-toggle="tab" 
                                            data-bs-target="#view-tab-pane" type="button" role="tab" 
                                            aria-controls="view-tab-pane" aria-selected="false">View</button>
                                </li>
                            </ul>
                            <div class="tab-content" id="myTabContent">
                                <div class="tab-pane fade" id="create-tab-pane" role="tabpanel" 
                                     aria-labelledby="create-tab" tabindex="0">
                                    <h6 class="mb-4">Create</h6>
                                    <form class="custom-form password-form" action="#" method="post" role="form">
                                        {"".join(f'<input type="text" name="{col_name}" id="create_{col_name}" '
                                                 f'class="form-control" placeholder="{col_name}" required>'
                                                 for col_name, col_type in columns)}
                                        <div class="d-flex">
                                            <button type="submit" class="form-control ms-2">Create</button>
                                        </div>
                                    </form>
                                </div>
                                <div class="tab-pane fade show active" id="view-tab-pane" role="tabpanel" 
                                     aria-labelledby="view-tab" tabindex="0">
                                    <h6>View</h6>
                                    <form id="search-form" class="custom-form profile-form">
                                        {"".join(f'<input class="form-control" type="text" id="search_{col_name}" '
                                                 f'name="{col_name}" placeholder="Search {col_name}" required>'
                                                 for col_name, col_type in columns)}
                                        <button type="submit" class="form-control ms-2">Search</button>
                                    </form>
                                    <hr>
                                    <div class="table-responsive">
                                        <table class="account-table table">
                                            <thead>
                                                <tr>
                                                    {"".join(f'<th>{col_name}</th>' for col_name, col_type in columns)}
                                                </tr>
                                            </thead>
                                            <tbody>
                                                <tr>
                                                    {"".join(f'<td>{{{{ {col_name} }}}}</td>' for col_name, col_type in columns)}
                                                </tr>
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </section>
            {{% endblock %}}
            """
            
            # Add to the result dictionary
        html_templates[model_name] = (html_template)
    
    return html_templates

# Example usage
if __name__ == "__main__":
    
    # Generate HTML for all models
    templates = generate_html_from_models(models_py_str)
    print(templates)
    

