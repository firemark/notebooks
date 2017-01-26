from multiprocessing import Process, Queue
from fractal import get_points, show_image
from sys import argv

n = int(argv[1])
data = [None] * n
queue = Queue()

def func(queue, part_num):
    queue.put([part_num, get_points(part_num)])

processes = [Process(target=func, args=(queue, i)) for i in range(n)]

for process in processes:
    process.start()

for i in range(n):
    part_num, result = queue.get()
    data[part_num] = result

for process in processes:
    process.join()

show_image(data)
