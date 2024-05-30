import bcrypt
import os
import io
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import CHAR
from datetime import datetime, timedelta
from hashlib import sha256
from PIL import Image
from base64 import encodebytes, b64encode

db = SQLAlchemy()
PATH = os.getcwd()
PATH = os.path.join(PATH, "elaboration")

#function that define database structure
def init_database(app, log):
    global logger
    logger = log
    db.init_app(app)
    return db

# User table defination
class User(db.Model):
    username = db.Column(db.String(20), primary_key=True)
    password = db.Column(db.String(64).with_variant(CHAR(64),"mysql", "mariadb"))
    token = db.Column(db.String(72).with_variant(CHAR(72),"mysql", "mariadb"))
    token_creation = db.Column(db.DateTime)
    elaborations = db.relationship('Elaboration', backref='user')

    def __repr__(self):
        return f'<User username: {self.username}>'

    # function for verify password of user
    def verify_password(self, password):
        password = sha256(password.encode('utf-8')).hexdigest()
        return password == self.password
    
    # function for create a token for user
    def create_auth_token(self):
        salt = bcrypt.gensalt()
        token = bcrypt.hashpw(self.username.encode('utf-8'), salt)
        self.token = token
        self.token_creation = datetime.now()
        db.session.commit()

        logger.info(f'created token for user {self.username}')

    # static function for check token validity
    @staticmethod
    def verify_auth_token(token):
        user = User.query.filter_by(token=token).first()
        if not user:
            logger.info(f'token {token} is not valid')
            return False

        if user.token_creation < datetime.today() - timedelta(days=30):
            logger.info(f'token for user {user.username} expired, need to login')
            return False
        
        return user

# Elaboration table defination
class Elaboration (db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_fk = db.Column(db.String(20), db.ForeignKey('user.username'))
    folder_path = db.Column(db.String(36).with_variant(CHAR(36),"mysql", "mariadb"))
    creation_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Elaboration id: {self.id} folder: {self.folder_path} date: {self.creation_date}>'

    # function for convert elaboration element in JSON
    def convert_to_json(self):
        full_path = os.path.join(PATH, self.folder_path)
        full_path_img = os.path.join(full_path, "img.jpg")
        full_path_mesh = os.path.join(full_path, "model.glb")
        img = Image.open(full_path_img)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format=img.format)
        img = encodebytes(img_bytes.getvalue()).decode('ascii')
        with open(full_path_mesh, "rb") as f:
            encodedZip = b64encode(f.read())
            mesh = encodedZip.decode()

            return {
                "id": self.id,
                "user": self.user_fk,
                "img": img,
                "mesh": mesh,
                "date": self.creation_date,
                "mesh_name": self.folder_path
            }