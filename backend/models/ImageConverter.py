import aspose.threed as a3d
import uuid
from facenet_pytorch import MTCNN
import cv2
import face_alignment
import numpy as np
from core import get_recon_model
import os
import torch
import core.utils as utils
from tqdm import tqdm
import core.losses as losses
from scipy.io import loadmat
from core.BFM09ReconModel import BFM09ReconModel
import torch.nn as nn
from pytorch3d.structures import Meshes
from pytorch3d.renderer import (
    look_at_view_transform,
    FoVPerspectiveCameras,
    PointLights,
    RasterizationSettings,
    MeshRenderer,
    MeshRasterizer,
    SoftPhongShader,
    TexturesVertex,
    blending
)

# Elaboration process guide: https://datahacker.rs/007-3d-face-modeling-3dmm-model-fitting-in-python/
# class that manage the conversion from image to 3d mesh
class ImageConverter:

    def __init__(self, logger, socketio, res_path, msg_ok):
        self.logger = logger
        self.socketio = socketio
        self.msg_ok = msg_ok

        # define elaboration var
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.logger.info(f"Device selected: {self.device}")
        self.recon_model = "bfm09"
        self.tar_size = 256 # size for rendering window. We use a square window

        self.rf_lr = 1e-2 # learning rate for rigid fitting
        self.first_rf_iters = 1000 # iteration number of rigid fitting for the first frame in video fitting.
        self.lm_loss_w = 100 # weight for landmark loss

        self.nrf_lr = 1e-2 # learning rate for non-rigid fitting
        self.first_nrf_iters = 500 # iteration number of non-rigid fitting for the first frame in video fitting
        self.id_reg_w = 1e-3 # weight for id coefficient regularizer
        self.exp_reg_w = 0.8e-3 # weight for expression coefficient regularizer
        self.tex_reg_w = 1.7e-6 # weight for texture coefficient regularizer
        self.tex_w = 1 # weight for texture reflectance loss.
        self.rgb_loss_w = 1.6 # weight for rgb loss

        self.res_folder = res_path

        self.load_models()

    # function that load ML models
    def load_models(self):
        self.logger.info(f"Loading models for elaboration")
        self.mtcnn = MTCNN(device=self.device, select_largest=False)
        self.fa = face_alignment.FaceAlignment(face_alignment.LandmarksType, flip_input=False)  

        model_path = 'BFM/BFM09_model_info.mat'
        model_dict = loadmat(model_path)
        self.recon_model = BFM09ReconModel(model_dict, device=self.device,batch_size=1,img_size=self.tar_size)
        self.logger.info(f"Models loaded succesfully")

    # function that elaborate the image
    def create(self, image, id):
        self.logger.info(f"Starting to elaborate")
        img_arr = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2RGB)

        face_detected = self.detect_face(img_arr, id)
        if len(face_detected) < 1:
            return "NO-FACE"
        
        face_img = face_detected[0]
        bbox = face_detected[1]
        face_w = face_detected[2]
        face_h = face_detected[3]

        resized_face_img = cv2.resize(face_img, (self.tar_size, self.tar_size))
        lms = self.fa.get_landmarks_from_image(resized_face_img)[0] # Detect landmarks
        lms = lms[:, :2][None, ...] # Take only the X, Y and drop the third axis, Z (3D to 2D)
        lms = torch.tensor(lms, dtype=torch.float32, device=self.device)
        img_tensor = torch.tensor(resized_face_img[None, ...], dtype=torch.float32, device=self.device)

        lm_weights = self.rigid_fitting(lms, id)
        valid_values = self.validate_weights()
        if not valid_values:
            return "INVALID-VALUES"
        self.non_rigid_fitting(img_tensor, lms, lm_weights, id)

        with torch.no_grad():
            coeffs = self.recon_model.get_packed_tensors()
            pred_dict = self.recon_model(coeffs, render=True)
            rendered_img = pred_dict['rendered_img']
            self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 60}, room=id)
            rendered_img = rendered_img.cpu().numpy().squeeze()
            out_img = rendered_img[:, :, :3].astype(np.uint8)
            out_mask = (rendered_img[:, :, 3] > 0).astype(np.uint8)
            resized_out_img = cv2.resize(out_img, (face_w, face_h))
            resized_mask = cv2.resize(out_mask, (face_w, face_h), cv2.INTER_NEAREST)[..., None]

            self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 70}, room=id)

            composed_img = img_arr.copy()
            composed_face = composed_img[bbox[1]:bbox[3], bbox[0]:bbox[2], :] * \
                (1 - resized_mask) + resized_out_img * resized_mask
            composed_img[bbox[1]:bbox[3], bbox[0]:bbox[2], :] = composed_face

        return self.save_elaboration(pred_dict, id)
    
    # function for save elaboration result
    def save_elaboration(self, pred_dict, id):
        basename = uuid.uuid4().hex
        utils.mymkdirs(self.res_folder)
        out_obj_path = os.path.join(self.res_folder, basename+'_mesh.obj')
        vs = pred_dict['vs'].cpu().numpy().squeeze()
        tri = pred_dict['tri'].cpu().numpy().squeeze()
        color = pred_dict['color'].cpu().numpy().squeeze()
        utils.save_obj(out_obj_path, vs, tri+1, color)

        new_name = self.convert_to_glb(basename)
        self.logger.info(f'composed image is saved at {self.res_folder} as {new_name}')
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 80}, room=id)
        return new_name
    
    # function that detect face inside the image
    def detect_face(self, img_arr, id):
        orig_h, orig_w = img_arr.shape[:2]
        bboxes, probs = self.mtcnn.detect(img_arr)
        if bboxes is None:
            self.logger.warning('no face detected')
            return []
        else:
            bbox = utils.pad_bbox(bboxes[0], (orig_w, orig_h), 0.3)
            face_w = bbox[2] - bbox[0]
            face_h = bbox[3] - bbox[1]
            assert face_w == face_h

        self.logger.info(f'Face is detected. l: {bbox[0]}, t: {bbox[1]}, r: {bbox[2]}, b: {bbox[3]}')
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 10}, room=id)

        face_img = img_arr[bbox[1]:bbox[3], bbox[0]:bbox[2], :]
        return [face_img, bbox, face_w, face_h]
    
    # first previsions of elaboration
    def rigid_fitting(self, lms, id):
        self.logger.info('start rigid fitting')
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 20}, room=id)

        rigid_optimizer = torch.optim.Adam([self.recon_model.get_rot_tensor(),self.recon_model.get_trans_tensor()],lr=self.rf_lr)
        lm_weights = utils.get_lm_weights(self.device)
        for i in tqdm(range(self.first_rf_iters)):
            rigid_optimizer.zero_grad()
            pred_dict = self.recon_model(self.recon_model.get_packed_tensors(), render=False)
            lm_loss_val = losses.lm_loss(pred_dict['lms_proj'], lms, lm_weights, img_size=self.tar_size)
            total_loss = self.lm_loss_w * lm_loss_val
            total_loss.backward()
            rigid_optimizer.step()
        
        self.logger.info(f'done rigid fitting. lm_loss: {lm_loss_val.detach().cpu().numpy()}')
        self.logger.info(f"Rotation    {self.recon_model.get_packed_tensors()[0, 224:227].cpu().detach().numpy()}")
        self.logger.info(f"Translation {self.recon_model.get_packed_tensors()[0, 254:257].cpu().detach().numpy()}")
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 30}, room=id)

        return lm_weights
    
    # second previsions of elaboration
    def non_rigid_fitting(self, img_tensor, lms, lm_weights, id):
        self.logger.info('start non-rigid fitting')
        nonrigid_optimizer = torch.optim.Adam(
            [self.recon_model.get_id_tensor(), self.recon_model.get_exp_tensor(),
            self.recon_model.get_gamma_tensor(), self.recon_model.get_tex_tensor(),
            self.recon_model.get_rot_tensor(), self.recon_model.get_trans_tensor()], lr=self.nrf_lr)
        
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 40}, room=id)
        
        for i in tqdm(range(self.first_nrf_iters)):
            nonrigid_optimizer.zero_grad()

            pred_dict = self.recon_model(self.recon_model.get_packed_tensors(), render=True)
            rendered_img = pred_dict['rendered_img']
            lms_proj = pred_dict['lms_proj']
            face_texture = pred_dict['face_texture']

            mask = rendered_img[:, :, :, 3].detach()

            photo_loss_val = losses.photo_loss(
                rendered_img[:, :, :, :3], img_tensor, mask > 0)

            lm_loss_val = losses.lm_loss(lms_proj, lms, lm_weights,img_size=self.tar_size)
            id_reg_loss = losses.get_l2(self.recon_model.get_id_tensor())
            exp_reg_loss = losses.get_l2(self.recon_model.get_exp_tensor())
            tex_reg_loss = losses.get_l2(self.recon_model.get_tex_tensor())
            tex_loss_val = losses.reflectance_loss(face_texture, self.recon_model.get_skinmask())

            loss = lm_loss_val*self.lm_loss_w + \
                id_reg_loss*self.id_reg_w + \
                exp_reg_loss*self.exp_reg_w + \
                tex_reg_loss*self.tex_reg_w + \
                tex_loss_val*self.tex_w + \
                photo_loss_val*self.rgb_loss_w

            loss.backward()
            nonrigid_optimizer.step()
        
        self.socketio.emit('status_elaboration', {"status": self.msg_ok, "value": 50}, room=id)
    
    # check if elaboration result contains valid values
    def validate_weights(self):
        check = np.isnan(self.recon_model.get_packed_tensors()[0, 224:227].cpu().detach().numpy())
        for v in check:
            if v == True:
                self.logger.info("Found some NAN valus inside result, need to reload models")
                return False
        return True
    
    # function that convert obj file in glb file
    def convert_to_glb(self, name):
        path = os.path.join(self.res_folder, name+'_mesh.obj')
        n_path = os.path.join(self.res_folder, name+'_mesh.glb')
        if self.validate_obj_file(path):
            os.remove(path)
            return "INVALID-VALUES"
        scene = a3d.Scene.from_file(path)
        scene.save(n_path)
        os.remove(path)
        return name+'_mesh.glb'
    
    # function that validate the obj file
    def validate_obj_file(self, path):
        f = open(path, "r")
        first_line = f.readline()

        return "nan" in first_line