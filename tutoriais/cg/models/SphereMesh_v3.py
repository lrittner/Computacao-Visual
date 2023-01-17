# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:31:48 2020

@author: Rapha
"""

import math
import ctypes
import numpy as np
import OpenGL.GL as gl
from PIL import Image

class SphereMesh():
    
    def __init__(self, radius, num_sectors, num_stacks):

        if(radius <= 0 ):
            radius = 0.2
    
        if(num_sectors < 3):
            num_sectors = 3
    
        if( num_stacks < 5):
            num_stacks = 5
    
        self.__radius = radius
        self.__numSectors = num_sectors
        self.__numStacks = num_stacks
    
        self.__numVertices = (num_sectors + 1) * (num_stacks - 1) + 2 * num_sectors #(n + 1) * (n - 1) + 2 * n    
        self.__numIndices = 2 * 3 * num_sectors + (num_sectors * (num_stacks - 2)) * 3 * 2 # 2 * 3 * n + 2 * ( n + 1 ) * ( n - 2 )
    
        self.__vertices = np.empty(self.__numVertices * 4, dtype=np.float32)
        self.__indices = np.empty(self.__numIndices, dtype=np.uint32)    
        self.__textureCoords = np.empty(self.__numVertices * 2, dtype=np.float32)
        self.__normals = np.empty(self.__numVertices * 3, dtype=np.float32)
        
        self.__calculateVertexPositions()
        self.__calculateVertexIndices()
        self.__calculateTextureCoordinates()
        self.__calculateVertexNormals()
    
        for i in range(self.__numIndices):
            self.__indices[i] /= 3
            
    def __calculateVertexPositions(self):

        inc_theta = 2 * math.pi / self.__numSectors
        inc_phi = math.pi / self.__numStacks
        theta = 0
        phi = inc_phi
        vertices_pos = 0
    
        #Pólo inferior
        for i in range(self.__numSectors):
            
            self.__vertices[vertices_pos] = 0.0
            self.__vertices[vertices_pos + 1] = -self.__radius
            self.__vertices[vertices_pos + 2] = 0.0
            self.__vertices[vertices_pos + 3] = 1.0        
            vertices_pos += 4

        for i in range(self.__numStacks - 1):
    
            r_sin_phi = self.__radius * math.sin(phi)
            r_cos_phi = self.__radius * math.cos(phi)
            theta = 0
    
            for j in range(self.__numSectors):
                
                self.__vertices[vertices_pos] = math.sin(theta) * r_sin_phi
                self.__vertices[vertices_pos + 1] = -r_cos_phi
                self.__vertices[vertices_pos + 2] = math.cos(theta) * r_sin_phi
                self.__vertices[vertices_pos + 3] = 1.0
                
                vertices_pos += 4
                theta += inc_theta
            
            self.__vertices[vertices_pos] = self.__vertices[vertices_pos - (self.__numSectors * 4)]
            vertices_pos += 1
            self.__vertices[vertices_pos] = self.__vertices[vertices_pos - (self.__numSectors * 4)]
            vertices_pos += 1
            self.__vertices[vertices_pos] = self.__vertices[vertices_pos - (self.__numSectors * 4)]
            vertices_pos += 1
            self.__vertices[vertices_pos] = 1.0
            vertices_pos += 1

            phi += inc_phi

#        Pólo superior
        for i in range(self.__numSectors):
            
            self.__vertices[vertices_pos] = 0.0
            self.__vertices[vertices_pos + 1] = self.__radius
            self.__vertices[vertices_pos + 2] = 0.0
            self.__vertices[vertices_pos + 3] = 1.0
            vertices_pos += 4

    def __calculateTextureCoordinates(self): #corrigido

        inc_texture_x = 1.0 / (self.__numSectors)
        inc_texture_y = 1.0 / self.__numStacks
        texture_x = inc_texture_x / 2.0
        texture_y = 1.0 - inc_texture_y
        texture_pos = 0;
    
        #Pólo inferior
        for i in range(self.__numSectors):
            
            self.__textureCoords[texture_pos] = texture_x
            self.__textureCoords[texture_pos + 1] = 1.0
            
            texture_pos += 2
            texture_x += inc_texture_x
    
        inc_texture_x = 1.0 / self.__numSectors
        texture_x = 0.0;

        for i in range(self.__numStacks - 1):
    
            texture_x = 0.0
    
            for j in range(self.__numSectors):
                
                self.__textureCoords[texture_pos] = texture_x
                self.__textureCoords[texture_pos + 1] = texture_y
                
                texture_pos += 2
                texture_x += inc_texture_x
    
            self.__textureCoords[texture_pos] = 1.0
            self.__textureCoords[texture_pos + 1] = texture_y
            
            texture_pos += 2
            texture_y -= inc_texture_y

#        Pólo superior
        inc_texture_x = 1.0 / (self.__numSectors)
        texture_x = inc_texture_x / 2.0

        for i in range(self.__numSectors):
            
            self.__textureCoords[texture_pos] = texture_x
            self.__textureCoords[texture_pos + 1] = 0.0
            
            texture_x += inc_texture_x
            texture_pos += 2
            
    def __calculateVertexIndices(self): #corrigido

        indices_pos = 0;
    
#        pólo inferior
        for i in range(self.__numSectors):
            self.__indices[indices_pos] = i * 3
            self.__indices[indices_pos + 1] = (self.__numSectors + i + 1) * 3
            self.__indices[indices_pos + 2] = (self.__numSectors + i) * 3
            indices_pos += 3        
    
#        meio
        for i in range(self.__numStacks - 2):
            for j in range(self.__numSectors):
    
                first = (self.__numSectors + 1) * (i + 1) + self.__numSectors + j
                second = (self.__numSectors + 1) * i + self.__numSectors + j
                third = (self.__numSectors + 1) * (i + 1) + self.__numSectors + j + 1
    
                self.__indices[indices_pos] = first * 3
                self.__indices[indices_pos + 1] = second * 3
                self.__indices[indices_pos + 2] = third * 3
                indices_pos += 3 
                
                first = (self.__numSectors + 1) * (i + 1) + self.__numSectors + j + 1
                second = (self.__numSectors + 1) * i + self.__numSectors + j 
                third = (self.__numSectors + 1) * i  + self.__numSectors + j + 1
    
                self.__indices[indices_pos] = first * 3
                self.__indices[indices_pos + 1] = second * 3
                self.__indices[indices_pos + 2] = third * 3
                indices_pos += 3 
    
#        pólo superior
        offset = (self.__numVertices - self.__numSectors) * 3
        for i in range(self.__numSectors):
    
            self.__indices[indices_pos] = offset + (i * 3)
            self.__indices[indices_pos + 1] = offset + (- self.__numSectors - 1 + i) * 3
            self.__indices[indices_pos + 2] = offset + (- self.__numSectors + i) * 3
            indices_pos += 3
            
    def __calculateVertexNormals(self):
        
        for i in range(self.__numVertices):                        
            self.__normals[i * 3] = self.__vertices[i * 4]
            self.__normals[i * 3 + 1] = self.__vertices[i * 4 + 1]
            self.__normals[i * 3 + 2] = self.__vertices[i * 4 + 2]
            
    def getVertexPositions(self):
        
        return self.__vertices
    
    def getVertexIndices(self):
        
        return self.__indices
    
    def getVertexTextureCoord(self):
        
        return self.__textureCoords
    
    def getVertexNormals(self):
        
        return self.__normals
    
    def applyHeightMap(self, image_path, height):
        
        print('TerrainMesh --> Trying to open', image_path)
        try:
            image = Image.open(image_path)         
        except IOError as ex:
            print('TerrainMesh --> IOError: failed to open texture file')
        
        print('opened file: size=', image.size, 'format=', image.format, 'mode=', image.mode)

        image_data = np.asarray(image)
        
        if(image_data.ndim == 3):
            image_data = image_data[:,:,0:3].mean(axis=2)
        
        max_value = image_data.max()
        
        # Para cada vértice, calcula o index da imagem correspondente
        vertex_positions = self.getVertexPositions()
        vertex_normals = self.getVertexNormals()
        vertex_tex = self.getVertexTextureCoord()
        
        img_ind_x = vertex_tex[0::2] * (image_data.shape[1] - 1)
        img_ind_y = vertex_tex[1::2] * (image_data.shape[0] - 1)
        
        img_ind_x = np.asarray(img_ind_x, dtype=np.int32)
        img_ind_y = np.asarray(img_ind_y, dtype=np.int32)
        
        # calcula a nova altura para cada vértice
        vertex_positions[0::4] = vertex_positions[0::4] + vertex_normals[0::3] * (image_data[img_ind_y, img_ind_x] / max_value) * height
        vertex_positions[1::4] = vertex_positions[1::4] + vertex_normals[1::3] * (image_data[img_ind_y, img_ind_x] / max_value) * height
        vertex_positions[2::4] = vertex_positions[2::4] + vertex_normals[2::3] * (image_data[img_ind_y, img_ind_x] / max_value) * height
        
        # calcula as normais considerando a nova altura de cada vértice
        vertex_indices = self.getVertexIndices()
        vertex_normals[:] = 0.0
        
        for i in range(vertex_indices.size // 3):
            
            pos0 = vertex_indices[i * 3]
            pos1 = vertex_indices[i * 3 + 1]
            pos2 = vertex_indices[i * 3 + 2]

            v1 = vertex_positions[(pos1 * 4): (pos1 * 4 + 3)] - vertex_positions[(pos0 * 4): (pos0 * 4 + 3)] 
            v2 = vertex_positions[pos2 * 4: pos2 * 4 + 3] - vertex_positions[pos1 * 4: pos1 * 4 + 3]

            normal = np.cross(v1, v2)
            vertex_normals[pos0 * 3: pos0 * 3 + 3] = vertex_normals[pos0 * 3: pos0 * 3 + 3] + normal
            vertex_normals[pos1 * 3: pos1 * 3 + 3] = vertex_normals[pos1 * 3: pos1 * 3 + 3] + normal
            vertex_normals[pos2 * 3: pos2 * 3 + 3] = vertex_normals[pos2 * 3: pos2 * 3 + 3] + normal
            
        # normaliza as normais
        for i in range(vertex_normals.size // 3):
            vertex_normals[i * 3: i * 3 + 3] = vertex_normals[i * 3: i * 3 + 3] / np.linalg.norm(vertex_normals[i * 3: i * 3 + 3])