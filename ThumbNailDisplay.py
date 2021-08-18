from PyQt5 import QtWidgets, QtGui, QtCore
import os 

class ThumbNailDisplay(QtWidgets.QGraphicsView):       
    selected = QtCore.pyqtSignal()
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
        self._hasImage = False
        self._ImageAddress = None

        self._validextensions = ['.png', '.jpg', '.jpeg', '.tif', '.tiff', '.PNG', '.JPG', '.JPEG', '.TIF', '.TIFF']
        

    def setPhoto(self, pixmap = None):
        #this function puts an image in the scece (if pixmap is not None), it
        #sets the zoom to zero  
        if pixmap and not pixmap.isNull():
            #self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)
            self._photo.setPixmap(pixmap)
            self.fitInView()
        else:
            self.setDragMode(QtWidgets.QGraphicsView.NoDrag)
            self._photo.setPixmap(QtGui.QPixmap())


    def fitInView(self):
        #this function takes care of accomodating the view so that it can fit
        #in the scene
        rect = QtCore.QRectF(self._photo.pixmap().rect())
        self.setSceneRect(rect)
        if not rect.isNull():
            unity = self.transform().mapRect(QtCore.QRectF(0, 0, 1, 1))
            self.scale(1 / unity.width(), 1 / unity.height())        
            viewrect = self.viewport().rect()
            scenerect = self.transform().mapRect(rect)
            factor = min(viewrect.width() / scenerect.width(),
                     viewrect.height() / scenerect.height())               
            self.scale(factor, factor)
            self.centerOn(rect.center())


    def resizeEvent(self, event):
        #this function assure that when the main window is resized the image 
        #is also resized preserving the h/w ratio
        self.fitInView()
           

    def mouseDoubleClickEvent(self, event):
        self.selected.emit()           