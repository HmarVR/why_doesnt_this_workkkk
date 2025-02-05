from src.loader import *
from engine.fbo import Framebuffers
import time

class SpaceScene:
    def __init__(self, app):
        self.app = app
        self.mesh = app.mesh
        self.ctx:mgl.Context = app.ctx
        self.opaque_objects = []
        self.tp_objects = []
        self.load()
        self.bg = Background(app)
        self.fbo = self.mesh.vao.Framebuffers.framebuffers["default"]
        self.blit_img = self.fbo.image_out[0]
        self.pr = ProcessRender(app)
        
    def add_opaque_object(self, obj):
        self.opaque_objects.append(obj)

    def add_tp_object(self, obj):
        self.tp_objects.append(obj)

    def load(self):
        self.add_opaque_object(Sun(self.app))
        self.add_tp_object(SpaceMenu(self.app))
        self.add_tp_object(SpaceShip(self.app))

    def update(self):
        self.ctx.new_frame()
        self.fbo.image_out[0].clear()
        self.fbo.depth_out.clear()
        for obj in self.opaque_objects:
            obj.update()

        self.bg.render()
  
        for obj in self.tp_objects:
            obj.update()
            
        self.pr.render()
        self.ctx.end_frame()
        
    def destroy(self):
        for obj in self.opaque_objects:
            obj.destroy()
        for obj in self.tp_objects:
            obj.destroy()