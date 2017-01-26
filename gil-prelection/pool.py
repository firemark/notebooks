from multiprocessing import Pool
from fractal import get_points, show_image
from sys import argv

n = int(argv[1])
pool = Pool(n)
data = pool.map(get_points, range(n))
show_image(data)
