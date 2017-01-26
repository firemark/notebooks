from sys import argv
from PIL import Image
from itertools import chain

n = int(argv[1])
width = 1200
height = 800
part_height = height // n


def seek_point(x, y): 
    p = complex(3.0 * x / width - 2.0, 2.0 * y / height - 1.0)
    z = complex(.0, .0) 
    for i in range(256):
        z = z * z + p 
        if abs(z) >= 2.0:
            return i
    return i


def get_points(part_num):
    y_shift = part_height * part_num
    return [
        seek_point(x, y)
        for y in range(y_shift, y_shift + part_height)
        for x in range(width)
    ]


def show_image(data):
    im = Image.new('L', (width, height))
    im.putdata(list(chain.from_iterable(data)))
    im.show()

