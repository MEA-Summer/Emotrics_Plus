# -*- coding: utf-8 -*-
"""
Created on Wed May 26 11:35:23 2021
@author: lukem
"""

from PyQt5 import QtWidgets, QtCore, QtGui
import numpy as np
from Utilities import find_circle_from_points

"""
This window show the eye and allows the user to select 4 points around the iris, 
it then fits a circle around these points. The user can accept the circle or 
re-initialize the point selection
"""


class ProcessEye(QtWidgets.QDialog):
    
    def __init__(self, image=None, iris_landmarks=None):
        super().__init__()
        self.setWindowTitle('Eye Selection')
        self.setGeometry(100, 100, 1200, 800)
        self._circle = None
        self._shape = None
        self._image = image
        self._iris_landmarks = iris_landmarks
        self.label_title = QtWidgets.QLabel()
        self.label_title.setText('Please click on four points around the iris')
        #self.label_title.setWordWrap(True) 
        self.label_title.setMaximumWidth(500)
        self.view = View(self)
        if self._image is not None:
            self.view._image = self._image
            self.view.set_picture()
            self.view._shape = self._iris_landmarks
            self.view._shape_orig = self._iris_landmarks
            self.view.update_shape()
        self.buttonReset = QtWidgets.QPushButton('Clear', self)
        self.buttonReset.clicked.connect(self.view.handleClearView)
        
        self.buttonDone = QtWidgets.QPushButton('Done',self)
        self.buttonDone.clicked.connect(self.handleReturn)
        
        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(self.label_title,0,0,1,2)
        layout.addWidget(self.view,1,0,1,2)
        layout.addWidget(self.buttonDone,2,0,1,1)
        layout.addWidget(self.buttonReset,2,1,1,1)
        
        
                
    def handleReturn(self):
        self._circle = self.view._circle
        self._shape = self.view._shape
        self.close()
            
class View(QtWidgets.QGraphicsView):
    
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        
        self._scene = QtWidgets.QGraphicsScene(self)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._scene.addItem(self._photo)
        self.setScene(self._scene)
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        
        #Variable where landmarks are saved
        self._shape = None
        self._shape_orig = None
        self._landmark_color = QtCore.Qt.red
        self._landmark_size = None
        self._PointToModify = None
        self._PointToModify_pos = None
        self._dragging_eye = False
        
        #this counts the number of click, if it reaches 4 then it stops accepting 
        #more points and draws the cirlce
        self._counter = 0 
        self._circle = None
        #this accomulates the position of the clicks
        self._mouse_pos= np.array([]).reshape(0,2)
        self._image = None
