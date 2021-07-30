from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QImage, QPainter
import sys
import numpy as np
from PIL import Image, ImageOps
import torch
from face_alignment.detection.blazeface.net_blazeface import BlazeFace
from lib.models import get_face_alignment_net
from lib.config import config, merge_configs
import os 
from pathlib import Path
from PyQt5 import QtGui
from arch.FAN import FAN
from arch.resnest.HeatMaps import model_resnest
from models.irislandmarks import IrisLandmarks
from ImageViewerandProcess2 import ImageViewer
from Facial_Landmarks import GetLandmarks
from Utilities import save_txt_file, get_info_from_txt
from MetricsWindow import MetricsWindow
from LandmarkSettingWindow import LandmarkSettingsWindow
from MetricsSettingsWindow import MetricsSettingsWindow


class SinglePhotoWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    def __init__(self, *args, **kwargs):
        super(SinglePhotoWindow, self).__init__(*args, **kwargs)
        
        """Start of Set up"""
        if os.name == 'posix': #is a mac or linux
            self.scriptDir = os.path.dirname(sys.argv[0])
        else: #is a  windows 
            self.scriptDir = os.getcwd()


        #self.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'include' +os.path.sep +'icon_color'+ os.path.sep + 'meei_3WR_icon.ico')
        
        """Thread Creation"""
        # create Thread  to take care of the landmarks and iris estimation   
        self.thread_landmarks = QtCore.QThread()  # no parent!
        
        """Loading Models"""
        FaceDetector = BlazeFace()
        FaceDetector.load_state_dict(torch.load('./models/blazeface.pth'))
        FaceDetector.load_anchors_from_npy(np.load('./models/anchors.npy'))
    
        
        # device = 'cuda' if torch.cuda.is_available() else 'cpu'
        #Face Detector
        FaceDetector.eval();
        self.FaceDetector = FaceDetector
        
        #Face Alignment
        FaceAlignment = torch.jit.load('./models/2DFAN4-cd938726ad.zip')
        FaceAlignment.eval();
        self.FaceAlignment = FaceAlignment
        
        #FAN Model
        model_path = './models/HR18-300W.pth'
        config_path = './models/HR18-300W.yaml'
        merge_configs(config, config_path)
        model = get_face_alignment_net(config)
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        model.eval();
        self.model = model
        
        #FAN_MEEE Model
        model_FAN = FAN(4)
        model_FAN.load_state_dict(torch.load('./arch/train160.pth.tar', map_location=torch.device('cpu')))
        model_FAN.eval();
        self.model_FAN = model_FAN
        
        #NLF Model
        model_NLF = model_resnest(out_channels=8, pretrained=False)
        model_NLF.load_state_dict(torch.load('./arch/heatmap_NSLF.pth', map_location=torch.device('cpu')))
        model_NLF.eval();
        self.model_NLF = model_NLF
        
        #Eye Model
        device = 'cpu'
        self.net = IrisLandmarks().to(device)
        self.net.load_weights('./models/irislandmarks.pth')
        
        #Model Names
        self.Modelname = 'FAN_MEEE' #Default Model is FAN_MEEE
        self.Modelname_NLF = True
        
        """Variable for Results Window"""
        self._new_window = None
        self._CalibrationType = 'Iris'
        self._CalibrationValue = 11.77
        self._file_name = None
        
        ################################################
        """Set Up the UI form"""
        ################################################
        self.initUI()
        
        """Loads first image on entry"""
        self.load_file()
        # #If no file is selected on there is an error, return to home screen **Incomplete**
        # if self.displayImage._image != None:
        #     pass
        # else:
        #     print('Returning to Home Window')
        #     self.close()


        
    def initUI(self):
        self.ui = uic.loadUi('uis/single.ui', self)
        
        """Button Connection"""
        #New Photograph Button
        self.loadNewPhotoButton.clicked.connect(self.load_file)
        
        #Previous Button
        self.previousButton.clicked.connect(self.previous)
        
        #Reference Side button
        self.referenceSideLeftButton.toggled.connect(self.leftSideSelected)
        self.referenceSideRightButton.toggled.connect(self.rightSideSelected)
        #Tab 1: Main
        #Measurements
        
        #Button 1.1.1: Measurements
        self.measurementsButton.clicked.connect(self.create_metrics_window)
        
        #Visualization
        
        #Button 1.2.1: Toggle Dots
        self.toggleDotsButton.clicked.connect(self.displayImage.toggle_dots)
        #Button 1.2.2: Toggle Midline
        self.toggleMidlineButton.clicked.connect(self.displayImage.toggle_midLine)
        # #Button 1.2.3: Toggle NLF
        # self.showNLFButton.clicked.connect(self.displayImage.show_NLF)
        
        #Save
        
        #Button 1.3.2: Save Dots
        self.saveDotsButton.clicked.connect(self.save_results)

        
        #Tab 2:Settings
        #Iris Settings
        
        #Button 2.1.2: Match Eyes Right to Left
        self.matchEyesRtoLButton.clicked.connect(self.displayImage.matchEyesRtoL)
        #Button 2.1.3: Match Eyes Left to Right
        self.matchEyesLtoRButton.clicked.connect(self.displayImage.matchEyesLtoR)
        
        #Landmark Settings
        
        #Button 2.2.1: Landmark Settings
        self.landmarkSettingsButton.clicked.connect(self.landmark_Setting)
        #Button 2.2.2: Add Dots
        self.addDotsButton.clicked.connect(self.displayImage.toggle_add_dots)
        #Button 2.2.3: Landmark Settings
        self.removeDotButton.clicked.connect(self.displayImage.removeDot)
        #Button 2.2.4: Adjust Midline 
        self.adjustMidlineButton.clicked.connect(self.displayImage.toggle_adjustingMidLine)
        #Button 2.2.5: Reset Midline 
        self.resetMidlineButton.clicked.connect(self.displayImage.reset_midline)
        
        #Measurement and Save Settings
        
        #Button 2.3.2: Landmark Settings
        self.metricsSettingsButton.clicked.connect(self.metrics_settings)

        
        """Shortcuts"""
        #Left arrow (Laterial)
        self.midLine_Laterial_move_left_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Left"), self)
        self.midLine_Laterial_move_left_shortcut.activated.connect(self.displayImage.midLine_Laterial_move_left)
        
        #Right arrow (Laterial)
        self.midLine_Laterial_move_right_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Ctrl+Right"), self)
        self.midLine_Laterial_move_right_shortcut.activated.connect(self.displayImage.midLine_Laterial_move_right)
        
        #Ctrl+Left arrow (Angular)
        self.midLine_Angular_move_left_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Left"), self)
        self.midLine_Angular_move_left_shortcut.activated.connect(self.displayImage.midLine_Angular_move_clockwise)
        
        #Ctrl+Right arrow (Angular)
        self.midLine_Angular_move_right_shortcut = QtWidgets.QShortcut(QtGui.QKeySequence("Right"), self)
        self.midLine_Angular_move_right_shortcut.activated.connect(self.displayImage.midLine_Angular_move_counterclockwise)
        

    def load_file(self):
        
        #load a file using the widget
        name,_ = QtWidgets.QFileDialog.getOpenFileName(
                self,'Load Image',
                '',"Image files (*.png *.jpg *.jpeg *.jfif *.tif *.tiff *.PNG *.JPG *.JPEG *.TIF *.TIFF)")
        self._imagePath = name
        name = Path(name)
        if name.is_file():
            try:
                #Displaying Image
                image = Image.open(name).convert('RGB')
                image = ImageOps.exif_transpose(image)
                image = np.array(image)
                self.displayImage._image = image
                self.displayImage.update_view()
                self.displayImage.clear_scene()
                
                os_name = os.path.normpath(self._imagePath)
                self._file_name = os_name
                #self.displayImage._opencvimage = image#cv2.imread(os_name)
                filename = os_name[:-4]
                if filename[-1] == '.':
                    filename = filename[:-1]
                file_txt = (filename + '.txt')
                
                # self._shapePath = Path(self._imagePath.stem + 'txt')

                if os.path.isfile(file_txt):
                        shape, lefteye, righteye, boundingbox = get_info_from_txt(file_txt)
                        self.displayImage._lefteye = lefteye
                        self.displayImage._righteye = righteye 
                        self.displayImage._shape = shape
                        self.displayImage._boundingbox = boundingbox
                        self.displayImage._points = None
                        self.displayImage._savedShape = True #Makes sure imported dots are not altered if NLF is calculated
                        #Checks if NLF landmarks need to be calculated
                        if self.Modelname_NLF == True and len(self.displayImage._shape) == 68:
                            self.startLandmarkThread(image)
                        # self.displayImage.update_shape()
                else:
                    #Resets Shape and Eyes
                    self.displayImage._shape = None
                    self.displayImage._lefteye = None
                    self.displayImage._righteye = None
                    self.displayImage._lefteye_landmarks = None
                    self.displayImage._righteye_landmarks = None
                    self.displayImage._savedShape = False
                    #Displaying Landmarks
                    self.startLandmarkThread(image)
                    
                #Automatically find landmark size based on size of scene
                H, W, C = self.displayImage._image.shape
                area = H*W
                self.displayImage._landmark_size = ((area)/(10**6))**.8
                # self.landmarkSizeBox.setValue(int(self.displayImage._landmark_size)) #makes sure size change is displayed
                # print('self.displayImage._scene.height() = ', self.displayImage._scene.height())
                # print('self.displayImage._image.shape = ', self.displayImage._image.shape)
                # print('self.displayImage._landmark_size =', self.displayImage._landmark_size)
                
                #Makes sure everything is up to date
                self.displayImage.update_shape()
            except:
                QtWidgets.QMessageBox.information(self, 'Error', 
                            'Error in Loading file', 
                            QtWidgets.QMessageBox.Ok)
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                            'No file selected', 
                            QtWidgets.QMessageBox.Ok)
    
    
    def create_metrics_window(self):
        """This function is used when the user clicks the measurement button.
        This function opens up a window and displays the metrics of the photo"""
        if max(self.displayImage._shape[:, 2]) >= 76:
            #This is to make sure that the midline exist
            if self.displayImage._points == None:
                self.displayImage.toggle_midLine()
                self.displayImage.toggle_midLine()
            #say to the window that presents the results that there is only 1 tab
            self._new_window = MetricsWindow(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, self._CalibrationType, self._CalibrationValue, self.displayImage._reference_side, self._file_name)
            #show the window with the results 
            self._new_window.show()
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 
                            'Not enough Landmarks. \nThere must be 76 or more Landmarks', 
                            QtWidgets.QMessageBox.Ok)
    
            
    def startLandmarkThread(self, image):
        self.landmarks = GetLandmarks(image, self.displayImage._shape, 
                                      self.displayImage._lefteye, self.displayImage._righteye,
                                      self.displayImage._savedShape, self.Modelname, self.Modelname_NLF, 
                                      self.FaceDetector, self.FaceAlignment,
                                      self.model, self.model_FAN, self.model_NLF, self.net)
        self.landmarks.moveToThread(self.thread_landmarks)
        self.thread_landmarks.start()
        self.thread_landmarks.started.connect(self.landmarks.run) #runs thread
        self.landmarks.landmarks.connect(self.displayImage.show_Facial_Landmarks) #connects signal to function
        self.landmarks.finished.connect(self.thread_landmarks.quit) #ends thread when done
        self.landmarks.finished.connect(self.displayImage.update_shape) #updates everything when done
        self.landmarks.finished.connect(self.displayImage.reset_save_variables)
    
    
    def leftSideSelected(self):
        self.displayImage._reference_side = 'Left'
    
    
    def rightSideSelected(self):
        self.displayImage._reference_side = 'Right'
     
        
    def landmark_Setting(self):
        """This function opens a window for the landmark setting"""
        self.landmark_Setting_window = LandmarkSettingsWindow(self.Modelname, self.displayImage._landmark_color, self.displayImage._landmark_color_lower_lid,
                                                              self.displayImage._iris_color, self.displayImage._midLine_color, self.displayImage._landmark_size)
        self.landmark_Setting_window.show()
        
        self.landmark_Setting_window.models.connect(self.changeModel)
        self.landmark_Setting_window.colors.connect(self.changeColors)
        self.landmark_Setting_window.size.connect(self.changeLandmarkSize)
    
    
    def changeModel(self, model, new_model_selected):
        """This function is used when a new model is selected in the landmark settings"""
        # try:
        if new_model_selected == True:
            if model == 'NLF_model':
                self.Modelname = model
                self.Modelname_NLF = False
            else:
                self.Modelname = model
                self.Modelname_NLF = True
            self.displayImage._savedShape = False
            self.startLandmarkThread(self.displayImage._image)
        else:
            print('No new model selected')
        # except:
        #     print('Error in changeModel')
        
    
    def changeColors(self, landmark_color1, landmark_color2, eye_color, midline_color):
        """This function is used when new colors are selected in the landmark settings"""
        # try:
        self.displayImage._landmark_color = landmark_color1
        self.displayImage._landmark_color_lower_lid = landmark_color2
        self.displayImage._landmark_color_lower_lips = landmark_color2
        self.displayImage._iris_color = eye_color
        self.displayImage._midLine_color = midline_color
        self.displayImage.update_shape()
        # except:
        #     print('Error in changeColors')
        
        
    def changeLandmarkSize(self, size):
        """This function is used when a new size is selected in the landmark settings"""
        # try:
        self.displayImage._landmark_size = size
        self.displayImage.update_shape()
        # except:
        #     print('Error in changeLandmarkSize')
        #     print('Size Selected = ', size)    
        
    
    def metrics_settings(self):
        """This function is used when the user clicks the measurement settings button.
        This function opens up a window and allows the user to change the calibration type"""
        self.metrics_Setting_window = MetricsSettingsWindow(self._CalibrationType, self._CalibrationValue)
        self.metrics_Setting_window.show()
        self.metrics_Setting_window.Calibration_Type.connect(self.changeCalibrationType)
        self.metrics_Setting_window.Calibration_Value.connect(self.changeCalibrationValue)
        
        
    def changeCalibrationValue(self, CalibrationValue):
       """This function is used when a new Calibration Value is selected in the metrics settings"""
       self._CalibrationValue = CalibrationValue
       
        
    def changeCalibrationType(self, CalibrationType):
       """This function is used when a new Calibration Value is selected in the metrics settings"""
       self._CalibrationType = CalibrationType
       
         
    def save_results(self):
        if self._imagePath is not None:
            name = os.path.normpath(self._imagePath)
            filename = name[:-4]
            file_txt = (filename + '.txt')
            if os.path.isfile(file_txt):
                os.remove(file_txt)
            save_txt_file(file_txt, self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._boundingbox)
    
    
    def save_as_results(self):
        if self._imagePath is not None:
            name = os.path.normpath(self._imagePath)
            filename = name[:-4]
            delimiter = os.path.sep
            temp=filename.split(delimiter)
            photo_name=temp[-1]
            photo_name = (photo_name + '(marked)')
            filename = (filename + '(marked)')
            if os.path.isfile(filename):
                os.remove(filename)
            print(filename)
            print(photo_name)
            marked_image = QImage()
            painter = QPainter(marked_image)
            self.displayImage._scene.render(painter)
            painter.end()
            print(marked_image)
            print('Saving Image')
            print(marked_image.save(photo_name,'JPG'))
            marked_image.save(photo_name,'JPG')
            print(marked_image.save(photo_name,'JPG'))
        
        
    def previous(self):
        self.finished.emit()
        self.close()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SinglePhotoWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()