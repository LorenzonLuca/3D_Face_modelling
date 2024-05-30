import base64
import re
from io import BytesIO
from flask_socketio import SocketIO, send, emit
from flask import request
from PIL import Image, ImageOps
from models.QueueManager import QueueManager

MAX_BUFFER_SIZE = 50 * 1000 * 1000
EVENT_OK = "OK"
EVENT_NOT_OK = "NOK"

# function that define socket.io events
def get_socket_manager(app, db, logger, res_path):
    socketio = SocketIO(app, cors_allowed_origins="*", max_http_buffer_size=MAX_BUFFER_SIZE)
    qm = QueueManager(app, socketio, EVENT_OK, EVENT_NOT_OK, db, logger, res_path)

    # socket.io event for start image process
    @socketio.on('process_image')
    def handle_user_image(data):
        logger.info(f"new elaboration received for id {request.sid}", request.remote_addr)
        try:
            image_data = re.sub('^data:image/.+;base64,', '', data["img"])
            img = Image.open(BytesIO(base64.b64decode(image_data)), mode='r')
            img = ImageOps.exif_transpose(img)
            img = img.convert('RGB')
            emit('image', {'status': EVENT_OK})
            logger.info(f"image from id {request.sid} is valid", request.remote_addr)
        except:
            emit('image', {'status': EVENT_NOT_OK})
            logger.warning(f"image from id {request.sid} is not valid", request.remote_addr)
            return
        qm.add_to_queue(request.sid, img, data["auth"])

    return socketio