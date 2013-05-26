import RTree
import GeneradorDePuntos
import struct
def loadRTree():
        #generateInputs()
        resultado = open("resultados.csv", 'w')
        for i in range(2,20):
                fileName  = "data"+str(i)+"D.bin"
                with open(fileName,'rb') as f:
                        #Obtener Dimension y numero de vertices
                        metadata = struct.unpack('@ii',f.read(8))
                        dimension = metadata[0]
                        points = metadata[1]
                        #Inicializar arbol
                        rtree = RTree.RTree(dimension)
                        for i in range(points):
                        #Obtener proximo punto (vector) a insertar
                                vector = []
                                for j in range(dimension):
                                        vector.append(struct.unpack('@d',f.read(8))[0])
                                #insertar el nuevo vector en el arbol
                                #print vector                             
                                rtree.insertar(rtree.chooseLeaf(rtree,vector),vector)
                #print rtree.printRTree()
        #print "puntos:"
        #print rtree.getPoints(rtree)
                radio = getRadio(i)
                testPoints = getConsultPoints(i)
                resultado.write("Resultados dimension: "+i+" \n")
                for point in testPoints:
                        res = rtree.rangeQuery(point,radio,rtree)
                        resultado.write(len(res[0]) + ";" + res[1] +" \n")

        resultado.close()
        """ 
        fileName  = "data2D.bin"
        with open(fileName,'rb') as f:
                #Obtener Dimension y numero de vertices
                metadata = struct.unpack('@ii',f.read(8))
                dimension = metadata[0]
                points = metadata[1]
                #Inicializar arbol
                rtree = RTree.RTree(dimension)
                for i in range(points):
                #Obtener proximo punto (vector) a insertar
                        vector = []
                        for j in range(dimension):
                                vector.append(struct.unpack('@d',f.read(8))[0])
                        #insertar el nuevo vector en el arbol
                        #print vector                             
                        rtree.insertar(rtree.chooseLeaf(rtree,vector),vector)
        #print rtree.printRTree()
        #print "puntos:"
        #print rtree.getPoints(rtree)
        res = rtree.RangeQuery([0.5]*dimension,0.3,rtree)
        print "resultado RangeQuery (0.5,0.5) radio 0,3):"
        print res[0]
        print "accesos:" + str(res[1])

        """

def getRadio(i):
        radios = [0.1765 ,0.2855,0.3755,0.4517,0.5211,0.5869,0.6452,0.7015,0.7620,0.8238,
                  0.8866,0.9204,0.9691,1.0104,1.0819,1.1178,1.1702,1.2121,1.2708]
        return radios[i-2]
def getConsultPoints(i):
        aux = []
        for i in range(1000):
                vector = []
                for i in range(i):
                        vector.append(random.random())
                aux.append(vector)
        return aux
                
def generateInputs():
        for i in range(2,20):
                GeneradorDePuntos.generar(i,100000)
        """
        vector=[]
        vector.append(0.1234)
        vector.append(0.2345)
        vector.append(0.3456)
        rtree.insertar(rtree.chooseLeaf(rtree,vector),vector)
        """
        #print rtree.printRTree()
        """
        if rtree.childs is []:
                print "fail"
        else:
                for child in rtree.childs:
                        print child
        """

#Insercion
#Si nodo es hoja reviso si tiene espacio, de ser asi, inserto
	
	#si no, hay que hacer split

#Nodo directorio, para cada hijo, reviso si su rectangulo contiene al vector
#a insertar, de ser asi, inserto ahí(Llamada recursiva)


#armar arbol

#GeneradorDePuntos.generar(2, 10)
loadRTree()

