import re
import db.database as db_models
from flask import request, g, request
from flask_httpauth import HTTPBasicAuth
from hashlib import sha256
from PIL import Image
from models.HistoryManager import HistoryManager

PSW_PATTERN = re.compile("^(?=.*[0-9])(?=.*[!@#$%^&*])[a-zA-Z0-9!@#$%^&*]{6,}$")

# function that define all the routes
def create_routes(app, db, logger):
    auth = HTTPBasicAuth()
    hm = HistoryManager(app, db, logger)

    # method for check user authentication
    @auth.verify_password
    def verify_password(usr_or_tkn, psw):
        # check token validity
        user = db_models.User.verify_auth_token(usr_or_tkn)
        if not user:
            # check password validity
            user = db_models.User.query.filter_by(username = usr_or_tkn).first()        
            if not user or not user.verify_password(psw):
                return False
        g.user = user
        return True
    
    # route for log inside the website
    @app.route('/api/login', methods=['GET'])
    @auth.login_required
    def login():
        logger.info("request for /api/login", request.remote_addr)
        token = get_token(g.user.username)
        if token:
            logger.info(f'user {g.user.username} logged in', request.remote_addr)
            return {'token': token}, 200
        return {}, 500

    # route for create a new user
    @app.route('/api/register', methods=['POST'])
    def register():
        logger.info(f'request for /api/register', request.remote_addr)
        username = request.form['username']
        psw = request.form['password']

        if len(username) < 5 or len(username) > 20:
            return {'msg': 'username-length-invalid'}, 400
        if not PSW_PATTERN.match(psw):
            return {'msg': 'password-invalid'}, 400
        user = bool(db_models.User.query.filter_by(username=username).first())
        if user:
            return {'msg': 'user-exist'}, 400

        password = sha256(psw.encode('utf-8')).hexdigest()
        new_user = db_models.User(username = username, password = password)
        db.session.add(new_user)
        db.session.commit()

        logger.info(f'user {username} created')

        token = get_token(username)
        if token:
            return {'token': token}, 201
        return {}, 201
    
    # route for get username from token
    @app.route('/api/user', methods=['GET'])
    @auth.login_required
    def get_user():
        logger.info("request for /api/user", request.remote_addr)
        return {'username': g.user.username}, 201

    # route for get history of user
    @app.route('/api/history', methods=['GET'])
    @auth.login_required
    def get_history():
        logger.info("request for /api/history", request.remote_addr)
        
        def get_history():
            history = hm.get_history_elements(g.user.username)
            return history

        history = logger.performance(f'getting history for user {g.user.username}', get_history)
        return {'history': history}, 201

    # function for get token from username
    def get_token(username):
        user = db_models.User.query.filter_by(username = username).first()
        if not user:
            return
        if user.token == None:
            user.create_auth_token()
        return user.token
