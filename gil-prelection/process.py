from multiprocessing import Process
from fractal import get_points, show_image
from sys import argv

n = int(argv[1])
data = [None] * n

def func(part_num):
    data[part_num] = get_points(part_num)

processes = [Process(target=func, args=(i,)) for i in range(n)]

for process in processes:
    process.start()
for process in processes:
    process.join()

show_image(data)
