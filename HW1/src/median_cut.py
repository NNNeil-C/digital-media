#!/usr/bin/env python
# encoding: utf-8
'''
@author: TszFung_Chan
@contact: ex_lunatic@hotmail.com
@software: TszFung_Chan
@file: median_cut_mannual
@time: 2018/10/17 14:16
@desc: median_cut and fit the img manually
'''

from PIL import Image
import numpy as np
import time
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# median-cut algorithm, implement by DFS
def median_cut(current_lis, depth):
    if depth == 8:
        # store all colors(RGB) of this part into all_color
        all_color = []
        for coordinate in current_lis:
            x = coordinate[0]
            y = coordinate[1]
            all_color.append(img.getpixel((x, y)))

        # get the average RGB value
        new_color = np.array(all_color).mean(axis=0)

        # add the average RGB value into LUT
        LUT.append(new_color)
        LUT_linear.append(int(new_color[0]))
        LUT_linear.append(int(new_color[1]))
        LUT_linear.append(int(new_color[2]))
        return

    rgb_max = [0, 0, 0]
    rgb_min = [256, 256, 256]

    # get the max and min rgb in current part
    for coordinate in current_lis:
        x = coordinate[0]
        y = coordinate[1]
        rgb_pixel = img.getpixel((x, y))

        for i in range(3):
            rgb_max[i] = max(rgb_max[i], rgb_pixel[i])
            rgb_min[i] = min(rgb_min[i], rgb_pixel[i])

    # get the rgb range in current part
    rgb_range = rgb_max.copy()
    for i in range(3):
        rgb_range[i] -= rgb_min[i]

    # sort the pixel in the part according to the channel that vary most
    for i in range(3):
        if rgb_range[i] == max(rgb_range):
            current_lis = sorted(current_lis, key=lambda value: img.getpixel((value[0], value[1]))[i])
            break

    # spilt current part into 2 parts, and do the same thing in each new part
    median_cut(current_lis[0: int(len(current_lis) / 2)], depth + 1)
    median_cut(current_lis[int(len(current_lis) / 2): ], depth + 1)


# convert the 24-bit image to a 8-bit image using the LUT from median-cut algorithm
def to8bit():
    global img_8bit
    global LUT
    global LUT_linear
    # create a 8-bit image using the LUT
    img_8bit = img_8bit.convert(mode='P')
    img_8bit.putpalette(LUT_linear)

    LUT = np.array(LUT)
    # set the value of each pixel according to the LUT
    for i in range(img_8bit.size[0]):
        for j in range(img_8bit.size[1]):
            # calculate the distance between LUT and current pixel
            dis = distance(LUT, np.array(img.getpixel((i, j))))
            # find the nearest color in LUT
            nearest = 1000000
            mark = -1
            for idx, dist in enumerate(dis):
                if dist < nearest:
                    nearest = dist
                    mark = idx
            # set pixel
            img_8bit.putpixel((i, j), mark)

    # save the 8-bit image
    img_8bit.save("../result/redapple_8bit.bmp")


# calculate the distance between LUT and current pixel
def distance(LUT, pixel):
    return np.sqrt(np.sum((LUT - pixel) ** 2, axis=1))


def draw_lut(LUT):
    map = plt.subplot(111, projection='3d')
    for i in range(256):
        color = [[LUT[i][0] / 255, LUT[i][1] / 255, LUT[i][2] / 255], ]
        map.scatter(LUT[i][0], LUT[i][1], LUT[i][2], s=10, c=color)

    map.set_xlabel('R')
    map.set_ylabel('G')
    map.set_zlabel('B')
    plt.show()


beginning = time.time()
# open image
img = Image.open("../assets/redapple.jpg")
img_8bit = img.copy()

lis = list([[] for i in range(512)])

# put all pixels in one part
for i in range(img.size[0]):
    for j in range(img.size[1]):
        lis[0].append([i, j])

LUT = []
LUT_linear = []

# run median-cut algorithm to get the LUT
median_cut(lis[0], 0)

# run the converter
to8bit()

ending = time.time()
print(ending - beginning)

# draw_lut(LUT)
