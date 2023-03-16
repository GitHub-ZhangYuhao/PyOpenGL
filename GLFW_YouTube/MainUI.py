import sys

from PySide2.QtGui import QPixmap ,QPicture
from PySide2.QtWidgets import *
from PySide2 import QtWidgets ,QtCore
from GLWindow import *

import GlobalVari




class MainWeidget(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWeidget , self).__init__()
        self.setWindowTitle("MainUI")
        self.setMaximumHeight(512)
        self.setAcceptDrops(True)
        self.InitUI()

    def InitUI(self):
        self.GL_Winow = GLWidget()
        self.setWindowTitle("MainUI")
        #self.setFixedSize(500, 200)  # 设置窗口固定大小
        self.main_widget = QtWidgets.QWidget()
        self.Grid_layout = QtWidgets.QGridLayout()
        self.H_layout = QtWidgets.QHBoxLayout()
        self.V_layout = QtWidgets.QVBoxLayout()
        

        #layout 布局
        self.H_layout.addLayout(self.Grid_layout)
        self.V_layout.addLayout(self.H_layout)
        self.main_widget.setLayout(self.V_layout)
        #self.H_layout.


        self.ImageLabels =[]
        self.PathLabels = []
        ''' TEST '''#TODO: Drag Event To Instand of
        path = "textures/OilTex2.png"  # TODO : Need Remove
        self.btn_test = QtWidgets.QPushButton("AddTexture")
        self.btn_test.clicked.connect(lambda :self.AddTexureLabels(path))
        ''' TEST '''

        self.btnCleanLabels = QtWidgets.QPushButton("CleanImages")
        self.btnCleanLabels.clicked.connect(self.CleanLabels)


        # Layout Widght 布局
        self.H_layout.addWidget(self.GL_Winow)
        self.V_layout.addWidget(self.btn_test)
        self.V_layout.addWidget(self.btnCleanLabels)


        self.setCentralWidget(self.main_widget)

    def CleanLabels(self):
        for ImageLabel in self.ImageLabels:
            ImageLabel.clear()
            self.Grid_layout.removeWidget(ImageLabel)
        for PathLabel in self.PathLabels:
            PathLabel.clear()
            self.Grid_layout.removeWidget(PathLabel)

        self.ImageLabels.clear()
        self.PathLabels.clear()
        self.setCentralWidget(self.main_widget)

    def AddTexureLabels(self , path):
        Label_Layout = QtWidgets.QVBoxLayout()
        V_Space = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)


        item = len(self.ImageLabels)
        row = int(item / 4)
        colums = item % 4

        imageLabel = QtWidgets.QLabel()
        imageLabel.setPixmap(QPixmap(path))
        imageLabel.setFixedSize(64,64)
        imageLabel.setScaledContents(True)
        imageLabel.setToolTip(path)

        pathLabel = QtWidgets.QLabel()
        pathLabel.setText(path)
        pathLabel.setMaximumSize(64,10)
        pathLabel.setToolTip(path)

        Label_Layout.addWidget(imageLabel)
        Label_Layout.addWidget(pathLabel)
        Label_Layout.addItem(V_Space)

        self.Grid_layout.addLayout(Label_Layout ,row ,colums)
        # self.Grid_layout.addWidget(imageLabel ,row ,colums)
        # self.Grid_layout.addWidget(pathLabel ,row , colums)

        self.ImageLabels.append(imageLabel)
        self.PathLabels.append(pathLabel)

        self.setCentralWidget(self.main_widget)

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        if event.mimeData().hasImage:
            event.setDropAction(QtCore.Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            #TODO : 在这里添加Drop函数
            print("导入图片 : " +  file_path)
            self.AddTexureLabels(file_path)


            # TODO : 在这里添加Drop函数
            event.accept()
        else:
            event.ignore()

def Main_UI():

    app = QtWidgets.QApplication(sys.argv)
    GlobalVari.UI_Window = MainWeidget()
    GlobalVari.UI_Window.show()
    app.exec_()
    #sys.exit(app.exec_())




