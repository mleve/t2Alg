import struct

values = []

with open('test4.bin', 'rb') as f:
    metadata = struct.unpack('@ii', f.read(8))
    dimension = metadata[0]
    print dimension
    n = metadata[1]
    print n
    for i in range(dimension*n):
        values.append(struct.unpack('@d', f.read(8))[0])

print values
print 'Done.'
