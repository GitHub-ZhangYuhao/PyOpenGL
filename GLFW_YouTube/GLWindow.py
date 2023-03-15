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


    def initializeGL(self):
        # Shader Create
        VertexFilePath = "shaders/Vertex.vert"
        FragFilePath = "shaders/Fragment.frag"
        shader = Shader(VertexFilePath, FragFilePath)

        # Texture Create
        TexturePath = "textures/OilTex2.png"
        texture = Texture(TexturePath)
        texture.SetShaderBindIndex(shader, 0)

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
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)


class ButtonApp(QtWidgets.QMainWindow):
    def __init__(self):
        '''
        州的先生 https://zmister.com
        '''
        super().__init__()
        self.setWindowTitle("Qt For Python按钮控件 | 州的先生")
        self.setFixedSize(500, 200)  # 设置窗口固定大小
        self.main_widget = QtWidgets.QWidget()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.btn_1 = QtWidgets.QPushButton("按钮一")
        self.main_layout.addWidget(self.btn_1)

        self.GLWindow = GLWidget()
        self.main_layout.addWidget(self.GLWindow)


        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    app = QApplication([])
    widget = ButtonApp()
    widget.show()
    app.exec_()