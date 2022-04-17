
import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow,
                             QWidget, QCheckBox, QPushButton, QSlider, QLabel, 
                             QVBoxLayout, QHBoxLayout, QFormLayout)
from PyQt5.Qt import Qt

import pyvista as pv
from pyvistaqt import QtInteractor

from library.ui import qt_objects as QtO
from library.ui.options_panel import OptionsPanel
from library import helpers
from library.plot_actors import PlotActor
                             

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clipping Demo")
        
        # Set up app layout
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)
        self.pageLayout = QVBoxLayout(self.centralWidget)
        
        # Create plotter
        self.plotter = QtInteractor(self)
        self.plotActor = PlotActor(self.plotter)
        
        # Create options panel
        self.optionsPanel = OptionsPanel(self.plotter, self.plotActor)
    
        # Add items to the window
        self.pageLayout.addWidget(self.plotter)
        self.pageLayout.addWidget(self.optionsPanel, alignment=Qt.AlignCenter)
        
        return

        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())