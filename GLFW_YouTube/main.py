import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import pyrr
from PIL import Image
from CommonUtility import *



import CommonUtility

# vertex_src = """
# # version 330
#
# layout(location = 0) in vec3 a_position;
# layout(location = 1) in vec3 a_color;
#
# uniform mat4 rotation;
#
# out vec3 v_color;
#
# void main()
# {
#     gl_Position = rotation * vec4(a_position, 1.0);
#     v_color = a_color;
# }
# """
#
# fragment_src = """
# # version 330
#
# uniform sampler2D Texture0;
# in vec3 v_color;
# out vec4 out_color;
#
# void main()
# {
#     vec4 Tex = texture(Texture0 , v_color.xy);
#     out_color = vec4(Tex.xyz, 1.0);
# }
# """

def window_resize(window, width, height):
    glViewport(0, 0, width, height)

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

vertices = [-0.5, -0.5, 0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, 0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, 0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, 0.5, 1.0, 1.0, 1.0,

            -0.5, -0.5, -0.5, 1.0, 0.0, 0.0,
             0.5, -0.5, -0.5, 0.0, 1.0, 0.0,
             0.5,  0.5, -0.5, 0.0, 0.0, 1.0,
            -0.5,  0.5, -0.5, 1.0, 1.0, 1.0]

indices = [0, 1, 2, 2, 3, 0,
           4, 5, 6, 6, 7, 4,
           4, 5, 1, 1, 0, 4,
           6, 7, 3, 3, 2, 6,
           5, 6, 2, 2, 1, 5,
           7, 4, 0, 0, 3, 7]

vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

#shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))
VertexFilePath = "shaders/Vertex.vert"
FragFilePath = "shaders/Fragment.frag"
shader = Shader(VertexFilePath , FragFilePath)

# Vertex Buffer Object
VBO = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, VBO)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Element Buffer Object
EBO = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 6, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, vertices.itemsize * 6, ctypes.c_void_p(12))


#Texture
# texture = glGenTextures(1)
# glBindTexture(GL_TEXTURE_2D , texture)
#
# glTexParameteri(GL_TEXTURE_2D , GL_TEXTURE_WRAP_S , GL_REPEAT)
# glTexParameteri(GL_TEXTURE_2D , GL_TEXTURE_WRAP_T , GL_REPEAT)
#
# glTexParameteri(GL_TEXTURE_2D , GL_TEXTURE_MIN_FILTER , GL_LINEAR)
# glTexParameteri(GL_TEXTURE_2D , GL_TEXTURE_MAG_FILTER , GL_LINEAR)



#load Image
# image = Image.open("textures/OilTex2.png")
# imgae = image.transpose(Image.FLIP_TOP_BOTTOM)
# img_data = image.convert("RGBA").tobytes()
# glTexImage2D(GL_TEXTURE_2D , 0 ,GL_RGBA , image.width , image.height , 0 ,GL_RGBA , GL_UNSIGNED_BYTE , img_data)

#set Shader Parameter
# glUseProgram(shader)
# glUniform1i(glGetUniformLocation(shader ,"Texture0") , 0)
# glActiveTexture(GL_TEXTURE0)

texture = CommonUtility.Texture("textures/OilTex2.png")
texture.SetShaderBindIndex(shader.get_shader() , 0)

shader.use()
glClearColor(0, 0.1, 0.1, 1)

glEnable(GL_DEPTH_TEST)
#rotation_loc = glGetUniformLocation(shader.m_shader , "rotation")

# the main application loop
while not glfw.window_should_close(window):
    glfw.poll_events()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    rot_x = pyrr.matrix44.create_from_x_rotation(0.5 * glfw.get_time())
    rot_y = pyrr.matrix44.create_from_y_rotation(0.8 * glfw.get_time())

    rot = pyrr.matrix44.multiply(rot_x , rot_y)

    #glUniformMatrix4fv(rotation_loc , 1 , GL_FALSE , np.dot(rot_x , rot_y))
    shader.set_Mat4("rotation" ,rot_x)


    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    glfw.swap_buffers(window)

# terminate glfw, free up allocated resources
glfw.terminate()






