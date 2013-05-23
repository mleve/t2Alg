import RTree

def loadRTree:
	with open('test4.bin','rb') as f:
#Obtener Dimension y numero de vertices
		metadata = struct.unpack('@ii,f.read(8))
		dimension = metadata[0]
		points = metadata[1]
#Inicializar arbol
		rtree = RTree(dimension)
		for i in range(n):
#Obtener proximo punto (vector) a insertar
			vector = []
			for j in range(dimension):
				vector.append(struct.unpack('@d',f.read(8)))
#insertar el nuevo vector en el arbol
		insertar(rtree,vector)

def insert(node,vector)
#Insercion
#Si nodo es hoja reviso si tiene espacio, de ser asi, inserto
	
	#si no, hay que hacer split

#Nodo directorio, para cada hijo, reviso si su rectangulo contiene al vector
#a insertar, de ser asi, inserto ahí(Llamada recursiva)


#armar arbol
	





