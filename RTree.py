class RTree:
	def __init__(self, dimension):
		maxNodes(dimension)
		self.isLeaf=0
		self.nodes=[][]
		
	def maxNodes(self,dim):
		self.M = (4096-8)/(dim*8*2)
		

