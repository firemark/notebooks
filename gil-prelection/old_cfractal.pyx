from libc.stdlib cimport malloc, free

cdef int multipler = 8
cdef int width = 1200 * multipler
cdef int height = 800 * multipler

cdef int seek_point(int x, int y) nogil: 
    cdef double zr = 0.0, zi = 0.0, temp_zr = 0.0
    cdef double pr = 3.0 * <double> x / <double> width - 2.0
    cdef double pi = 2.0 * <double> y / <double> height - 1.0
    cdef int i
    for i in range(256):
        temp_zr = zr * zr - zi * zi + pr
        zi = 2.0 * zr * zi + pi
        zr = temp_zr 
        if zr * zr + zi * zi >= 4.0:
            return i
    return i

def get_points(int part_num, int part_height):
    part_height = part_height * multipler
    cdef int y_shift = part_height * part_num
    return [
        seek_point(x, y)
        for y in range(y_shift, y_shift + part_height)
        for x in range(width)
    ]

