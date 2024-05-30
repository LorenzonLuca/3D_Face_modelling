import os
from flask import Flask
from flask_cors import CORS
from api.routes import create_routes
from sockets.manager import get_socket_manager
from dotenv import load_dotenv
from db.database import init_database
from models.Logger import Logger

load_dotenv()
app = Flask(__name__)
cors = CORS(app)
cors = CORS(app, origins="*")

PORT=os.getenv('PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DB_CONNECTION')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logger = Logger(app)
logger.info(f"Start setup application")
db = init_database(app, logger)

with app.app_context():
    db.create_all()

create_routes(app, db, logger)

res_path = os.getenv('RESULT_ELABORATION_PATH')
socket_app = get_socket_manager(app, db, logger, res_path)

if __name__ == "__main__":
    logger.info(f"App started on port {PORT}")
    socket_app.run(app, host="0.0.0.0", debug=False, port=PORT, ssl_context=('./../3dfacemodelling.crt', './../3dfacemodelling-privateKey.key'))