from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Stadium(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stadium_name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(100))
    description = db.Column(db.String(500)) 
    capacity = db.Column(db.Integer)
    owner = db.Column(db.String(50))  
    yearBuilt = db.Column(db.Integer)  
    fieldSize = db.Column(db.String(50))  
    stadiumImage = db.Column(db.String(255))
    rating = db.Column(db.Integer) 
    stars_number = db.Column(db.Integer) 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stadium_id = db.Column(db.Integer, db.ForeignKey('stadium.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # Assuming a numerical rating
    comment = db.Column(db.String(255))  # The text of the review
    stadium = db.relationship('Stadium', backref=db.backref('reviews', lazy=True))
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))


