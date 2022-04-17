from PyQt5.QtWidgets import (QGroupBox, QVBoxLayout, QHBoxLayout, 
                             QWidget, QCheckBox, QPushButton, QLabel,
                             QRadioButton)
from PyQt5.QtCore import Qt, pyqtSlot

import pyvista as pv

from library import plot_actors
from library.ui import qt_objects as QtO
from library.ui.slider_widgets import DoubleSliderWidget, SliderWidget
from library import helpers
                             
## Bottom (HBox)
# Left: Generate new grid
# Center: Clipping
# Right: Scaling

class MeshRendering(QWidget):
    def __init__(self, plotter, plotActor):
        super().__init__()
        self.plotter = plotter
        self.plotActor = plotActor
        self.slicers = []
        
        layout = QVBoxLayout(self)
        
        # Mesh Visualization
        meshTitle = QLabel("<b>Mesh Rendering")
        self.noMesh = QtO.new_radio('None', self.toggle_mesh, checked=True)
        self.tubeMesh = QtO.new_radio('Tube', self.toggle_mesh)
        self.gridMesh = QtO.new_radio('Grid', self.toggle_mesh)
        self.footMesh = QtO.new_radio('Foot Bones', self.toggle_mesh)
        self.stHelensMesh = QtO.new_radio("Mount St. Helens", self.toggle_mesh)
        self.brainMesh = QtO.new_radio("Brain", self.toggle_mesh)
        self.laurentMesh = QtO.new_radio("Laurent Lattice", self.toggle_mesh)
        
        # Plotter Options
        plotterTitle = QLabel("<b>Plotter Options")
        self.showGrid = QtO.new_checkbox('Show Grid', self.toggle_grid)
        self.showBounds = QtO.new_checkbox('Show Bounds', self.toggle_bounds)
        
        items = [meshTitle, self.noMesh, self.tubeMesh, self.gridMesh, 
                 self.stHelensMesh, self.footMesh, self.stHelensMesh,
                 self.brainMesh, self.laurentMesh, 5,
                 plotterTitle, self.showGrid, self.showBounds]
        QtO.add_widgets(layout, items)
        
    # Mesh Options
    @pyqtSlot()
    def toggle_mesh(self):
        if not self.sender().isChecked():
            return
        
        # Clear the actor 
        self.plotter.reset_camera()
        self.plotter.remove_actor(self.plotActor.clipped)
        self.toggle_plotter_options(self.noMesh.isChecked()) # Toggle options
        
        if self.noMesh.isChecked():
            self.plotActor.reset() # Reset the actor
            return
        
        # Add new mesh to the actor
        if self.tubeMesh.isChecked():
            self.plotActor.original = helpers.load_tube()
        elif self.gridMesh.isChecked():
            self.plotActor.original = helpers.load_grid()
        elif self.footMesh.isChecked():
            self.plotActor.original = helpers.load_foot()
        elif self.stHelensMesh.isChecked():
            self.plotActor.original = helpers.load_st_helens()
        elif self.brainMesh.isChecked():
            self.plotActor.original = helpers.load_brain()
        elif self.laurentMesh.isChecked():
            self.plotActor.original = helpers.load_Laurent_lattice()
            
        
        # Add new actor to the scene
        if self.plotActor.original:
            self.plotActor.clipped = self.plotter.add_mesh(self.plotActor.original,
                                                        smooth_shading=True,
                                                        show_scalar_bar=False)
        
        self.update_clip_bounds(self.plotActor.original.bounds)
        return

    def toggle_new_grid(self, locked):
        self.newGrid.setEnabled(locked)   
    
    # Plotter Options
    def toggle_plotter_options(self, locked):
        if locked:
            self.showGrid.setChecked(False)
            self.showBounds.setChecked(False)
        self.showGrid.setDisabled(locked)
        self.showBounds.setDisabled(locked)
        
        self.toggle_slicers(locked)
    
    def toggle_grid(self):
        if self.showGrid.isChecked():
            self.plotter.show_grid(location='outer')
        else:
            self.plotter.remove_bounds_axes()
    
    def toggle_bounds(self):
        if self.showBounds.isChecked():
            self.plotter.add_bounding_box(reset_camera=False)
        else:
            self.plotter.remove_bounding_box()
            
    # Slicing Control
    def connect_slicer(self, toggle_function, bound_function):
        self.toggle_slicers = toggle_function
        self.update_clip_bounds = bound_function
    
    


