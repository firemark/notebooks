from threading import Thread
from cfractal import get_points
from fractal import show_image, part_height
from sys import argv

n = int(argv[1])
data = [None] * n

def func(part_num):
    data[part_num] = get_points(part_num, part_height)

threads = [Thread(target=func, args=(i,)) for i in range(n)]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

show_image(data)
