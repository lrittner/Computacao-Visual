import math
import ctypes
import numpy as np
from PIL import Image

from cg.models.SquareMesh_v2 import SquareMesh

class TerrainMesh():
    
    def __init__(self, image_path, width, height, depth, columns, rows):
        
        self.__columns = columns
        self.__rows = rows 
        self.__squareMesh = SquareMesh(width, height, columns, rows)
        
        print('TerrainMesh --> Trying to open', image_path)
        try:
            image = Image.open(image_path)         
        except IOError as ex:
            print('TerrainMesh --> IOError: failed to open texture file')
        
        print('opened file: size=', image.size, 'format=', image.format, 'mode=', image.mode)

        image_data = np.asarray(image)
        
        if(image_data.ndim == 3):
            image_data = image_data.mean(axis=2)
        
        max_value = image_data.max()
        
        # Para cada vértice, calcula o index da imagem correspondente
        vertex_positions = self.__squareMesh.getVertexPositions()
        
        img_ind_x = ((vertex_positions[0::4] + (width / 2.0)) / width) * (image_data.shape[0] - 1)
        img_ind_y = ((vertex_positions[1::4] + (height / 2.0)) / height) * (image_data.shape[1] - 1)
        
        img_ind_x = np.asarray(img_ind_x, dtype=np.int32)
        img_ind_y = np.asarray(img_ind_y, dtype=np.int32)
        
        # calcula a nova altura para cada vértice
        vertex_positions[2::4] = (image_data[img_ind_x, img_ind_y] / max_value) * depth
        
        # calcula as normais considerando a nova altura de cada vértice
        vertex_indices = self.__squareMesh.getVertexIndices()
        vertex_normals = self.__squareMesh.getVertexNormals()
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


    def getPositionAt(self, row, col):
        
        if(col < 0):
            print('TerrainMesh --> Index col out of range!')
            col = 0
        
        if(row < 0):
            print('TerrainMesh --> Index row out of range!')
            row = 0
        
        if(col > self.__columns):
            print('TerrainMesh --> Index col out of range!')
            col = self.__columns
        
        if(row > self.__rows):
            print('TerrainMesh --> Index row out of range!')
            row = self.__rows
            
        vertex_positions = self.__squareMesh.getVertexPositions()
        
        index = col + (self.__columns + 1) * row
        return vertex_positions[index * 4: index * 4 + 4]
        
    def getVertexPositions(self):
        
        return self.__squareMesh.getVertexPositions()
    
    def getVertexIndices(self):
        
        return self.__squareMesh.getVertexIndices()
    
    def getVertexNormals(self):
        
        return self.__squareMesh.getVertexNormals()