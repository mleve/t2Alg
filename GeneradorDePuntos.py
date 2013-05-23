import struct
import random

def generar(dimPuntos, numPuntos):
    nombreArchivo = "data"+str(dimPuntos)+"D.bin"
    print nombreArchivo
    with open(nombreArchivo, 'wb') as f:
        f.write(struct.pack('ii', dimPuntos, numPuntos))
        for i in range(dimPuntos*numPuntos):
            f.write(struct.pack('d', random.random()))
