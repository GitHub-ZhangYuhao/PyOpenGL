import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from PIL import Image



class Texture:

    m_texture = 0
    m_image = 0
    m_img_data = 0
    m_path = ""
    m_Format = GL_RGBA
    m_WrapMode = GL_REPEAT
    m_FilterMode = GL_LINEAR

    def CreateTexture(self):
        self.m_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D , self.m_texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, self.m_WrapMode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, self.m_WrapMode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, self.m_FilterMode)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, self.m_FilterMode)

    def SetImageData(self):
        self.m_image = Image.open(self.m_path)
        self.m_image = self.m_image.transpose(Image.FLIP_TOP_BOTTOM)
        self.m_img_data = self.m_image.convert("RGBA").tobytes()

    def FillImageData(self ):
        glTexImage2D(GL_TEXTURE_2D , 0, self.m_Format , self.m_image.width , self.m_image.height ,0 ,self.m_Format , GL_UNSIGNED_BYTE ,self.m_img_data)

    #设置Shader绑定Uniform Texture_
    def SetShaderBindIndex(self , Shader , TextureBindIndex):
        glUseProgram(Shader)
        BindName = "Texture" + str(TextureBindIndex)
        glUniform1i(glGetUniformLocation(Shader , BindName) , TextureBindIndex)
        glActiveTexture(GL_TEXTURE0 + TextureBindIndex)


    def __init__(self , path ,Format = GL_RGBA, WrapMode = GL_REPEAT , FilterMode = GL_LINEAR):
        self.m_path = path
        self.m_Format = Format
        self.m_WrapMode = WrapMode
        self.m_FilterMode = FilterMode

        self.CreateTexture()
        self.SetImageData()
        self.FillImageData()
