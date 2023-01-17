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

class MultiLightPhongShadingShaderProgram():
    
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
        
        uniform bool isLightEnabled[5];
        uniform int lightModel[5];
        uniform int specularModel[5];
        uniform bool hasAttenuation[5];
        
        struct LightInfo
        {
            vec4 position; // eye Coordinates
            vec3 direction; // normalized
            float cutoff; // already calculated
            float exp;
            vec3 La;
            vec3 Li;
        };
        uniform LightInfo light[5];
        
        struct AttenuationInfo
        {
            float Kc;
            float Kl;
            float Kq;
        };
        uniform AttenuationInfo att[5];

        struct MaterialInfo
        {
            vec3 Ka;
            vec3 Kd;
            vec3 Ks;
            float shininess; 
        };
        uniform MaterialInfo material;
        
        out vec4 output_color;
        
        vec3 phongModel(int light_index, vec3 normal, vec3 lightDirection, vec3 viewDirection)
        {
            vec3 r = reflect(-lightDirection, normal);
            vec3 specular = material.Ks * light[light_index].Li * pow(max(dot(r, viewDirection), 0.0), material.shininess);
            return specular;
        }

        vec3 blinnModel(int light_index, vec3 normal, vec3 lightDirection, vec3 viewDirection)
        {
            vec3 halfVector = normalize(lightDirection + viewDirection);
            vec3 specular = material.Ks * light[light_index].Li * pow(max(dot(halfVector, normal), 0.0), material.shininess);
            return specular;
        }

        float attenuationFunc(int light_index, float dist)
        {
            return 1.0 / (att[light_index].Kc + att[light_index].Kl * dist + att[light_index].Kq * dist * dist);
        }
        
        vec3 computeSpecular(int light_index, float lightDotNormal, vec3 normal, vec3 lightDirection, vec3 viewDirection)
        {
            vec3 specular = vec3(0.0);
            if(lightDotNormal > 0.0)
            {
                if(specularModel[light_index] == 6)
                    specular = phongModel(light_index, normal, lightDirection, viewDirection);
                else 
                    specular = blinnModel(light_index, normal, lightDirection, viewDirection);
            }
            return specular;
        }

        vec4 pointLight(int light_index, vec3 normal)
        {
            vec3 ambient =  material.Ka * light[light_index].La;
            vec3 lightDirection = normalize(vec3(light[light_index].position - frag_position));
            float lightDotNormal = max(0.0, dot(normal, lightDirection));
            vec3 diffuse = material.Kd * light[light_index].Li * lightDotNormal;
            vec3 specular = computeSpecular(light_index, lightDotNormal, normal, lightDirection, normalize(-frag_position.xyz));

            if(hasAttenuation[light_index])
            {
                float attenuation = attenuationFunc(light_index, length(vec3(light[light_index].position - frag_position)));
                vec3 rgb = min(frag_color.rgb * (ambient + attenuation * diffuse) + attenuation * specular, vec3(1.0));
                return vec4(rgb, frag_color.a);
            
            } else {
            
                vec3 rgb = min(frag_color.rgb * (ambient + diffuse) + specular, vec3(1.0));
                return vec4(rgb, frag_color.a);
            }
        }
        
        vec4 directionalLight(int light_index, vec3 normal)
        {
            vec3 ambient =  material.Ka * light[light_index].La;
            vec3 lightDirection = -light[light_index].direction;
            float lightDotNormal = max(0.0, dot(normal, lightDirection));
            vec3 diffuse = material.Kd * light[light_index].Li * lightDotNormal;
            vec3 specular = computeSpecular(light_index, lightDotNormal, normal, lightDirection, normalize(-frag_position.xyz));

            vec3 rgb = min(frag_color.rgb * (ambient + diffuse) + specular, vec3(1.0));
            return vec4(rgb, frag_color.a);
        }

        vec4 spotlight(int light_index, vec3 normal)
        {
            vec3 ambient =  material.Ka * light[light_index].La;
            vec3 lightDirection = normalize(vec3(light[light_index].position - frag_position));
            float angle = dot(-lightDirection, light[light_index].direction);
            float cutoff = clamp(light[light_index].cutoff, 0.0, 1.0);

            if(angle > cutoff)
            {
                float lightDotNormal = max(0.0, dot(normal, lightDirection));
                vec3 diffuse = material.Kd * light[light_index].Li * lightDotNormal;
                vec3 specular = computeSpecular(light_index, lightDotNormal, normal, lightDirection, normalize(-frag_position.xyz));
                float falloff = pow(angle, light[light_index].exp);
                
                if(hasAttenuation[light_index])
                {
                    float attenuation = attenuationFunc(light_index, length(vec3(light[light_index].position - frag_position))) * falloff;
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
            output_color = vec4(0.0, 0.0, 0.0, 0.0);
            
            for(int light_index = 0; light_index < 5; light_index++)
            {
                if(isLightEnabled[light_index])
                {
                    if(lightModel[light_index] == 3)
                        output_color += pointLight(light_index, normal);

                    else if(lightModel[light_index] == 4)
                        output_color += directionalLight(light_index, normal);

                    else 
                        output_color += spotlight(light_index, normal);
                }
            }
            
            output_color = min(vec4(output_color.rgb, frag_color.a), vec4(1.0));
        }
        """
        
        self.__maxNumberOfLights = 5
        
        use_uniform_color = 0
        uniform_color = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        
        mvp_matrix = glm.mat4()
        model_view_matrix = glm.mat4()
        
        is_light_enabled = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        is_light_enabled[0] = 1
        light_model = MultiLightPhongShadingShaderProgram.POINT_LIGHT;
        specular_mode = MultiLightPhongShadingShaderProgram.PHONG_SPECULAR;
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
        
        self.__isLightEnabledLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__lightModelLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__specularModelLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__hasAttenuationLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__lightPositionLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__lightDirectionLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__cutoffLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__lightExpLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__lightLaLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__lightLiLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__attKcLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__attKlLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        self.__attKqLoc = np.zeros(self.__maxNumberOfLights, dtype=np.int32)
        
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
        
        for i in range(self.__maxNumberOfLights):
            
            self.__isLightEnabledLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "isLightEnabled[" + str(i) + "]");
            
            self.__lightModelLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "lightModel[" + str(i) + "]");
            self.__specularModelLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "specularModel[" + str(i) + "]");
            self.__hasAttenuationLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "hasAttenuation[" + str(i) + "]");

            gl.glUniform1i(self.__isLightEnabledLoc[i], is_light_enabled[i]);
            gl.glUniform1i(self.__lightModelLoc[i], light_model);
            gl.glUniform1i(self.__specularModelLoc[i], specular_mode);
            gl.glUniform1i(self.__hasAttenuationLoc[i], has_attenuation);

            self.__lightPositionLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light[" + str(i) + "].position");
            self.__lightDirectionLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light[" + str(i) + "].direction");
            self.__cutoffLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light[" + str(i) + "].cutoff");
            self.__lightExpLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light[" + str(i) + "].exp");
            self.__lightLaLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light[" + str(i) + "].La");
            self.__lightLiLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "light[" + str(i) + "].Li");

            gl.glUniform4fv(self.__lightPositionLoc[i], 1, glm.value_ptr(light_position));
            gl.glUniform3fv(self.__lightDirectionLoc[i], 1, glm.value_ptr(light_direction));
            gl.glUniform1f(self.__cutoffLoc[i], math.cos(math.radians(light_cutoff)));
            gl.glUniform1f(self.__lightExpLoc[i], light_exp);
            gl.glUniform3fv(self.__lightLaLoc[i], 1, light_la);
            gl.glUniform3fv(self.__lightLiLoc[i], 1, light_li);

            self.__attKcLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "att[" + str(i) + "].Kc");
            self.__attKlLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "att[" + str(i) + "].Kl");
            self.__attKqLoc[i] = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "att[" + str(i) + "].Kq");

            gl.glUniform1f(self.__attKcLoc[i], att_kc);
            gl.glUniform1f(self.__attKlLoc[i], att_kl);
            gl.glUniform1f(self.__attKqLoc[i], att_kq);
        
        self.__materialKaLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.Ka");
        self.__materialKdLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.Kd");
        self.__materialKsLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.Ks");
        self.__materialShininessLoc = gl.glGetUniformLocation(self.__shaderProgram.getProgramID(), "material.shininess");
        
        gl.glUniform3fv(self.__materialKaLoc, 1, material_ka);
        gl.glUniform3fv(self.__materialKdLoc, 1, material_kd);
        gl.glUniform3fv(self.__materialKsLoc, 1, material_ks);
        gl.glUniform1f(self.__materialShininessLoc, material_shininess);
        
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
    
    def enableLight(self, light_index):
        
        gl.glUniform1i(self.__isLightEnabledLoc[light_index], 1);
    
    def disableLight(self, light_index):
        
        gl.glUniform1i(self.__isLightEnabledLoc[light_index], 0);
        
    def setUniformLightMode(self, light_index, light_mode):
        
        if(light_mode >= 3 and light_mode <= 5):
            gl.glUniform1i(self.__lightModelLoc[light_index], light_mode)
        else:
            print("MultiLightPhongShadingShaderProgram::setUniformLightMode --> modo inválida. Mudando para modo Point light!")
            gl.glUniform1i(self.__lightModelLoc[light_index], MultiLightPhongShadingShaderProgram.POINT_LIGHT)
    
    def setUniformSpecularMode(self, light_index, specular_mode):
        
        if(specular_mode == 6 or specular_mode == 7):
            gl.glUniform1i(self.__specularModelLoc[light_index], specular_mode)
        else:
            print("MultiLightPhongShadingShaderProgram::setUniformSpecularMode --> modo inválida. Mudando para modo Phong specular!")
            gl.glUniform1i(self.__specularModelLoc[light_index], MultiLightPhongShadingShaderProgram.PHONG_SPECULAR)
    
    def useUniformLightAttenuation(self, light_index, state):
        
        if(state):
            gl.glUniform1i(self.__hasAttenuationLoc[light_index], 1)
        else:
            gl.glUniform1i(self.__hasAttenuationLoc[light_index], 0)
    
    def setUniformLightPosition(self, light_index, position):
        
        gl.glUniform4fv(self.__lightPositionLoc[light_index], 1, glm.value_ptr(position));
        
    def setUniformLightDirection(self, light_index, direction):
        
        norm_direction = direction / np.linalg.norm(direction)
        
        gl.glUniform3fv(self.__lightDirectionLoc[light_index], 1, glm.value_ptr(norm_direction));
    
    def setUniformSpotlightCutoff(self, light_index, cutoff_angle):
        
        gl.glUniform1f(self.__cutoffLoc[light_index], 1, math.cos(math.radians(cutoff_angle)));
        
    def setUniformSpotlightExpAtt(self, light_index, exp_att):
        
        gl.glUniform1f(self.__lightExpLoc[light_index], exp_att);
        
    def setUniformLightAmbient(self, light_index, ambiente_color):
        
        gl.glUniform3fv(self.__lightLaLoc[light_index], 1, ambiente_color);
        
    def setUniformLightIntensity(self, light_index, light_color):
        
        gl.glUniform3fv(self.__lightLiLoc[light_index], 1, light_color);

    def setUniformLightConstantAttenuation(self, light_index, const_att):
        
        gl.glUniform1f(self.__attKcLoc[light_index], const_att);
        
    def setUniformLightLinearAttenuation(self, light_index, linear_att):
    
        gl.glUniform1f(self.__attKlLoc[light_index], linear_att);
    
    def setUniformLightQuadraticAttenuation(self, light_index, quadratic_att):
        
        gl.glUniform1f(self.__attKqLoc[light_index], quadratic_att);
        
    def setUniformMaterialAmbient(self, material_ambient):
        
        gl.glUniform3fv(self.__materialKaLoc, 1, material_ambient);

    def setUniformMaterialDiffuse(self, material_diffuse):
        
        gl.glUniform3fv(self.__materialKdLoc, 1, material_diffuse);
        
    def setUniformMaterialSpecular(self, material_specular):
        
        gl.glUniform3fv(self.__materialKsLoc, 1, material_specular);
        
    def setUniformMaterialShininess(self, material_shininess):
        
        gl.glUniform1f(self.__materialShininessLoc, material_shininess);
        
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