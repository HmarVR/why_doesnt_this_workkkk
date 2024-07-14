import numpy as np
import glm
import struct
import json
from engine.vbo import InstancingVBO

class TilemapForTrashDrivers:
    def __init__(self, app, tile_size=16):
        self.app = app
        self.ctx: mgl.Context = app.ctx
        self.tile_size = tile_size
        
        with open(f"./assets/json/tiles_list.json") as file:
            tiles_list = json.load(file)
            
        with open(f"./assets/json/decor_list.json") as file:
            decor_list = json.load(file)
            
        str_dict = {}
        giga_list = []
        j = 0
        
        for i in decor_list:
            str_dict[i] = j
            giga_list.append('AlbaseeProps/'+i)
            j += 1
            
        decorMax = j
            
            
        for i in tiles_list:
            str_dict[i] = j
            giga_list.append('tiles/'+i)
            j += 1
            
        str_dict['0'] = 0
        self.str_dict = str_dict
            
            
        with open(f"file.json") as file:
            self.tilemap = json.load(file)
            self.app.share_data['tilemap'] = self
            self.app.camera.freemove = False

        self.offgrid_tiles = []

        self.MAPSIZE = sum([len(tilemap_i) for tilemap_i in self.tilemap.values()])
        self.size = self.MAPSIZE + 256

        self.block_arr = np.zeros((self.size, 4), dtype="f4")
        
        giga_i = 0        
        for index, tilemap_i in reversed(self.tilemap.items()):
            for j in tilemap_i.items():
                key = j[0].split(";")
                print(key, int(index))
                self.block_arr[giga_i] = [int(key[0]), -int(key[1]), self.str_dict[str(j[1][4])], int(index)*0.1 ]
                giga_i += 1

        self.block_arr.reshape((self.size, 4))
        self.buffer = self.ctx.buffer(self.block_arr)

        self.ibo = InstancingVBO(self.ctx, self.buffer, "4f", "posOffset", offset=2)
        self.app.mesh.vao.vbo.vbos["mapIbo"] = self.ibo

        self.vao = app.mesh.vao.get_ins_vao(
            fbo=self.app.mesh.vao.Framebuffers.framebuffers["default"],
            program=self.app.mesh.vao.program.programs["tilemap"],
            vbo=self.app.mesh.vao.vbo.vbos["plane"],
            ibo=self.ibo,
            umap={
                "m_model": "mat4",
                "m_view": "mat4",
                "decor": "int",
            },
            tmap=["Tiles"],
        )
        self.app.mesh.vao.vaos["tiler"] = self.vao
        self.tex0 = app.mesh.texture.from_list("./assets/textures/", giga_list, '.png')
        self.app.mesh.texture.textures['Tiles'] = self.tex0
        self.vao.texture_bind(0, "Tiles", self.tex0)

        self.pos = glm.vec3(0)
        self.roll = 0
        self.scale = glm.vec2(self.tile_size/2)

        self.m_model = self.get_model_matrix()
        self.vao.uniform_bind("m_model", self.m_model.to_bytes())
        self.vao.uniform_bind("decor", decorMax)
        self.decorMax = decorMax
        self.app.camera.position.z = 120

    def update(self):
        self.vao.texture_bind(0, "Tiles", self.tex0)
        self.vao.uniform_bind(
            "m_view",
            (self.app.camera.m_proj * self.app.camera.m_view * self.m_model).to_bytes(),
        )
        self.vao.render(instance_count=self.MAPSIZE)

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, glm.radians(self.roll), glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, glm.vec3(self.scale[0], self.scale[1], 1))
        return m_model

    def render(self): ...
    
    def destroy(self):
        self.app.mesh.vao.del_vao('tiler')
        self.app.ctx.release(self.ibo)



class Tilemap:
    def __init__(self, app, tile_size=16):
        self.app = app
        self.ctx: mgl.Context = app.ctx
        self.tile_size = tile_size
        
        with open(f"./assets/json/tiles_list.json") as file:
            tiles_list = json.load(file)
            
        with open(f"./assets/json/decor_list.json") as file:
            decor_list = json.load(file)
            
        str_dict = {}
        giga_list = []
        j = 0
        
        for i in tiles_list:
            str_dict[i] = j
            j += 1
            
        decorMax = j
            
            
        for i in decor_list:
            str_dict[i] = j
            j += 1
            
        str_dict['0'] = 0
        self.str_dict = str_dict
        self.j = j
            
            
        with open(f"file.json") as file:
            self.tilemap = json.load(file)
            self.app.share_data['tilemap'] = self
            self.app.camera.freemove = False

        self.offgrid_tiles = []

        self.MAPSIZE = sum([len(tilemap_i) for tilemap_i in self.tilemap.values()])
        self.size = self.MAPSIZE + 256

        self.block_arr = np.zeros((self.size, 4), dtype="f4")
        
        giga_i = 0        
        for index, tilemap_i in reversed(self.tilemap.items()):
            for j in tilemap_i.items():
                key = j[0].split(";")
                print(key, int(index))
                self.block_arr[giga_i] = [int(key[0]), -int(key[1]), self.str_dict[str(j[1][4])], int(index)*0.1 ]
                giga_i += 1

        self.block_arr.reshape((self.size, 4))
        self.buffer = self.ctx.buffer(self.block_arr)

        self.ibo = InstancingVBO(self.ctx, self.buffer, "4f", "posOffset", offset=2)
        self.app.mesh.vao.vbo.vbos["mapIbo"] = self.ibo

        self.vao = app.mesh.vao.get_ins_vao(
            fbo=self.app.mesh.vao.Framebuffers.framebuffers["default"],
            program=self.app.mesh.vao.program.programs["tilemap"],
            vbo=self.app.mesh.vao.vbo.vbos["plane"],
            ibo=self.ibo,
            umap={
                "m_model": "mat4",
                "m_view": "mat4",
                "decor": "int",
            },
            tmap=["Tiles", "Decor"],
        )
        self.app.mesh.vao.vaos["tiler"] = self.vao
        self.tex0 = app.mesh.texture.from_list("./assets/textures/tiles/", tiles_list, '.png')
        self.tex1 = app.mesh.texture.from_list("./assets/textures/AlbaseeProps/", decor_list , '.png')
        self.app.mesh.texture.textures['Tiles'] = self.tex0
        self.app.mesh.texture.textures['Decor'] = self.tex1
        self.vao.texture_bind(0, "Tiles", self.tex0)
        self.vao.texture_bind(1, "Decor", self.tex1)

        self.pos = glm.vec3(0)
        self.roll = 0
        self.scale = glm.vec2(self.tile_size/2)

        self.m_model = self.get_model_matrix()
        self.vao.uniform_bind("m_model", self.m_model.to_bytes())
        self.vao.uniform_bind("decor", self.j-decorMax+1)
        self.decorMax = decorMax
        self.app.camera.position.z = 120

    def update(self):
        self.vao.uniform_bind(
            "m_view",
            (self.app.camera.m_proj * self.app.camera.m_view * self.m_model).to_bytes(),
        )
        self.vao.render(instance_count=self.MAPSIZE)

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translate
        m_model = glm.translate(m_model, self.pos)
        # rotate
        m_model = glm.rotate(m_model, glm.radians(self.roll), glm.vec3(0, 0, 1))
        # scale
        m_model = glm.scale(m_model, glm.vec3(self.scale[0], self.scale[1], 1))
        return m_model

    def render(self): ...
    
    def destroy(self):
        self.app.mesh.vao.del_vao('tiler')
        self.app.ctx.release(self.ibo)

