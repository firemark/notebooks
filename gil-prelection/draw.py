#!/usr/bin/python2
from PIL import Image
from sys import stdin

width = 1200
height = 800
data = stdin.read()

img = Image.new('L', (width, height))
img.putdata([int(x) for x in data.split(' ')])
img.show()

