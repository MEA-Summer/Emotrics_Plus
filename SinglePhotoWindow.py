from PyQt5 import QtWidgets, QtCore, uic
from PyQt5.QtGui import QImage, QPainter
import sys
import numpy as np
from PIL import Image, ImageOps
import torch
import os 
from pathlib import Path
from PyQt5 import QtGui
from ImageViewerandProcess2 import ImageViewer
from Facial_Landmarks import GetLandmarks
from Metrics import get_measurements_from_data
from Utilities import save_txt_file, get_info_from_txt
from MetricsWindow import MetricsWindow
from Auto_eFaceWindow import Auto_eFaceWindow
from LandmarkSettingWindow import LandmarkSettingsWindow
from MetricsSettingsWindow import MetricsSettingsWindow
from SaveMetricsWindow import SaveMetricsWindow


class SinglePhotoWindow(QtWidgets.QMainWindow):
    finished = QtCore.pyqtSignal()
    busy = QtCore.pyqtSignal()
    got_landmarks = QtCore.pyqtSignal()
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
        self.thread_landmarks = QtCore.QThread(parent=self)  
        
        
        #Model Names
        self.Modelname = 'FAN_MEEE' #Default Model is FAN_MEEE
        self.Modelname_NLF = True
        #Models
        self.FaceAlignment = None
        self.FaceDetector = None
        self.model = None
        self.model_FAN = None
        self.model_NLF = None
        self.net = None
        
        """Variable for Results Window"""
        self._new_window = None
        self._CalibrationType = 'Iris'
        self._CalibrationValue = 11.77
        self._file_name = None
        self._patientID = None
        self._expression = 'Resting'
        
        """Variable for closing"""
        self._IsMainWindow = False  #if this window is created by a SevenPhotoWindow, this remains False
                                    #if this window is create by home page, this will be set to true

        """Set Up the UI form"""
        self.initUI()
        

    ########################################################################################################################
    ########################################################################################################################
    """Set-up Functions"""
    ########################################################################################################################
    ########################################################################################################################

    
    def initUI(self):
        self.ui = uic.loadUi('uis/single.ui', self)

        #Set Date
        self.dateEdit.setDate(QtCore.QDate.currentDate())
        #Set Patient ID
        self.patientIDLineEdit.textChanged.connect(self.setPatientID)
        
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
        #Button 1.1.2: Auto eFace
        self.auto_eFaceButton.clicked.connect(self.create_auto_eFace_window)
        #Visualization
        
        #Button 1.2.1: Toggle Dots
        self.toggleDotsButton.clicked.connect(self.displayImage.toggle_dots)
        #Button 1.2.2: Toggle Midline
        self.toggleMidlineButton.clicked.connect(self.displayImage.toggle_midLine)
        # #Button 1.2.3: Toggle NLF
        # self.showNLFButton.clicked.connect(self.displayImage.show_NLF)
        
        #Save
        
        #Button 1.3.1: Save Screenshot
        self.screenShotButton.clicked.connect(self.save_screenshot)
        #Button 1.3.2: Save Dots
        self.saveDotsButton.clicked.connect(self.save_results)
        #Button 1.3.3: Save Metrics
        self.saveMeasurementsButton.clicked.connect(self.save_metrics)

        
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
    
    
    def setPhoto(self, name):
        try:
            self._imagePath = name
            name = Path(name)
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
            
            # self._shapePath = Path(self._imagePath1.stem + 'txt')

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
                    self.got_landmarks.emit()
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
            print('Error in Loading file')
    
    
    def setReferenceSide(self, side):
        if side == 'Left':
            self.displayImage._reference_side = 'Left'
            self.referenceSideLeftButton.setChecked(True)
            self.referenceSideRightButton.setChecked(False)
        elif side == 'Right':
            self.displayImage._reference_side = 'Right'
            self.referenceSideLeftButton.setChecked(False)
            self.referenceSideRightButton.setChecked(True)
        else:
            print('Invalid Reference Side')


    def setTaskName(self, taskName):
        self._expression = taskName

    
    def setPatientID(self, patientID):
        self._patientID = patientID
        self.patientIDLineEdit.setText(self._patientID)
        self.setWindowTitle(f"Emotrics+ | {self._patientID}")




    ########################################################################################################################
    ########################################################################################################################
    """Loading Functions"""
    ########################################################################################################################
    ########################################################################################################################


    def load_file(self):
        #Verify is current dots are saved
        self.verifySave()
        
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
                        self.got_landmarks.emit()
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
                # print('self.displayImage._scene.height() = ', self.displayImage._scene.height())
                # print('self.displayImage._image.shape = ', self.displayImage._image.shape)
                # print('self.displayImage._landmark_size =', self.displayImage._landmark_size)
                
                #Makes sure everything is up to date
                self.displayImage.update_shape()
            except Exception as e:
                if self.displayImage._image is None:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                        f'Error in Loading file.\nPlease try again.',#\n Error message: {e}', 
                        QtWidgets.QMessageBox.Ok)
                    self.load_file()
                else:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                        'Error in Loading file.',#\n Error message: {e}', 
                        QtWidgets.QMessageBox.Ok)
        else:
            #If no file is selected or there is an error, return to home screen **Incomplete**
            if self.displayImage._image is None:
                QtWidgets.QMessageBox.information(self, 'Error', 
                    'No file selected.\nPlease try again.', 
                    QtWidgets.QMessageBox.Ok)
                self.load_file()
    
            
    def startLandmarkThread(self, image):
        self.landmarks = GetLandmarks(image, self.displayImage._shape, 
                                      self.displayImage._lefteye, self.displayImage._righteye,
                                      self.displayImage._savedShape, self.Modelname, self.Modelname_NLF, 
                                      self.FaceDetector, self.FaceAlignment,
                                      self.model, self.model_FAN, self.model_NLF, self.net)
        self.landmarks.moveToThread(self.thread_landmarks)
        self.thread_landmarks.start()
        self.thread_landmarks.started.connect(self.setBusy) #shows that the thread has started
        self.thread_landmarks.started.connect(self.landmarks.run) #runs thread
        self.landmarks.landmarks.connect(self.displayImage.show_Facial_Landmarks) #connects signal to function
        self.landmarks.finished.connect(self.thread_landmarks.quit) #ends thread when done
        self.landmarks.finished.connect(self.displayImage.update_shape) #updates everything when done
        self.landmarks.finished.connect(self.displayImage.reset_save_variables)
        self.displayImage.dots_shown.connect(self.setNormalCursor) #shows that everything is done loading
    
    def setBusy(self):
        """This function is to show that the program is current working on something
        (most likely Landmark Thread). It shows this by set the cursor to the busy cursor"""
        # print('Busy\nBusy Cursor Set')
        self.displayImage._busy = True
        self.setCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.busy.emit()
    
    def setNormalCursor(self):
        """This function is to show that the program is current working on something
        (most likely Landmark Thread). It shows this by set the cursor to the busy cursor"""
        # print('Finished\nNormal Cursor Set')
        self.displayImage._busy = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.got_landmarks.emit()

    ########################################################################################################################
    ########################################################################################################################
    """Metrics Functions"""
    ########################################################################################################################
    ########################################################################################################################

    
    def create_metrics_window(self):
        """This function is used when the user clicks the measurement button.
        This function opens up a window and displays the metrics of the photo"""
        try:
            if max(self.displayImage._shape[:, 2]) >= 76:
                #This is to make sure that the midline exist
                if self.displayImage._points == None:
                    self.displayImage.toggle_midLine()
                    self.displayImage.toggle_midLine()
                #Create Metrics Window
                self._new_window = MetricsWindow(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, self._CalibrationType, self._CalibrationValue, self.displayImage._reference_side, self._file_name)
                #show the window with the results 
                self._new_window.show()
            else:
                QtWidgets.QMessageBox.information(self, 'Error', 
                    'Not enough Landmarks. \nThere must be 76 or more Landmarks', 
                    QtWidgets.QMessageBox.Ok)
        except Exception as e:
            QtWidgets.QMessageBox.information(self, 'Error', 
                    f'Error in creating metrics window.',#\n Error message: {e}', 
                    QtWidgets.QMessageBox.Ok)
    

    def create_auto_eFace_window(self):
        """This function is used when the user clicks the Auto eFace button.
        This function opens up a window and displays the Auto eFace graph of the photo"""
        try:
            if max(self.displayImage._shape[:, 2]) >= 76:
                if self._expression == 'Resting' or self._expression == 'Big Smile' or self._expression == '"ooooo"':
                    """This if statement prevents the window from opening if there is no parameter to be displayed.
                        This is typically subject to change therefore the window itself mantains its ability to show these
                        expression but is locked by this if statement"""
                    #This is to make sure that the midline exist
                    if self.displayImage._points == None:
                        self.displayImage.toggle_midLine()
                        self.displayImage.toggle_midLine()
                    self._new_window = Auto_eFaceWindow(self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, self._CalibrationType, self._CalibrationValue, self.displayImage._reference_side, self._file_name, self._expression)
                    #show the window with the results 
                    self._new_window.show()
                else:
                    QtWidgets.QMessageBox.information(self, 'Error', 
                        'Auto-eFACE Graph is not available for this expression.', 
                        QtWidgets.QMessageBox.Ok)    
            else:
                QtWidgets.QMessageBox.information(self, 'Error', 
                    'Not enough Landmarks. \nThere must be 76 or more Landmarks', 
                    QtWidgets.QMessageBox.Ok)
        except Exception as e:
            QtWidgets.QMessageBox.information(self, 'Error', 
                    f'Error in creating Auto-eFace Window.',#\n Error message: {e}', 
                    QtWidgets.QMessageBox.Ok)
    
    def leftSideSelected(self):
        self.displayImage._reference_side = 'Left'
    
    
    def rightSideSelected(self):
        self.displayImage._reference_side = 'Right'
    

    ########################################################################################################################
    ########################################################################################################################
    """Landmark Settings Functions"""
    ########################################################################################################################
    ########################################################################################################################

        
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
        try:
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
        except:
            print('Error in changeModel')
        
    
    def changeColors(self, landmark_color1, landmark_color2, eye_color, midline_color):
        """This function is used when new colors are selected in the landmark settings"""
        try:
            self.displayImage._landmark_color = landmark_color1
            self.displayImage._landmark_color_lower_lid = landmark_color2
            self.displayImage._landmark_color_lower_lips = landmark_color2
            self.displayImage._iris_color = eye_color
            self.displayImage._midLine_color = midline_color
            self.displayImage.update_shape()
        except:
            print('Error in changeColors')
        
        
    def changeLandmarkSize(self, size):
        """This function is used when a new size is selected in the landmark settings"""
        try:
            self.displayImage._landmark_size = size
            self.displayImage.update_shape()
        except:
            print('Error in changeLandmarkSize')
            print('Size Selected = ', size)    
    

    ########################################################################################################################
    ########################################################################################################################
    """Metrics Settings Functions"""
    ########################################################################################################################
    ########################################################################################################################


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
    

    ########################################################################################################################
    ########################################################################################################################
    """Saving Functions"""
    ########################################################################################################################
    ########################################################################################################################

          
    def save_results(self):
        if self._imagePath is not None:
            name = os.path.normpath(self._imagePath)
            filename = name[:-4]
            file_txt = (filename + '.txt')
            if os.path.isfile(file_txt):
                os.remove(file_txt)
            save_txt_file(file_txt, self.displayImage._shape, self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._boundingbox)
    
    
    def save_screenshot(self):
        """This function save a screenshot of the current graphics scene."""
        if self._imagePath is not None:
            try:
                name = os.path.normpath(self._imagePath)
                filename = name[:-4]
                delimiter = os.path.sep
                temp=filename.split(delimiter)
                photo_name=temp[-1]
                photo_name = (photo_name + '(marked)')
                filename = (filename + '(marked)')
                if os.path.isfile(filename):
                    os.remove(filename)

                image = QImage(self.displayImage._scene.width(), self.displayImage._scene.height(), QImage.Format_RGB32)
                painter = QPainter(image)

                # Render the region of interest to the QImage.
                self.displayImage._scene.render(painter)
                painter.end()

                # Save the image to a file.
                image.save(filename +'.jpg')

                QtWidgets.QMessageBox.information(self, 'Saved', 
                    f'Screenshot succesfully saved.\nPhoto name is {photo_name}', 
                    QtWidgets.QMessageBox.Ok)
            except Exception as e:
                QtWidgets.QMessageBox.information(self, 'Error', 
                    f'Error in saving screenshot.',#\n Error message: {e}', 
                    QtWidgets.QMessageBox.Ok)
    

    def save_metrics(self):
        """This function saves the metrics as an xls file."""
        try:
            if max(self.displayImage._shape[:, 2]) >= 76:
                #This is to make sure that the midline exist
                if self.displayImage._points == None:
                    self.displayImage.toggle_midLine()
                    self.displayImage.toggle_midLine()

                (MeasurementsLeft, MeasurementsRight, 
                MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(self.displayImage._shape, 
                    self.displayImage._lefteye, self.displayImage._righteye, self.displayImage._points, 
                    self._CalibrationType, self._CalibrationValue, self.displayImage._reference_side)
                
                temp = SaveMetricsWindow(self, self._file_name, MeasurementsLeft, MeasurementsRight, MeasurementsDeviation, MeasurementsPercentual)
                temp.exec_()
            else:
                QtWidgets.QMessageBox.information(self, 'Error', 
                    'Not enough Landmarks. \nThere must be 76 or more Landmarks', 
                    QtWidgets.QMessageBox.Ok)
        except Exception as e:
            QtWidgets.QMessageBox.information(self, 'Error', 
                    f'Error in creating metrics window.',#\n Error message: {e}', 
                    QtWidgets.QMessageBox.Ok)

    

    ########################################################################################################################
    ########################################################################################################################
    """Closing Function"""
    ########################################################################################################################
    ########################################################################################################################


    def verifySave(self):
        """This function verifies that the current landmarks are save."""
        try:
            filename = self._file_name[:-4]
            if filename[-1] == '.':
                filename = filename[:-1]
            file_txt = (filename + '.txt')
            if os.path.isfile(file_txt):
                shape, lefteye, righteye, boundingbox = get_info_from_txt(file_txt)
                currently_Saved = True #the landmarks are assumed to be saved unless a difference is found
                for i in range(len(self.displayImage._shape)):
                    if (self.displayImage._shape[i,0] != shape[i,0] or
                    self.displayImage._shape[i,1] != shape[i,1] or
                    self.displayImage._shape[i,2] != shape[i,2]):
                        #checks if shape is the same
                        # print('Difference Found in boundingbox')
                        # print('self.displayImage._shape = ', self.displayImage._shape)
                        # print('shape = ', shape)
                        currently_Saved = False
                if currently_Saved == True:
                    #only checks if no differences are found in shape
                    for i in range(len(self.displayImage._righteye)):
                        if self.displayImage._righteye[i] != righteye[i]:
                            #checks if righteye is the same
                            # print('Difference Found in boundingbox')
                            # print('self.displayImage._righteye = ', self.displayImage._righteye)
                            # print('righteye = ', righteye)
                            currently_Saved = False
                if currently_Saved == True:
                    #only checks if no differences are found in shape
                    for i in range(len(self.displayImage._lefteye)):
                        if self.displayImage._lefteye[i] != lefteye[i]:
                            #checks if lefteye is the same
                            # print('Difference Found in boundingbox')
                            # print('self.displayImage._lefteye = ', self.displayImage._lefteye)
                            # print('lefteye = ', lefteye)
                            currently_Saved = False
                if currently_Saved == True:
                    #only checks if no differences are found in shape
                    for i in range(len(self.displayImage._boundingbox)):
                        if self.displayImage._boundingbox[i] != boundingbox[i]:
                            #checks if lefteye is the same
                            # print('Difference Found in boundingbox')
                            # print('self.displayImage._boundingbox = ', self.displayImage._boundingbox)
                            # print('boundingbox = ', boundingbox)
                            currently_Saved = False
                
                if currently_Saved == False:
                    #If difference is found ask if the user wants to be saved
                    saveDotsQuestion = QtWidgets.QMessageBox
                    saveDotsBox = saveDotsQuestion.question(self, 'Save Dots', 
                        'New Landmarks adjustments are currently not saved.\nWould you like to save the new Landmarks?', 
                        saveDotsQuestion.Yes | saveDotsQuestion.No) 
                    if saveDotsBox == saveDotsQuestion.Yes:
                        try:
                            self.save_results()
                        except Exception as e:
                            QtWidgets.QMessageBox.information(self, 'Error', 
                                f'Error in saving current Landmarks.',#\n Error message: {e}', 
                                QtWidgets.QMessageBox.Ok)
            else:
                saveDotsQuestion = QtWidgets.QMessageBox
                saveDotsBox = saveDotsQuestion.question(self, 'Save Dots', 
                    'The Landmarks are currently not saved.\nWould you like to save the current Landmarks?', 
                    saveDotsQuestion.Yes | saveDotsQuestion.No) 
                if saveDotsBox == saveDotsQuestion.Yes:
                    try:
                        self.save_results()
                    except Exception as e:
                        QtWidgets.QMessageBox.information(self, 'Error', 
                            f'Error in saving current Landmarks.',#\n Error message: {e}', 
                            QtWidgets.QMessageBox.Ok)
        except:
            print('Error in verifying save')
            # QtWidgets.QMessageBox.information(self, 'Error', 
            #     'Error in verifying saved Landmarks.', 
            #     QtWidgets.QMessageBox.Ok)


    def previous(self):
        """This function is used to close the window.
        It verifies the the landmarks are saved then closes the window and goes back to the home window"""
        # self.verifySave()
                        
        self.finished.emit()
        self.close()

    
    def closeEvent(self, event):
        """This function is used to close the program.
        It verifies the the landmarks are saved then closes the program"""
        self.verifySave()
        if self._IsMainWindow == False:
            self.finished.emit()
        event.accept()



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SinglePhotoWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()