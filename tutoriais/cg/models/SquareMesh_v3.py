# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 18:18:05 2020

@author: Rapha
"""

import math
import ctypes
import numpy as np
import OpenGL.GL as gl
from PIL import Image

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
        self.__normals = np.empty(self.__numVertices * 3, dtype=np.float32)
        self.__textureCoords = np.empty(self.__numVertices * 2, dtype=np.float32)
        
        self.__calculateVertexPositions()
        self.__calculateVertexIndices()
        self.__calculateVertexNormals()
        self.__calculateTextureCoordinates()
            
    def __calculateVertexPositions(self):

        inc_height = self.__height / (self.__rows)
        inc_width = self.__width / (self.__columns)
        acc_height = -self.__height / 2.0
        acc_width = -self.__width / 2.0
    
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

    def __calculateTextureCoordinates(self):
    
        inc_texture_x = 1.0 / (self.__columns)
        inc_texture_y = 1.0 / (self.__rows)
        texture_x = 0
        texture_y = 1.0
    
        texture_pos = 0;
        inc_texture_x = 1.0 / self.__columns
        texture_x = 0.0

        for i in range(self.__rows + 1):

            texture_x = 0.0
    
            for j in range(self.__columns + 1):
                
                self.__textureCoords[texture_pos] = texture_x
                self.__textureCoords[texture_pos + 1] = texture_y
                texture_pos += 2
    
                texture_x += inc_texture_x
    
            texture_y -= inc_texture_y
            
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
            
    def __calculateVertexNormals(self):
        
        for i in range(self.__numVertices):
            self.__normals[i * 3] = 0.0
            self.__normals[i * 3 + 1] = 0.0
            self.__normals[i * 3 + 2] = 1.0
            
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