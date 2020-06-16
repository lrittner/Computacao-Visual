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
        in vec2 tex_coord;
        
        uniform bool use_uniform_color;
        uniform vec4 uniform_color;
        uniform mat4 mvp_matrix;
        
        out vec4 frag_color;
        out vec2 frag_tex_coord;
        
        void main()
        {
            gl_Position = mvp_matrix * position;
            
            if(use_uniform_color)
                frag_color = uniform_color;
            else
                frag_color = color;
            
            frag_tex_coord = tex_coord;
        }
        """
            
        FRAGMENT_SHADER = """
        #version 330
        
        in vec4 frag_color;
        in vec2 frag_tex_coord;
        
        out vec4 output_color;
        
        uniform bool is_tex_enabled;
        uniform sampler2D tex_image;
        
        void main()
        {
            if(is_tex_enabled)
                output_color = texture(tex_image, frag_tex_coord);
            else
                output_color = frag_color;
        }
        """
        
        self.__shaderProgram = ShaderProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.__shaderProgram.bind()
        
        self.__useUniformColorLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "use_uniform_color");
        self.__uniformColorLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "uniform_color");
        self.__mvpMatrixLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "mvp_matrix");
        
        identity = glm.mat4()
        color = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(identity))
        gl.glUniform1i(self.__useUniformColorLoc, 0)
        gl.glUniform4fv(self.__uniformColorLoc, 1, color);
        
        self.__texImageLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "tex_image");
        self.__isTexEnabledLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "is_tex_enabled");
        
        gl.glUniform1i(self.__texImageLoc, 0)
        gl.glUniform1i(self.__isTexEnabledLoc, 0)
        
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
    
    def bindTexture2D(self, texture_id):
    
        if(texture_id > 0):
            gl.glUniform1i(self.__isTexEnabledLoc, 1)
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, texture_id)
             
        else:
            gl.glUniform1i(self.__isTexEnabledLoc, 0)
            gl.glActiveTexture(gl.GL_TEXTURE0)
            gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    def releaseTexture2D(self):
        
        gl.glUniform1i(self.__isTexEnabledLoc, 0)
             
        gl.glActiveTexture(gl.GL_TEXTURE0)
        gl.glBindTexture(gl.GL_TEXTURE_2D, 0)
        
    def bind(self):
        
        self.__shaderProgram.bind()
        
    def release(self):
        
        self.__shaderProgram.release()
    
    def getVertexPositionLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "position")
    
    def getVertexColorLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "color")
    
    def getVertexTextureCoordLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "tex_coord")