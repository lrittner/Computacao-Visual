# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 18:18:05 2020

@author: Rapha
"""

import math
import ctypes
import numpy as np
import OpenGL.GL as gl

class SquareMesh():
    
    def __init__(self, width, height, columns, rows):

        if(width <= 0):
            width = 0.1
            
        if(height <= 0):
            height = 0.1
    
        if(columns <= 0):
            columns = 1
    
        if(rows <= 0):
            rows = 1
    
        self.__width = width
        self.__height = height
        self.__rows = rows
        self.__columns = columns
    
        self.__numVertices = (rows + 1) * (columns + 1)
        self.__numIndices = rows * columns * 3 * 2
        
        self.__vertices = np.empty(self.__numVertices * 4, dtype=np.float32)
        self.__indices = np.empty(self.__numIndices, dtype=np.uint32)
        
        self.__calculateVertexPositions()
        self.__calculateVertexIndices()
            
    def __calculateVertexPositions(self):

        inc_height = self.__height / (self.__rows)
        inc_width = self.__width / (self.__columns)
        acc_height = -self.__height / 2.0
        acc_width = -self.__width / 2.0
        # acc_height = 0
        # acc_width =  0
    
        vertices_pos = 0

        for i in range(self.__rows + 1):

            acc_width = -self.__width / 2.0
    
            for j in range(self.__columns + 1):
                
                self.__vertices[vertices_pos] = acc_width
                self.__vertices[vertices_pos + 1] = acc_height
                self.__vertices[vertices_pos + 2] = 0
                self.__vertices[vertices_pos + 3] = 1
                vertices_pos += 4
    
                acc_width += inc_width
    
            acc_height += inc_height
            
    def __calculateVertexIndices(self):

        indices_pos = 0;

        for i in range(self.__rows):
            for j in range(self.__columns):
    
                first = (self.__columns + 1) * (i + 1) + j
                second = (self.__columns + 1) * i + j
                third = (self.__columns + 1) * (i + 1) + j + 1
    
                self.__indices[indices_pos] = first
                self.__indices[indices_pos + 1] = second
                self.__indices[indices_pos + 2] = third
                indices_pos += 3 
                
                first = (self.__columns + 1) * (i + 1) + j + 1
                second = (self.__columns + 1) * i + j 
                third = (self.__columns + 1) * i + j + 1
    
                self.__indices[indices_pos] = first
                self.__indices[indices_pos + 1] = second
                self.__indices[indices_pos + 2] = third
                indices_pos += 3 
            
    def getVertexPositions(self):
        
        return self.__vertices
    
    def getVertexIndices(self):
        
        return self.__indices
