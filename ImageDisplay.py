# -*- coding: utf-8 -*-
"""
Created on Fri Jul 23 00:56:37 2021

@author: lukem
"""
from PyQt5 import QtWidgets, QtGui, QtCore


class ImageDisplay(QtWidgets.QGraphicsView):       
    
    def __init__(self, *args, **kwargs):
        #usual parameters to make sure the image can be zoom-in and out and is 
        #possible to move around the zoomed-in view
        super().__init__(*args, **kwargs)
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
        self._image = None
        
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
            

                