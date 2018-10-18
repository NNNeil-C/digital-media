#!/usr/bin/env python
# encoding: utf-8
'''
@author: TszFung_Chan
@contact: ex_lunatic@hotmail.com
@software: TszFung_Chan
@file: transition
@time: 2018/10/8 14:57
@desc: image A to image B
'''

from PIL import Image
import numpy
import imageio
import time

beginning = time.time()
# open images
imgA = Image.open("../assets/诺贝尔.jpg")
imgB = Image.open("../assets/lena.jpg")

# get the red channel
Ar, Ag, Ab = imgA.split()
Br, Bg, Bb = imgB.split()
pre_image = Ar
nxt_image = Br

width = pre_image.size[0]
height = nxt_image.size[1]

# the half diagonal
radius = numpy.sqrt(numpy.square(width) + numpy.square(height)) / 2

# the center pixel of image
center = numpy.array([width / 2, height / 2])

# the gif frames
frames = []

# produce 25 frames
for i in range(25):
    cur_image = pre_image.copy()
    # set pixel of the current frame image
    for x in range(0, width):
        for y in range(0, height):
            vector = numpy.array([x, y])
            # calculate the distance between current position and center position
            if numpy.linalg.norm(center - vector) < i / 24 * radius:
                # set pixel
                cur_image.putpixel((x, y), (nxt_image.getpixel((x, y))))
    # save the frames to the disk
    cur_image.save("../frames/{0}.jpg".format(i))
    # store the frames
    frames.append(numpy.array(cur_image))

output_file_name = "../result/transition.gif"
imageio.mimsave(output_file_name, frames, 'GIF', duration=0.04)

ending = time.time()
print(ending - beginning)