#        pen = QtGui.QPen(QtCore.Qt.green)
#        Rec= QtCore.QRectF(150, 150,300,300)
#        self.scene().addEllipse(Rec, pen)


    def update_shape(self):
        """This function is used to show the landmarks on the scene
        and to update the scene when the landmarks are changed"""
        self.remove_dots()
        for i in range(len(self._shape)):
            x = self._shape[i,0]
            y = self._shape[i,1]
            self.draw_dot(x, y)
        self.process_circle()


    def remove_dots(self):
        for item in self._scene.items():
            if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                self._scene.removeItem(item)

    
    def draw_dot(self, x, y):
        if self._landmark_size == None:
            self._landmark_size = max(int(self._scene.width()*(1/300)),1)
        ellipse_w = 2*self._landmark_size #Width of QGraphicsEllipseItem
        ellipse_h = 2*self._landmark_size #Height of QGraphicsEllipseItem
        ellipse_x = x - ellipse_w/2 #X of QGraphicsEllipseItem (i.e.: X value of top left in QRect)
        ellipse_y = y - ellipse_h/2 #Y of QGraphicsEllipseItem (i.e.: Y value of top left in QRect)
        
        Ellipse = QtWidgets.QGraphicsEllipseItem(ellipse_x, ellipse_y, ellipse_w, ellipse_h)
        # Ellipse.setPos(ellipse_x, ellipse_y)
        pen = QtGui.QPen(self._landmark_color)
        brush = QtGui.QBrush(self._landmark_color)
        #Sets color    
        Ellipse.setPen(pen)      
        #if I want to fill the ellipse i should do this: 
        Ellipse.setBrush(brush)
        Ellipse.setTransform(QtGui.QTransform())        
        self._scene.addItem(Ellipse)


    def find_radius(self, center, points):
        """This function transforms the the landmarks of the iris
        in to center (x, y) and radius"""    
        distance_sum = 0
        for i, point in enumerate(points):
            distance = np.sqrt(((center[0] - points[i,0])**2 + (center[1] - points[i,1])**2))
            distance_sum = distance_sum + distance
            
        radius = distance_sum/4
        return radius

         
    def process_circle(self):
        center = self._shape[0,:]
        points = self._shape[1:,:]
        radius = self.find_radius(center, points)
        self._circle = [center[0], center[1], radius]      
        
        Ellipse = QtWidgets.QGraphicsEllipseItem(0,0,self._circle[2]*2,self._circle[2]*2)
        #ellipse will be green
        pen = QtGui.QPen(QtCore.Qt.green)
        Ellipse.setPen(pen)      
        #if I want to fill the ellipse i should do this:
        #brush = QtGui.QBrush(QtCore.Qt.green) 
        #Ellipse.setPen(brush)
        
        #this is the position of the top-left corner of the ellipse.......
        Ellipse.setPos(self._circle[0]-self._circle[2], self._circle[1]-self._circle[2])
        Ellipse.setTransform(QtGui.QTransform())        
        self._scene.addItem(Ellipse)


    def normalize_landmarks(self):
        """This function resets all landmarks based on the current circle parameter.
        This makes all the landmarks perfectly vertical and horizontal."""
        #Point 1: Right or "East" Point (x_center + radius, y_center)
        self._shape[1,0] = self._circle[0] + self._circle[2]
        self._shape[1,1] = self._circle[1]
        #Point 2: Above or "North" Point (x_center, y_center - radius)
        self._shape[2,0] = self._circle[0] 
        self._shape[2,1] = self._circle[1] - self._circle[2] #Since y increases as it goes down the radius is subtracted not added
        #Point 3: Right or "East" Point (x_center - radius, y_center)
        self._shape[3,0] = self._circle[0] - self._circle[2]
        self._shape[3,1] = self._circle[1]
        #Point 4: Right or "East" Point (x_center, y_center + radius)
        self._shape[4,0] = self._circle[0] 
        self._shape[4,1] = self._circle[1] + self._circle[2]
        
        
    def mousePressEvent(self,event):
        
        if event.button() == QtCore.Qt.LeftButton:
            """A left click is for "lifting" a dot and/or placing it back done"""
            scenePos = self.mapToScene(event.pos())
            x_mousePos = scenePos.toPoint().x()
            y_mousePos = scenePos.toPoint().y()
            # print('Mouse clicked')
            dot_removed = False
            if self._PointToModify is None:
                for item in self._scene.items():
                    """Following Code is for "moving" landmarks by remebering the ID of the dot removed
                        then making the next dot placed have the same ID.
                        """
                    if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                        center_of_ellipseX = item.rect().x() + item.rect().width()/2
                        center_of_ellipseY = item.rect().y() + item.rect().height()/2
                        if np.sqrt(((x_mousePos - center_of_ellipseX)**2 + (y_mousePos - center_of_ellipseY)**2)) < self._landmark_size*2:
                            if item.rect().height() <= self._landmark_size*2:
                                if dot_removed == False:
                                    self._scene.removeItem(item)
                                    dot_removed = True
                                    self._PointToModify_pos = [center_of_ellipseX, center_of_ellipseY]
                if dot_removed == True:
                    for i, point in enumerate(self._shape):
                        if point[0] == self._PointToModify_pos[0] and point[1] == self._PointToModify_pos[1]:
                            self._PointToModify = i
            else:
                #Makes sure center of ellipse is where the mouse is pressed
                center_of_ellipseX = x_mousePos  
                center_of_ellipseY = y_mousePos 
                #Saving new dot
                self._shape[self._PointToModify,0] = center_of_ellipseX
                self._shape[self._PointToModify,1] = center_of_ellipseY
                self.update_shape()
                #Resets PointToModify
                self._PointToModify = None
                self._PointToModify_pos = None
        
        if event.button() == QtCore.Qt.RightButton:
            """A right click is for "dragging" the entire eye 
            which will cause all landmarks to alter.
            Each landmark will be move directly above, below, left, and right 
            with a distance of the current radius. The center will be directly under the mouse
            and will stop moving when the button is released"""
            scenePos = self.mapToScene(event.pos())
            x_mousePos = scenePos.toPoint().x()
            y_mousePos = scenePos.toPoint().y()
            for item in self._scene.items():
                if isinstance(item, QtWidgets.QGraphicsEllipseItem):
                    center_of_ellipseX = item.rect().x() + item.rect().width()/2
                    center_of_ellipseY = item.rect().y() + item.rect().height()/2
                    if np.sqrt(((x_mousePos - center_of_ellipseX)**2 + (y_mousePos - center_of_ellipseY)**2)) < self._landmark_size*2:
                        if item.rect().height() <= self._landmark_size*2:
                            self._dragging_eye = True
                            self.setCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
                            self.normalize_landmarks()
                            self.update_shape()
                            
    
        QtWidgets.QGraphicsView.mousePressEvent(self, event)


    def mouseMoveEvent(self, event):
        """This function handles dragging the eye and updating the scene
        as the mouse is moving"""
        if self._dragging_eye == True:
            scenePos = self.mapToScene(event.pos())
            x_mousePos = scenePos.toPoint().x()
            y_mousePos = scenePos.toPoint().y()
            self._shape[0,0] = x_mousePos
            self._shape[0,1] = y_mousePos
            self._circle[0] = x_mousePos
            self._circle[1] = y_mousePos
            self.normalize_landmarks()
            self.update_shape()


    def mouseReleaseEvent(self,event):
        """This function handles stopping the dragging mode"""
        self._dragging_eye = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        
        QtWidgets.QGraphicsView.mouseReleaseEvent(self, event)
        
        
    def set_picture(self):
        image = self._image.copy()
        height, width, channel = image.shape
        bytesPerLine = 3 * width
        img_Qt = QtGui.QImage(image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        img_show = QtGui.QPixmap.fromImage(img_Qt)
        self._photo = QtWidgets.QGraphicsPixmapItem()
        self._photo.setPixmap(img_show)   
        self._scene.addItem(self._photo)
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        self.fitInView(rect)
        self.setSceneRect(rect)
            
    def resizeEvent(self, event):
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        self.fitInView(rect)
        self.setSceneRect(rect)
        
    def handleClearView(self):
        self._shape = self._shape_orig
        self.update_shape()
        

        

if __name__ == '__main__':

    import sys
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
    
    GUI = ProcessEye()
    #GUI.resize(640, 480)
    GUI.show()
    sys.exit(app.exec_())            
        