from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QImage, QPainter
import sys
import numpy as np
# import cv2 
from PIL import Image, ImageOps
import torch
import torch.nn as nn
from face_alignment.detection.blazeface.net_blazeface import BlazeFace
from lib.models import get_face_alignment_net
from lib.config import config, merge_configs
import os 
from pathlib import Path
from PyQt5 import QtGui
#import yaml
from arch.FAN import FAN
from arch.resnest.HeatMaps import model_resnest
from ImageViewerandProcess2 import ImageViewer
from LandmarkSetting1 import ShowSettings
from Facial_Landmarks import GetLandmarks
from Utilities import save_txt_file, get_info_from_txt
from Results_Window import ShowResults, CustomTabResult 
from MetricsWindow import MetricsWindow
from Metrics import get_measurements_from_data
from arch.mode_NLF import HeadBlock
from arch.MobileNetV2 import mobilenet_v2

class SinglePhotoWindow(QtWidgets.QMainWindow):
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
        # FaceDetector.to(device)
        FaceDetector.eval();
        self.FaceDetector = FaceDetector
        
        #Face Alignment
        FaceAlignment = torch.jit.load('./models/2DFAN4-cd938726ad.zip')
        # FaceAlignment.to(device)
        FaceAlignment.eval();
        self.FaceAlignment = FaceAlignment
        
        #FAN Model
        model_path = './models/HR18-300W.pth'
        config_path = './models/HR18-300W.yaml'
        merge_configs(config, config_path)
        model = get_face_alignment_net(config)
        model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
        # model.to(device)
        model.eval();
        self.model = model
        
        #FAN_MEEE Model
        model_FAN = FAN(4)
        model_FAN.load_state_dict(torch.load('./arch/train160.pth.tar', map_location=torch.device('cpu')))
        # model_FAN.to(device)
        model_FAN.eval();
        self.model_FAN = model_FAN
        
        #NLF Model
        # backbone = mobilenet_v2()
        # #backbone.load_state_dict(torch.load(r'D:\NeuroFace_FineTuning\pretrained_models\mobilenet_v2-b0353104.pth'), strict=False)
        # nopoints = 8
        # #head = HeadBlock(152, 152, nopoints)
        # head = HeadBlock(1432, 1432, nopoints)
        # model_NLF = nn.Sequential(backbone, head)
        # model_NLF.load_state_dict(torch.load('./arch/NLF.pth', map_location=torch.device('cpu')))
        # # model_NLF.to(device);
        model_NLF = model_resnest(out_channels=8, pretrained=False)
        model_NLF.load_state_dict(torch.load('./arch/heatmap_NSLF.pth', map_location=torch.device('cpu')))
        model_NLF.eval();
        self.model_NLF = model_NLF
        
        #Model Names
        self.Modelname = 'FAN_MEEE' #Default Model is FAN_MEEE
        self.Modelname_NLF = True
        
        """Variable for Results Window"""
        self._new_window = None
        self._CalibrationType = 'Iris'
        self._CalibrationValue = 11.77
        self._file_name = None
        
        ########################
        """Set Up the UI form"""
        ########################
        self.initUI()
        
        """Loads first image on entry"""
        self.load_file()
        
    def initUI(self):
        self.ui = uic.loadUi('Main_Single_Photograph.ui', self)
        
        """Button Connection"""
        #New Photograph Button
        self.loadNewPhotoButton.clicked.connect(self.load_file)
        
        #Previous Button
        # self.previousButton.clicked.connect(self.previous)
        
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
        
        #Button 1.3.1: Save Dots
        self.saveDotsButton.clicked.connect(self.save_results)

        
        #Tab 2:Settings
        
        #Iris Settings
        #Button 2.1.2: Match Eyes Right to Left
        self.matchEyesRtoLButton.clicked.connect(self.displayImage.matchEyesRtoL)
        #Button 2.1.2: Match Eyes Left to Right
        self.matchEyesLtoRButton.clicked.connect(self.displayImage.matchEyesLtoR)
        
        #Landmark Settings
        
        #Button 2.2.1: Add Dots
        self.addDotsButton.clicked.connect(self.displayImage.toggle_add_dots)
        #Button 2.2.2: Landmark Settings
        self.removeDotButton.clicked.connect(self.displayImage.removeDot)
        #Button 2.2.3: Adjust Midline 
        self.adjustMidlineButton.clicked.connect(self.displayImage.toggle_adjustingMidLine)
        #Combo Box 2.2.4: Model ComboBox
        self.modelComboBox.addItem('FAN_MEEE')
        self.modelComboBox.addItem('FAN')
        self.modelComboBox.addItem('HRNet')
        self.modelComboBox.addItem('NLF_model')
        self.modelComboBox.activated[str].connect(self.changeModel)
        #Button 2.2.5: Landmark Color Button and Label
        self.landmarkColorButton.clicked.connect(self.changeDefaultColor)
        self.landmarkColorLabel.setStyleSheet('QWidget {background-color:rgb(255,0,0)}' )
        #Button 2.2.6: Landmark Color Button 2 and Label 2
        self.landmarkColorButton2.clicked.connect(self.changeSecondaryColor)
        self.landmarkColorLabel2.setStyleSheet('QWidget {background-color:rgb(0,0,255)}')
        #Button 2.2.7: Landmark Size Spin Box 
        self.landmarkSizeBox.setValue(self.displayImage._landmark_size)
        self.landmarkSizeBox.valueChanged.connect(self.changeLandmarkSize)
        
        
        
        
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
                    self.displayImage._savedShape = False
                    #Displaying Landmarks
                    self.startLandmarkThread(image)
                    
                #Automatically find landmark size based on size of scene
                H, W, C = self.displayImage._image.shape
                area = H*W
                self.displayImage._landmark_size = ((area)/(10**6))**.8
                self.landmarkSizeBox.setValue(int(self.displayImage._landmark_size)) #makes sure size change is displayed
                # print('self.displayImage._scene.height() = ', self.displayImage._scene.height())
                # print('self.displayImage._image.shape = ', self.displayImage._image.shape)
                print('self.displayImage._landmark_size =', self.displayImage._landmark_size)
                
                #Makes sure everything is up to date
                self.displayImage.update_shape()
            except:
                print('No file given')
        else:
            self._imagePath = None
            pass
            #the user will load an single image so get rid of Patient and the
            # changephotoAction in the toolbar
            print('file ready')
    
    
    def create_metrics_window(self):
        
        
        if max(self.displayImage._shape[:, 2]) >= 76:
            #This is to make sure that the midline exist
            if self.displayImage._points == None:
                self.displayImage.toggle_midLine()
                self.displayImage.toggle_midLine()
            #say to the window that presents the results that there is only 1 tab
            self._new_window = MetricsWindow(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, self._CalibrationType, self._CalibrationValue, self._file_name)
            #show the window with the results 
            self._new_window.show()
        else:
            print('Shape is not greater or equal to 76')
            
            
    def create_new_window(self):
        #this creates a new window to display all the facial metrics, there 
        #are two modes, one if there is no Patient (self._Patient = None)
        #and another if there is a patient (two photos)
        
        if self.displayImage._shape is not None:
            #if the measurements window is already open then close it
            if self._new_window is not None:
                self._new_window.close()
                self._new_window = None
            
            #compute the facial metrics using the landmarks
            #makes sure Midline points exist 
            if self.displayImage._points == None:
                self.displayImage.toggle_midLine()
                self.displayImage.toggle_midLine()
                
            MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual = get_measurements_from_data(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, self._CalibrationType, self._CalibrationValue)
            
            #send all the information the the appropiate places in the window 
            self._tab1_results  =  CustomTabResult()
            
            #filling t_new_window_tab1_results he info for the right
            self._tab1_results._CE_right.setText('{0:.2f}'.format(MeasurementsRight.CommissureExcursion))
            self._tab1_results._SA_right.setText('{0:.2f}'.format(MeasurementsRight.SmileAngle))
            self._tab1_results._DS_right.setText('{0:.2f}'.format(MeasurementsRight.DentalShow))
            self._tab1_results._MRD1_right.setText('{0:.2f}'.format(MeasurementsRight.MarginalReflexDistance1))
            self._tab1_results._MRD2_right.setText('{0:.2f}'.format(MeasurementsRight.MarginalReflexDistance2))
            self._tab1_results._BH_right.setText('{0:.2f}'.format(MeasurementsRight.BrowHeight))
            self._tab1_results._PFH_right.setText('{0:.2f}'.format(MeasurementsRight.PalpebralFissureHeight))

            
            #filling the info for the left
            self._tab1_results._CE_left.setText('{0:.2f}'.format(MeasurementsLeft.CommissureExcursion))
            self._tab1_results._SA_left.setText('{0:.2f}'.format(MeasurementsLeft.SmileAngle))
            self._tab1_results._DS_left.setText('{0:.2f}'.format(MeasurementsLeft.DentalShow))
            self._tab1_results._MRD1_left.setText('{0:.2f}'.format(MeasurementsLeft.MarginalReflexDistance1))
            self._tab1_results._MRD2_left.setText('{0:.2f}'.format(MeasurementsLeft.MarginalReflexDistance2))
            self._tab1_results._BH_left.setText('{0:.2f}'.format(MeasurementsLeft.BrowHeight))
            self._tab1_results._PFH_left.setText('{0:.2f}'.format(MeasurementsLeft.PalpebralFissureHeight))
            
            #deviation
            self._tab1_results._CE_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommissureExcursion))
            self._tab1_results._SA_dev.setText('{0:.2f}'.format(MeasurementsDeviation.SmileAngle))
            self._tab1_results._MRD1_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance1))
            self._tab1_results._MRD2_dev.setText('{0:.2f}'.format(MeasurementsDeviation.MarginalReflexDistance2))
            self._tab1_results._BH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.BrowHeight))
            self._tab1_results._DS_dev.setText('{0:.2f}'.format(MeasurementsDeviation.DentalShow))
            self._tab1_results._CH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.CommisureHeightDeviation))
            self._tab1_results._UVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.UpperLipHeightDeviation))
            self._tab1_results._LVH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.LowerLipHeightDeviation))
            self._tab1_results._PFH_dev.setText('{0:.2f}'.format(MeasurementsDeviation.PalpebralFissureHeight))
            
            
            self._tab1_results._CE_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.CommissureExcursion))
            self._tab1_results._SA_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.SmileAngle))
            self._tab1_results._MRD1_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance1))
            self._tab1_results._MRD2_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.MarginalReflexDistance2))
            self._tab1_results._BH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.BrowHeight))
            self._tab1_results._DS_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.DentalShow))
            self._tab1_results._PFH_dev_p.setText('{0:.2f}'.format(MeasurementsPercentual.PalpebralFissureHeight))
            
            
            delimiter = os.path.sep
            temp=self._file_name.split(delimiter)
            photo_name=temp[-1]
            photo_name=photo_name[0:-4]
            self._tab1_results._tab_name=photo_name
            
            
            #say to the window that presents the results that there is only 1 tab
            self._new_window = ShowResults(self._tab1_results)
            #show the window with the results 
            self._new_window.show()
       
        else:
            print('Shape does not exist')
        
    def startLandmarkThread(self, image):
        self.landmarks = GetLandmarks(image, self.displayImage._shape, 
                                      self.displayImage._lefteye, self.displayImage._righteye,
                                      self.displayImage._savedShape, self.Modelname, self.Modelname_NLF, 
                                      self.FaceDetector, self.FaceAlignment,
                                      self.model, self.model_FAN, self.model_NLF)
        self.landmarks.moveToThread(self.thread_landmarks)
        self.thread_landmarks.start()
        self.thread_landmarks.started.connect(self.landmarks.run) #runs thread
        self.landmarks.landmarks.connect(self.displayImage.show_Facial_Landmarks) #connects signal to function
        self.landmarks.finished.connect(self.thread_landmarks.quit) #ends thread when done
        self.landmarks.finished.connect(self.displayImage.update_shape) #updates everything when done
        self.landmarks.finished.connect(self.displayImage.reset_save_variables)
        
    def landmark_settings(self):
        Settings = ShowSettings(self.Modelname, self.Modelname_NLF, int(self.displayImage._landmark_size))
        Settings.exec_()
        
        """Size"""
        #check if the user decided to change the landmark size
        user_size_landmark = Settings.tab2.selectLandmarkSize.text()
        old_size_landmark = self.displayImage._landmark_size
        is_landmark_changed = False
        if user_size_landmark == "":
            size_landmarks = old_size_landmark
        elif int(user_size_landmark) ==  0: #used entered zero, just ignore it 
            size_landmarks = old_size_landmark
        else:
            size_landmarks = int(user_size_landmark)
            
        if size_landmarks == old_size_landmark:
            pass
        else:
            is_landmark_changed = True
            #update landmark size information 
            self.displayImage._landmark_size = size_landmarks/100
        
        
        """Color"""
        #check if the user decided to change the landmark color
        user_color_landmark = Settings.tab2.selectedColor
        old_color_landmark = self.displayImage._landmark_color
        is_landmark_color_changed = False
        if user_color_landmark is None:
            color_landmarks = old_color_landmark
        else:
            color_landmarks = user_color_landmark
            
        if color_landmarks == old_color_landmark:
            pass
        else:
            is_landmark_color_changed = True
            #update landmark size information 
            self.displayImage._landmark_color = color_landmarks
        
        
        """Model"""
        #check if the user decided to change the landmark model
        user_model = Settings.tab1.Modelname
        user_model_NLF = Settings.tab1.NLF_Model
        old_model = self.Modelname
        old_model_NLF = self.Modelname_NLF
        is_model_changed = False
        
        if user_model == old_model and user_model_NLF == old_model_NLF:
            pass
        else:
            if user_model == old_model:
                self.displayImage._savedShape = True
            else:
                self.displayImage._savedShape = False
            is_model_changed = True
            self.Modelname = user_model
            self.Modelname_NLF = user_model_NLF
        
        """Updates Dots"""
        #update dots based on new settings
        if is_model_changed == True:
            self.startLandmarkThread(self.displayImage._image)
            
        
        elif is_landmark_color_changed == True or is_landmark_changed == True:
            if self.displayImage._shape is not None:
                self.displayImage.remove_dots()
                self.displayImage.update_shape()
    
        else:
            pass
    
    
    def changeModel(self, model):
        """This function is for when the user selects a new option in the model Combo box"""
        if model == 'NLF_model':
            self.Modelname = model
            self.Modelname_NLF = False
        else:
            self.Modelname = model
            self.Modelname_NLF = True
        self.displayImage._savedShape = False
        self.startLandmarkThread(self.displayImage._image)
        
    
    def changeDefaultColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.displayImage._landmark_color = color
            print('Color Selected: ', color.name())
            self.landmarkColorLabel.setStyleSheet('QWidget {background-color:%s}' %color.name())
            self.displayImage.update_shape()
    
    
    def changeSecondaryColor(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.displayImage._landmark_color_lower_lid = color
            self.displayImage._landmark_color_lower_lips = color
            print('Color Selected: ', color.name())
            self.landmarkColorLabel2.setStyleSheet('QWidget {background-color:%s}' %color.name())
            self.displayImage.update_shape()
    
            
    def changeLandmarkSize(self, size):
        try:
            self.displayImage._landmark_size = size
            self.displayImage.update_shape()
        except:
            print('Error')
            print('Size Selected = ', size)
            
    
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
        
        
    
    def about_app(self):
        
        #show a window with some information
        QtWidgets.QMessageBox.information(self, 'Emotrics', 
                            'Emotrics is a tool for estimation of objective facial measurements, it uses machine learning to automatically localize facial landmarks in photographs. Its objective is to reduce subjectivity in the evaluation of facial palsy.\n\nEmotrics was developed by: Diego L. Guarin, PhD. at the Facial Nerve Centre, Massachusetts Eye and Ear Infirmary; part of Harvard Medical School.\n\nA tutorial can be found by searching for Emotrics on YouTube.\n\nThis is an open source software provided with absolutely no guarantees. You can run, study, share and modify the software. It is distributed under the GNU General Public License.\n\nThis software was written in Python, source code and additional information can be found in github.com/dguari1/Emotrics ', 
                            QtWidgets.QMessageBox.Ok)  
    
    def previous(self):
        app = QtWidgets.QApplication(sys.argv)
        sys.exit(app.exec_())

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SinglePhotoWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()