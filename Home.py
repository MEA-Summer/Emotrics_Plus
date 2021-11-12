import sys
from PyQt5 import QtWidgets, uic
import numpy as np
import torch
from face_alignment.detection.blazeface.net_blazeface import BlazeFace
from lib.models import get_face_alignment_net
from lib.config import config, merge_configs
from arch.FAN import FAN
from arch.resnest.HeatMaps import model_resnest
from models.irislandmarks import IrisLandmarks
from SinglePhotoWindow import SinglePhotoWindow
from DoublePhotoWindow import DoublePhotoWindow
from DoubleSelectionWindow import DoubleSelectionWindow
from SingleSelectionWindow import SingleSelectionWindow
from SevenPhotoWindow import SevenPhotoWindow
from SevenSelectionWindow import SevenSelectionWindow

class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(HomeWindow, self).__init__(*args, **kwargs)

        self.ui = uic.loadUi('uis/Home.ui', self)
        
        self.pushButton.clicked.connect(self.load_SinglePhotoWindow)
        self.pushButton_2.clicked.connect(self.load_DoublePhotoWindow)
        self.pushButton_3.clicked.connect(self.load_SevenPhotoWindow)


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
        model_NLF.load_state_dict(torch.load('./arch/heatmap_NSLF_3.pth', map_location=torch.device('cpu')))
        model_NLF.eval();
        self.model_NLF = model_NLF
        
        #Eye Model
        device = 'cpu'
        self.net = IrisLandmarks().to(device)
        self.net.load_weights('./models/irislandmarks.pth')

    def load_SinglePhotoWindow(self):
        self._new_window = SinglePhotoWindow()
        self._new_window._IsMainWindow = True #informs window it is made by HomeWindow not SevenPhotoWindow
        self._new_window.FaceAlignment = self.FaceAlignment
        self._new_window.FaceDetector = self.FaceDetector
        self._new_window.model = self.model
        self._new_window.model_FAN = self.model_FAN
        self._new_window.model_NLF = self.model_NLF
        self._new_window.net = self.net
        #Opens selection window before showing window
        self._selection_window = SingleSelectionWindow()
        self._selection_window.show()
        self._selection_window.file.connect(self._new_window.setPhoto)
        self._selection_window.reference_Side.connect(self._new_window.setReferenceSide)
        self._selection_window.taskName.connect(self._new_window.setTaskName)
        self._selection_window.patientID.connect(self._new_window.setPatientID)
        #Show window when selection is finally finished
        self._selection_window.finished.connect(self._new_window.show)
        #Hides Home window until the previous button is hit
        self.setVisible(False)
        self._selection_window.canceled.connect(self._new_window.close)
        self._selection_window.canceled.connect(self.showHomeWindow)
        self._new_window.finished.connect(self._new_window.close)
        self._new_window.finished.connect(self.showHomeWindow)

    def load_DoublePhotoWindow(self):
        self._new_window = DoublePhotoWindow()
        self._new_window.FaceAlignment = self.FaceAlignment
        self._new_window.FaceDetector = self.FaceDetector
        self._new_window.model = self.model
        self._new_window.model_FAN = self.model_FAN
        self._new_window.model_NLF = self.model_NLF
        self._new_window.net = self.net
        #Opens selection window before showing window
        self._selection_window = DoubleSelectionWindow()
        self._selection_window.show()
        self._selection_window.file1.connect(self._new_window.setPhoto1)
        self._selection_window.file2.connect(self._new_window.setPhoto2)
        self._selection_window.reference_Side.connect(self._new_window.setReferenceSide)
        self._selection_window.task.connect(self._new_window.setTask)
        self._selection_window.taskName.connect(self._new_window.setTaskName)
        self._selection_window.patientID.connect(self._new_window.setPatientID)
        #Show window when selection is finally finished
        self._selection_window.finished.connect(self._new_window.show)
        #Hides Home window until the previous button is hit
        self.setVisible(False)
        self._selection_window.canceled.connect(self._new_window.close)
        self._selection_window.canceled.connect(self.showHomeWindow)
        self._new_window.finished.connect(self._new_window.close)
        self._new_window.finished.connect(self.showHomeWindow)

    def load_SevenPhotoWindow(self):
        self._new_window = SevenPhotoWindow()
        """Fill models"""
        #Resting
        self._new_window.restingWindow.FaceAlignment = self.FaceAlignment
        self._new_window.restingWindow.FaceDetector = self.FaceDetector
        self._new_window.restingWindow.model = self.model
        self._new_window.restingWindow.model_FAN = self.model_FAN
        self._new_window.restingWindow.model_NLF = self.model_NLF
        self._new_window.restingWindow.net = self.net
        #Brow Raise 
        self._new_window.browRaiseWindow.FaceAlignment = self.FaceAlignment
        self._new_window.browRaiseWindow.FaceDetector = self.FaceDetector
        self._new_window.browRaiseWindow.model = self.model
        self._new_window.browRaiseWindow.model_FAN = self.model_FAN
        self._new_window.browRaiseWindow.model_NLF = self.model_NLF
        self._new_window.browRaiseWindow.net = self.net
        #Gentle Eye Closure
        self._new_window.GentleEyeClosureWindow.FaceAlignment = self.FaceAlignment
        self._new_window.GentleEyeClosureWindow.FaceDetector = self.FaceDetector
        self._new_window.GentleEyeClosureWindow.model = self.model
        self._new_window.GentleEyeClosureWindow.model_FAN = self.model_FAN
        self._new_window.GentleEyeClosureWindow.model_NLF = self.model_NLF
        self._new_window.GentleEyeClosureWindow.net = self.net
        #Tight Eye Closure
        self._new_window.TightEyeClosureWindow.FaceAlignment = self.FaceAlignment
        self._new_window.TightEyeClosureWindow.FaceDetector = self.FaceDetector
        self._new_window.TightEyeClosureWindow.model = self.model
        self._new_window.TightEyeClosureWindow.model_FAN = self.model_FAN
        self._new_window.TightEyeClosureWindow.model_NLF = self.model_NLF
        self._new_window.TightEyeClosureWindow.net = self.net
        #Big Smile
        self._new_window.BigSmileWindow.FaceAlignment = self.FaceAlignment
        self._new_window.BigSmileWindow.FaceDetector = self.FaceDetector
        self._new_window.BigSmileWindow.model = self.model
        self._new_window.BigSmileWindow.model_FAN = self.model_FAN
        self._new_window.BigSmileWindow.model_NLF = self.model_NLF
        self._new_window.BigSmileWindow.net = self.net
        #"eeeek"
        self._new_window.eeeekWindow.FaceAlignment = self.FaceAlignment
        self._new_window.eeeekWindow.FaceDetector = self.FaceDetector
        self._new_window.eeeekWindow.model = self.model
        self._new_window.eeeekWindow.model_FAN = self.model_FAN
        self._new_window.eeeekWindow.model_NLF = self.model_NLF
        self._new_window.eeeekWindow.net = self.net
        #"ooooo"
        self._new_window.oooooWindow.FaceAlignment = self.FaceAlignment
        self._new_window.oooooWindow.FaceDetector = self.FaceDetector
        self._new_window.oooooWindow.model = self.model
        self._new_window.oooooWindow.model_FAN = self.model_FAN
        self._new_window.oooooWindow.model_NLF = self.model_NLF
        self._new_window.oooooWindow.net = self.net

        #Opens selection window before showing window
        self._selection_window = SevenSelectionWindow()
        self._selection_window.show()
        self._selection_window.file_R.connect(self._new_window.setPhoto_R)
        self._selection_window.file_BR.connect(self._new_window.setPhoto_BR)
        self._selection_window.file_GEC.connect(self._new_window.setPhoto_GEC)
        self._selection_window.file_TEC.connect(self._new_window.setPhoto_TEC)
        self._selection_window.file_BS.connect(self._new_window.setPhoto_BS)
        self._selection_window.file_eeeek.connect(self._new_window.setPhoto_eeeek)
        self._selection_window.file_ooooo.connect(self._new_window.setPhoto_ooooo)
        self._selection_window.reference_Side.connect(self._new_window.setReferenceSide)
        self._selection_window.patientID.connect(self._new_window.setPatientID)
        #Show window when selection is finally finished
        self._selection_window.finished.connect(self._new_window.show)
        self._selection_window.finished.connect(self._new_window.update_Plots)
        #Hides Home window until the previous button is hit
        self.setVisible(False)
        self._selection_window.canceled.connect(self._new_window.close)
        self._selection_window.canceled.connect(self.showHomeWindow)
        self._new_window.finished.connect(self._new_window.close)
        self._new_window.finished.connect(self.showHomeWindow)

    def showHomeWindow(self):
        self.setVisible(True)
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = HomeWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()