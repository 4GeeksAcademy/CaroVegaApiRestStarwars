from flask_admin.contrib.sqla import ModelView
from models import User

class UserAdminView(ModelView):
    column_list = ['id', 'username', 'email']