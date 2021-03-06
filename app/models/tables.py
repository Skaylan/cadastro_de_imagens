from app import app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app) #database variable
migrate = Migrate(app, db)


class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    image = db.relationship('Images', backref='owner')
    
    def __init__(self, name, username, email, password):
        self.name = name
        self.username = username
        self.email = email
        self.password = password



class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_name = db.Column(db.Text, nullable=False)
    posted_at = db.Column(db.DateTime(), default=datetime.utcnow)
    owner_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    owner_username = db.Column(db.String(30), nullable=False)
    
    def __init__(self, file_name, owner_id, owner_username):
        self.file_name = file_name
        self.owner_id = owner_id
        self.owner_username = owner_username