class SlicingControl(QWidget):
    def __init__(self, plotter, plotActor):
        super().__init__()
        self.plotter = plotter
        self.plotActor = plotActor
        self.boxWidget = plot_actors.ClippingBox(self.plotter, self.plotActor)
        
        middleLayout = QVBoxLayout(self)
        middleLayout.setSpacing(0)
        clippingLabel = QLabel("<b>Axis Clipping")
        
        self.clipRealTime = QtO.new_checkbox('Real-time Clipping', 
                                            self.toggle_realtime)
        
        self.xClipWidget = DoubleSliderWidget('X Plane: ', self.boxWidget,
                                              self.update_slicing_box_position)
        self.yClipWidget = DoubleSliderWidget('Y Plane: ', self.boxWidget,
                                              self.update_slicing_box_position)
        self.zClipWidget = DoubleSliderWidget('Z Plane: ', self.boxWidget,
                                              self.update_slicing_box_position)
        
        self.slicers = [self.xClipWidget, self.yClipWidget, self.zClipWidget]

        self.resetClip = QPushButton("Reset Clipping")
        QtO.connect_button(self.resetClip, [self.xClipWidget.reset_values,
                                            self.yClipWidget.reset_values,
                                            self.zClipWidget.reset_values,
                                            self.reset_clipping])
        
        middle_widgets = [clippingLabel, self.clipRealTime,
                          self.xClipWidget, self.yClipWidget, 
                          self.zClipWidget, self.resetClip]
        QtO.add_widgets(middleLayout, middle_widgets)
        
    def toggle_slicers(self, locked):
        for slicer in self.slicers:
            slicer.setDisabled(locked)
            
    def toggle_realtime(self):
        self.boxWidget.realtime_clipping = self.clipRealTime.isChecked()
       
    def reset_clipping(self):
        self.boxWidget.reset_mesh_clip()
        return
    
    def update_clip_ranges(self, bounds):
        self.xClipWidget.update_minmax(bounds[0], bounds[1])
        self.yClipWidget.update_minmax(bounds[2], bounds[3])
        self.zClipWidget.update_minmax(bounds[4], bounds[5])
        
    def update_slicing_box_position(self):
        xmin, xmax = self.xClipWidget.return_value()
        ymin, ymax = self.yClipWidget.return_value()
        zmin, zmax = self.zClipWidget.return_value()
        bounds = [xmin, xmax, ymin, ymax, zmin, zmax]
        self.boxWidget.update_position(bounds)
        

class ScalingControl(QWidget):
    def __init__(self, plotter):
        super().__init__()
        self.plotter = plotter
        rightLayout = QVBoxLayout(self)
        rightLayout.setSpacing(0)
        scalingLabel = QLabel("<b>Plot Scaling")
        
        self.xScalingWidget = SliderWidget("X Scale: ", self.plotter, 0)
        self.yScalingWidget = SliderWidget("Y Scale: ", self.plotter, 1)
        self.zScalingWidget = SliderWidget("Z Scale: ", self.plotter, 2)
        
        self.resetScale = QPushButton("Reset Scale")
        QtO.connect_button(self.resetScale, [self.xScalingWidget.reset_values,
                                             self.yScalingWidget.reset_values,
                                             self.zScalingWidget.reset_values])
        
        right_widgets = [scalingLabel, 
                        self.xScalingWidget, self.yScalingWidget, 
                        self.zScalingWidget, self.resetScale]
        QtO.add_widgets(rightLayout, right_widgets)        


class OptionsPanel(QGroupBox):
    def __init__(self, plotter, plotActor):
        super().__init__()
        self.plotter = plotter
        self.plotActor = plotActor
        
        self.panelLayout = QHBoxLayout(self)
        
        ### Left Panel - Mesh and Plotter Options ###
        leftWidget = MeshRendering(self.plotter, self.plotActor)
        
        ### Middle Pannel - Mesh Clipping Controls ###
        middleWidget = SlicingControl(self.plotter, self.plotActor)
        leftWidget.connect_slicer(middleWidget.toggle_slicers,
                                  middleWidget.update_clip_ranges)
        leftWidget.toggle_plotter_options(True)

        ### Right Pannel - Plotter Scaling ###
        rightWidget = ScalingControl(self.plotter)
        
        panel_widgets = [0, leftWidget, QtO.dividing_line('vertical', 2),
                         middleWidget, QtO.dividing_line('vertical', 2),
                         rightWidget, 0]
        QtO.add_widgets(self.panelLayout, panel_widgets)
        return