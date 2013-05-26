import RTree
import GeneradorDePuntos
import struct
def loadRTree():
        with open('data2D.bin','rb') as f:
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
        print rtree.printRTree()
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


loadRTree()

