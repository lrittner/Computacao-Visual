# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 15:49:43 2020

@author: Rapha
"""

import glm
import math
import numpy as np
import OpenGL.GL as gl
from cg.shader_programs.ShaderProgram import ShaderProgram

class PhongShadingShaderProgram():
    
    POINT_LIGHT = 3
    DIRECTIONAL_LIGHT = 4
    SPOTLIGHT = 5

    PHONG_SPECULAR = 6
    BLINN_SPECULAR = 7
    
    def __init__(self):
        
        VERTEX_SHADER = """
        #version 330
        
        in vec4 position;
        in vec4 color;
        in vec3 normal;
        
        out vec4 frag_position;
        out vec4 frag_color;
        out vec3 frag_normal;
        
        uniform bool use_uniform_color;
        uniform vec4 uniform_color;
        
        uniform mat4 mvpMatrix;
        uniform mat4 modelViewMatrix;
        
        void main()
        {
            gl_Position = mvpMatrix * position;
        
            frag_position = modelViewMatrix * position;
            frag_normal = transpose(inverse(mat3(modelViewMatrix))) * normal;
            
            if(use_uniform_color)
                frag_color = uniform_color;
            else
                frag_color = color;
        }
        """
            
        FRAGMENT_SHADER = """
        #version 330
        
        in vec4 frag_position;
        in vec4 frag_color;
        in vec3 frag_normal;
        
        uniform int lightModel;
        uniform int specularModel;
        uniform bool hasAttenuation;
        
        struct LightInfo
        {
            vec4 position; // eye Coordinates
            vec3 direction; // normalized
            float cutoff; // already calculated
            float exp;
            vec3 La;
            vec3 Li;
        };
        uniform LightInfo light;

        struct MaterialInfo
        {
            vec3 Ka;
            vec3 Kd;
            vec3 Ks;
            float shininess; 
        };
        uniform MaterialInfo material;

        struct AttenuationInfo
        {
            float Kc;
            float Kl;
            float Kq;
        };
        uniform AttenuationInfo att;
        
        out vec4 output_color;
        
        vec3 phongModel(vec3 normal, vec3 lightDirection, vec3 viewDirection)
        {
            vec3 r = reflect(-lightDirection, normal);
            vec3 specular = material.Ks * light.Li * pow(max(dot(r, viewDirection), 0.0), material.shininess);
            return specular;
        }

        vec3 blinnModel(vec3 normal, vec3 lightDirection, vec3 viewDirection)
        {
            vec3 halfVector = normalize(lightDirection + viewDirection);
            vec3 specular = material.Ks * light.Li * pow(max(dot(halfVector, normal), 0.0), material.shininess);
            return specular;
        }

        float attenuationFunc(float dist)
        {
            return 1.0 / (att.Kc + att.Kl * dist + att.Kq * dist * dist);
        }
        
        vec3 computeSpecular(float lightDotNormal, vec3 normal, vec3 lightDirection, vec3 viewDirection)
        {
            vec3 specular = vec3(0.0);
            if(lightDotNormal > 0.0)
            {
                if(specularModel == 6)
                    specular = phongModel(normal, lightDirection, viewDirection);
                else 
                    specular = blinnModel(normal, lightDirection, viewDirection);
            }
            return specular;
        }

        vec4 pointLight(vec3 normal)
        {
            vec3 ambient =  material.Ka * light.La;
            vec3 lightDirection = normalize(vec3(light.position - frag_position));
            float lightDotNormal = max(0.0, dot(normal, lightDirection));
            vec3 diffuse = material.Kd * light.Li * lightDotNormal;
            vec3 specular = computeSpecular(lightDotNormal, normal, lightDirection, normalize(-frag_position.xyz));

            if(hasAttenuation)
            {
                float attenuation = attenuationFunc(length(vec3(light.position - frag_position)));
                vec3 rgb = min(frag_color.rgb * (ambient + attenuation * diffuse) + attenuation * specular, vec3(1.0));
                return vec4(rgb, frag_color.a);
            
            } else {
            
                vec3 rgb = min(frag_color.rgb * (ambient + diffuse) + specular, vec3(1.0));
                return vec4(rgb, frag_color.a);
            }
        }
        
        vec4 directionalLight(vec3 normal)
        {
            vec3 ambient =  material.Ka * light.La;
            vec3 lightDirection = -light.direction;
            float lightDotNormal = max(0.0, dot(normal, lightDirection));
            vec3 diffuse = material.Kd * light.Li * lightDotNormal;
            vec3 specular = computeSpecular(lightDotNormal, normal, lightDirection, normalize(-frag_position.xyz));

            vec3 rgb = min(frag_color.rgb * (ambient + diffuse) + specular, vec3(1.0));
            return vec4(rgb, frag_color.a);
        }

        vec4 spotlight(vec3 normal)
        {
            vec3 ambient =  material.Ka * light.La;
            vec3 lightDirection = normalize(vec3(light.position - frag_position));
            float angle = dot(-lightDirection, light.direction);
            float cutoff = clamp(light.cutoff, 0.0, 1.0);

            if(angle > cutoff)
            {
                float lightDotNormal = max(0.0, dot(normal, lightDirection));
                vec3 diffuse = material.Kd * light.Li * lightDotNormal;
                vec3 specular = computeSpecular(lightDotNormal, normal, lightDirection, normalize(-frag_position.xyz));
                float falloff = pow(angle, light.exp);
                
                if(hasAttenuation)
                {
                    float attenuation = attenuationFunc(length(vec3(light.position - frag_position))) * falloff;
                    vec3 rgb = min(frag_color.rgb * (ambient + attenuation * diffuse) + attenuation * specular, vec3(1.0));
                    return vec4(rgb, frag_color.a);
                    
                } else {
                
                    vec3 rgb = min(frag_color.rgb * (ambient + falloff * diffuse) + falloff * specular, vec3(1.0));
                    return vec4(rgb, frag_color.a);
                }

            } else 
                return vec4(frag_color.rgb * ambient, frag_color.a);
        }
        
        void main()
        {
            vec3 normal = normalize(frag_normal);
            
            if(lightModel == 3)
                output_color = pointLight(normal);
                
            else if(lightModel == 4)
                output_color = directionalLight(normal);
                
            else 
                output_color = spotlight(normal);
        }
        """
        
        use_uniform_color = 0
        uniform_color = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        
        mvp_matrix = glm.mat4()
        model_view_matrix = glm.mat4()
        
        light_model = PhongShadingShaderProgram.POINT_LIGHT;
        specular_mode = PhongShadingShaderProgram.PHONG_SPECULAR;
        has_attenuation = 0;

        light_position = glm.vec4(5.0, 5.0, 0.0, 1.0)
        light_direction = glm.vec3(0.0, -5.0, -5.0)
        light_direction = light_direction / np.linalg.norm(light_direction)
        light_cutoff = 10;
        light_exp = 5;
        light_la = np.array([0.3, 0.3, 0.3], dtype=np.float32)
        light_li = np.array([1.0, 1.0, 1.0], dtype=np.float32)
        
        material_ka = np.array([0.8, 0.8, 0.8], dtype=np.float32)
        material_kd = np.array([0.8, 0.8, 0.8], dtype=np.float32)
        material_ks = np.array([0.7, 0.7, 0.7], dtype=np.float32)
        material_shininess = 40.0

        att_kc = 0.1;
        att_kl = 0.1;
        att_kq = 0.05;
        
        self.__shaderProgram = ShaderProgram(VERTEX_SHADER, FRAGMENT_SHADER)
        self.__shaderProgram.bind()
        
        self.__useUniformColorLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "use_uniform_color");
        self.__uniformColorLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "uniform_color");
        
        gl.glUniform1i(self.__useUniformColorLoc, use_uniform_color)
        gl.glUniform4fv(self.__uniformColorLoc, 1, uniform_color);
        
        self.__mvpMatrixLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "mvpMatrix");
        self.__modelViewMatrixLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "modelViewMatrix");
        
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(mvp_matrix))
        gl.glUniformMatrix4fv(self.__modelViewMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(model_view_matrix))
        
        self.__lightModelLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "lightModel");
        self.__specularModelLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "specularModel");
        self.__hasAttenuationLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "hasAttenuation");
        
        gl.glUniform1i(self.__lightModelLoc, light_model);
        gl.glUniform1i(self.__specularModelLoc, specular_mode);
        gl.glUniform1i(self.__hasAttenuationLoc, has_attenuation);
        
        self.__lightPositionLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light.position");
        self.__lightDirectionLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light.direction");
        self.__cutoffLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light.cutoff");
        self.__lightExpLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light.exp");
        self.__lightLaLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light.La");
        self.__lightLiLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light.Li");
        
        gl.glUniform4fv(self.__lightPositionLoc, 1, glm.value_ptr(light_position));
        gl.glUniform3fv(self.__lightDirectionLoc, 1, glm.value_ptr(light_direction));
        gl.glUniform1f(self.__cutoffLoc, math.cos(math.radians(light_cutoff)));
        gl.glUniform1f(self.__lightExpLoc, light_exp);
        gl.glUniform3fv(self.__lightLaLoc, 1, light_la);
        gl.glUniform3fv(self.__lightLiLoc, 1, light_li);
        
        self.__materialKaLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.Ka");
        self.__materialKdLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.Kd");
        self.__materialKsLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.Ks");
        self.__materialShininessLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.shininess");
        
        gl.glUniform3fv(self.__materialKaLoc, 1, material_ka);
        gl.glUniform3fv(self.__materialKdLoc, 1, material_kd);
        gl.glUniform3fv(self.__materialKsLoc, 1, material_ks);
        gl.glUniform1f(self.__materialShininessLoc, material_shininess);
        
        self.__attKcLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "att.Kc");
        self.__attKlLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "att.Kl");
        self.__attKqLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "att.Kq");
        
        gl.glUniform1f(self.__attKcLoc, att_kc);
        gl.glUniform1f(self.__attKlLoc, att_kl);
        gl.glUniform1f(self.__attKqLoc, att_kq);
        
        self.__shaderProgram.release()
        
    def useUniformMaterialColor(self, state):
        
        if(state):
            gl.glUniform1i(self.__useUniformColorLoc, 1)
        else:
            gl.glUniform1i(self.__useUniformColorLoc, 0)
            
    def setUniformMaterialColor(self, color):
        
        gl.glUniform4fv(self.__uniformColorLoc, 1, color);
        
    def setUniformMVPMatrix(self, mvp_matrix):
        
        gl.glUniformMatrix4fv(self.__mvpMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(mvp_matrix))
        
    def setUniformModelViewMatrix(self, mv_matrix):
        
        gl.glUniformMatrix4fv(self.__modelViewMatrixLoc, 1, gl.GL_FALSE, glm.value_ptr(mv_matrix))
        
    def setUniformLightMode(self, light_mode):
        
        if(light_mode >= 3 and light_mode <= 5):
            gl.glUniform1i(self.__lightModelLoc, light_mode)
        else:
            print("PhongShadingShaderProgram::setUniformLightMode --> modo inválida. Mudando para modo Point light!")
            gl.glUniform1i(self.__lightModelLoc, PhongShadingShaderProgram.POINT_LIGHT)
    
    def setUniformSpecularMode(self, specular_mode):
        
        if(specular_mode == 6 or specular_mode == 7):
            gl.glUniform1i(self.__specularModelLoc, specular_mode)
        else:
            print("PhongShadingShaderProgram::setUniformSpecularMode --> modo inválida. Mudando para modo Phong specular!")
            gl.glUniform1i(self.__specularModelLoc, PhongShadingShaderProgram.PHONG_SPECULAR)
    
    def useUniformLightAttenuation(self, state):
        
        if(state):
            gl.glUniform1i(self.__hasAttenuationLoc, 1)
        else:
            gl.glUniform1i(self.__hasAttenuationLoc, 0)
    
    def setUniformLightPosition(self, position):
        
        gl.glUniform4fv(self.__lightPositionLoc, 1, glm.value_ptr(position));
        
    def setUniformLightDirection(self, direction):
        
        norm_direction = direction / np.linalg.norm(direction)
        
        gl.glUniform3fv(self.__lightDirectionLoc, 1, glm.value_ptr(norm_direction));
    
    def setUniformSpotlightCutoff(self, cutoff_angle):
        
        gl.glUniform1f(self.__cutoffLoc, math.cos(math.radians(cutoff_angle)));
        
    def setUniformSpotlightExpAtt(self, exp_att):
        
        gl.glUniform1f(self.__lightExpLoc, exp_att);
        
    def setUniformLightAmbient(self, ambiente_color):
        
        gl.glUniform3fv(self.__lightLaLoc, 1, ambiente_color);
        
    def setUniformLightIntensity(self, light_color):
        
        gl.glUniform3fv(self.__lightLiLoc, 1, light_color);
        
    def setUniformMaterialAmbient(self, material_ambient):
        
        gl.glUniform3fv(self.__materialKaLoc, 1, material_ambient);

    def setUniformMaterialDiffuse(self, material_diffuse):
        
        gl.glUniform3fv(self.__materialKdLoc, 1, material_diffuse);
        
    def setUniformMaterialSpecular(self, material_specular):
        
        gl.glUniform3fv(self.__materialKsLoc, 1, material_specular);
        
    def setUniformMaterialShininess(self, material_shininess):
        
        gl.glUniform1f(self.__materialShininessLoc, material_shininess);
        
    def setUniformLightConstantAttenuation(self, const_att):
        
        gl.glUniform1f(self.__attKcLoc, const_att);
        
    def setUniformLightLinearAttenuation(self, linear_att):
    
        gl.glUniform1f(self.__attKlLoc, linear_att);
    
    def setUniformLightQuadraticAttenuation(self, quadratic_att):
        
        gl.glUniform1f(self.__attKqLoc, quadratic_att);
        
    def bind(self):
        
        self.__shaderProgram.bind()
        
    def release(self):
        
        self.__shaderProgram.release()
    
    def getVertexPositionLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "position")
    
    def getVertexColorLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "color")
    
    def getVertexNormalLoc(self):
        
        return gl.glGetAttribLocation(self.__shaderProgram.getProgramID(), "normal")