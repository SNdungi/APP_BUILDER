import os
def generate_html_document(application_name, model_columns, output_dir="templates"):
    """
    Generate an HTML document for CRUD operations for a given model.

    Args:
        application_name (str): Name of the application (e.g., "MyApp").
        model_columns (list): List of column names (e.g., ["id", "name", "email"]).
        output_dir (str): Directory to save the generated HTML document (default: "templates").
    """
    # Sanitize and lowercase the app name for consistency
    app_name = application_name.lower()
    
    # Year for the footer
    from datetime import datetime
    year_now = datetime.now().year

    # Generate the HTML using an f-string
    base_html = f"""
<!DOCTYPE html>
<html>
  <head>
    <title>{{{{ '{app_name}' | default('') ~ ' - ' if '{app_name}' else '' }}}}</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="">
    <meta name="author" content="">

    <!-- Core CSS -->
    <link href="https://fonts.googleapis.com/css2?family=Unbounded:wght@300;400;700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Instrument+Sans&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:400,700">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-9ndCyUaIbzAi2FUVXJi0CjmCapSmO7SnpJef0486qhLnuZ2cdeRhO02iuK6FUUVM" crossorigin="anonymous">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.14.0/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.5.0/font/bootstrap-icons.css" />

    <!-- Additional CSS -->

  </head>
  <body>
    <div class="container{{{{ '-fluid' if config.get('APP_BOILERPLATE_LAYOUT', False) else '' }}}}">
      <!-- Navbar -->
      <nav class="navbar navbar-expand-lg navbar-dark bg-dark mb-2">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#admin-navbar-collapse">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="admin-navbar-collapse">
          <a class="navbar-brand" href="#">{{{{ '{app_name}'.capitalize() }}}}</a>
          <ul class="navbar-nav flex-row">
          {{% for model in model_columns %}}
            <li class="nav-item">
              <a class="nav-link link-body-emphasis px-2 active" aria-current="page" href="#">
                <i class="bi-house-fill me-2"></i> {{ model }}
              </a>
            </li>
          {{% endfor %}}
          </ul>
        </div>
      </nav>

      <!-- Body -->
      <main>
        {{% block content %}}
        {{% endblock %}}
      </main>

      <footer class="site-footer">
        <div class="container">
          <p class="copyright-text">Copyright © {app_name} {year_now}</p>
        </div>
      </footer>
    </div>

    <!-- Core JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.min.js"></script>

    <!-- Additional JS -->
  </body>
</html>
"""
    # Save the generated HTML to the output directory
        # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Output file path
    output_path = os.path.join(output_dir, "bases.html")
    output_path = f"{output_dir}/base.html"
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(base_html)
    print(f"HTML document generated and saved to {output_path}")
# Application name and model columns
application_name = "MyApp"
model_columns = ["id", "name", "email"]

# Generate the HTML document
generate_html_document(application_name, model_columns)



