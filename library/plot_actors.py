import vtk
class PlotActor:
    def __init__(self, plotter):
        self.plotter = plotter
        self.reset()
        return

    def load_original(self, mesh):
        self.original = mesh
        self.bounds = mesh.bounds
    
    def reset(self):
        self.original = None
        self.clipped = None
        self.bounds = [0, 10, 0, 10, 0, 10]
        

class ClippingBox(vtk.vtkBoxWidget):
    def __init__(self, plotter, plotActor):
        super().__init__()
        self.plotter = plotter
        self.plotActor = plotActor
        self.realtime_clipping = False
        
        self.HandlesOff()
        self.GetHandleProperty().SetOpacity(0)
        self.GetOutlineProperty().SetColor((1,1,1))
        self.SetInteractor(plotter.iren.interactor)
        self.SetCurrentRenderer(plotter.renderer)
        self.SetPlaceFactor(1)
        self.SetRotationEnabled(False)
        self.SetTranslationEnabled(True)
        self.PlaceWidget([0, 1, 0, 1, 0, 1])
        self.On()
        # self.AddObserver(vtk.vtkCommand.EndInteractionEvent, self.pass_planes)
        # _the_callback(box_widget, None)
        
        self.toggle_opacity(False)
        
    def update_position(self, bounds):
        self.PlaceWidget(bounds)
        self.bounds = bounds
        self.plotter.update()
        if self.realtime_clipping:
            self.update_mesh_clip()
                
    def update_mesh_clip(self):
        new_clipped = self.plotActor.original.clip_box(self.bounds, invert=False)
        
        self.plotter.remove_actor(self.plotActor.clipped)
        self.plotActor.clipped = self.plotter.add_mesh(new_clipped,
                                                       smooth_shading=True,
                                                        show_scalar_bar=False,
                                                        reset_camera=False)
    
    def reset_mesh_clip(self):
        self.bounds = self.plotActor.original.bounds
        self.update_mesh_clip()
        self.plotter.reset_camera()
        
    def toggle_opacity(self, in_view=False):
        self.GetOutlineProperty().SetOpacity(int(in_view))
        if not in_view:
            self.Off()
        else:
            self.On()

        