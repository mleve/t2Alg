import struct
import random

dimension = 3
print dimension
n = 50
print n

values = []
for i in range(dimension*n):
    values.append(random.random())

print values

with open('test3D.bin', 'wb') as f:
    f.write(struct.pack('@ii', dimension, n))
    for value in values:
        f.write(struct.pack('@d', value))

print 'Done.'
