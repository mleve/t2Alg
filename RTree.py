import random
class RTree:
	def __init__(self, dimension):
		self.dim = dimension
		self.isLeaf=1
		self.childCount=0
		self.parent=None
		self.rectangle = []
		#self.M = (4096-8)/(dimension*8*2)
                self.M = 10
                self.m = 5
		self.childs=[]

	def printRTree(self):
                printarray = []
                printarray.append("dimension: "+str(self.dim))
                printarray.append("isLeaf: "+str(self.isLeaf))
                printarray.append("childCount: "+str(self.childCount))
                printarray.append("parent: "+str(self.parent))
                printarray.append("rectangle: "+str(self.rectangle))
                printarray.append("M: "+str(self.M))
                printarray.append("children: "+str(self.childs))
                if self.isLeaf==0:
                        for child in self.childs:
                                print child[1].printRTree()
                return printarray

	def chooseLeaf(self, node, point):
		if(node.isLeaf==1):
			return node
		else:
			if(node.isFull()):
				node.split(node)
                                #print "se lleno la raiz"
                                #exit
				if(node.parent is None):
                                        return node.chooseLeaf(node,point)
                                else:
                                        return node.chooseLeaf(node.parent,point)
			else:
				#childDir=chooseChild(node,point)
				#return chooseLeaf(loadNode(childDir),point)
                                return node.chooseLeaf(node.childs[0][1],point)

        def calcVolume(self, node, rectangle):
                #Asumimos por implementacion que rectangle viene en la forma [(min1,...,mind), (max1,...,maxd)]
                diffs = []
                result = 1
                for i in range(node.dim):
                        diffs[i] = rectangle[1][i]-rectangle[0][i]
                        result *= diffs[i]
                return result

        def calcVolumeInefficiency(self, node, rectangle1, rectangle2):
                mins = [1]*node.dim
                maxs = [0]*node.dim
                for i in range(node.dim):
                        if (rectangle1[0][i] < mins[i]):
                                mins[i] = rectangle1[0][i]
                        if (rectangle1[1][i] > maxs[i]):
                                maxs[i] = rectangle1[1][i]
                        if (rectangle2[0][i] < mins[i]):
                                mins[i] = rectangle2[0][i]
                        if (rectangle2[1][i] > maxs[i]):
                                maxs[i] = rectangle2[1][i]
                boundingRectangle = [mins, maxs]
                return calcVolume(node, boundingRectangle) - calcVolume(node, rectangle1) - calcVolume(node, rectangle2)

        def calcVolumeEnlargement(self, node, targetRectangle, newRectangle):
                mins = targetRectangle[0]
                maxs = targetRectangle[1]
                for i in range(node.dim):
                        if (newRectangle[0][i] < mins[i]):
                                mins[i] = newRectangle[0][i]
                        if (newRectangle[1][i] > maxs[i]):
                                maxs[i] = newRectangle[1][i]
                enlargedRectangle = [mins, maxs]
                return calcVolume(node, enlargedRectangle) - calcVolume(node, targetRectangle)
        
	def insertar(self,node,point):
		node.childs.append(((point, point), point))
		node.childCount+=1
		node.calcRectangle(node,point)
		aux = node.parent
		while aux is not None:
                        node.dirRectangle(aux)
                        aux = aux.parent
		if(node.isFull()):
			node.split(node)

        #def splitDir(self,node):
                

        def split(self,node):
                #print "estoy spliteando"
                newNode1 = RTree(node.dim)
                newNode2 = RTree(node.dim)
                if(node.isLeaf==0):
                        newNode1.isLeaf=0
                        newNode2.isLeaf=0
                newNode1.childs.append(node.childs[0])
                newNode1.childCount+=1
                newNode2.childs.append(node.childs[1])
                newNode2.childCount+=1
                for i in range(2, node.childCount):
                        if(random.randint(1,2)==1):
                                newNode1.childs.append(node.childs[i])
                                newNode1.childCount+=1
                                
                        else:
                                newNode2.childCount+=1
                                newNode2.childs.append(node.childs[i])
                if(node.isLeaf==0):
                        for i in range (newNode1.childCount):
                                newNode1.childs[i][1].parent = newNode1
                        for i in range (newNode2.childCount):
                                newNode2.childs[i][1].parent = newNode2
                        node.dirRectangle(newNode1)
                        node.dirRectangle(newNode2)
                else:
                        newNode1.pointsRectangle(newNode1)
                        newNode2.pointsRectangle(newNode2)
                if(node.parent==None):
                        newNode1.parent = node
                        newNode2.parent = node
                        node.childs=[]
                        node.childs.append((newNode1.rectangle,newNode1))
                        node.childs.append((newNode2.rectangle,newNode2))
                        node.childCount=2
                        node.isLeaf=0
                        node.dirRectangle(node)
                else:
                        newNode1.parent = node.parent
                        newNode2.parent = node.parent
                        #print node.parent.childs
                        #print node
                        #print node.rectangle
                        node.parent.childs.append((newNode1.rectangle,newNode1))
                        node.parent.childs.append((newNode2.rectangle,newNode2))
                        node.parent.childCount+=1
                        node.parent.childs = [child for child in node.parent.childs if child[1] is not node]
                        #node.parent.childs.remove(x for x in node.parent.childs if x[1] is node)
                        #node.parent.childs.remove((node.rectangle,node))
                        #print node.parent.childs
                        node.dirRectangle(node.parent)

        def calcRectangle(self,node,point):
                #Si es hoja, rectangulo de puntos
                if(node.isLeaf==1):
                        if(not node.contains(node,point)):
                                node.pointsRectangle(node)
                                if(not (node.parent is None)):
                                        node.dirRectangle(node.parent)
                else:
                        if(not node.contains(node,point)):
                                node.dirRectangle(node)

        def contains(self,node,point):
                if(not node.rectangle):
                        return False
                for i in range(node.dim):
                        if(point[i]< node.rectangle[0][i] or point[i] > node.rectangle[1][i]):
                                return False
                return True
        
        def dirRectangle(self,node):
                mins = []
                maxs = []
                for i in range(node.childCount):
                        #print node.childs[i][0]
                        mins.append(node.childs[i][0][0])
                        maxs.append(node.childs[i][0][1])
                #print mins
                #print maxs
                minVals= [1]*node.dim
                maxVals= [0]*node.dim
                for j in range(len(mins)):
                        for k in range(node.dim):
                                if(mins[j][k]<minVals[k]):
                                        minVals[k]=mins[j][k]
                                if(maxs[j][k]>maxVals[k]):
                                        maxVals[k] = maxs[j][k]
                
                node.rectangle = (minVals,maxVals)
                #print "rec cubridor:"
                #print node.rectangle
                #print "endRec"
                                
                                
                                
                                    
                """
                for i in range node.dim:
                        if(point[i]< node.rectangle[0][i]):
                                node.rectangle[0][i] = point[i]
                        if(point[i]> node.rectangle[1][i]):
                                node.rectangle[1][i] = point[i]
        """

        def pointsRectangle(self,node):
                minVals= [1]*node.dim
                maxVals= [0]*node.dim
                for i in range(node.childCount):
                        for j in range(node.dim):
                                if (node.childs[i][1][j] < minVals[j]):
                                        minVals[j] = node.childs[i][1][j]
                                if (node.childs[i][1][j] > maxVals[j]):
                                        maxVals[j] = node.childs[i][1][j]
                node.rectangle = [minVals, maxVals]
                                
        
        def chooseChild(self,node,point):
                return node

	def loadNode(self,childDir):
	#Carga un nuevo nodo desde el archivo childDir y lo retorna
                return None

        def isFull(self):
                return self.childCount == self.M
		
				
		
			

