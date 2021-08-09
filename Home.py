import sys
from PyQt5 import QtWidgets, uic
from SinglePhotoWindow import SinglePhotoWindow
from DoublePhotoWindow import DoublePhotoWindow
from DoubleSelectionWindow import DoubleSelectionWindow
from SingleSelectionWindow import SingleSelectionWindow

class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(HomeWindow, self).__init__(*args, **kwargs)

        self.ui = uic.loadUi('uis/Home.ui', self)
        
        self.pushButton.clicked.connect(self.load_SinglePhotoWindow)
        self.pushButton_2.clicked.connect(self.load_DoublePhotoWindow)

    def load_SinglePhotoWindow(self):
        self._new_window = SinglePhotoWindow()
        #Opens selection window before showing window
        self._selection_window = SingleSelectionWindow()
        self._selection_window.show()
        self._selection_window.file.connect(self._new_window.setPhoto)
        self._selection_window.reference_Side.connect(self._new_window.setReferenceSide)
        self._selection_window.taskName.connect(self._new_window.setTaskName)
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
        #Opens selection window before showing window
        self._selection_window = DoubleSelectionWindow()
        self._selection_window.show()
        self._selection_window.file1.connect(self._new_window.setPhoto1)
        self._selection_window.file2.connect(self._new_window.setPhoto2)
        self._selection_window.reference_Side.connect(self._new_window.setReferenceSide)
        self._selection_window.task.connect(self._new_window.setTask)
        self._selection_window.taskName.connect(self._new_window.setTaskName)
        #Show window when selection is finally finished
        self._selection_window.finished.connect(self._new_window.show)
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