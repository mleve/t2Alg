class RTree:
	def __init__(self, dimension):
		self.isLeaf=1
		self.childCount=0
		self.parent=None
		self.rectangle = []
		self.M = (4096-8)/(dimension*8*2)
		self.childs=[]

	def chooseLeaf(self, node, point):
		if(node.isLeaf==1):
			return node
		else:
			if(node.isFull()):
				split(node)
				return chooseLeaf(node.parent,point)
			else:
				childDir=chooseChild(node,point)
				return chooseLeaf(loadNode(childDir),point)
        
	def insertar(self,node,point):
		node.childs.append(point)
		if(node.isFull()):
			split(node)

        def split(self,node):
                return
        
        def chooseChild(self,node,point):
                return node

	def loadNode(self,childDir):
	#Carga un nuevo nodo desde el archivo childDir y lo retorna
                return None

        def isFull(self):
                return False
		
				
		
			

