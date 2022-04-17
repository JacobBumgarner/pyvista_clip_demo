from math import ceil, floor

from PyQt5.QtWidgets import (QWidget, QDoubleSpinBox, QHBoxLayout,
                             QLineEdit, QSlider, QLabel)
from PyQt5.QtCore import Qt
from qtrangeslider import QRangeSlider


from library.ui import qt_objects as QtO


class SliderWidget(QWidget):
    def __init__(self, header_text, plotter, axis=0):
        super().__init__()
        self.axis = axis
        self.plotter = plotter
        
        # Widget Layout
        layout = QHBoxLayout(self)
        
        self.header = QLabel(header_text)
        
        self.spin = QtO.new_doublespin(0.1, 10, 1, width=60, 
                                       callback=self.box_update)
        self.spin.valueChanged.connect(self.box_update)
        
        self.slider = QSlider(orientation=Qt.Horizontal)
        self.slider.setMinimum(1)
        self.slider.setMaximum(100)
        self.slider.setFixedWidth(100)
        self.slider.setFixedHeight(30)
        self.slider.setValue(10)
        
        self.slider.valueChanged.connect(self.slider_update)
        
        QtO.add_widgets(layout, [self.header, self.spin, self.slider])

    def box_update(self):
        self.toggle_blocks(True)
        self.slider.setValue(self.spin.value() * 10)
        self.toggle_blocks(False)
        self.update_plotter_scale()
        
    def slider_update(self):
        self.toggle_blocks(True)
        self.spin.setValue(self.slider.value() / 10)
        self.toggle_blocks(False)
        self.update_plotter_scale()
        
    def update_plotter_scale(self):
        current_scale = self.plotter.scale
        current_scale[self.axis] = self.spin.value()
        self.plotter.set_scale()
        self.plotter.update()

    def reset_values(self):
        self.slider.setValue(10)
        self.plotter.reset_camera()
        
    def toggle_blocks(self, block):
        self.slider.blockSignals(block)
        self.spin.blockSignals(block)


class DoubleSliderWidget(QWidget):
    def __init__(self, header_text, boxWidget, box_update):
        super().__init__()
        self.boxWidget = boxWidget
        
        self.axis_range = 10
        self.minimum = 0
        self.maximum = 10
        
        layout = QHBoxLayout(self)
        
        self.header = QLabel(header_text)
        
        # Spins
        self.leftSpin = QtO.new_doublespin(0, 9.9, 
                                           width=60, decimals=1,
                                           callback=self.box_update)
        self.rightSpin = QtO.new_doublespin(0.1, 10, starting_value=10,
                                            width=60, decimals=1,
                                            callback=self.box_update)
        # Connect the spinners
        self.leftSpin.valueChanged.connect(box_update)
        self.leftSpin.valueChanged.connect(self.boxWidget.update_mesh_clip)
        
        self.rightSpin.valueChanged.connect(box_update)
        self.rightSpin.valueChanged.connect(self.boxWidget.update_mesh_clip)
        
        
        # Slider
        self.slider = QRangeSlider(orientation=Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setFixedWidth(200)
        self.slider.setFixedHeight(40)
        self.slider.setValue((0, 100))
        
        # Connect the slider 
        self.slider.sliderPressed.connect(self.pressed_action)
        self.slider.sliderReleased.connect(self.released_action)
        self.slider.valueChanged.connect(box_update)
        self.slider.valueChanged.connect(self.slider_update)
        
        QtO.add_widgets(layout, [self.header, self.leftSpin, self.slider, 
                                 self.rightSpin])
        
    def box_update(self):
        self.toggle_blocks(True)
        min_val = self.leftSpin.value()
        max_val = self.rightSpin.value()
        if min_val > max_val:
            max_val = min_val + 0.1
            self.rightSpin.setValue(max_val)
        elif max_val <= min_val:
            min_val = max_val - 0.1
            self.leftSpin.setValue(min_val)
        
        slider_max = (max_val - self.min_val) / self.axis_range * 100
        slider_min = (min_val - self.min_val) / self.axis_range * 100
        self.slider.setValue((slider_min, slider_max))
        
        self.toggle_blocks(False)
    
    def slider_update(self):
        self.toggle_blocks(True)
        min_val, max_val = self.slider.value()
        
        if min_val == 0:
            min_val = self.min_val
        else:
            # print (type(min_val), type(self.axis_range), type(self.min_val))
            min_val = min_val / 100 * self.axis_range + self.min_val
        if max_val == 100:
            max_val = self.max_val
        else:
            max_val = max_val / 100 * self.axis_range + self.min_val
        

        self.leftSpin.setValue(min_val)
        self.rightSpin.setValue(max_val)
        self.toggle_blocks(False)

    def update_minmax(self, min_val, max_val):
        min_val = floor(min_val*100)/100 - 0.1
        max_val = ceil(max_val*100)/100 + 0.1
        self.axis_range = max_val - min_val
        self.min_val = min_val
        self.max_val = max_val
        
        self.toggle_blocks(True)
        self.slider.setValue((0, 100))
        
        self.leftSpin.setMinimum(min_val)
        self.leftSpin.setMaximum(max_val-0.1)
        self.rightSpin.setMinimum(min_val+0.1)
        self.rightSpin.setMaximum(max_val)
        self.leftSpin.setValue(min_val)
        self.rightSpin.setValue(max_val)
        self.toggle_blocks(False)
        return
    
    def reset_values(self):
        self.toggle_blocks(True)
        self.slider.setValue((self.slider.minimum(), self.slider.maximum()))
        self.leftSpin.setValue(self.leftSpin.minimum())
        self.rightSpin.setValue(self.rightSpin.maximum())
        self.toggle_blocks(False)
        
    def pressed_action(self):
        self.boxWidget.toggle_opacity(True)
    
    def released_action(self):
        self.boxWidget.toggle_opacity(False)
        self.boxWidget.update_mesh_clip()
        
    def return_value(self):
        min_val = self.leftSpin.value()
        max_val = self.rightSpin.value()
        return min_val, max_val
    
    def toggle_blocks(self, block=False):
        self.leftSpin.blockSignals(block)
        self.rightSpin.blockSignals(block)
        self.slider.blockSignals(block)