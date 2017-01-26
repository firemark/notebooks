from threading import Thread
from fractal import get_points, show_image
from sys import argv

n = int(argv[1])
data = [None] * n

def func(part_num):
    data[part_num] = get_points(part_num)

threads = [Thread(target=func, args=(i,)) for i in range(n)]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()

show_image(data)
