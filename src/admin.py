import os
from flask_admin import Admin
from models import db, User,People, UserFavoritePeople
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
from adminviews import UserAdminView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'clave de muestra')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='4Geeks Admin', template_mode='bootstrap3')

    admin.add_view(UserAdminView(User, db.session))
    admin.add_view(ModelView(People, db.session))
    admin.add_view(ModelView(UserFavoritePeople, db.session))

    # Agrega un enlace a la vista de perfil de usuario en el menú de navegación
    admin.add_link(MenuLink(name='Perfil de Usuario', url='/admin/user-profile', category='Usuarios'))

