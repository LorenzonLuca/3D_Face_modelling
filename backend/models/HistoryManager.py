import uuid
import os
import datetime
import base64
import db.database as db_models
from sqlalchemy import desc
import aspose.threed as a3d

# class for manage the history
class HistoryManager:
    def __init__(self,app, db, logger):
        self.app = app
        self.db = db
        self.logger = logger

    # function for save image and mesh for history
    def save_history_element(self, auth, img, mesh):
        with self.app.app_context():
            user = db_models.User.query.filter_by(token = auth).first()
            folder = self.create_folder(user.username)
            img_folder = os.path.join(folder, 'img.jpg')
            img.save(img_folder, optimize=True)
            mesh_file = base64.b64decode(mesh, validate=True)
            mesh_folder = os.path.join(folder, 'model.glb')
            with open(mesh_folder, 'wb') as f:
                f.write(mesh_file)
            self.logger.info(f"Image of {user.username} saved in {img_folder}")

    #function that create a folder for save inside elaboration files
    def create_folder(self, user):
        folder = uuid.uuid4().hex
        parent = os.getcwd()
        parent = os.path.join(parent, 'elaboration')
        path = os.path.join(parent, folder)
        os.mkdir(path)

        self.logger.info(f"created folder {folder} for user {user}")

        date = datetime.datetime.now()

        # add elaboration record inside the database
        el = db_models.Elaboration(user_fk = user, folder_path = folder, creation_date = date)
        self.db.session.add(el)
        self.db.session.commit()
        return path
    
    # function for retrieve history elements of user
    def get_history_elements(self, username):
        with self.app.app_context():
            elements = db_models.Elaboration.query.filter_by(user_fk = username).order_by(desc(db_models.Elaboration.creation_date))
            history_arr = []
            for el in elements:
                history_arr.append(el.convert_to_json())
            
            return history_arr

