# -*- coding: utf-8 -*-
"""
Created on Wed Aug 16 10:53:19 2017

@author: Diego L.Guarin -- 
"""

import numpy as np
import torch
from PyQt5 import QtWidgets, QtGui, QtCore
from scipy.spatial.distance import cdist

from Metrics import estimate_lines, find_NLF
from Manual_eye_process import get_iris_manual #this function opens a new window to manually select the iris

"""
This class is in charge of drawing the picture and the landmarks in the main 
window, it also takes care of lifting and re-location of landmarks. 
"""

class ImageViewer(QtWidgets.QGraphicsView):       
    dots_shown = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        #usual parameters to make sure the image can be zoom-in and out and is 
        #possible to move around the zoomed-in view
        super(ImageViewer, self).__init__(*args, **kwargs)
        self._zoom = 0
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setTransformationAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtWidgets.QGraphicsView.AnchorUnderMouse)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.setBackgroundBrush(QtGui.QBrush(QtGui.QColor(255,255,255)))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
        self.setMouseTracking(True)
        self._busy = False
        
        #this is used to show the dots and update the dots in image
        """Variable for patient"""
        self._shape = None
        self._lefteye = None
        self._righteye = None
        self._lefteye_landmarks = None
        self._righteye_landmarks = None
        self._reference_side = 'Right' #reference side is right by default
        self._image = None
        #self._opencvimage = None
        self._boundingbox = None
        self._PointToModify = None
        self._IrisToModify = None
        self._points = None
        self._NLF_points = None
        self._pointAdded = 0
        self._savedShape = False
        # self._numPoints = 68
        
        
        """Setting Parameters"""
        #Landmarks Setting
        self._landmark_size = 1 #Size of landmarks (used to make sure landmarks adjust based on num of pixels)
        self._landmark_color = QtGui.QColor(QtCore.Qt.red) #Color of current landmarks
        self._landmark_color_lower_lid = QtGui.QColor(QtCore.Qt.blue) #Color of default landmarks
        self._landmark_color_lower_lips = QtGui.QColor(QtCore.Qt.blue) #Color of landmarks and metrics in lips
        self._iris_color = QtGui.QColor(QtCore.Qt.green) #Color of Iris
        self._label_color = QtGui.QColor(QtCore.Qt.white) #Color of numbers next to landmarks
        self._NLF_color = QtGui.QColor(QtCore.Qt.black) #Color of NLF angle label
        
        #Visualization Setting
        self._IsShapeVisible = True #Tracks if user hides dots
        self._IsMidLineVisible = False #Tracks if user ask to show midline
        self._IsNLFVisible = False #Tracks if user ask to show NLF
        
        #Midline Setting
        self._AdjustingMidLine = False
        self._IsMouseOverMidLine = False
        self._IsMidLineMoving = False
        self._midLine_color = QtGui.QColor(QtCore.Qt.yellow) #Color of lines in Midline
        
        #These variables control actions from clicks
        self._IsPointLifted = False
        self._AddLandmarks = False
        
        #These variables control action from mouse movement
        self._IsDragEyes = False
        #These track what eye the person is trying to move if self._IsDragEyes = True
        self._IsDragLeft = False
        self._IsDragRight = False
        self._BothEyesTogether = False

        #QtWidgets.QGraphicsView.RubberBandDrag
   

    ########################################################################################################################
    ########################################################################################################################
    """Basic Functions"""
    ########################################################################################################################
    ########################################################################################################################
    
    
    def setPhoto(self, pixmap = None):
        #this function puts an image in the scece (if pixmap is not None), it
        #sets the zoom to zero 
        self._zoom = 0        
        if pixmap and not pixmap.isNull():
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView()
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())


    def fitInView(self):
        #this function takes care of accomodating the view so that it can fit
        #in the scene, it resets the zoom to 0 (i think is a overkill, i took
        #it from somewhere else)
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        #self.setSceneRect(rect)
        if not rect.isNull():
            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())        
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                     viewrect.height() / scenerect.height())               
            self.scale(factor, factor)
            self.centerOn(rect.center())
            self._zoom = 0                        


    def zoomFactor(self):
        return self._zoom
    

    def set_update_photo(self, toggle=True):
        #this function takes care of updating the view without re-setting the 
        #zoom. Is usefull for when you lift or relocate landmarks or when 
        #drawing lines in the middle of the face

        #image = cv2.cvtColor(temp_image,cv2.COLOR_BGR2RGB)
        if self._image is not None:

            height, width, channel = self.image.shape
            bytesPerLine = 3 * width
            img_Qt = QtGui.QImage(self.image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            img_show = QtGui.QPixmap.fromImage(img_Qt)
            
            self._photo.setPixmap(img_show)    
            self._scene.addItem(self._photo)
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    
    
    def show_entire_image(self):
        #this is a little utility to reset the zoom with a single click
        self.fitInView()
        
    
        
    def resizeEvent(self, event):
        #this function assure that when the main window is resized the image 
        #is also resized preserving the h/w ratio
        self.fitInView()
        
            
            
    def update_view(self):
        #this function takes care of updating the view by re-setting the zoom.
        #is usefull to place the image in the scene for the first time
        
        
        #if shape then add shape to image
    
        #image = cv2.cvtColor(temp_image,cv2.COLOR_BGR2RGB)
        if self._image is not None:
            height, width, channel = self._image.shape
            bytesPerLine = 3 * width
            img_Qt = QtGui.QImage(self._image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
            img_show = QtGui.QPixmap.fromImage(img_Qt)
            #show the photo
            self.setPhoto(img_show)
  

    ########################################################################################################################
    ########################################################################################################################  
    """Event Functions"""    
    ########################################################################################################################
    ########################################################################################################################
    
    
    def wheelEvent(self, event):
        #this take care of the zoom, it modifies the zoom factor if the mouse 
        #wheel is moved forward or backward by 20%
        if not self._photo.pixmap().isNull():
            move=(event.angleDelta().y()/120)
            if move > 0:
                factor = 1.2
                self._zoom += 1
            else:
                factor = 0.8
                self._zoom -= 1
                                        
            if self._zoom > 0:
                self.scale(factor, factor)
            elif self._zoom <= 0:
                self._zoom = 0
                self.fitInView()
                
                
    def mousePressEvent(self, event):
        #this function takes care of lifting (if RightClick) and relocating (if
        #a point is lifted and LeftClick) landmarks. It also verifies if the 
        #user wants to manually modify the position of the iris. In that case,
        #it opens up a new window showing only the eye (left or right) where 
        #the user can select four points around the iris
        if self._busy == True:
            event.ignore()
        elif not self._photo.pixmap().isNull():

            scenePos = self.mapToScene(event.pos())
            x_mousePos = scenePos.toPoint().x()
            y_mousePos = scenePos.toPoint().y()
            
            
            if event.button() == QtCore.Qt.RightButton:
                if self._IsMidLineVisible == True:
                    # print('Checking if Mouse is over Midline')
                    if self._IsMouseOverMidLine == True:
                        print('Moving Midline')
                        self._IsMidLineMoving = True
                        #remove the Drag option
                        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)    
                        #make the cursor a cross to facilitate localization of eye center     
                        self.setCursor(QtGui.QCursor(QtCore.Qt.SplitHCursor))
                if self._IsShapeVisible == True and self._IsMidLineMoving == False:
                    dot_removed = False
                    if self._PointToModify is None:
                        for item in self._scene.items():
                            """Following Code is for "moving" landmarks by remebering the ID of the dot removed
                                then making the next dot placed have the same ID.
                                """
                            if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                                center_of_ellipseX = item.pos().x() + item.rect().center().x()
                                center_of_ellipseY = item.pos().y() + item.rect().center().y()
                                if np.sqrt(((x_mousePos - center_of_ellipseX)**2 + (y_mousePos - center_of_ellipseY)**2)) < self._landmark_size*2:
                                    if item.rect().height() <= self._landmark_size*2:
                                        if dot_removed == False:
                                            self._scene.removeItem(item)
                                            dot_removed = True
                            
                        """Following Code is "attepmting" to track any removed IDs"""
                        try:
                            current_IDs = []
                            list_of_IDs = np.arange(1,len(self._shape)+1)
                            list_of_IDs.tolist()
                            any_missing = False
                            missing_IDs = []
                            for item in self._scene.items():
                                if isinstance(item, QtWidgets.QGraphicsSimpleTextItem):
                                    if item.text().isnumeric():
                                        current_IDs.append(item.text())
                            current_IDs = list(set(current_IDs))
                            for ID in list_of_IDs:
                                Label = str(ID)
                                if Label not in current_IDs:
                                    missing_IDs.append(Label)
                                    any_missing = True
                            if any_missing:
                                self._PointToModify = missing_IDs[0] #if multiple missing IDs, next placed will be 
                        except:
                            print('Error in finding self._PointToModify /n')
                            print('self._shape = ', self._shape)


                        if self._AddLandmarks == True and dot_removed == False:
                            point_temp = np.array([x_mousePos, y_mousePos, len(self._shape)+1])
                            point_temp = torch.from_numpy(point_temp).view(1,3)
                            self._shape = torch.cat((self._shape, point_temp), -2)
                            self.draw_dot([x_mousePos, y_mousePos, 2], str(len(self._shape)))
                            # self._numPoints +=1
                            
                        
                        elif self._AddLandmarks == False and dot_removed == False:
                            scenePos = self.mapToScene(event.pos())
                            x_mousePos = scenePos.toPoint().x()
                            y_mousePos = scenePos.toPoint().y()
                            mousePos = np.array([(x_mousePos, y_mousePos)])                   
                            distance = cdist([[self._righteye[0],self._righteye[1]],
                                            [self._lefteye[0],self._lefteye[1]]]
                                            , mousePos)
                            distance = distance[:,0]
                            #check if a landmark (including the eyes) is no more than 
                            #3 pixels away from the click location. If there is then lift that
                            #landmark from the face. If the image is taller than 1000 pixels 
                            #then the distance is 5 pixels
                            if self._scene.height() < 1000:
                                PointToModify = [i for i, j in enumerate(distance) if j <=3 ]
                            else:
                                PointToModify = [i for i, j in enumerate(distance) if j <=6 ]
                                
                            if PointToModify:
                                self._IrisToModify = PointToModify[0]
                                if self._IrisToModify == 0:
                                    #user wants to move the right eye, Both eyes have to move together 
                                    self._IsDragEyes = True
                                    self._IsDragRight = True 
                                    self._IsDragLeft = False 
                                    self._BothEyesTogether = False
             
                                elif self._IrisToModify == 1:
                                    #user wants to move the left eye, Both eyes have to move together 
                                    self._IsDragEyes = True
                                    self._IsDragRight = False 
                                    self._IsDragLeft = True 
                                    self._BothEyesTogether = False
                                
            
                                
                                #remove the Drag option
                                self.setDragMode(QtWidgets.QGraphicsView.NoDrag)    
                                #make the cursor a cross to facilitate localization of eye center     
                                self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
                                        
                                self.draw_circle(self._righteye)
                                self.draw_circle(self._lefteye) 
                                            
                    if self._PointToModify is not None and dot_removed == False:
                        for i, point in enumerate(self._shape):
                            point_ID = int(point.numpy()[2])
                            if point_ID == int(self._PointToModify):
                                self._shape[i,0] = x_mousePos
                                self._shape[i,1] = y_mousePos
                        self.draw_dot([x_mousePos, y_mousePos, 2], self._PointToModify)
                        self._PointToModify = None
                        
                    
            elif event.button() == QtCore.Qt.LeftButton:
                new_window_opened = False 
                if self._PointToModify is None:
                    for item in self._scene.items():
                        """Following Code is for "moving" landmarks by remebering the ID of the dot removed
                            then making the next dot placed have the same ID.
                            """
                        if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                            center_of_ellipseX = item.pos().x() + item.rect().center().x()
                            center_of_ellipseY = item.pos().y() + item.rect().center().y()
                            if np.sqrt(((x_mousePos - center_of_ellipseX)**2 + (y_mousePos - center_of_ellipseY)**2)) < self._landmark_size*2:
                                if item.rect().height() > self._landmark_size*2:
                                    if np.sqrt(((x_mousePos - self._lefteye[0])**2 + (y_mousePos - self._lefteye[1])**2)) < self._landmark_size*2:
                                        position = 'left'
                                        if self._lefteye_landmarks is None:
                                            self.normalize_eye_landmarks(normalize_left=True, normalize_right=False)
                                        if self._lefteye_landmarks[0,0] != self._lefteye[0]:
                                            self.normalize_eye_landmarks(normalize_left=True, normalize_right=False)
                                        temp_circle, temp_iris = get_iris_manual(self._image, self._shape, self._lefteye_landmarks, 
                                                               self._landmark_size, position)
                                        new_window_opened = True
                                        if temp_circle is not None and temp_iris is not None:
                                            self._lefteye = temp_circle
                                            self._lefteye_landmarks = temp_iris
                                            if self._points != None:
                                                self._points[1] = (self._lefteye[0], self._lefteye[1]) #Reset the interpupil line based on new eye location
                                            # print('self._lefteye = ', self._lefteye,
                                            #       'self._lefteye_landmarks = ', self._lefteye_landmarks)
                                    elif np.sqrt(((x_mousePos - self._righteye[0])**2 + (y_mousePos - self._righteye[1])**2)) < self._landmark_size*2:
                                        position = 'right'
                                        if self._righteye_landmarks is None:
                                            self.normalize_eye_landmarks(normalize_left=False, normalize_right=True)
                                        if self._righteye_landmarks[0,0] != self._righteye[0]:
                                            self.normalize_eye_landmarks(normalize_left=False, normalize_right=True)
                                        temp_circle, temp_iris = get_iris_manual(self._image, self._shape, self._righteye_landmarks, 
                                                               self._landmark_size, position)
                                        new_window_opened = True
                                        if temp_circle is not None and temp_iris is not None:
                                            self._righteye = temp_circle
                                            self._righteye_landmarks = temp_iris
                                            if self._points != None:
                                                self._points[0] = (self._righteye[0], self._righteye[1]) #Reset the interpupil line based on new eye location
                                            # print('self._righteye = ', self._righteye,
                                            #       'self._righteye_landmarks = ', self._righteye_landmarks)
                                    self.update_shape()        
                        
                    
                if new_window_opened != True:
                    self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)
                            
        QtWidgets.QGraphicsView.mousePressEvent(self, event)
    
        
    def mouseReleaseEvent(self, event):     
        #this function defines what happens when you release the mouse click 
        
        #if the eye is being moved, stop moving it
        self._IsDragEyes = False
        self._IsDragLeft = False
        self._IsDragRight = False
        self._BothEyesTogether = False
        self._IsMidLineMoving = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        
        self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)

   
    def mouseDoubleClickEvent(self, event):
   
        #if the user double click on one of the iris the both iris will be able to move together
        if self._busy == True:
            event.ignore()
        elif event.button() == QtCore.Qt.RightButton:
            event.accept()
            if self._shape is not None:
                scenePos = self.mapToScene(event.pos())
                x_mousePos = scenePos.toPoint().x()
                y_mousePos = scenePos.toPoint().y()
                mousePos = np.array([(x_mousePos, y_mousePos)])                   
                distance = cdist([[self._righteye[0],self._righteye[1]],
                                [self._lefteye[0],self._lefteye[1]]]
                                , mousePos)
                distance = distance[:,0]
                #check if a landmark (including the eyes) is no more than 
                #3 pixels away from the click location. If there is then lift that
                #landmark from the face. If the image is taller than 1000 pixels 
                #then the distance is 5 pixels
                if self._scene.height() < 1000:
                    PointToModify = [i for i, j in enumerate(distance) if j <=3 ]
                else:
                    PointToModify = [i for i, j in enumerate(distance) if j <=6 ]
                    
                if PointToModify:
                    self._IrisToModify = PointToModify[0]
                    if self._IrisToModify == 0:
                        #user wants to move the right eye, Both eyes have to move together 
                        self._IsDragEyes = True
                        self._IsDragRight = True 
                        self._IsDragLeft = False 
                        self._BothEyesTogether = True
 
                    elif self._IrisToModify == 1:
                        #user wants to move the left eye, Both eyes have to move together 
                        self._IsDragEyes = True
                        self._IsDragRight = False 
                        self._IsDragLeft = True 
                        self._BothEyesTogether = True
                    

                    
                    #remove the Drag option
                    self.setDragMode(QtWidgets.QGraphicsView.NoDrag)    
                    #make the cursor a cross to facilitate localization of eye center     
                    self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

                    
        else:
            event.ignore()
        try:  
            self.draw_circle(self._righteye)
            self.draw_circle(self._lefteye) 
        except:
            pass
        QtWidgets.QGraphicsView.mouseDoubleClickEvent(self, event)
                

    
    def mouseMoveEvent(self, event):
        #this function takes care of the pan (move around the photo) and draggin of the eyes
        
        if self._AdjustingMidLine == True:
                
            #First test if the cursor needs to indicate whether it is located at midline
            #to signify it can be moved if clicked only if the adjustment mode is on
            scenePos = self.mapToScene(event.pos())
            x_mousePos = scenePos.toPoint().x()
            y_mousePos = scenePos.toPoint().y()
            if self._IsMidLineVisible == True:
                try:
                    x1, y1 = self._points[3]
                    x2, y2 = self._points[5]
                    if x2-x1 == 0:
                        print('x2-x1 == 0')
                        if abs(x_mousePos-x1) < 5*self._landmark_size:
                            self.setCursor(QtGui.QCursor(QtCore.Qt.SplitHCursor))
                            self._IsMouseOverMidLine = True
                        else:
                            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                            self._IsMouseOverMidLine = False
                    else:
                        m = (y2-y1)/(x2-x1) #finds slope of midline
                        delta_y_1 = m*(0-x1) #finds difference between y coordinates for x1 and y intercept
                        b = y1 + delta_y_1
                        x_ML = (y_mousePos-b)/m
                        if abs(x_mousePos-x_ML) < 5*self._landmark_size:
                            self.setCursor(QtGui.QCursor(QtCore.Qt.SplitHCursor))
                            self._IsMouseOverMidLine = True
                        else:
                            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                            self._IsMouseOverMidLine = False
                except:
                    self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
                    
            if self._IsMidLineMoving == True:
                event.accept()
                
                scenePos = self.mapToScene(event.pos())
                x_mousePos = scenePos.toPoint().x()
                y_mousePos = scenePos.toPoint().y()
                
                x0,y0 = self._points[2]
                x1, y1 = self._points[3]
                x2, y2 = self._points[5]
                
                
                if x2-x1 == 0:
                    x_ML = x1 #The x value is the same at all values of y on the Midline
                else:
                    m = (y2-y1)/(x2-x1) #finds slope of midline
                    delta_y_1 = m*(0-x1) #finds difference between y coordinates for x1 and y intercept
                    b = y1 + delta_y_1
                    x_ML = (y_mousePos-b)/m
                
                delta_x = x_mousePos - x_ML
                
                new_x0 = x0 + delta_x
                new_x1 = x1 + delta_x
                new_x2 = x2 + delta_x
                
                self._points[2] = (new_x0,y0)
                self._points[3] = (new_x1,y1)
                self._points[4] = (new_x0,y0)
                self._points[5] = (new_x2,y2)
                
                self.update_shape()
            else:
                event.ignore()
            
    
        #if _IsDragEyes == true then the user wants to change the position of the eyes
        if self._IsDragEyes == True:
            event.accept()
            
            scenePos = self.mapToScene(event.pos())
            x_mousePos = scenePos.toPoint().x()
            y_mousePos = scenePos.toPoint().y()
            
            if self._points == None:
                self.toggle_midLine()
                self.toggle_midLine()
            
            if self._BothEyesTogether == True:
                if self._IsDragLeft == True:
                    #find how much the mouse moved the eye                    
                    delta_x = x_mousePos - self._lefteye[0]
                    delta_y = y_mousePos - self._lefteye[1]
                    new_right_x = self._righteye[0] + delta_x
                    new_right_y = self._righteye[1] + delta_y
                    #update the iris info
                    self._lefteye[0] = x_mousePos
                    self._lefteye[1] = y_mousePos
                    self._righteye[0] = new_right_x
                    self._righteye[1] = new_right_y
                    self.normalize_eye_landmarks(normalize_left=True, normalize_right=True)
                    self._points[0] = (self._righteye[0], self._righteye[1]) #Reset the interpupil line based on new eye location
                    self._points[1] = (self._lefteye[0], self._lefteye[1]) #Reset the interpupil line based on new eye location
                
                elif self._IsDragRight == True:
                    #find how much the mouse moved the eye                    
                    delta_x = x_mousePos - self._righteye[0]
                    delta_y = y_mousePos - self._righteye[1]
                    new_left_x = self._lefteye[0] + delta_x
                    new_left_y = self._lefteye[1] + delta_y
                    #find how much the mouse moved the eye                    
                    self._lefteye[0] = new_left_x
                    self._lefteye[1] = new_left_y
                    self._righteye[0] = x_mousePos
                    self._righteye[1] = y_mousePos
                    self.normalize_eye_landmarks(normalize_left=True, normalize_right=True)
                    self._points[0] = (self._righteye[0], self._righteye[1]) #Reset the interpupil line based on new eye location
                    self._points[1] = (self._lefteye[0], self._lefteye[1]) #Reset the interpupil line based on new eye location
            elif self._BothEyesTogether == False:
                if self._IsDragLeft == True:
                    #update the iris info
                    self._lefteye[0] = x_mousePos
                    self._lefteye[1] = y_mousePos
                    self.normalize_eye_landmarks(normalize_left=True, normalize_right=False)
                    self._points[1] = (self._lefteye[0], self._lefteye[1]) #Reset the interpupil line based on new eye location
                elif self._IsDragRight == True:
                    self._righteye[0] = x_mousePos
                    self._righteye[1] = y_mousePos
                    self.normalize_eye_landmarks(normalize_left=False, normalize_right=True)
                    self._points[0] = (self._righteye[0], self._righteye[1]) #Reset the interpupil line based on new eye location
            self.update_shape()
        
        else:
            event.ignore()
            
            

        QtWidgets.QGraphicsView.mouseMoveEvent(self, event)
    
    ########################################################################################################################
    ########################################################################################################################       
    """Draw Functions"""
    ########################################################################################################################
    ########################################################################################################################
    
    
    def draw_dot(self, CircleInformation, ID):
        
        """Setting a standard circle size"""
        radius = self._landmark_size
        CircleInformation[2] = radius
        
        
        #this function draws an circle with specific center and radius 
        
        Ellipse = QtWidgets.QGraphicsEllipseItem(0,0,CircleInformation[2]*2,CircleInformation[2]*2)
        #Label = QtWidgets.QGraphicsSimpleTextItem(str(ID), parent=Ellipse)
        #ellipse will be colored based on ID
        if ID == '':
            #checks if the point is the unmarks eye landmarks
            pen = QtGui.QPen(self._iris_color)
            brush = QtGui.QBrush(self._iris_color)
        else:
            if int(ID) == 37 or (int(ID) >= 40 and int(ID) <= 43) or int(ID) == 43 or (int(ID) >= 46 and int(ID) <= 48):
                #checks if the dot is in the lower lid of the eye
                pen = QtGui.QPen(self._landmark_color_lower_lid)
                brush = QtGui.QBrush(self._landmark_color_lower_lid) 
            elif int(ID) == 61 or (int(ID) >= 65 and int(ID) <= 68):
                #checks if the dot is in the lower inner lip
                pen = QtGui.QPen(self._landmark_color_lower_lips)
                brush = QtGui.QBrush(self._landmark_color_lower_lips)
            else:
                pen = QtGui.QPen(self._landmark_color)
                brush = QtGui.QBrush(self._landmark_color) 
                
            
        #set the ellipse line width according to the image size
        if self._landmark_size > 0.5:
            if self._scene.height() < 1000:
                pen.setWidth(1)
            else:
                pen.setWidth(3)
        
        #Sets color    
        Ellipse.setPen(pen)      
        #if I want to fill the ellipse i should do this: 
        Ellipse.setBrush(brush)
        
        #this is the position of the top-left corner of the ellipse.......
        Ellipse.setPos(CircleInformation[0]-CircleInformation[2],CircleInformation[1]-CircleInformation[2])
        Ellipse.setTransform(QtGui.QTransform())        
        self._scene.addItem(Ellipse)
        
        #Adds Label to the Circle

        Label = QtWidgets.QGraphicsSimpleTextItem('', parent=Ellipse)
        #Check whether to adjust text size or not
        if self._landmark_size > 3:
            Font = Label.font()
            Font.setPixelSize(max(3*self._landmark_size, 1))
            Label.setFont(Font)
        elif self._landmark_size < 1:
            Font = Label.font()
            Font.setPointSize(max(self._landmark_size*10, 1))
            Label.setFont(Font)
        # print('Label.font().pixelSize() = ', Label.font().pixelSize())
        # print('Label.font().pointSize() = ', Label.font().pointSize())
        Label.setBrush(self._label_color)
        Label.setText(str(ID))
        # self._scene.addItem(Label)
    
        
    def draw_circle(self, CircleInformation):
        """This function draws an circle as well as a dot in the center with specific center and radius""" 
        
        Circle = QtWidgets.QGraphicsEllipseItem(0,0,CircleInformation[2]*2,CircleInformation[2]*2)
        pen = QtGui.QPen(self._iris_color)
        brush = QtGui.QBrush(self._iris_color) 
        #set the ellipse line width according to the image size
        if self._landmark_size > 0.5:
            if self._scene.height() < 1000:
                pen.setWidth(1)
            else:
                pen.setWidth(3)
        Circle.setPen(pen)      

        #this is the position of the top-left corner of the ellipse.......
        Circle.setPos(CircleInformation[0]-CircleInformation[2],CircleInformation[1]-CircleInformation[2])
        Circle.setTransform(QtGui.QTransform())        
        self._scene.addItem(Circle)

        """Adding Dot in center"""
        radius = self._landmark_size*2 #sets dot to be twice the size as a landmark
        Ellipse = QtWidgets.QGraphicsEllipseItem(0,0,radius*2,radius*2)
        #Sets color    
        Ellipse.setPen(pen)      
        #if I want to fill the ellipse i should do this: 
        Ellipse.setBrush(brush)
        
        #this is the position of the top-left corner of the ellipse.......
        Ellipse.setPos(CircleInformation[0]-radius,CircleInformation[1]-radius)
        Ellipse.setTransform(QtGui.QTransform())        
        self._scene.addItem(Ellipse)
    
    
    def draw_line(self, LineInformation, ID=None):
        point_1 = np.array(LineInformation[0])
        point_2 = np.array(LineInformation[1])
        Line = QtWidgets.QGraphicsLineItem(point_1[0],point_1[1],point_2[0],point_2[1])
        pen = QtGui.QPen(self._midLine_color)
        #set the line width according to the image size
        if self._scene.height() < 1000:
            pen.setWidth(1)
        else:
            pen.setWidth(3)
        
        Line.setPen(pen)
        
        self._scene.addItem(Line)
        if ID:
            #Adds Label to the Circle
            # print('Adding Label to Cirle')
            degree = u'\u00b0'
            ID = str(ID) + degree
            Label = QtWidgets.QGraphicsSimpleTextItem(str(ID), parent=Line)
            #Check whether to adjust text size or not
            if self._landmark_size > 3:
                Font = Label.font()
                Font.setPixelSize(3*self._landmark_size)
                Label.setFont(Font)
            Label.setBrush(self._NLF_color)
            Label.setPos(point_1[0],point_1[1])
            self._scene.addItem(Label)
    

    ########################################################################################################################
    ########################################################################################################################
    """Visualization Functions"""
    ########################################################################################################################
    ########################################################################################################################
    
    
    def show_Facial_Landmarks(self, Facial_landmarks, left_eye, right_eye, lefteye_landmarks, righteye_landmarks, boundingbox):
        self._shape = Facial_landmarks
        self._boundingbox = boundingbox
        self._lefteye = left_eye
        self._righteye = right_eye
        self._lefteye_landmarks = lefteye_landmarks
        self._righteye_landmarks = righteye_landmarks
        # print('self._lefteye = ', self._lefteye,
        #       '\n self._righteye = ', self._righteye,
        #       '\n self._lefteye_landmarks = ', self._lefteye_landmarks,
        #       '\n self._righteye_landmarks = ', self._righteye_landmarks)
        self.update_shape()
        self.dots_shown.emit()
    
    
    def toggle_dots(self):
        if self._IsShapeVisible == True:
            self.remove_dots()
            self._IsShapeVisible = False
        elif self._IsShapeVisible == False:
            self._IsShapeVisible = True
            self.update_shape()
        else:
            print('Toggle Failed')

    
    def show_iris(self):
        self.draw_circle(self._lefteye)
        self.draw_circle(self._righteye)
        # self.draw_dot(self._lefteye, '')
        # self.draw_dot(self._righteye, '')
        
    def show_iris_landmarks(self, lefteye_landmarks, righteye_landmarks):
        """This function is to display dots that represent the landmarks 
        of the eyes found in the eye model"""
        self._lefteye_landmarks = lefteye_landmarks
        self._righteye_landmarks = righteye_landmarks
        #Since the landmarks should be the same size, only one for loop needs to be used
        try:
            if ( self._lefteye_landmarks != np.array([[0,0],[0,0],[0,0],[0,0],[0,0]]) 
            and self._righteye_landmarks != np.array([[0,0],[0,0],[0,0],[0,0],[0,0]]) ):
                for i in range(5):
                    left_point = [self._lefteye_landmarks[i,0], self._lefteye_landmarks[i,1], 1]
                    right_point = [self._righteye_landmarks[i,0], self._righteye_landmarks[i,1], 1]
                    self.draw_dot(left_point, '')
                    self.draw_dot(right_point, '')
        except:
            print('Error in show_iris_landmarks')
        
    def toggle_midLine(self):
        if self._IsMidLineVisible == False and self._points == None:
            try:
                self._points = estimate_lines(self._image, self._lefteye, self._righteye)
                self.draw_line((self._points[0], self._points[1]))
                self.draw_line((self._points[2], self._points[3]))
                self.draw_line((self._points[4], self._points[5]))
                self._IsMidLineVisible = True
            except:
                print('Error in toggle_midline, estimate_lines failed')
        elif self._IsMidLineVisible == False and self._points != None:
            self.draw_line((self._points[0], self._points[1]))
            self.draw_line((self._points[2], self._points[3]))
            self.draw_line((self._points[4], self._points[5]))
            self._IsMidLineVisible = True
            
        elif self._IsMidLineVisible == True:
            for item in self._scene.items():
                if isinstance(item, QtWidgets.QGraphicsLineItem):
                    self._scene.removeItem(item)
            self._IsMidLineVisible = False
            if self._IsNLFVisible == True:
                self._IsNLFVisible = False
                self.show_NLF()
                
        
        else:
            pass
    
    
    def update_midLine(self):
        if self._IsMidLineVisible == True:
            for item in self._scene.items():
                    if isinstance(item, QtWidgets.QGraphicsLineItem):
                        self._scene.removeItem(item)
                        
            self.draw_line((self._points[0], self._points[1]))
            self.draw_line((self._points[2], self._points[3]))
            self.draw_line((self._points[4], self._points[5]))
    
            
    def show_NLF(self):
        if len(self._shape) < 76:
            print('Not enough landmarks')
        else:
            if self._IsNLFVisible == False:
                if self._IsMidLineVisible == False:
                    #This makes sure the midline points exsist
                    self._points = estimate_lines(self._image, self._lefteye, self._righteye)
                self._NLF_points, self._NLF_angles = find_NLF(self._shape, self._points)
                if self._NLF_angles[0] != 0:
                    self.draw_line((self._NLF_points[0], self._NLF_points[1]), ID=self._NLF_angles[0])
                if self._NLF_angles[1] != 0:
                    self.draw_line((self._NLF_points[2], self._NLF_points[3]), ID=self._NLF_angles[1])
                self._IsNLFVisible = True
            elif self._IsNLFVisible == True:
                #Doing this twice removes all lines then adds only the Midline back
                self.remove_lines() #Removes all lines
                self.update_midLine() #Then checks if the midline needs to be added back
                self._IsNLFVisible = False
    
    ########################################################################################################################
    ########################################################################################################################
    """Adjustment Functions"""
    ########################################################################################################################
    ########################################################################################################################
    
    
    def matchEyesRtoL(self):
        self._lefteye[2] = self._righteye[2]
        self.normalize_eye_landmarks(normalize_left=True, normalize_right=False)
        self.update_shape()
    
    def matchEyesLtoR(self):
        self._righteye[2] = self._lefteye[2]
        self.normalize_eye_landmarks(normalize_left=False, normalize_right=True)
        self.update_shape()
    
    
    def normalize_eye_landmarks(self, normalize_left=True, normalize_right=True):
        """The following is adjusting the eye landmarks to match the new eye location"""
        if self._lefteye_landmarks is None:
            self._lefteye_landmarks = np.array([[0,0],[0,0],[0,0],[0,0],[0,0]])
            
        if self._righteye_landmarks is None:
            self._righteye_landmarks = np.array([[0,0],[0,0],[0,0],[0,0],[0,0]])
            
        
        if normalize_left == True:
            #Point 0: Center
            self._lefteye_landmarks[0,0] = self._lefteye[0]
            self._lefteye_landmarks[0,1] = self._lefteye[1]
            #Point 1: Right or "East" Point (x_center + radius, y_center)
            self._lefteye_landmarks[1,0] = self._lefteye[0] + self._lefteye[2]
            self._lefteye_landmarks[1,1] = self._lefteye[1]
            #Point 2: Above or "North" Point (x_center, y_center - radius)
            self._lefteye_landmarks[2,0] = self._lefteye[0] 
            self._lefteye_landmarks[2,1] = self._lefteye[1] - self._lefteye[2] #Since y increases as it goes down the radius is subtracted not added
            #Point 3: Right or "East" Point (x_center - radius, y_center)
            self._lefteye_landmarks[3,0] = self._lefteye[0] - self._lefteye[2]
            self._lefteye_landmarks[3,1] = self._lefteye[1]
            #Point 4: Right or "East" Point (x_center, y_center + radius)
            self._lefteye_landmarks[4,0] = self._lefteye[0] 
            self._lefteye_landmarks[4,1] = self._lefteye[1] + self._lefteye[2]
            
        if normalize_right == True:
            #Point 0: Center
            self._righteye_landmarks[0,0] = self._righteye[0]
            self._righteye_landmarks[0,1] = self._righteye[1]
            #Point 1: Right or "East" Point (x_center + radius, y_center)
            self._righteye_landmarks[1,0] = self._righteye[0] + self._righteye[2]
            self._righteye_landmarks[1,1] = self._righteye[1]
            #Point 2: Above or "North" Point (x_center, y_center - radius)
            self._righteye_landmarks[2,0] = self._righteye[0] 
            self._righteye_landmarks[2,1] = self._righteye[1] - self._righteye[2] #Since y increases as it goes down the radius is subtracted not added
            #Point 3: Right or "East" Point (x_center - radius, y_center)
            self._righteye_landmarks[3,0] = self._righteye[0] - self._righteye[2]
            self._righteye_landmarks[3,1] = self._righteye[1]
            #Point 4: Right or "East" Point (x_center, y_center + radius)
            self._righteye_landmarks[4,0] = self._righteye[0] 
            self._righteye_landmarks[4,1] = self._righteye[1] + self._righteye[2]
    
    
    def toggle_adjustingMidLine(self):
        if self._AdjustingMidLine == True:
            self._AdjustingMidLine = False
            
        elif self._AdjustingMidLine == False:
            self._AdjustingMidLine = True
            self.update_shape()
            
        else:
            pass
        print('self._AdjustingMidLine = ', self._AdjustingMidLine)
    
        
    def midLine_Laterial_move_left(self):
        if self._AdjustingMidLine == True:
            self.adjust_midLine(-1,0)
    
    def midLine_Laterial_move_right(self):
        if self._AdjustingMidLine == True:
            self.adjust_midLine(1,0)
    
    def midLine_Angular_move_clockwise(self):
        if self._AdjustingMidLine == True:
            self.adjust_midLine(0,-1/200)
    
    def midLine_Angular_move_counterclockwise(self):
        if self._AdjustingMidLine == True:
            self.adjust_midLine(0,1/200)
    
    
    def adjust_midLine(self, laterial_change, angular_change):
        h, w, _ = self._image.shape
        (x_1,y_1) = self._points[0]
        (x_2,y_2) = self._points[1]
        (x_m,y_m) = self._points[2]
        (x_p1,y_p1) = self._points[3]
        (x_p2,y_p2) = self._points[5]
        
        #find the point in the middle of the line
        x_m_new = x_m + laterial_change #this addition causes the movement left   
        m = (y_2-y_1)/(x_2-x_1)   
        y_m_new = (y_1+m*(x_m-x_1)) #calculates new y_m based on movement in x_m
        
        x_m_new = int(round(x_m_new,0))
        y_m_new = int(round(y_m_new,0))
        
        if laterial_change != 0:
            delta_x = x_m_new - x_m
            delta_y = y_m_new - y_m
            
            (x_p1,y_p1) = self._points[3]
            x_p1_new = x_p1 + delta_x
            y_p1_new = y_p1 + delta_y
            
            (x_p2,y_p2) = self._points[5]
            x_p2_new = x_p2 + delta_x
            y_p2_new = y_p2 + delta_y
            
        if angular_change != 0:
            if (x_p2-x_p1) == 0: #to insure it doesn't attempt to divide by zero
                angle = np.pi/2 + angular_change #this addition causes the movement
            else:
                m_p = (y_p2-y_p1)/(x_p2-x_p1)
                angle = np.arctan(m_p) + angular_change #this addition causes the movement
            
            x_p1_new = int(round(x_m+0.5*h*np.cos(angle)))
            y_p1_new = int(round(y_m+0.5*h*np.sin(angle)))
            
            x_p2_new = int(round(x_m-0.5*h*np.cos(angle)))
            y_p2_new = int(round(y_m-0.5*h*np.sin(angle)))     
            
        self._points = [(x_1,y_1), (x_2,y_2), (x_m_new, y_m_new), (x_p1_new ,y_p1_new), (x_m_new, y_m_new), (x_p2_new, y_p2_new)]
        self.update_midLine()   
        
        
    def reset_midline(self):
        self._points = estimate_lines(self._image, self._lefteye, self._righteye)
        self.update_shape()
        

    def toggle_add_dots(self):
        if self._AddLandmarks == False:
            self._AddLandmarks = True
            self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
        elif self._AddLandmarks == True:
            self._AddLandmarks = False
            self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
            
        else:
            pass
    
    
    def removeDot(self):
        try:
            max_ID = max(self._shape[:, 2])
            self._shape = self._shape[self._shape[:, 2] <  max_ID]
            self.update_shape()
        except:
            print('No more dots')


    ########################################################################################################################   
    ########################################################################################################################    
    """Update Functions"""
    ########################################################################################################################
    ########################################################################################################################
    
    
    def update_shape(self):
        self.remove_dots()
        self.remove_lines()
        try:
            for i in range(len(self._shape)):
                point = [self._shape[i,0], self._shape[i,1], 1]
                self.draw_dot(point, int(self._shape.numpy()[i,2]))
            if self._lefteye != None and self._righteye != None:
                self.show_iris()
                # self.show_iris_landmarks(self._lefteye_landmarks, self._righteye_landmarks)
            self.update_visualization() 
        except:
            print('Error in update_shape')
            # print('self._shape = ', self._shape)
    
            
    def update_visualization(self):
        # print('update_visualization')
        #Checks whether the user has turned on the NLF button
        if self._IsShapeVisible == False:
            # print('Hiding Dots')
            self.remove_dots()
        
        #Checks whether the user has turned on the NLF button
        if self._IsNLFVisible == True:
            # print('Showing NLF')
            if len(self._shape) < 76:
                print('Not enough landmarks')
            else:
                self._IsNLFVisible = False
                self.show_NLF()
                
            
        #Checks whether the user has turned on the Midline button is turned on
        if self._IsMidLineVisible == True:
            # print('Showing Midline')
            self._IsMidLineVisible = False
            self.toggle_midLine()


    def remove_dots(self):
        for item in self._scene.items():
            if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                self._scene.removeItem(item)


    def remove_lines(self):
        for item in self._scene.items():
            if isinstance(item, QtWidgets.QGraphicsLineItem):
                    self._scene.removeItem(item)


    def clear_scene(self):
        for item in self._scene.items():
            if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                self._scene.removeItem(item)
            if isinstance(item, QtWidgets.QGraphicsLineItem):
                    self._scene.removeItem(item)

    def reset_save_variables(self):
        self._savedShape = False
        
    def get_midline(self):
        try:
            self._points = estimate_lines(self._image, self._lefteye, self._righteye)    
        except:
            print('Error in get_midline')  