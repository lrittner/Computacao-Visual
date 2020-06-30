# -*- coding: utf-8 -*-
"""
Created on Sun Mar  1 16:42:13 2020

@author: Rapha
"""

import math
import ctypes
import numpy as np
import OpenGL.GL as gl

class Torus2DMesh():
    
    def __init__(self, slices, outer_radius, inner_radius):

        if(outer_radius <= 0.0):
            outer_radius = 0.2
    
        if(inner_radius < 0.0):
            inner_radius = 0.0
            
        if(inner_radius > outer_radius):
            inner_radius = outer_radius * 0.1
            
        if(slices < 3):
            slices = 3
    
        self.__outerRadius = outer_radius
        self.__innerRadius = inner_radius
        self.__slices = slices
    
        self.__numVertices = 6 * slices
        self.__vertices = np.empty(self.__numVertices * 4, dtype=np.float32)
        self.__normals = np.empty(self.__numVertices * 3, dtype=np.float32)
        self.__textureCoords = np.empty(self.__numVertices * 2, dtype=np.float32)
        
        self.__calculateVertexPositions()
        self.__calculateTextureCoordinates()
        self.__calculateVertexNormals();
        
    def __calculateVertexPositions(self):

        inc_angle = 2 * math.pi / self.__slices
        angle = 0
        vertices_pos = 0
        
        inner_x = self.__innerRadius * math.cos(angle)
        inner_y = self.__innerRadius * math.sin(angle)
        
        outer_x = self.__outerRadius * math.cos(angle)
        outer_y = self.__outerRadius * math.sin(angle)

        angle = inc_angle
        
        for i in range(self.__slices):
            
            next_inner_x = self.__innerRadius * math.cos(angle)
            next_inner_y = self.__innerRadius * math.sin(angle)
            
            next_outer_x = self.__outerRadius * math.cos(angle)
            next_outer_y = self.__outerRadius * math.sin(angle)
            
            self.__vertices[vertices_pos] = inner_x
            self.__vertices[vertices_pos + 1] = inner_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = outer_x
            self.__vertices[vertices_pos + 1] = outer_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = next_outer_x
            self.__vertices[vertices_pos + 1] = next_outer_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = inner_x
            self.__vertices[vertices_pos + 1] = inner_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = next_outer_x
            self.__vertices[vertices_pos + 1] = next_outer_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4
            
            self.__vertices[vertices_pos] = next_inner_x
            self.__vertices[vertices_pos + 1] = next_inner_y
            self.__vertices[vertices_pos + 2] = 0
            self.__vertices[vertices_pos + 3] = 1
            
            vertices_pos += 4            
            angle += inc_angle
            
            inner_x = next_inner_x
            inner_y = next_inner_y
            
            outer_x = next_outer_x
            outer_y = next_outer_y
    
    def __calculateTextureCoordinates(self):

        inc_texture = 1.0 / self.__slices
        texture = 0
        texture_pos = 0;
        
        inner_x_tex = texture
        inner_y_tex = 0.0
        
        outer_x_tex = texture
        outer_y_tex = 1.0

        texture = inc_texture
        
        for i in range(self.__slices):
            
            next_inner_x_tex = texture
            next_inner_y_tex = 0.0
            
            next_outer_x_tex = texture
            next_outer_y_tex = 1.0
            
            self.__textureCoords[texture_pos] = inner_x_tex
            self.__textureCoords[texture_pos + 1] = inner_y_tex
            
            texture_pos += 2
            
            self.__textureCoords[texture_pos] = outer_x_tex
            self.__textureCoords[texture_pos + 1] = outer_y_tex
            
            texture_pos += 2
            
            self.__textureCoords[texture_pos] = next_outer_x_tex
            self.__textureCoords[texture_pos + 1] = next_outer_y_tex
            
            texture_pos += 2
            
            self.__textureCoords[texture_pos] = inner_x_tex
            self.__textureCoords[texture_pos + 1] = inner_y_tex
            
            texture_pos += 2
            
            self.__textureCoords[texture_pos] = next_outer_x_tex
            self.__textureCoords[texture_pos + 1] = next_outer_y_tex

            texture_pos += 2
            
            self.__textureCoords[texture_pos] = next_inner_x_tex
            self.__textureCoords[texture_pos + 1] = next_inner_y_tex
            
            texture_pos += 2
            texture += inc_texture
            
            inner_x_tex = next_inner_x_tex
            inner_y_tex = next_inner_y_tex
            
            outer_x_tex = next_outer_x_tex
            outer_y_tex = next_outer_y_tex
            
    def __calculateVertexNormals(self):
        
        for i in range(self.__numVertices):
            self.__normals[i * 3] = 0.0
            self.__normals[i * 3 + 1] = 0.0
            self.__normals[i * 3 + 2] = 1.0

    def getVertexPositions(self):
        
        return self.__vertices
    
    def getVertexTextureCoord(self):
        
        return self.__textureCoords
    
    def getVertexNormals(self):
        
        return self.__normals