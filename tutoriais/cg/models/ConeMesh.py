# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 16:42:13 2020

@author: Rapha
"""

import math
import ctypes
import numpy as np
import OpenGL.GL as gl

class ConeMesh():
    
    def __init__(self, slices, radius, height, create_base=True):

        if(radius <= 0.0):
            radius = 0.2
            
        if(slices < 3):
            slices = 3
    
        self.__radius = radius
        self.__slices = slices
        self.__height = height
    
        num_vertices = 6 * slices
        self.__vertices = np.empty(num_vertices * 4, dtype=np.float32)        
        self.__calculateVertexPositions()
        
    def __calculateVertexPositions(self):

        inc_angle = 2 * math.pi / self.__slices
        angle = 0
        vertices_pos = 0
        
        x = self.__radius * math.cos(angle)
        y = self.__radius * math.sin(angle)

        angle = inc_angle
        
        #create base
        for i in range(self.__slices):
            
            next_x = self.__radius * math.cos(angle)
            next_y = self.__radius * math.sin(angle)
            
            self.__vertices[vertices_pos] = 0
            self.__vertices[vertices_pos + 1] = 0
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = next_x
            self.__vertices[vertices_pos + 1] = next_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = x
            self.__vertices[vertices_pos + 1] = y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4            
            angle += inc_angle
            
            x = next_x
            y = next_y
        
        angle = 0
        
        x = self.__radius * math.cos(angle)
        y = self.__radius * math.sin(angle)

        angle = inc_angle
        
        #create cone
        for i in range(self.__slices):
            
            next_x = self.__radius * math.cos(angle)
            next_y = self.__radius * math.sin(angle)
            
            self.__vertices[vertices_pos] = 0
            self.__vertices[vertices_pos + 1] = 0
            self.__vertices[vertices_pos + 2] = self.__height
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = x
            self.__vertices[vertices_pos + 1] = y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = next_x
            self.__vertices[vertices_pos + 1] = next_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4            
            angle += inc_angle
            
            x = next_x
            y = next_y

    def getVertexPositions(self):
        
        return self.__vertices