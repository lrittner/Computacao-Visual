# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 09:16:49 2020

@author: Rapha
"""
from cg.shader_programs.ShaderProgram import ShaderProgram
import OpenGL.GL as gl
import numpy as np
import glm

class SunEffectShaderProgram():
    
    def __init__(self):
        
        VERTEX_SHADER = """
        #version 330
        
        layout (location=0) in vec4 position;
        layout (location=1) in vec2 tex_coord;
        
        uniform mat4 mvp_matrix;
        
        out vec2 frag_tex_coord;
        
        void main()
        {
            gl_Position = mvp_matrix * position;
            frag_tex_coord = tex_coord;
        }
        """
            
        FRAGMENT_SHADER = """
        #version 330
        
        in vec2 frag_tex_coord;
        
        uniform float iTime; 
        
        out vec4 outputColor;
        
        #define f length(fract(q*=m*=.6+.1*d++)-.5)
        
        void main()
        {
            vec2 uv;
            if(frag_tex_coord.x > 0.5)
                uv = vec2(1.0 - frag_tex_coord.x, frag_tex_coord.y) * 10;
            else 
                uv = vec2(frag_tex_coord) * 10;
                
            float d = 0.;
            vec3 q = vec3(uv - 13., iTime*.5);
            mat3 m = mat3(-2,-1,2, 3,-2,1, -1,1,3);
            vec3 col = vec3(pow(min(min(f,f),f), 7.)*40.);
            outputColor = vec4(clamp(col + vec3(0.6, 0.35, 0.1), 0.0, 1.0), 1.0);
        }
        """
        
        self.__shaderProgram = ShaderProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        
        self.__shaderProgram.bind()
        
        self.__iTime = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "iTime")
        
        gl.glUniform1f(self.__iTime, 0)
        
        self.__mvpMatrixLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "mvp_matrix");
        
        trans = glm.mat4()
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(trans))
        
        self.__shaderProgram.release()
        
    def setTime(self, time):
        
        gl.glUniform1f(self.__iTime, time)
        
    def setUniformMVPMatrix(self, mvp_matrix):
        
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(mvp_matrix))
        
    def bind(self):
        
        self.__shaderProgram.bind()
        
    def release(self):
        
        self.__shaderProgram.release()
    
    def getVertexPositionLoc(self):
        
        return 0;
    
    def getVertexTextureCoordLoc(self):
        
        return 1;