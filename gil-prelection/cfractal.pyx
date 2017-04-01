from libc.stdlib cimport malloc, free

cdef int width = 1200
cdef int height = 800

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
    part_height = part_height
    cdef int y_shift = part_height * part_num
    cdef int size = width * part_height
    cdef int *data = <int*>malloc(size * sizeof(int))
    cdef int index=0, x, y
    try:
        with nogil:
            for y in range(part_height):
                for x in range(width):
                    index += 1
                    data[index] = seek_point(x, y + y_shift)
        return [data[i] for i in range(size)]
    finally:
        free(data)

