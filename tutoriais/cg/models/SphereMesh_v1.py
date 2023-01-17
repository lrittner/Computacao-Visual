# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:31:48 2020

@author: Rapha
"""

import math
import ctypes
import numpy as np
import OpenGL.GL as gl

class SphereMesh():
    
    def __init__(self, radius, num_sectors, num_stacks, use_face_normal=False):

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
        
        self.__calculateVertexPositions()
        self.__calculateVertexIndices()
    
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
            
    def getVertexPositions(self):
        
        return self.__vertices
    
    def getVertexIndices(self):
        
        return self.__indices
        