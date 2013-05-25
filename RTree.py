import random
class RTree:
	def __init__(self, dimension):
                self.dim = dimension
		self.isLeaf=1
		self.childCount=0
		self.parent=None
		self.rectangle = []
		#self.M = (4096-8)/(dimension*8*2)
                self.M = 50
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
                                printarray.append(child[1].printRTree())
                return printarray

	def chooseLeaf(self, node, point):
		if(node.isLeaf==1):
			return node
		else:
			if(node.isFull()):
				split(node)
				return node.chooseLeaf(node.parent,point)
			else:
				#childDir=chooseChild(node,point)
				#return chooseLeaf(loadNode(childDir),point)
                                return node.chooseLeaf(node.childs[1][1],point)
        
	def insertar(self,node,point):
		node.childs.append((0,point))
		node.childCount+=1
		if(node.isFull()):
			node.split(node)

        def split(self,node):
                print "estoy spliteando"
                newNode1 = RTree(node.dim)
                newNode2 = RTree(node.dim)
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
                newNode1.calcRectangle()
                newNode2.calcRectangle()
                if(node.parent==None):
                        newNode1.parent = node.parent
                        newNode2.parent = node.parent
                        node.childs=[]
                        node.childs.append((newNode1.rectangle,newNode1))
                        node.childs.append((newNode2.rectangle,newNode2))
                        node.childCount=2
                        node.isLeaf=0
                else:
                        newNode1.parent = node
                        newNode2.parent = node

        def calcRectangle(self):
                self.rectangle=0
        
        def chooseChild(self,node,point):
                return node

	def loadNode(self,childDir):
	#Carga un nuevo nodo desde el archivo childDir y lo retorna
                return None

        def isFull(self):
                return self.childCount == self.M
		
				
		
			

