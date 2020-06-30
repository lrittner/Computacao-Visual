import numpy as np
import pywavefront

class ObjectInfo:
    
    def __init__(self):
        
        self.numVertices = 0
        self.vertexFormat = ''
        self.vertices = []
                
class ObjLoader:
    
    def __init__(self, file):
        
        self.scene = pywavefront.Wavefront(file, strict=False, create_materials=True, cache=True)
        
        self.__objectInfo = { }
    
        for name, material in self.scene.materials.items():
            
            print('material_name =', name, '- vertex_format =', material.vertex_format, '- min =', min(material.vertices), '- max =', max(material.vertices))
            
            self.__objectInfo[name] = ObjectInfo()
            self.__objectInfo[name].numVertices = int(len(material.vertices) / material.vertex_size)
            self.__objectInfo[name].vertexFormat = material.vertex_format
            self.__objectInfo[name].vertices = np.empty(self.__objectInfo[name].numVertices * 4, dtype=np.float32)
            self.__objectInfo[name].normals = []
            self.__objectInfo[name].textureCoords = []
            
            if(self.__objectInfo[name].vertexFormat == "T2F_N3F_V3F"):
                
                vertices = np.array(material.vertices, dtype=np.float32)
                self.__objectInfo[name].vertices[0::4] = vertices[5::8]
                self.__objectInfo[name].vertices[1::4] = vertices[6::8]
                self.__objectInfo[name].vertices[2::4] = vertices[7::8]
                self.__objectInfo[name].vertices[3::4] = 1.0
                
                self.__objectInfo[name].normals = np.zeros(self.__objectInfo[name].numVertices * 3, dtype=np.float32)
                self.__objectInfo[name].normals[0::3] = vertices[2::8]
                self.__objectInfo[name].normals[1::3] = vertices[3::8]
                self.__objectInfo[name].normals[2::3] = vertices[4::8]
                
                self.__objectInfo[name].textureCoords = np.zeros(self.__objectInfo[name].numVertices * 2, dtype=np.float32)
                self.__objectInfo[name].textureCoords[0::2] = vertices[0::8]
                self.__objectInfo[name].textureCoords[1::2] = vertices[1::8]
                
            elif(self.__objectInfo[name].vertexFormat == 'T2F_V3F'):
                
                vertices = np.array(material.vertices, dtype=np.float32)
                self.__objectInfo[name].vertices[0::4] = vertices[2::5]
                self.__objectInfo[name].vertices[1::4] = vertices[3::5]
                self.__objectInfo[name].vertices[2::4] = vertices[4::5]
                self.__objectInfo[name].vertices[3::4] = 1.0
                
                self.__objectInfo[name].textureCoords = np.zeros(self.__objectInfo[name].numVertices * 2, dtype=np.float32)
                self.__objectInfo[name].textureCoords[0::2] = vertices[0::5]
                self.__objectInfo[name].textureCoords[1::2] = vertices[1::5]
                
            elif(self.__objectInfo[name].vertexFormat == 'N3F_V3F'):
                
                vertices = np.array(material.vertices, dtype=np.float32)
                self.__objectInfo[name].vertices[0::4] = vertices[3::6]
                self.__objectInfo[name].vertices[1::4] = vertices[4::6]
                self.__objectInfo[name].vertices[2::4] = vertices[5::6]
                self.__objectInfo[name].vertices[3::4] = 1.0
                
                self.__objectInfo[name].normals = np.zeros(self.__objectInfo[name].numVertices * 3, dtype=np.float32)
                self.__objectInfo[name].normals[0::3] = vertices[0::6]
                self.__objectInfo[name].normals[1::3] = vertices[1::6]
                self.__objectInfo[name].normals[2::3] = vertices[2::6]
                
    def getItemNames(self):
        
        return list(self.__objectInfo)
    
    def getVertexPositions(self, item_name):
    
        return self.__objectInfo[item_name].vertices

    def getVertexTextureCoord(self, item_name):
        
        return self.__objectInfo[item_name].textureCoords
    
    def getVertexNormals(self, item_name):
        
        return self.__objectInfo[item_name].normals
    
    def hasVertexNormals(self, item_name):
        
        return (len(self.__objectInfo[item_name].normals) > 0)
    
    def hasVertexTextureCoord(self, item_name):
        
        return (len(self.__objectInfo[item_name].textureCoords) > 0)