import os.path

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from PIL import Image
from glfw import *


#---------------------Functions---------------------
def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def initWindow(width ,height):
    # initializing glfw library
    if not init():
        raise Exception("glfw can not be initialized!")

    # creating the window
    window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

    # check if window was created
    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    # set window's position
    glfw.set_window_pos(window, 400, 200)

    # set the callback function for window resize
    glfw.set_window_size_callback(window, window_resize)

    # make the context current
    glfw.make_context_current(window)

    return window

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

def initWindow(width ,height):
    # initializing glfw library
    if not glfw.init():
        raise Exception("glfw can not be initialized!")

    # creating the window
    window = glfw.create_window(1280, 720, "My OpenGL window", None, None)

    # check if window was created
    if not window:
        glfw.terminate()
        raise Exception("glfw window can not be created!")

    # set window's position
    glfw.set_window_pos(window, 400, 200)

    # set the callback function for window resize
    glfw.set_window_size_callback(window, window_resize)

    # make the context current
    glfw.make_context_current(window)

    return window

def CreateRT(width , height  , Format = GL_RGBA, WrapMode = GL_REPEAT , FilterMode = GL_LINEAR , data = None):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, WrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, WrapMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, FilterMode)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, FilterMode)
    glTexImage2D(GL_TEXTURE_2D, 0, Format, width, height, 0, Format,
                 GL_UNSIGNED_BYTE, data)
    glBindTexture(GL_TEXTURE_2D , 0)
    return texture

def SaveTexture(window , Path ,width , height , Format=GL_RGBA ,Type=GL_UNSIGNED_BYTE):
    Cur_Width , Cur_Height = glfw.get_window_size(window)
    glViewport(0,0, width , height)

    pixels = glReadPixels(0,0, width , height,Format , Type)
    img_out = Image.frombytes("RGBA" , (width , height) ,pixels)
    img_out = img_out.transpose(Image.FLIP_TOP_BOTTOM)

    folderPath = os.path.dirname(Path)
    if not os.path.exists(folderPath):
        os.makedirs(folderPath)
    img_out.save(Path )
    glViewport(0,0,Cur_Width , Cur_Height)

def Cursor_Event(window):
    WindowSize_X , WindowSize_Y = glfw.get_window_size(window)
    cursorPos_X , cursorPos_Y = glfw.get_cursor_pos(window)
    ScreenCoord = ( cursorPos_X / WindowSize_X , cursorPos_Y / WindowSize_Y)
    if(ScreenCoord[0] >1 or ScreenCoord[0] <0 or ScreenCoord[1]>1 or ScreenCoord[1]<0):
        return
    print( ScreenCoord)

def ProcessInput(window):
    if(glfw.get_key(window , glfw.KEY_ESCAPE) == glfw.PRESS ):
        glfw.set_window_should_close(window , True)
    Cursor_Event(window)

#---------------------Functions---------------------

#---------------------Class---------------------
class Shader:
    m_shader = 0
    def __init__(self , VertexFilePath , FragmentFilePath):
        vertexCode = ""
        fragmentCode =  ""
        with open(VertexFilePath , "r") as vertFile:
            vertexCode = vertFile.read()
        with open(FragmentFilePath , "r") as fragFile:
            fragmentCode = fragFile.read()
        #Debug
        #print(vertexCode + "\n")
        #print(fragmentCode + "\n")

        self.m_shader = compileProgram(compileShader(vertexCode ,GL_VERTEX_SHADER),
                                       compileShader(fragmentCode , GL_FRAGMENT_SHADER))

    def get_shader(self):
        return self.m_shader
    def use(self):
        glUseProgram(self.m_shader)
    def set_float(self , name,value):
        variLocation = glGetUniformLocation( self.m_shader , name)
        glUniform1f(variLocation ,value)

    def set_Int(self , name,value):
        variLocation = glGetUniformLocation( self.m_shader , name)
        glUniform1i(variLocation ,value)

    def set_Vec(self, name, value):
        variLocation = glGetUniformLocation(self.m_shader, name)
        glUniform3fv(variLocation , 1 , value)

    def set_Mat4(self, name, value):
        variLocation = glGetUniformLocation(self.m_shader, name)
        glUniformMatrix4fv(variLocation , 1 ,GL_FALSE , value)

class Texture:
    # 初始化Texture后直接调用SetShaderBindIndex()    把Texture 绑定到Shader的Texture? (?是索引)
    m_texture = 0
    m_image = 0
    m_img_data = 0
    m_path = ""
    m_Format = GL_RGBA
    m_WrapMode = GL_REPEAT
    m_FilterMode = GL_LINEAR

    def GetExtent(self):
        return (self.m_image.width , self.m_image.height)

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
        glUseProgram(Shader.get_shader())
        BindName = "Texture" + str(TextureBindIndex)
        glUniform1i(glGetUniformLocation(Shader.get_shader() , BindName) , TextureBindIndex)
        glActiveTexture(GL_TEXTURE0 + TextureBindIndex)


    def __init__(self , path ,Format = GL_RGBA, WrapMode = GL_REPEAT , FilterMode = GL_LINEAR):
        self.m_path = path
        self.m_Format = Format
        self.m_WrapMode = WrapMode
        self.m_FilterMode = FilterMode

        self.CreateTexture()
        self.SetImageData()
        self.FillImageData()

class FrameBuffer:
    m_Texture = None
    m_Frame_Buffer = None
    m_Depth_Buff = None

    def Get_Extent(self):
        return (self.m_Texture.m_Width , self.m_Texture.m_Height)

    def Get_FBO(self):
        return self.m_Frame_Buffer

    def __init__(self , texture , width , height):
        self.m_Texture = texture;

        self.m_Depth_Buff = glGenRenderbuffers(1)
        self.m_Frame_Buffer = glGenFramebuffers(1)

        glBindRenderbuffer(GL_RENDERBUFFER , self.m_Depth_Buff)
        glRenderbufferStorage(GL_RENDERBUFFER , GL_DEPTH_COMPONENT ,width , height)

        glBindFramebuffer(GL_FRAMEBUFFER , self.m_Frame_Buffer)
        glFramebufferTexture2D(GL_FRAMEBUFFER , GL_COLOR_ATTACHMENT0 , GL_TEXTURE_2D , self.m_Texture , 0)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER , GL_DEPTH_ATTACHMENT , GL_RENDERBUFFER , self.m_Depth_Buff)
        glBindFramebuffer(GL_FRAMEBUFFER , 0)
        glBindRenderbuffer(GL_RENDERBUFFER , 0)
#---------------------Class---------------------