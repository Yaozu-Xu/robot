# -*- coding: utf-8 -*-
# Time    : 2018/11/1 11:35
# Author  : XYZ
import math
import matplotlib
import matplotlib.pyplot as plt
from conf.settings import *
from core.search import *
matplotlib.rcParams['animation.convert_path'] = 'D:\\ImageMagick-7.0.8-Q16\\convert.exe'

'''
f(n) = g(n) + h(n)
f(n):节点n的估价函数。
g(n)：从起始点到n节点的实际代价。
h(n)：从节点n到目标节点最佳路径的估计代价。

'''

show_animation = True


class Node:
    def __init__(self, x, y, cost, pind):
        self.x = x
        self.y = y
        self.cost = cost
        self.pind = pind

    def __str__(self):
        return str(self.x) + "," + str(self.y) + "," + str(self.cost) + "," + str(self.pind)


def calc_fianl_path(ngoal, closedset, reso):
    # generate final course

    rx, ry = [ngoal.x * reso], [ngoal.y * reso]
    pind = ngoal.pind
    while pind != -1:
        n = closedset[pind]
        rx.append(n.x * reso)
        ry.append(n.y * reso)
        pind = n.pind
    return rx, ry


def a_star_planning(sx, sy, gx, gy, ox, oy, reso, rr):
    """
       gx,gy : 终点x,y
       ox,oy:  障碍物的x,y的列表
       reso: 格子的大小
       rr:   机器人的半径
    """
    nstart = Node(round(sx / reso), round(sy / reso), 0.0, -1)
    ngoal = Node(round(gx / reso), round(gy / reso), 0.0, -1)
    ox = [i / reso for i in ox]
    oy = [i / reso for i in oy]
    obmap, minx, miny, maxx, maxy, xw, yw = calc_obstacle_map(ox, oy, reso, rr)

    motion = get_motion_model()

    openset, closedset = dict(), dict()
    openset[calc_index(nstart, xw, minx, miny)] = nstart

    while 1:
        c_id = min(
            openset, key=lambda o: openset[o].cost + calc_heuristic(ngoal, openset[o]))
        current = openset[c_id]

        # show graph
        # if show_animation:
        #     plt.plot(current.x * reso, current.y * reso, "xc")
        #     if len(closedset.keys()) % 10 == 0:
        #         plt.pause(0.001)

        if current.x == ngoal.x and current.y == ngoal.y:
            print("Find goal")
            ngoal.pind = current.pind
            ngoal.cost = current.cost
            break

        # Remove the item from the open set
        del openset[c_id]
        # Add it to the closed set
        closedset[c_id] = current

        # expand search grid based on motion model
        for i in range(len(motion)):
            node = Node(current.x + motion[i][0],
                        current.y + motion[i][1],
                        current.cost + motion[i][2], c_id)
            print(node)
            n_id = calc_index(node, xw, minx, miny)

            if n_id in closedset:
                continue

            if not verify_node(node, obmap, minx, miny, maxx, maxy):
                continue

            if n_id not in openset:
                openset[n_id] = node  # Discover a new node
            else:
                if openset[n_id].cost >= node.cost:
                    # print(openset[n_id].cost)
                    # This path is the best until now. record it!
                    openset[n_id] = node

    rx, ry = calc_fianl_path(ngoal, closedset, reso)
    return rx, ry


def calc_heuristic(n1, n2):
    w = 1.0  # weight of heuristic
    d = w * math.sqrt((n1.x - n2.x)**2 + (n1.y - n2.y)**2)
    return d


def verify_node(node, obmap, minx, miny, maxx, maxy):

    if node.x < minx:
        return False
    elif node.y < miny:
        return False
    elif node.x >= maxx:
        return False
    elif node.y >= maxy:
        return False

    if obmap[node.x][node.y]:
        return False
    return True


def calc_index(node, xwidth, xmin, ymin):
    return (node.y - ymin) * xwidth + (node.x - xmin)


def get_motion_model():
    # dx, dy, cost
    motion = [[1, 0, 1],
              [0, 1, 1],
              [-1, 0, 1],
              [0, -1, 1],
              [-1, -1, math.sqrt(2)],
              [-1, 1, math.sqrt(2)],
              [1, -1, math.sqrt(2)],
              [1, 1, math.sqrt(2)]]

    return motion


def calc_obstacle_map(ox, oy, reso, vr):

    minx = round(min(ox))
    miny = round(min(oy))
    maxx = round(max(ox))
    maxy = round(max(oy))
    #  print("minx:", minx)
    #  print("miny:", miny)
    #  print("maxx:", maxx)
    #  print("maxy:", maxy)

    xwidth = round(maxx - minx)
    ywidth = round(maxy - miny)
    #  print("xwidth:", xwidth)
    #  print("ywidth:", ywidth)

    # obstacle map generation
    obmap = [[False for _ in range(xwidth)] for _ in range(ywidth)]
    for ix in range(xwidth):
        x = ix + minx
        for iy in range(ywidth):
            y = iy + miny
            #  print(x, y)
            for iox, ioy in zip(ox, oy):
                d = math.sqrt((iox - x)**2 + (ioy - y)**2)
                if d <= vr / reso:
                    obmap[ix][iy] = True
                    break

    return obmap, minx, miny, maxx, maxy, xwidth, ywidth


def draw(ox, oy, px, py, lpx, lpy, fpx, fpy, show_path=False):
    sx, sy, gx, gy = area_mode.values()
    # 传入障碍物的横纵列表 和 植株的横纵列表
    plt.plot(ox, oy, ".k", label="o")  # obstacle
    plt.plot(sx, sy, "xr", label="s")  # 起点
    plt.plot(gx, gy, "xb", label="g")  # 终点
    plt.plot(px, py, "*g", label="p")  # 植株
    plt.plot(lpx, lpy, "*y", label="lp")  # 慢性传播
    plt.plot(fpx, fpy, "*", color="purple", label="fp")  # 快速传播
    plt.grid(True)
    plt.axis("equal")
    plt.legend(loc=2, ncol=1)
    if show_path:
        print('show path')
        rx, ry = a_star_planning(sx, sy, gx, gy, ox, oy, grid_size, robot_size)
        plt.plot(rx, ry, "-r")
        # 以疾病植株为圆心的搜索策略
        fast_search(plt, fpx, fpy)
    plt.savefig(astar_pic_path, dpi=400)

