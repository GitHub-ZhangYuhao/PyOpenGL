import sys

from PySide2.QtGui import QPixmap ,QPicture
from PySide2.QtWidgets import QApplication , QLabel








############################################################

app = QApplication(sys.argv)

TextureLabel = ImageLabel("textures/OilTex2.png")
TextureLabel.Show()

app.exec_()