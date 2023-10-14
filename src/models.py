from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            
            # do not serialize the password, its a security breach
        }

class People (db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False )
    gender = db.Column(db.String(100))
    skin_color = db.Column(db.String(100))
    eye_color = db.Column(db.String(100))
    Birth_Year = db.Column(db.String(100))

    def __repr__(self):
        return '<People %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender":self.gender,
            "Birth_Year":self.Birth_Year
        }

class UserFavoritePeople(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    people_id = db.Column(db.Integer,  db.ForeignKey('people.id'), nullable=False)

    def __repr__(self):
        return '<UserFavoritePeople %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "user" :self.user_id,
            "people_id": self.people_id
        }