# -*- coding: utf-8 -*-
"""
Created on Wed May  5 15:35:46 2021

@author: lukem
"""
from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal 
import numpy as np
import cv2 
import torch
from face_alignment.detection.blazeface.utils import resize_and_crop_image
from face_alignment.utils import crop, get_preds_fromhm


class GetLandmarks(QtCore.QThread):
    
    landmarks = pyqtSignal(torch.Tensor, object, object, object, object, object)
    finished = pyqtSignal()
    
    
    def __init__(self, image, shape, lefteye, righteye, savedshape, ModelName, Modelname_NLF, FaceDetector, FaceAlignment, model, model_FAN, model_NLF, net):
        super(GetLandmarks, self).__init__()
        self._image = image
        self._shape = torch.Tensor()
        self._savedShape = savedshape
        if savedshape == True:
            print('saveshape = ', savedshape)
            self._shape = shape
            
            
        if lefteye == None and righteye == None:
            self._lefteye = [-1,-1,-1]
            self._righteye = [-1,-1,-1]
            self._eyesDone = False
        else:
            if lefteye[0] <= 0 or righteye[0] <= 0 or lefteye[1] <= 0 or righteye[1] <= 0 or lefteye[2] <= 0 or righteye[2] <= 0:
                self._eyesDone = False
            else:
                
                self._lefteye = lefteye
                self._righteye = righteye
                self._eyesDone = True
        self._lefteye_landmarks = [0, 0, 0, 0, 0]
        self._righteye_landmarks = [0, 0, 0, 0, 0]
        self._boundingbox = [-1,-1,-1,-1]
        self.ModelName = ModelName
        self.ModelName_NLF = Modelname_NLF
        self.FaceDetector = FaceDetector
        self.FaceAlignment = FaceAlignment
        self.model = model
        self.model_FAN = model_FAN
        self.model_NLF = model_NLF
        self.net = net
        
        
    def run(self):
        print('Starting thread...')
        self.find_landmarks()
    
    
    def find_face(self):
        """Finding Face"""
        #################################################################
    
        
        """Finding and Centering Face"""
        # FaceDetector = BlazeFace()
        # FaceDetector.load_state_dict(torch.load('./models/blazeface.pth'))
        # FaceDetector.load_anchors_from_npy(np.load('./models/anchors.npy'))
    
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # FaceDetector.to(device)
        # FaceDetector.eval();
        FaceDetector = self.FaceDetector
        H, W, C = self._image.shape
        orig_size = min(H, W)
        img, (xshift, yshift) = resize_and_crop_image(self._image,128)
        preds = FaceDetector.predict_on_image(img)
        shift = np.array([xshift,yshift] * 2)
        scores = preds[:,-1:]
        locs = np.concatenate((preds[:,1:2], preds[:,0:1], preds[:,3:4], preds[:,2:3]), axis=1)
        fp = np.concatenate((locs * orig_size + shift, scores), axis=1)[0]
        
        return fp
    
    
    def find_landmarks(self):
        #Find face
        fp = self.find_face()
        self._boundingbox = fp[:-1]
        
        image = self._image.copy()
        
        """Cropping Image"""
        #################################################################
    
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        # FaceAlignment = torch.jit.load('./models/2DFAN4-cd938726ad.zip')
        # FaceAlignment.to(device)
        # FaceAlignment.eval();
        
        FaceAlignment = self.FaceAlignment
    
        """Adjusting Image to allow landmark detection"""
        center = torch.tensor([fp[2] - (fp[2] - fp[0]) / 2.0, fp[3] - (fp[3] - fp[1]) / 2.0])
        center[1] = center[1] - (fp[3] - fp[1]) * 0.12 #number 0.12 taken out of FAN github
        scale = (fp[2] - fp[0] + fp[3] - fp[1]) / 195 #number 195 taken out of Blazeface github
        #we are going to create a 256x256 image centered around the face
    
        img = crop(image, center, scale, 256)
        
        #Debugging line
        # print('In thread, self._shape = ', self._shape)
        
        if self._savedShape == False:
            
            print('Running new model')
            if self.ModelName == 'FAN':
        
                """Finding Facial Landmarks using FAN"""
                #################################################################
            
                
                img = torch.from_numpy(img.transpose(2,0,1)).float() #images are organized HxWxC, but torch expects CxHxW
                # img.to(device)
                img.div_(255.0).unsqueeze_(0)
            
                output = FaceAlignment(img).detach()
                output = output.cpu().numpy()
            
                """Finding Points"""
                pts, pts_img = get_preds_fromhm(output, center.numpy(), scale) #this function returns the landmarks position in the heatmaps - in a 64x64 square, a the landmarks position in the 
                pts_img = torch.from_numpy(pts_img).view(68,2)
                labels = np.arange(1,69)
                labels = torch.from_numpy(labels).view(68,1)
                
                pts_img = torch.cat((pts_img, labels), 1)
            
            elif self.ModelName == 'FAN_MEEE':
                print('Using FAN_MEEE model')
                model_FAN = self.model_FAN
                
                img = torch.from_numpy(img.transpose(2,0,1)).float() #images are organized HxWxC, but torch expects CxHxW
                # img.to(device)
                img.div_(255.0).unsqueeze_(0)
            
                output = model_FAN(img).detach()
                output = output.cpu().numpy()
            
                """Finding Points"""
                pts, pts_img = get_preds_fromhm(output, center.numpy(), scale) #this function returns the landmarks position in the heatmaps - in a 64x64 square, a the landmarks position in the 
                pts_img = torch.from_numpy(pts_img).view(68,2)
                labels = np.arange(1,69)
                labels = torch.from_numpy(labels).view(68,1)
                
                pts_img = torch.cat((pts_img, labels), 1)
            
            elif self.ModelName == 'HRNet':
    
                """Finding Facial Landmarks using HRNet"""
                #################################################################
            
                # """Loading Model"""
                # model_path = './models/HR18-300W.pth'
                # config_path = './models/HR18-300W.yaml'
            
                # merge_configs(config, config_path)
            
                # model = get_face_alignment_net(config)
                # model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
                # model.to(device)
                # model.eval();
                model = self.model
                """Finding Landmarks"""
                #these values are taken directly from github
                mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
                std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
            
                center = torch.tensor([fp[2] - (fp[2] - fp[0]) / 2.0, fp[3] - (fp[3] - fp[1]) / 2.0])
            
                center[1] = center[1] - (fp[3] - fp[1]) * 0.12 #number 0.12 taken out of FAN github
                scale = (fp[2] - fp[0] + fp[3] - fp[1]) / 195 #number 195 taken out of Blazeface github
                #we are going to create a 256x256 image centered around the face
                img = crop(image, center, scale, 256)
            
                img = (img/255.0 - mean) / std
                img = torch.from_numpy(img.transpose(2,0,1)).float() #images are organized HxWxC, but torch expects CxHxW
                img = img.unsqueeze(0)
            
                output = model(img).detach()
                output = output.cpu().numpy()
            
                pts, pts_img = get_preds_fromhm(output, center.numpy(), scale) #this function returns the landmarks position in the heatmaps - in a 64x64 square, a the landmarks position in the 
                pts_img = torch.from_numpy(pts_img).view(-1,2)
                
                labels = np.arange(1,len(pts_img)+1)
                labels = torch.from_numpy(labels).view(-1,1)
                
                pts_img = torch.cat((pts_img, labels), 1)
            
            elif self.ModelName == 'NLF_model':
                model = self.model_NLF
                """Finding Landmarks"""
                #these values are taken directly from github
                mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
                std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
            
                center = torch.tensor([fp[2] - (fp[2] - fp[0]) / 2.0, fp[3] - (fp[3] - fp[1]) / 2.0])
            
                center[1] = center[1] - (fp[3] - fp[1]) * 0.12 #number 0.12 taken out of FAN github
                scale = (fp[2] - fp[0] + fp[3] - fp[1]) / 195 #number 195 taken out of Blazeface github
                #we are going to create a 256x256 image centered around the face
                img = crop(image, center, scale, 256)
            
                img = (img/255.0 - mean) / std
                img = torch.from_numpy(img.transpose(2,0,1)).float() #images are organized HxWxC, but torch expects CxHxW
                img = img.unsqueeze(0)
            
                output = model(img)[0].detach()
                output = output.cpu().numpy()
            
                pts, pts_img = get_preds_fromhm(output, center.numpy(), scale) #this function returns the landmarks position in the heatmaps - in a 64x64 square, a the landmarks position in the 
                pts_img = torch.from_numpy(pts_img).view(-1,2)
                
                labels = np.arange(1,len(pts_img)+1)
                labels = torch.from_numpy(labels).view(-1,1)
                
                pts_img = torch.cat((pts_img, labels), 1)
                
            """Saves Initial Points, then check if the NLF is added"""
            self._shape = pts_img    
        
        if self.ModelName_NLF == True:
            model = self.model_NLF
            """Finding Landmarks"""
            #these values are taken directly from github
            mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
            std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
        
            center = torch.tensor([fp[2] - (fp[2] - fp[0]) / 2.0, fp[3] - (fp[3] - fp[1]) / 2.0])
        
            center[1] = center[1] - (fp[3] - fp[1]) * 0.12 #number 0.12 taken out of FAN github
            scale = (fp[2] - fp[0] + fp[3] - fp[1]) / 195 #number 195 taken out of Blazeface github
            #we are going to create a 256x256 image centered around the face
            img = crop(image, center, scale, 256)
        
            img = (img/255.0 - mean) / std
            img = torch.from_numpy(img.transpose(2,0,1)).float() #images are organized HxWxC, but torch expects CxHxW
            img = img.unsqueeze(0)
        
            output = model(img)[0].detach()
            output = output.cpu().numpy()
        
            pts, pts_img = get_preds_fromhm(output, center.numpy(), scale) #this function returns the landmarks position in the heatmaps - in a 64x64 square, a the landmarks position in the 
            pts_img = torch.from_numpy(pts_img).view(-1,2)
            
            try:
                labels = np.arange(len(self._shape)+1, len(self._shape)+len(pts_img)+1)
            except:
                labels = np.arange(1,len(pts_img)+1)
            
            labels = torch.from_numpy(labels).view(-1,1)
            
            pts_img = torch.cat((pts_img, labels), 1)
            
            # print('In thread (right before combining NLF and 68 landmarks), self._shape = ', self._shape)
            self._shape = torch.cat((self._shape, pts_img), -2)
            # print('In thread (right after combining NLF and 68 landmarks), self._shape = ', self._shape)
        
        
        #Testing get_iris and process_eye
        
        try:
            if len(self._shape) >= 68 and self._eyesDone == False:
                self.new_get_iris()
                
            elif self._eyesDone == False:
                self._lefteye = [0, 0, 0]
                self._righteye = [0, 0, 0]
            else:
                print('Eyes already computed')
                print('self._lefteye = ', self._lefteye,
                      'self._righteye = ', self._righteye)
                    
        except:
            self._lefteye = [0, 0, 0]
            self._righteye = [0, 0, 0]
            print('Error')
            print('self._shape = ', self._shape)
        
        
        
        # print('self._shape: ', self._shape)
        # print('self._lefteye: ', self._lefteye)
        # print('self._righteye: ', self._righteye)
        
        self.landmarks.emit(self._shape, self._lefteye, self._righteye, self._lefteye_landmarks, self._righteye_landmarks, self._boundingbox)
        
        self.finished.emit()
        print('Finished Thread')
    

    def transform_np_vector(self, point, center, scale, resolution, invert=False):
        """Generate and affine transformation matrix.
    
        Given a set of points, a center, a scale and a targer resolution, the
        function generates and affine transformation matrix. If invert is ``True``
        it will produce the inverse transformation.
    
        Arguments:
            point {numpy.array} -- the input 2D point
            center {numpy.array} -- the center around which to perform the transformations
            scale {float} -- the scale of the face/object
            resolution {float} -- the output resolution
    
        Keyword Arguments:
            invert {bool} -- define wherever the function should produce the direct or the
            inverse transformation matrix (default: {False})
        """
    
        
        _pt = np.ones((point.shape[0],3))
        _pt[:,:2] = point
    
        h = 200.0 * scale
        t = np.eye(3)
        t[0, 0] = resolution / h
        t[1, 1] = resolution / h
        t[0, 2] = resolution * (-center[0] / h + 0.5)
        t[1, 2] = resolution * (-center[1] / h + 0.5)
    
        if invert:
            t = np.ascontiguousarray(np.linalg.pinv(t))
    
        new_point = np.dot(t,_pt.T).T[:,:2]
    
        return new_point.astype(np.int32)
   

    def find_radius(self, center, points):
        """This function transforms the the landmarks of the iris
        in to center (x, y) and radius"""    
        distance_sum = 0
        for i, point in enumerate(points):
            distance = np.sqrt(((center[0] - points[i,0])**2 + (center[1] - points[i,1])**2))
            distance_sum = distance_sum + distance
            
        radius = distance_sum/4
        return radius
        
    def new_get_iris(self):
        #function that selects the eye from a face image and uses -get_pupil- to 
        #localize the iris. 


        #left eye cropping
        leye_position = np.array([self._shape[42:48,0].min().numpy(), self._shape[42:48,1].min().numpy(),
                                  self._shape[42:48,0].max().numpy(), self._shape[42:48,1].max().numpy()])
        #find center or face based on the face detection 
        center_leye = torch.tensor([leye_position[2] - (leye_position[2] - leye_position[0]) / 2.0,
                                    leye_position[3] - (leye_position[3] - leye_position[1]) / 2.0])
        center_leye[1] = center_leye[1] - (leye_position[3] - leye_position[1]) * 0.12  #number 0.12 taken out of FAN github 
        scale_leye = (leye_position[2] - leye_position[0] + leye_position[3] - leye_position[1]) / 100 #number 195 taken out of BlazeFace github
        #we are going to create a 256x256 image centered around the face
        inp_leye = crop(self._image, center_leye, scale_leye,64)
        
        
        #right eye cropping
        reye_position = np.array([self._shape[36:42,0].min().numpy(), self._shape[36:42,1].min().numpy(),
                                  self._shape[36:42,0].max().numpy(), self._shape[36:42,1].max().numpy()])
        #find center or face based on the face detection 
        center_reye = torch.tensor([reye_position[2] - (reye_position[2] - reye_position[0]) / 2.0,
                                    reye_position[3] - (reye_position[3] - reye_position[1]) / 2.0])
        center_reye[1] = center_reye[1] - (reye_position[3] - reye_position[1]) * 0.12  #number 0.12 taken out of FAN github 
        scale_reye = (reye_position[2] - reye_position[0] + reye_position[3] - reye_position[1]) / 100 #number 195 taken out of BlazeFace github
        #we are going to create a 256x256 image centered around the face
        inp_reye = crop(self._image, center_reye, scale_reye,64)

        
        #Left eye Landmarks
        eye_gpu, iris_gpu = self.net.predict_on_image(np.array(inp_leye))
        iris_landmarks_left = iris_gpu.cpu().numpy()
        iris_landmarks_left_orig = self.transform_np_vector(iris_landmarks_left[0][:,:2]*4, center_leye, scale_leye, 256, invert=True)
        self._lefteye_landmarks = iris_landmarks_left_orig
        # print('self._lefteye_landmarks = ', self._lefteye_landmarks)
        
        #Right eye Landmarks
        eye_gpu, iris_gpu = self.net.predict_on_image(np.array(inp_reye))
        iris_landmarks_right = iris_gpu.cpu().numpy()
        iris_landmarks_right_orig = self.transform_np_vector(iris_landmarks_right[0][:,:2]*4, center_reye, scale_reye, 256, invert=True)        
        self._righteye_landmarks = iris_landmarks_right_orig
        # print('self._righteye_landmarks = ', self._righteye_landmarks)
        
        #Left eye
        iris_left = [iris_landmarks_left_orig[0,0], iris_landmarks_left_orig[0,1], 0]
        iris_left[2] = self.find_radius(iris_landmarks_left_orig[0,:], iris_landmarks_left_orig[1:,:])
        self._lefteye = iris_left
        # print('self._lefteye = ', self._lefteye)
        
        #Right eye
        iris_right = [iris_landmarks_right_orig[0,0], iris_landmarks_right_orig[0,1], 0]
        iris_right[2] = self.find_radius(iris_landmarks_right_orig[0,:], iris_landmarks_right_orig[1:,:])
        self._righteye = iris_right
        # print('self._righteye = ', self._righteye)
    
       