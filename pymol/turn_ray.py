#! /usr/bin/python

"""
A script that will execute a 360 degree spin of the structure, ray-tracing the
structure at each interval and saving the image.
"""

from pymol import cmd
import os.path

FRAMES = 360  # How many frames to spread the spin over
AXIS = 'y'  # The axis about which to spin
OUTPUT = 'turn_ray_images'  # The output directory for images
RAY_X = 0  # The x-dimension of the image, 0 will use current window size
RAY_Y = 0  # The y-dimension of the image, 0 will use current window size

os.mkdir(OUTPUT)

for i in xrange(FRAMES):
    cmd.turn(AXIS, 360.0 / FRAMES)
    cmd.ray(width=RAY_X, height=RAY_Y)
    frame_name = '{0}.png'.format(str(i).zfill(4))
    cmd.png(os.path.join(os.getcwd(), OUTPUT, frame_name))
