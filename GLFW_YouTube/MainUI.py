import sys

from PySide2.QtGui import QPixmap ,QPicture
from PySide2.QtWidgets import *
from PySide2 import QtWidgets ,QtCore

import GlobalVari




class MainWeidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWeidget , self).__init__()
        self.setWindowTitle("MainUI")
        self.setMaximumHeight(512)
        self.setDocumentMode(True)
        #self.setWindowFlags(QtCore.Qt.WindowType.WindowMinimizeButtonHint)
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle("MainUI")
        #self.setFixedSize(500, 200)  # 设置窗口固定大小
        self.main_widget = QtWidgets.QWidget()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)

        path = "textures/OilTex2.png" #TODO : Need Remove
        self.ImageLabels =[]
        self.PathLabels = []

        ''' TEST '''
        self.btn_test = QtWidgets.QPushButton()
        self.btn_test.clicked.connect(lambda :self.AddTexureLabels(path))
        self.main_layout.addWidget(self.btn_test)
        ''' TEST '''
        self.btnCleanLabels = QtWidgets.QPushButton("CleanImages")
        self.btnCleanLabels.clicked.connect(self.CleanLabels)
        self.main_layout.addWidget(self.btnCleanLabels)

        self.setCentralWidget(self.main_widget)

    def CleanLabels(self):
        for ImageLabel in self.ImageLabels:
            ImageLabel.clear()
            self.main_layout.removeWidget(ImageLabel)
        for PathLabel in self.PathLabels:
            PathLabel.clear()
            self.main_layout.removeWidget(PathLabel)

        self.ImageLabels.clear()
        self.PathLabels.clear()
        self.setCentralWidget(self.main_widget)


    def AddTexureLabels(self , path):
        imageLabel = QtWidgets.QLabel()
        imageLabel.setPixmap(QPixmap(path))
        imageLabel.setFixedSize(64,64)
        imageLabel.setScaledContents(True)

        pathLabel = QtWidgets.QLabel()
        pathLabel.setText(path)

        self.main_layout.addWidget(imageLabel)
        self.main_layout.addWidget(pathLabel)

        self.ImageLabels.append(imageLabel)
        self.PathLabels.append(pathLabel)

        self.setCentralWidget(self.main_widget)

    def Test(self):
        self.GL = QtWidgets.QOpenGLWidget()
        self.GL.connect()

def Main_UI():

    app = QtWidgets.QApplication(sys.argv)
    GlobalVari.UI_Window = MainWeidget()
    GlobalVari.UI_Window.show()
    app.exec_()
    #sys.exit(app.exec_())




