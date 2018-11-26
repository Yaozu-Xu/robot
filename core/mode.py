# -*- coding: utf-8 -*-
# Time    : 2018/11/22 22:50
# Author  : XYZ
import random
from conf.settings import fast_spread_disease_rate, low_spread_disease_rate


def generate_disease(px, py):
    lpx, lpy = [], []
    fpx, fpy = [], []
    for x, y in zip(px, py):
        if random.random() <= low_spread_disease_rate:
            lpx.append(x)
            lpy.append(y)
        if random.random() <= fast_spread_disease_rate:
            fpx.append(x)
            fpy.append(y)
    return lpx, lpy, fpx, fpy


def average_distribution_mode():
    data_dic = {}
    ox, oy = [], []
    px, py = [], []

    for i in range(10, 51):
        px.append(10)
        py.append(i)
    for i in range(10, 51):
        px.append(30)
        py.append(i)
    for i in range(10, 51):
        px.append(50)
        py.append(i)
    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(20, 41):
        ox.append(20.0)
        oy.append(i)
    for i in range(30, 51):
        ox.append(40.0)
        oy.append(i)
    lpx, lpy, fpx, fpy = generate_disease(px, py)

    data_dic['ox'] = ox
    data_dic['oy'] = oy
    data_dic['px'] = px
    data_dic['py'] = py
    data_dic['lpx'] = lpx
    data_dic['lpy'] = lpy
    data_dic['fpx'] = lpx
    data_dic['fpy'] = fpy
    return data_dic


def area_distribution_mode():
    data_dic = {}
    ox, oy = [], []
    px, py = [], []
    for i in range(10, 20):
        for j in range(10, 20):
            if j == 15:
                continue
            px.append(j)
            py.append(i)
    for i in range(11, 21):
        for j in range(41, 51):
            if j == 45:
                continue
            px.append(j)
            py.append(i)
    for i in range(41, 51):
        for j in range(41, 51):
            if j == 45:
                continue
            px.append(j)
            py.append(i)
    for i in range(40, 50):
        for j in range(10, 20):
            if j == 15:
                continue
            px.append(j)
            py.append(i)

    for i in range(60):
        ox.append(i)
        oy.append(0.0)
    for i in range(60):
        ox.append(60.0)
        oy.append(i)
    for i in range(61):
        ox.append(i)
        oy.append(60.0)
    for i in range(61):
        ox.append(0.0)
        oy.append(i)
    for i in range(0, 51):
        ox.append(20.0)
        oy.append(i)
    for i in range(10, 61):
        ox.append(40.0)
        oy.append(i)
    lpx, lpy, fpx, fpy = generate_disease(px, py)
    data_dic['ox'] = ox
    data_dic['oy'] = oy
    data_dic['px'] = px
    data_dic['py'] = py
    data_dic['lpx'] = lpx
    data_dic['lpy'] = lpy
    data_dic['fpx'] = lpx
    data_dic['fpy'] = fpy
    return data_dic
