# -*- coding: utf-8 -*-
# Time    : 2018/11/23 9:31
# Author  : XYZ
import sys
from core import astar, mode
from core.infection import *
from PyQt5 import QtWidgets, QtGui


def test():
    # 生成模型
    ox, oy, px, py, lpx, lpy, fpx, fpy = mode.area_distribution_mode()
    # 搜索路线
    astar.draw(ox, oy, px, py, lpx, lpy, fpx, fpy)
    # 点图
    r1, r2 = draw_scatter(ox, oy, px, py, lpx, lpy, fpx, fpy)
    # 调整参数范围
    ox = narrow_axis(ox)
    oy = narrow_axis(oy)
    px = narrow_axis(px)
    py = narrow_axis(py)
    lpx = narrow_axis(lpx)
    lpy = narrow_axis(lpy)
    fpx = narrow_axis(fpx)
    fpy = narrow_axis(fpy)
    # 饼图
    draw_pie(r1, r2)


app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget()
window.show()
sys.exit(app.exec_())