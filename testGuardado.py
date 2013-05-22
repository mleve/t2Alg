import struct
import random

dimension = random.randint(2,20)
print dimension
n = random.randint(1,10)
print n

values = []
for i in range(dimension*n):
    values.append(random.random())

print values

with open('test4.bin', 'wb') as f:
    f.write(struct.pack('@ii', dimension, n))
    for value in values:
        f.write(struct.pack('@d', value))

print 'Done.'
