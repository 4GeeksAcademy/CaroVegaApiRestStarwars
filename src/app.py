"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, UserFavoritePeople
from flask_admin.contrib.sqla import ModelView
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
#inicio codigo
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = list(map(lambda item: item.serialize(),all_users))
    return jsonify(results), 200

@app.route('/people', methods=['GET'])
def get_characters():
    all_people = People.query.all()
    results = list(map(lambda item: item.serialize(),all_people))
    return jsonify(results), 200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_character(people_id):
    character = People.query.filter_by(id=people_id).first()
    result = character.serialize()
    return jsonify(result), 200

@app.route('/user<int:user_id>/favorites', methods=['GET'])
def get_favorites(user_id):
    allfavorites= UserFavoritePeople.query.filter_by(id=user_id).first()
    print(allfavorites)
    return jsonify({"msg": "favoritousuario"}), 200

@app.route('/people', methods=['POST'])
def insert_character():
    data_character = request.json
    new_character = People(  name=data_character['name'],
    gender=data_character['gender'],
    skin_color=data_character['skin_color'],
    eye_color=data_character['eye_color'],
    Birth_Year=data_character['Birth_Year']
    )
    db.session.add(new_character)
    db.session.commit()
    return jsonify({"msg":"personaje agregado"}), 201

@app.route('/people', methods=['DELETE'])
def delete_character():
    data = request.json
    if 'id' not in data:
        return jsonify({"error":"el campo 'id' es obligatorio"}),400
    id_character = data['id']
    delete_character = People.query.filter_by(id = id_character).first()
    if delete_character is not None:
        db.session.delete(delete_character)
        db.session.commit()
        return jsonify({"msg":"personaje eliminado"}), 201
    else:
        return jsonify({"error":"Personaje no encontrado"}),404

def user_profile_link(user_id):
    return url_for('admin.user_profile', user_id=user_id)

class UserAdminView(ModelView):
     column_formatters = {
        'username': lambda v, c, m, p: f'<a href="{user_profile_link(m.id)}">{m.username}</a>'}

@app.route('/admin/user-profile/<int:user_id>')
def admin_user_profile(user_id):
    user = User.query.get(user_id)
    return f'Perfil del usuario: {user.username}'  # Personaliza la vista según tus necesidades
#final codigo

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
