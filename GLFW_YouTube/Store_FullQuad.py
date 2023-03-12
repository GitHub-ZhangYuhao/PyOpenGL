import sys

import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec3 a_color;
layout(location = 2) in vec2 a_UV;

out vec3 v_color;
out vec2 uv;

void main()
{
    gl_Position = vec4(a_position, 1.0);
    v_color = a_color;
    uv = a_UV;
}
"""

fragment_src = """
# version 330

in vec3 v_color;
in vec2 uv;
out vec4 out_color;

void main()
{
    out_color = vec4(v_color, 1.0);
    out_color = vec4(uv, 0,1.0);
}
"""

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


def Main_OpenGL():

    window = initWindow(800 , 600)

    #Data   :   Position               Color               UV
    vertices = [ 0.5 ,  0.5 , 0.0 ,   1.0 , 0.0 , 0.0 ,   1.0 , 1.0 ,
                 0.5 , -0.5 , 0.0 ,   0.0 , 1.0 , 0.0 ,   1.0 , 0.0 ,
                -0.5 , -0.5 , 0.0 ,   0.0 , 0.0 , 1.0 ,   0.0 , 0.0 ,
                -0.5 ,  0.5 , 0.0 ,   1.0 , 1.0 , 0.0 ,   0.0 , 1.0  ]

    indices = [0,1,2,
               0,2,3]

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices , dtype= np.uint32)

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

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

    glUseProgram(shader)
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