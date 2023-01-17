# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:49:43 2020

@author: Rapha
"""

import glm
import numpy as np
import OpenGL.GL as gl
from cg.shader_programs.ShaderProgram import ShaderProgram

class SimpleShaderProgram():
    
    def __init__(self):
        
        VERTEX_SHADER = """
        #version 330
        
        layout (location=0) in vec4 position;
        layout (location=1) in vec4 color;
        
        uniform bool use_uniform_color;
        uniform vec4 uniform_color;
        
        uniform mat4 mvpMatrix;
        
        out vec4 frag_color;
        
        void main()
        {
            gl_Position = mvpMatrix * position;
            
            if(use_uniform_color)
                frag_color = uniform_color;
            else
                frag_color = color;
        }
        """
            
        FRAGMENT_SHADER = """
        #version 330
        
        in vec4 frag_color;
        out vec4 output_color;
        
        void main()
        {
            output_color = frag_color;
        }
        """
        
        self.__shaderProgram = ShaderProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.__shaderProgram.bind()
        
        self.__useUniformColorLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "use_uniform_color");
        self.__uniformColorLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "uniform_color");
        
        self.__mvpMatrixLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "mvpMatrix");
        
        identity = glm.mat4()
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(identity))
        
        gl.glUniform1i(self.__useUniformColorLoc, 0)
        
        color = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        gl.glUniform4fv(self.__uniformColorLoc, 1, color);
        
        self.__shaderProgram.release()
        
    def useUniformColor(self, state):
        
        if(state):
            gl.glUniform1i(self.__useUniformColorLoc, 1)
        else:
            gl.glUniform1i(self.__useUniformColorLoc, 0)
            
    def setUniformColor(self, color):
        
        gl.glUniform4fv(self.__uniformColorLoc, 1, color);
        
    def setUniformMVPMatrix(self, mvp_matrix):
        
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(mvp_matrix))
        
    def bind(self):
        
        self.__shaderProgram.bind()
        
    def release(self):
        
        self.__shaderProgram.release()
    
    def getVertexPositionLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "position")
    
    def getVertexColorLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "color")