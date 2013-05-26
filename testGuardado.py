import struct
import random

dimension = 2
print dimension
n = 10
print n

values = []
for i in range(dimension*n):
    values.append(random.random())

print values

with open('data2D.bin', 'wb') as f:
    f.write(struct.pack('@ii', dimension, n))
    for value in values:
        f.write(struct.pack('@d', value))

print 'Done.'
