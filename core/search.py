# -*- coding: utf-8 -*-
# Time    : 2018/11/23 8:58
# Author  : XYZ
from conf.settings import fast_spread, low_spread
import math


def fast_search(plt, fx, fy):
    r = fast_spread
    sep = 2*math.pi/360
    for x, y in zip(fx, fy):
        point_x = []
        point_y = []
        for angle in range(361):
            cx = x + r * math.cos(sep*angle)
            cy = y + r * math.sin(sep*angle)
            point_x.append(cx)
            point_y.append(cy)
        plt.plot(point_x, point_y, "-", color="purple")



