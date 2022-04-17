from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QFormLayout,
                             QPushButton, QCheckBox, QSlider, QDoubleSpinBox,
                             QFrame, QRadioButton)
from pytools import F


def convert_alignment(alignment):
    """Converts a text alignment direction to a Qt alignment
    
    Parameters
    ----------
    alignment: str
        'left', 'right', 'center'
        
    Returns
    -------
    Qt.AlignmentFlag
    
    """
    if not isinstance(alignment, str):
        TypeError('Alignment must be passed as a string')
    elif alignment not in ['left', 'right', 'center']:
        ValueError("alignment must be passed as a string with one of the following values:\n"
                   "'left', 'right', 'center'")
        
    if alignment == 'left':
        alignmentFlag = Qt.AlignLeft
    elif alignment == 'right':
        alignmentFlag = Qt.AlignRight
    elif alignment == 'center':
        alignmentFlag = Qt.AlignCenter
        
    return alignmentFlag

def add_widgets(layout, widgets, alignment='center'):
    """Given a layout and widgets, adds the widgets to the layout
    
    Parameters
    ----------
    layout: QBoxLayout
    
    widgets: 2D list or tuple of QWidget objects or integers for spacing
        - 0 is used to add a strecth to the layout
        - Integers > 0 are used for spacing
        
    
    alignment: str, optional
        Text-based alignmnet instructinos for the widgets
    
    """
    
    alignmentFlag = convert_alignment(alignment)
    for item in widgets:
        if isinstance(item, int):
            if item:
                layout.addSpacing(item)
            else:
                layout.addStretch(item)
        else:
            if type(item) == QFrame:

                layout.addWidget(item)
            else:
                layout.addWidget(item, alignment=alignmentFlag)
    
    return

def dividing_line(orientation='horizontal', size=None):
    """Creates a boundary line to visually separate widgets
    
    Parameters
    ----------
    orientation: str
        Default: 'horizontal'
        Options: 'horizontal', 'vertical'
    
    size: int, optional
    
    Returns
    -------
    QFrame
        
    """
    
    line = QFrame()
    if not isinstance(orientation, str):
        TypeError("Orientation must be a string of either:\n"
                  "'horizontal' or 'vertical'")
    if orientation not in ['horizontal', 'vertical']:
        ValueError("Orientation must be a string of either:\n"
                  "'horizontal' or 'vertical'")
        
    if orientation == 'horizontal':
        shape = QFrame.HLine
    elif orientation == 'vertical':
        shape = QFrame.VLine
        
    if size:
        line.setFixedWidth(size)
        
    line.setFrameShape(shape)
    line.setFrameShadow(QFrame.Sunken)
    
    return line

def new_doublespin(minimum, maximum, starting_value=0, width=100, 
                   alignment='left', decimals=1, suffix=None, callback=None):
    """Creates a new QDoubleSpinBox object
    
    Parameters
    ----------
    minimum: int, float
    
    maximum: int, float
    
    starting_value: int, float, optional
        Default starting value of the box
        
    width: int, optional
        Fixed width of the box
        
    alignment: str, optional
        Alignment of the text within the box.
        Options: 'left', 'right', 'center'
        
    decimals: int, optionals
        Number of digits following the decimal point
    
    suffix: str, optional
        Suffix to be placed after the value in the box
        
    callback: callback function, optional
        Callback function to be evoked on 'valueChanged'
    
    Returns
    -------
    QDoubleSpinBox
    
    """
    doublespin = QDoubleSpinBox()
    doublespin.setMinimum(minimum)
    doublespin.setMaximum(maximum)
    doublespin.setDecimals(decimals)
    doublespin.setAlignment(convert_alignment(alignment))
    
    if starting_value:
        doublespin.setValue(starting_value)
    
    if suffix:
        doublespin.setSuffix(suffix)
    
    if callback:
        doublespin.valueChanged.connect(callback)
    
    if width:
        doublespin.setFixedWidth(width)
        
    return doublespin

def new_pushbutton(title, callback):
    """Creates a new QPushButton
    
    Parameters
    ----------
    title: str
    
    callback: function
    
    Returns
    -------
    QPushButton
    """
    button = QPushButton(title)
    button.clicked.connect(callback)
    
    return button

def new_checkbox(title, callback):
    """Creates a new QCheckBox
    
    Parameters
    ----------
    title: str
    
    callback: function
    
    Returns
    -------
    QCheckBox
    """
    box = QCheckBox(title)
    box.stateChanged.connect(callback)
    return box
    

def new_radio(title, callback, checked=False):
    """Creats a QRadioButton
    
    Parameters
    ----------
    title: str
    
    callback: function
    
    Returns
    -------
    QRadioButton
    
    """
    radio = QRadioButton(title)
    if checked:
        radio.setChecked(True)
    
    radio.toggled.connect(callback)
    return radio
    
    
def connect_button(button, callback):
    """Connects a QPushButton to specific callback function or list of functions
    
    Parameters
    ----------
    button: QPushButton
    
    callback: callback function, or list or tuple of function
    
    """
    if not isinstance(callback, (list, tuple)):
        callback = [callback]
        
    for call in callback:
        button.clicked.connect(call)