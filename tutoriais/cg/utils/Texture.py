# -*- coding: utf-8 -*-
"""
Created on Fri Jan 31 14:47:49 2020

@author: Rapha
"""
from PIL import Image
import OpenGL.GL as gl
import numpy as np

class Texture():
    
    def __init__(self, filename, flip_image=False):
        
        self.__textureID = 0
        self.__flipImage = flip_image
        self.loadTexture(filename)

    def loadTexture(self, filename):
        # PIL can open BMP, EPS, FIG, IM, JPEG, MSP, PCX, PNG, PPM
        # and other file types.  We convert into a texture using GL.
        print('trying to open', filename)
        try:
            image = Image.open(filename)
            
            if(self.__flipImage):
                image = image.transpose(Image.FLIP_TOP_BOTTOM)
         
        except IOError as ex:
            print('IOError: failed to open texture file')
     
        print('opened file: size=', image.size, 'format=', image.format, 'mode=', image.mode)
        
        if(image.mode == 'P'):
            print('convert to RGBA')
            image = image.convert('RGBA')
        
        imageData = np.array(list(image.getdata()), np.uint8)

        self.__textureID = gl.glGenTextures(1)
        gl.glBindTexture(gl.GL_TEXTURE_2D, self.__textureID)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MAG_FILTER, gl.GL_LINEAR)
        gl.glTexParameterf(gl.GL_TEXTURE_2D, gl.GL_TEXTURE_MIN_FILTER, gl.GL_LINEAR)
        
        if(image.mode == 'RGB'):
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.size[0], image.size[1], 0, gl.GL_RGB, gl.GL_UNSIGNED_BYTE, imageData)
        
        elif(image.mode == 'RGBA'):
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.size[0], image.size[1], 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imageData)
        
        elif(image.mode == 'P'):
            gl.glTexImage2D(gl.GL_TEXTURE_2D, 0, gl.GL_RGBA, image.size[0], image.size[1], 0, gl.GL_RGBA, gl.GL_UNSIGNED_BYTE, imageData)
        
        else:
            print('Texture loading: unknown format!')
        
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)

        image.close()
      
    def getTextureID(self):
      
        return self.__textureID