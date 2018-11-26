# -*- coding: utf-8 -*-


import sys
import os
from conf.settings import astar_pic_path, pie_path, scatter_path
from core import astar, mode
from core.infection import *
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QLabel, QApplication, QPushButton


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.set_up_ui()
        self.data_dic = None

    def set_up_ui(self):
        self.setMinimumHeight(500)
        self.setMinimumWidth(750)
        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('农业机器人病株检测系统')
        # 图片画板1 显示模型和路径规划后的图片
        self.img_board1 = QLabel("图片展示区域", self)
        self.img_board1.setFixedWidth(400)
        self.img_board1.setFixedHeight(200)
        self.img_board1.setScaledContents(True)
        self.img_board1.move(0, 20)
        self.area_mode_button = QPushButton("区域密集型农田", self)
        self.area_mode_button.clicked.connect(self.area_mode_button_click)
        self.show()

    @pyqtSlot()
    def area_mode_button_click(self):
        self.data_dic = mode.area_distribution_mode()
        astar.draw(self.data_dic['ox'], self.data_dic['oy'],
                   self.data_dic['px'], self.data_dic['py'],
                   self.data_dic['lpx'], self.data_dic['lpy'],
                   self.data_dic['fpx'], self.data_dic['fpy'])
        self.open_pic(astar_pic_path)
        return True

    @pyqtSlot()
    def path_button_click(self):
        if not self.data_dic:
            self.data_dic = mode.area_distribution_mode()
        astar.draw(self.data_dic['ox'], self.data_dic['oy'],
                   self.data_dic['px'], self.data_dic['py'],
                   self.data_dic['lpx'], self.data_dic['lpy'],
                   self.data_dic['fpx'], self.data_dic['fpy'], show_path=True)
        return True

    def open_pic(self, path):
        if os.path.exists(path):
            png_obj = QtGui.QPixmap(path)
            self.img_board1.setPixmap(png_obj)
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())