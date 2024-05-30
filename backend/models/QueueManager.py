import os
import time
from io import BytesIO
from base64 import encodebytes, b64encode
from threading import Thread
from queue import Queue
from models.HistoryManager import HistoryManager
from models.ImageConverter import ImageConverter

#class that manage the queue of elaborations
class QueueManager:
    def __init__(self, app, socketio, msg_ok, msg_not_ok, db, logger, res_path):
        self.q = Queue()
        self.app = app
        self.socketio = socketio
        self.msg_ok = msg_ok
        self.msg_not_ok = msg_not_ok
        self.process_running = False
        self.hm = HistoryManager(app, db, logger)
        self.ic = ImageConverter(logger, socketio, res_path, msg_ok)
        self.logger = logger
        self.res_path = res_path
        self.start_process()

    # function for adding an element to the queue
    def add_to_queue(self, id, img, auth):
        if id and img:
            v = QueueValue(id, img, auth)
            self.q.put(v)
            self.logger.info(f"elaboration with id {id} add to queue")

    # queue thread
    def process_queue(self):
        with self.app.app_context():
            while True:
                time.sleep(1)
                if self.q.qsize() <= 0:
                    continue
                new_q = Queue()
                for i in range(self.q.qsize()):
                    v = self.q.get_nowait()
                    if not v.done:
                        new_q.put(v)
                    self.socketio.emit('queue_number', {"status": self.msg_ok, "index": i}, room=v.id)

                self.q = new_q

                if not self.process_running and self.q.qsize() > 0:
                    self.logger.info("No elaboration are running")
                    v = self.q.queue[0]
                    # start new elaboration
                    elaboration_thread = Thread(target=self.elaborate_image, args=(v,))
                    elaboration_thread.daemon = True
                    elaboration_thread.start()

    # image elaboration
    def elaborate_performance(self, v):
        # setup
        self.logger.info(f"starting to elaborate image with id {v.id}")
        self.process_running = True
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 0}, room=v.id)

        # image elaboration
        mesh_name = self.ic.create(v.img, v.id)

        if mesh_name == "NO-FACE" or mesh_name == "INVALID-VALUES":
            v.done = True
            self.process_running = False
            self.socketio.emit('status_elaboration', {"status": self.msg_not_ok, "msg": mesh_name})
            self.ic.load_models()
            return
        mesh_b64 = self.glb_to_base64(mesh_name)

        # end process
        if v.auth != "":
            self.hm.save_history_element(v.auth, v.img, mesh_b64)
        
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 90}, room=v.id)
        v.done = True
        self.process_running = False
        img_base64 = self.img_to_base64(v.img)
        self.remove_tmp_file(mesh_name)
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 100, 'img': img_base64, 'mesh': mesh_b64}, room=v.id)

    # start image elaboration registering performance
    def elaborate_image(self, v):
        self.logger.performance(f"elaboration with id {v.id}", self.elaborate_performance, v)

    # function for convert image in base64 string
    def img_to_base64(self, img):
        new = img.copy()
        buffer = BytesIO()
        new.save(buffer, format="JPEG")
        encoded = encodebytes(buffer.getvalue()).decode('ascii')
        return encoded

    # function for convert glb in base64 string
    def glb_to_base64(self, mesh):
        path = os.path.join(self.res_path, mesh)
        with open(path, "rb") as f:
            encodedZip = b64encode(f.read())
            str_data = encodedZip.decode()
            return str_data
        
    # function for remove tmp files of elaboration
    def remove_tmp_file(self, mesh):
        path = os.path.join(self.res_path, mesh)
        os.remove(path)

    # function that start queue process in another thread
    def start_process(self):
        queue_thread = Thread(target=self.process_queue)
        queue_thread.daemon = True
        queue_thread.start()

# class that define queue element instances
class QueueValue:
    def __init__(self, id, img, auth):
        self.id = id
        self.img = img
        self.auth = auth
        self.done = False

    def __repr__(self) -> str:
        return f"<Value with id {self.id} >"