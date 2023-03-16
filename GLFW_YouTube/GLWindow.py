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
        self.setMinimumSize(512 ,512)


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


class ImageLabel(QtWidgets.QWidget):
    def __init__(self , Path):
        super(ImageLabel, self).__init__()

        self.PathLabel = QtWidgets.QLabel(Path)     # path

        self.ImageLabel = QtWidgets.QLabel()
        self.ImageLabel.setPixmap(QPixmap(Path))
        self.ImageLabel.setFixedSize(200 , 200)
        self.ImageLabel.setScaledContents(True)

        Layout = QtWidgets.QVBoxLayout()
        Layout.addWidget(self.ImageLabel)
        Layout.addWidget(self.PathLabel)

        self.setLayout(Layout)

class MainApp(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        self.ImageLabel_Array = []
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle("主窗口")
        #self.setFixedSize(500, 200)  # 设置窗口固定大小
        self.main_widget = QtWidgets.QWidget()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        self.btn_1 = QtWidgets.QPushButton("按钮一")
        self.btn_1.clicked.connect(lambda:self.AddImageLabelList("textures/OilTex2.png"))
        self.main_layout.addWidget(self.btn_1)

        self.btn_2 = QtWidgets.QPushButton("按钮二")
        self.btn_2.clicked.connect(self.PopImageLabel)
        self.main_layout.addWidget(self.btn_2)

        self.GLWindow = GLWidget()
        self.main_layout.addWidget(self.GLWindow)

        #TODO : Label Test
        Path = "textures/OilTex2.png"
        self.AddImageLabelList(Path)

        self.setCentralWidget(self.main_widget)

    def AddImageLabelList(self , Path):
        imageLabel = ImageLabel(Path)
        self.main_layout.addWidget(imageLabel)
        self.ImageLabel_Array.append(imageLabel)
        self.setCentralWidget(self.main_widget)

    def PopImageLabel(self):
        self.main_layout.removeWidget(self.ImageLabel_Array[len(self.ImageLabel_Array) - 1])
        self.ImageLabel_Array.pop()
        self.setCentralWidget(self.main_widget)
        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    app = QApplication([])
    widget = MainApp()
    widget.show()
    app.exec_()