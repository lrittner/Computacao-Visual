# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 11:47:27 2020

@author: Rapha
"""

import math
#import ctypes
import numpy as np
import OpenGL.GL as gl

class OrbitPolygon():
    
    def __init__(self, semi_major_axis, semi_minor_axis, focus, num_vertices):

        if(num_vertices < 10):
            num_vertices = 10
    
        self.__numVertices = num_vertices
        self.__semiMajorAxis = semi_major_axis
        self.__semiMinorAxis = semi_minor_axis
        self.__focus = focus
    
        self.__vertices = np.empty(self.__numVertices * 4, dtype=np.float32)
        self.__calculateVertices()
    
    def __calculateVertices(self):

        inc_theta = 2 * math.pi / self.__numVertices
        theta = 0
    
        vertices_pos = 0
    
        for i in range(self.__numVertices):
            
            x, y = self.getPositionAt(theta)
            
            self.__vertices[vertices_pos] = x
            self.__vertices[vertices_pos + 1] = y
            self.__vertices[vertices_pos + 2] = 0.0
            self.__vertices[vertices_pos + 3] = 1.0
            
            vertices_pos += 4
            theta += inc_theta
            
    def getPositionAt(self, angle):
        
        x = self.__semiMajorAxis * np.sin(angle) + self.__focus
        y = self.__semiMinorAxis * np.cos(angle)
        
        return (x, y)
    
    def getVertexPositions(self):
        
        return self.__vertices