import sys
from PyQt5 import QtWidgets, uic
from SinglePhotoWindow import SinglePhotoWindow
from DoublePhotoWindow import DoublePhotoWindow


class HomeWindow(QtWidgets.QMainWindow):
    def __init__(self, *args, **kwargs):
        super(HomeWindow, self).__init__(*args, **kwargs)

        self.ui = uic.loadUi('Home.ui', self)
        
        
        self.pushButton.clicked.connect(self.load_SinglePhotoWindow)
        self.pushButton_2.clicked.connect(self.load_DoublePhotoWindow)

    def load_SinglePhotoWindow(self):
        self = SinglePhotoWindow(self)
        self.show()

    def load_DoublePhotoWindow(self):
        self = DoublePhotoWindow(self)
        self.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = HomeWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()