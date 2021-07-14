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
from Utilities import find_circle_from_points
from models.irislandmarks import IrisLandmarks
from face_alignment.detection.blazeface.utils import resize_and_crop_image
from face_alignment.utils import crop, get_preds_fromhm


class GetLandmarks(QtCore.QThread):
    
    landmarks = pyqtSignal(torch.Tensor, object, object, object)
    finished = pyqtSignal()
    
    
    def __init__(self, image, shape, lefteye, righteye, savedshape, ModelName, Modelname_NLF, FaceDetector, FaceAlignment, model, model_FAN, model_NLF):
        super(GetLandmarks, self).__init__()
        self._image = image
        self._shape = torch.Tensor()
        self._savedShape = savedshape
        if savedshape == True:
            self._shape = shape
            
            
        if lefteye == None and righteye == None:
            self._lefteye = [-1,-1,-1]
            self._righteye = [-1,-1,-1]
            self._eyesDone = False
        else:
            if lefteye[2] == 0 and righteye[2] == 0:
                self._eyesDone = False
            else:
                self._lefteye = lefteye
                self._righteye = righteye
                self._eyesDone = True
        self._boundingbox = [-1,-1,-1,-1]
        self.ModelName = ModelName
        self.ModelName_NLF = Modelname_NLF
        self.FaceDetector = FaceDetector
        self.FaceAlignment = FaceAlignment
        self.model = model
        self.model_FAN = model_FAN
        self.model_NLF = model_NLF
        
        
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
                    
        except:
            self._lefteye = [0, 0, 0]
            self._righteye = [0, 0, 0]
            print('Error')
            print('self._shape = ', self._shape)
        
        
        
        # print('self._shape: ', self._shape)
        # print('self._lefteye: ', self._lefteye)
        # print('self._righteye: ', self._righteye)
        
        self.landmarks.emit(self._shape, self._lefteye, self._righteye, self._boundingbox)
        
        self.finished.emit()
        print('Finished Thread')
        
        

    def get_iris(self):
        #function that selects the eye from a face image and uses -get_pupil- to 
        #localize the iris. 


        #Left Eye
        x_left = self._shape[42,0]
        w_left = (self._shape[45,0]-x_left)
        y_left = min(self._shape[43,1],self._shape[44,1])
        h_left = (max(self._shape[46,1],self._shape[47,1])-y_left)
        Eye = self._image.copy()
        Eye = Eye[int(y_left-5):int(y_left+h_left+5),int(x_left-5):int(x_left+w_left+5)]
        
        selected_circle_left = self.process_eye(Eye)
        selected_circle_left[0] = int(selected_circle_left[0]) + int(x_left-5)
        selected_circle_left[1] = int(selected_circle_left[1]) + int(y_left-5)
        selected_circle_left[2] = int(selected_circle_left[2])
        
        self._lefteye = selected_circle_left
        
        #Right Eye    
        x_right = self._shape[36,0]
        w_right = (self._shape[39,0]-x_right)
        y_right = min(self._shape[37,1],self._shape[38,1])
        h_right = (max(self._shape[41,1],self._shape[40,1])-y_right)
        Eye = self._image.copy()
        Eye = Eye[int(y_right-5):int(y_right+h_right+5),int(x_right-5):int(x_right+w_right+5)]
        
        selected_circle_right = self.process_eye(Eye)
        selected_circle_right[0] = int(selected_circle_right[0]) + int(x_right-5)
        selected_circle_right[1] = int(selected_circle_right[1]) + int(y_right-5)
        selected_circle_right[2] = int(selected_circle_right[2])
            
        self._righteye = selected_circle_right 
        
        
    def process_eye(self, InputImage):
        #this function appplies a modified Daugman procedure for iris detection.
        #See 'How Iris Recognition Works, Jhon Dougman - IEEE Transactions on 
        #circuits and systems for video technology, January 2004'
        
        #get dimension of image 
        h_eye, w_eye, d_eye = InputImage.shape
        
        #this is the variable that will be return after processing
        circle=[]
        
        #verify that it is a color image
        if d_eye < 3:
            print('Pupil cannot be detected -- Color image is required')
            #circle=[int(w_eye/2), int(h_eye/2), int(w_eye/4)]
            circle=[-1,-1,-1]
            return circle
            
        #verify that the eye is open  
        #print(w_eye/h_eye)
        if w_eye/h_eye > 3.2:
            print('Pupil cannot be detected -- Eye is closed')
            circle=[int(w_eye/2), int(h_eye/2), int(w_eye/4)]
            return circle
        
        #reduce brightness to help with light-colored eyes
        InputImage = np.array(InputImage*0.75+0, dtype=InputImage.dtype)
        
        #split image into its different color channels 
        b,g,r = cv2.split(InputImage)
        
        #and create a new gray-image combining the blue and green channels, this 
        #will help to differentiate between the iris and sclera 
        #the function cv2.add guarantees that the resulting image has values 
        #between 0 (white) and 255 (black)
        bg = cv2.add(b,g)
        #filter the image to smooth the borders
        bg = cv2.GaussianBlur(bg,(3,3),0)
        
        #we assume that the radii of the iris is between 1/5.5 and 1/3.5 times the eye 
        #width (this value was obtained after measuring multiple eye images, it only
        #works if the eye section was obtained via dlib)
        Rmin = int(w_eye/5.5)
        Rmax = int(w_eye/3.5)
        radius = range(Rmin,Rmax+1)
        
        result_value = np.zeros(bg.shape, dtype=float)
        result_index_ratio = np.zeros(bg.shape, dtype=bg.dtype)
        mask = np.zeros(bg.shape, dtype=bg.dtype)
        
        #apply the Dougnman's procedure for iris detection. In this case I modify the 
        #procedure instead of use a full circunference it only uses 1/5 of 
        #a circunference. The procedure uses a circle between -35deg-0deg and 
        #180deg-215deg if the center beeing analized is located in the top half of the 
        #eye image, and a circle between 0deg-35deg and 145deg-180deg if the center 
        #beeing analized is located in the bottom half of the eye image
        
        possible_x = range(Rmin,w_eye-Rmin)
        possible_y = range(0,h_eye)
        for x in possible_x:
            for y in possible_y:  
                          
                intensity=[]
                for r in radius:
                    
                    if y>=int(h_eye/2):
                        temp_mask=mask.copy()   
                        #cv2.circle(temp_mask,(x,y),r,(255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, -35, 0, (255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, 180, 215, (255,255,255),1)
                        processed = cv2.bitwise_and(bg,temp_mask)
                        intensity.append(cv2.sumElems(processed)[0]/(2*3.141516*r))
                    
                    else:
                        temp_mask = mask.copy()   
                        #cv2.circle(temp_mask,(x,y),r,(255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, 0, 35, (255,255,255),1)
                        cv2.ellipse(temp_mask, (x,y), (r,r), 0, 145, 180, (255,255,255),1)
                        processed = cv2.bitwise_and(bg,temp_mask)
                        intensity.append(cv2.sumElems(processed)[0]/(2*3.141516*r))                
        
        
                diff_vector = np.diff(intensity)
                max_value = max(diff_vector)
                max_index = [i for i, j in enumerate(diff_vector) if j == max_value]   
                result_value[y,x] = max_value
                result_index_ratio[y,x] = max_index[0]
            
        
        
        #the results are filtered by a Gaussian filter, as suggested by Daugman
        result_value = cv2.GaussianBlur(result_value,(7,7),0)
        
        
        
        #now we need to find the center and radii that show the largest change in 
        #intensity    
        matrix = result_value
        needle = np.max(matrix)
        
        matrix_dim = w_eye
        item_index = 0
        for row in matrix:
            for i in row:
                if i == needle:
                    break
                item_index += 1
            if i == needle:
                break
        
        #this is the center and radius of the selected circle
        c_y_det = int(item_index / matrix_dim) 
        c_x_det = item_index % matrix_dim
        r_det = radius[result_index_ratio[c_y_det,c_x_det]]
        
        circle = [c_x_det,c_y_det,r_det]   
        
        return circle 
    

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
            
    
        
    def new_get_iris(self):
        #function that selects the eye from a face image and uses -get_pupil- to 
        #localize the iris. 
        
        

        #left eye
        leye_position = np.array([self._shape[42:48,0].min().numpy(), self._shape[42:48,1].min().numpy(),
                                  self._shape[42:48,0].max().numpy(), self._shape[42:48,1].max().numpy()])
        #find center or face based on the face detection 
        center_leye = torch.tensor([leye_position[2] - (leye_position[2] - leye_position[0]) / 2.0,
                                    leye_position[3] - (leye_position[3] - leye_position[1]) / 2.0])
        center_leye[1] = center_leye[1] - (leye_position[3] - leye_position[1]) * 0.12  #number 0.12 taken out of FAN github 
        scale_leye = (leye_position[2] - leye_position[0] + leye_position[3] - leye_position[1]) / 100 #number 195 taken out of BlazeFace github
        #we are going to create a 256x256 image centered around the face
        inp_leye = crop(self._image, center_leye, scale_leye,64)
        
        
        #right eye
        reye_position = np.array([self._shape[36:42,0].min().numpy(), self._shape[36:42,1].min().numpy(),
                                  self._shape[36:42,0].max().numpy(), self._shape[36:42,1].max().numpy()])
        #find center or face based on the face detection 
        center_reye = torch.tensor([reye_position[2] - (reye_position[2] - reye_position[0]) / 2.0,
                                    reye_position[3] - (reye_position[3] - reye_position[1]) / 2.0])
        center_reye[1] = center_reye[1] - (reye_position[3] - reye_position[1]) * 0.12  #number 0.12 taken out of FAN github 
        scale_reye = (reye_position[2] - reye_position[0] + reye_position[3] - reye_position[1]) / 100 #number 195 taken out of BlazeFace github
        #we are going to create a 256x256 image centered around the face
        inp_reye = crop(self._image, center_reye, scale_reye,64)

        
        device = 'cpu'
        net = IrisLandmarks().to(device)
        net.load_weights('./models/irislandmarks.pth')

        eye_gpu, iris_gpu = net.predict_on_image(np.array(inp_leye))
        iris_landmarks_left = iris_gpu.cpu().numpy()
        iris_landmarks_left_orig = self.transform_np_vector(iris_landmarks_left[0][:,:2]*4, center_leye, scale_leye, 256, invert=True)
        print('iris_landmarks_left_orig = ', iris_landmarks_left_orig)
        
        eye_gpu, iris_gpu = net.predict_on_image(np.array(inp_reye))
        iris_landmarks_right = iris_gpu.cpu().numpy()
        iris_landmarks_right_orig = self.transform_np_vector(iris_landmarks_right[0][:,:2]*4, center_reye, scale_reye, 256, invert=True)        
        print('iris_landmarks_right_orig = ', iris_landmarks_right_orig)
    
        iris_left_x = iris_landmarks_left_orig[:,0]
        iris_left_y = iris_landmarks_left_orig[:,1]
        iris_left = find_circle_from_points(iris_left_x, iris_left_y)
        self._lefteye = iris_left
        
        iris_right_x = iris_landmarks_right_orig[:,0]
        iris_right_y = iris_landmarks_right_orig[:,1]
        iris_right = find_circle_from_points(iris_right_x, iris_right_y)
        self._righteye = iris_right
    
       