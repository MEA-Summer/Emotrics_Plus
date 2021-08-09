import numpy as np
from PyQt5 import QtWidgets, QtGui, uic, QtCore
import sys
import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure
from Metrics import get_measurements_from_data
from Compute_eFace import Compute_Resting_eFace


class NavigationToolbar(NavigationToolbar2QT):
    # only display the buttons we need
    toolitems = [t for t in NavigationToolbar2QT.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class Auto_eFaceWindow(QtWidgets.QMainWindow):
    
    def __init__(self, shape, left_pupil, right_pupil, points, CalibrationType, CalibrationValue, reference_side, file_name, expression):
        super() .__init__()
        self._shape = shape
        self._lefteye = left_pupil
        self._righteye = right_pupil
        self._points = points
        self._CalibrationType = CalibrationType
        self._CalibrationValue = CalibrationValue
        self._reference_side = reference_side
        self._fileName = file_name
        self._expression = expression


        self.initUI()
        
        
    def initUI(self):
        sc = MplCanvas(self, width=10, height=4, dpi=100)

        ##############
        """Plotting"""
        ##############
        if self._expression == 'Resting':
            (MeasurementsLeft, MeasurementsRight, 
            MeasurementsDeviation, MeasurementsPercentual) = get_measurements_from_data(
                self._shape, self._lefteye, self._righteye, self._points, 
                self._CalibrationType, self._CalibrationValue, self._reference_side)
            Resting_Brow, Resting_Palpebral_Fissure, Oral_Commisure_at_Rest = Compute_Resting_eFace(MeasurementsLeft, MeasurementsRight, self._reference_side)
            x = ['Resting Brow', 'Resting Palpebral Fissure', 'Oral Commisure at Rest']

            y = [Resting_Brow, Resting_Palpebral_Fissure, Oral_Commisure_at_Rest]

            x_pos = [i for i, _ in enumerate(x)]

            sc.axes.bar(x, y, color='blue')
            sc.axes.set_xlabel('Parameters')
            sc.axes.set_ylabel('Auto-eFace Score')
            sc.axes.set_title('Static Parameters')
            sc.axes.set_ylim(0,200)

            # sc.axes.xaxis.set_ticks(x_pos, x)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

