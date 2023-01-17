# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 14:54:59 2020

@author: Rapha
"""

import OpenGL.GL as gl

class ShaderProgram():
    
    def __init__(self, vertex_source, fragment_source):
        
        self.__program = gl.glCreateProgram()
        vertex = gl.glCreateShader(gl.GL_VERTEX_SHADER)
        fragment = gl.glCreateShader(gl.GL_FRAGMENT_SHADER)

        # Set shaders source
        gl.glShaderSource(vertex, vertex_source)
        gl.glShaderSource(fragment, fragment_source)

        # Compile shaders
        gl.glCompileShader(vertex)
        if not gl.glGetShaderiv(vertex, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(vertex).decode()
            print(error)
            raise RuntimeError("Vertex shader compilation error!")

        gl.glCompileShader(fragment)
        if not gl.glGetShaderiv(fragment, gl.GL_COMPILE_STATUS):
            error = gl.glGetShaderInfoLog(fragment).decode()
            print(error)
            raise RuntimeError("Fragment shader compilation error!")

        gl.glAttachShader(self.__program, vertex)
        gl.glAttachShader(self.__program, fragment)
        gl.glLinkProgram(self.__program)

        if not gl.glGetProgramiv(self.__program, gl.GL_LINK_STATUS):
            print(gl.glGetProgramInfoLog(self.__program))
            raise RuntimeError('Linking error!')

        gl.glDetachShader(self.__program, vertex)
        gl.glDetachShader(self.__program, fragment)
        
        gl.glDeleteShader(vertex)
        gl.glDeleteShader(fragment)
        
    def getProgramID(self):
        
        return self.__program
        
    def bind(self):
        
        gl.glUseProgram(self.__program)
        
    def release(self):
        
        gl.glUseProgram(0)