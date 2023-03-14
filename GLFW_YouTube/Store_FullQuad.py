import sys

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
from CommonUtility import *


def Main_OpenGL():

    window = initWindow(800 , 600)

    #Data   :   Position               Color               UV
    vertices = [ 1 ,  1 , 0.0 ,   1.0 , 0.0 , 0.0 ,   1.0 , 1.0 ,
                 1 , -1 , 0.0 ,   0.0 , 1.0 , 0.0 ,   1.0 , 0.0 ,
                -1 , -1 , 0.0 ,   0.0 , 0.0 , 1.0 ,   0.0 , 0.0 ,
                -1 ,  1 , 0.0 ,   1.0 , 1.0 , 0.0 ,   0.0 , 1.0  ]
    indices = [0,1,2,
               0,2,3]
    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices , dtype= np.uint32)

    #Shader Create
    VertexFilePath = "shaders/Vertex.vert"
    FragFilePath = "shaders/Fragment.frag"
    shader = Shader(VertexFilePath, FragFilePath)

    #FBO
    FrameRT = CreateRT(512 , 512 )
    FBO = FrameBuffer(FrameRT ,512 , 512)
    #FBO

    #Texture Create
    TexturePath = "textures/OilTex2.png"
    texture = Texture(TexturePath)
    texture.SetShaderBindIndex(shader, 0)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER , EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER , indices.nbytes , indices ,GL_STATIC_DRAW)
    #position
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(ctypes.c_float)*8, ctypes.c_void_p(0))
    #color
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(ctypes.c_float)*8, ctypes.c_void_p(3*sizeof(ctypes.c_float)))
    #uv
    glEnableVertexAttribArray(2)
    glVertexAttribPointer(2 ,2, GL_FLOAT, GL_FALSE, sizeof(ctypes.c_float)*8, ctypes.c_void_p(6*sizeof(ctypes.c_float)))

    shader.use()
    glClearColor(0, 0.1, 0.1, 1)

    # the main application loop
    while not glfw.window_should_close(window):
        glfw.poll_events()

        glClear(GL_COLOR_BUFFER_BIT)

        #glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
        glDrawElements(GL_TRIANGLES ,len(indices) , GL_UNSIGNED_INT ,None)

        glfw.swap_buffers(window)

        print()

    # terminate glfw, free up allocated resources
    glfw.terminate()

if __name__ == "__main__":
    Main_OpenGL()