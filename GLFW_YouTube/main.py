import Store_FullQuad


Store_FullQuad.Main_OpenGL()




import numpy as np
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from PIL import Image

# def init():
#     # 设置窗口大小
#     glutInitWindowSize(600, 600)
#     # 创建窗口
#     glutCreateWindow(b"PyOpenGL 示例程序")
#     # 设置窗口背景颜色
#     glClearColor(0.0, 0.0, 0.0, 1.0)
#     # 设置纹理参数
#     glEnable(GL_TEXTURE_2D)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
#     glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#
#     # 加载纹理
#     img = Image.open("texture.png")
#     img_data = np.array(list(img.getdata()), np.uint8)
#     glBindTexture(GL_TEXTURE_2D, 1)
#     glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
#
# def display():
#     # 清除颜色缓冲区
#     glClear(GL_COLOR_BUFFER_BIT)
#     # 绘制矩形并显示纹理
#     glBegin(GL_QUADS)
#     glTexCoord2f(0.0, 0.0); glVertex2f(-0.5, -0.5)
#     glTexCoord2f(1.0, 0.0); glVertex2f(0.5, -0.5)
#     glTexCoord2f(1.0, 1.0); glVertex2f(0.5, 0.5)
#     glTexCoord2f(0.0, 1.0); glVertex2f(-0.5, 0.5)
#     glEnd()
#
#     # 获取纹理的像素数据
#     pixels = glReadPixels(0, 0, img.width, img.height, GL_RGBA, GL_UNSIGNED_BYTE)
#
#     # 将像素数据转换成图像并保存
#     img_out = Image.frombytes("RGBA", (img.width, img.height), pixels)
#     img_out.save("texture_out.png")
#
#     # 刷新窗口
#     glutSwapBuffers()
#
# if __name__ == '__main__':
#     glutInit()
#     glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
#     init()
#     glutDisplayFunc(display)
#     glutIdleFunc(display)
#     glutMainLoop()