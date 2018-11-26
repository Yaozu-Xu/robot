# -*- coding: utf-8 -*-
# Time    : 2018/11/26 9:04
# Author  : XYZ
from conf.settings import scatter_path, pie_path
from matplotlib import pyplot as plt
from numpy import arange


def draw_pie(r1, r2):
    path = pie_path
    labels = 'fast', 'low', 'health'
    rate = [r1*100, r2*100, (1-r1-r2)*100]
    explode = [0, 0, 0.1]  # 突出健康部分
    plt.axes(aspect=1)
    plt.pie(x=rate, labels=labels, explode=explode, autopct='%3.1f %%',
            shadow=False, labeldistance=1.1, startangle=90, pctdistance=0.6)
    plt.savefig(path, dpi=300)


def draw_scatter(ox, oy, px, py, lpx, lpy, fpx, fpy):
    """
    :args 模型的所有参数
    绘制两种病的第一阶段内感染范围
    :return: 两种病的感染比率
    """
    figure = plt.figure()
    path = scatter_path
    # 图1 显示快速感染传播范围
    ax1 = figure.add_subplot(121)
    ax1.set_title("疾病类型f")
    # 1. 障碍
    ax1.scatter(ox, oy, s=2, c="black")
    # 2. 植株
    ax1.yaxis.set_visible(False)
    ax1.xaxis.set_visible(False)
    ax1.scatter(px, py, s=1.5, c="green")
    # 3. 慢性病株
    ax1.scatter(lpx, lpy, s=1.5, c="yellow")
    # 4. 快速传播病株 感染半径，感染范围， 标记可能感染植株
    infection_fpx_axis = get_infection_axis(fpx, 0.01)
    infection_fpy_axis = get_infection_axis(fpy, 0.01)
    infection_fpx_spread, infection_fpy_spread = get_infection_spread(infection_fpx_axis, infection_fpy_axis)
    infection_fpx, infection_fpy = prevent_out_range(infection_fpx_spread, infection_fpy_spread, px, py)
    f_rate = infection_rate(infection_fpx, px)
    ax1.scatter(infection_fpx, infection_fpy, s=2, c="purple")

    # 图2显示慢性感染传播范围
    ax2 = figure.add_subplot(122)
    ax2.set_title("疾病类型l")
    ax2.scatter(ox, oy, s=2, c="black")
    ax2.yaxis.set_visible(False)
    ax2.xaxis.set_visible(False)
    ax2.scatter(px, py, s=1.5, c="green")
    ax2.scatter(fpx, fpy, s=1.5, c="purple")
    infection_lpx_axis = get_infection_axis(lpx, 0.02)
    infection_lpy_axis = get_infection_axis(lpy, 0.02)
    infection_lpx, infection_lpy = prevent_out_range(infection_lpx_axis, infection_lpy_axis, px, py)
    l_rate = infection_rate(infection_lpx, px)
    ax2.scatter(infection_lpx, infection_lpy, s=2, c="yellow")
    plt.savefig(path, dpi=400)
    return f_rate, l_rate


def prevent_out_range(fpx, fpy, px, py):
    """
    感染范围超过植物范围
    :return:
    """
    rx = []
    ry = []
    for x, y in zip(fpx, fpy):
        if x not in px or y not in py:
            continue
        rx.append(x)
        ry.append(y)
    return rx, ry


def narrow_axis(l):
    return [float(i)/100 for i in l]


def get_infection_axis(infec, step):
    """

    :param infec: 感染列表
    :param step:  感染半径
    :return:      可能感染的坐标
    """
    res = []
    temp = [arange(x - step, x + step, step) for x in infec]
    for x in temp:
        for i in x:
            if i not in res:
                res.append(i)
    return res


def get_infection_spread(x, y):
    """
    适用于快速扩散类型
    :param x: x坐标列表
    :param y: y坐标列表
    :return:  扩散后坐标
    """
    infect_x = []
    infect_y = []
    for i in x:
        for j in y:
            infect_x.append(i)
            infect_y.append(j)
    return infect_x, infect_y


def infection_rate(x, px):
    return len(x) / len(px)