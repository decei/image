import imageio
import numpy
from secrets import randbelow


SEED = 5

numpy.random.seed(SEED)
pix = numpy.random.randint(256, size=(10, 10, 3))
pic = imageio.imwrite("randomii.png", pix.astype(numpy.uint8))

A = numpy.array([1, 2, 3, 4])
B = numpy.array([1, 2, 3, 4])
C = numpy.divide(A, 2)

print(C)
