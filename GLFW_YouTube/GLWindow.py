import ctypes
import logging

import numpy as np
import OpenGL.GL as gl
from PySide2.QtWidgets import QApplication
from PySide2.QtGui import QOpenGLWindow

from CommonUtility import *


# Data   :   Position               Color               UV
vertices = [ 1 ,  1 , 0.0 ,   1.0 , 0.0 , 0.0 ,   1.0 , 1.0 ,
             1 , -1 , 0.0 ,   0.0 , 1.0 , 0.0 ,   1.0 , 0.0 ,
            -1 , -1 , 0.0 ,   0.0 , 0.0 , 1.0 ,   0.0 , 0.0 ,
            -1 ,  1 , 0.0 ,   1.0 , 1.0 , 0.0 ,   0.0 , 1.0  ]
indices = [0,1,2,
           0,2,3]
vertices = np.array(vertices, dtype=np.float32)
indices = np.array(indices, dtype=np.uint32)

class GLWidget(QtWidgets.QOpenGLWidget):
    def __init__(self):
        super(GLWidget, self).__init__()
        #self.setMinimumSize(256 ,256)
        self.Texture_Array = []
        self.setFixedSize(256 , 256)

    def initializeGL(self):
        # Shader Create
        VertexFilePath = "shaders/Vertex.vert"
        FragFilePath = "shaders/Fragment.frag"
        shader = Shader(VertexFilePath, FragFilePath)

        # Texture Create
        TexturePath = "textures/OilTex2.png"
        texture = Texture(TexturePath)
        texture.SetShaderBindIndex(shader, 1)

        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        # position
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sizeof(ctypes.c_float) * 8, ctypes.c_void_p(0))
        # color
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, sizeof(ctypes.c_float) * 8,
                              ctypes.c_void_p(3 * sizeof(ctypes.c_float)))
        # uv
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, sizeof(ctypes.c_float) * 8,
                              ctypes.c_void_p(6 * sizeof(ctypes.c_float)))

        shader.use()
        glClearColor(0, 0.1, 0.1, 1)

    def paintGL(self):
        glClearColor(1, 0.1, 0.1, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    def mouseMoveEvent(self, e):

        self.Mouse_Pos = self.Get_Mouse_Pos(e)
        print(self.Mouse_Pos)

    def Get_Mouse_Pos(self , event):
        Mouse_Pos = event.localPos()
        x = Mouse_Pos.x() / self.width()
        y = Mouse_Pos.y() / self.height()
        return (x,y)

    def Dynamic_Add_Texture(self):
        pass





if __name__ == '__main__':
    app = QApplication([])
    widget = GLWidget()
    widget.show()
    app.exec_()