from flask import redirect, url_for, request
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.menu import MenuLink
from flask_admin.form import FileUploadField
from flask_admin.contrib.sqla import ModelView
from app.models import db, StructureHistory
  # Import your SQLAlchemy instance


def create_admin(app):
    with app.app_context():

        class MainIndexLink(MenuLink):
            def get_url(self):
                return url_for("main.index")

        class MyAdminIndexView(AdminIndexView):
            def is_visible(self):
                return False

        class TablesAdm(ModelView):
            form_overrides = {
                'file_data': FileUploadField
            }

            def is_accessible(self):
                return current_user.is_authenticated

            def inaccessible_callback(self, name, **kwargs):
                return redirect(url_for('home', next=request.url))

            def on_model_change(self, form, model, is_created):
                if form.file_data.data:
                    model.file_data = form.file_data.data.read()

        admin = Admin(app, index_view=MyAdminIndexView())
        admin.add_link(MainIndexLink(name='Exit'))

        # Pass db.session when adding views
        admin.add_view(TablesAdm(StructureHistory, db.session))

        return admin

  

    

