import random
import math
import copy
class RTree:
	def __init__(self, dimension):
		self.dim = dimension
		self.isLeaf=1
		self.childCount=0
		self.parent=None
		self.rectangle = []
		self.M = math.floor((4096-8)/(dimension*8*2))
                self.m = self.M/2
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

        def getPoints(self, node):
                points = []
                if(node.isLeaf == 1):
                        for child in node.childs:
                                points.append(child[1])
                else:
                        for child in node.childs:
                                points = points + node.getPoints(child[1])
                return points

        def RangeQuery(self,point, radio, node):
                res = []
                accesos=0
                
                if(node.isLeaf==1):
                        for child in node.childs:
                              if(node.vectorDist(point,child[1])<= radio):
                                      res.append(child[1])
                                      accesos+=1
                else:
                        for child in node.childs:
                                if(node.minDist(point,child[0]) <= radio):
                                        aux = node.RangeQuery(point,radio,child[1])
                                        res = res + aux[0]
                                        accesos = accesos + aux[1] + 1
                                        
                return (res,accesos)
                
        def vectorDist(self,p1,p2):
                res=0
                for i in range(len(p1)):
                     res=res + ((p1[i]-p2[i])*(p1[i]-p2[i]))
                return math.sqrt(res)

        def  minDist(self,point,rectangle):
                res=0
                for i in range(len(point)):
                        if(point[i]<= rectangle[0][i]):
                                res = res + (rectangle[0][i]-point[i])**2
                        elif (point[i]>= rectangle[1][i]):
                                res = res+ (point[i]-rectangle[1][i])**2
                return res
                                
                
                

	def chooseLeaf(self, node, point):
		if(node.isLeaf==1):
			return node
		else:
			if(node.isFull()):
				node.split(node)
				if(node.parent is None):
                                        return node.chooseLeaf(node,point)
                                else:
                                        return node.chooseLeaf(node.parent,point)
			else:
                                diffs = []
                                for child in node.childs:
                                        diffs.append(node.calcVolumeEnlargement(node, child[0], (point, point)))
                                min_diff = min(diffs)
                                min_diff_indexes = []
                                for i in range(len(diffs)):
                                        if diffs[i] == min_diff:
                                                min_diff_indexes.append(i)
                                if len(min_diff_indexes)>1:
                                        volumes = []
                                        for index in min_diff_indexes:
                                                volumes.append(node.calcVolume(node, node.childs[index][0]))
                                        selected_index = min_diff_indexes[volumes.index(min(volumes))]
                                        return node.chooseLeaf(node.childs[selected_index][1], point)
                                else:
                                        return node.chooseLeaf(node.childs[min_diff_indexes[0]][1], point)
                                                     

        def calcVolume(self, node, rectangle):
                #Asumimos por implementacion que rectangle viene en la forma [(min1,...,mind), (max1,...,maxd)]
                diffs = [0]*node.dim
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
                return node.calcVolume(node, boundingRectangle) - node.calcVolume(node, rectangle1) - node.calcVolume(node, rectangle2)

        def calcVolumeEnlargement(self, node, targetRectangle, newRectangle):
                mins = []
                maxs = []
                for i in range(node.dim):
                        mins.append(targetRectangle[0][i])
                        maxs.append(targetRectangle[1][i])
                for i in range(node.dim):
                        if (newRectangle[0][i] < mins[i]):
                                mins[i] = newRectangle[0][i]
                        if (newRectangle[1][i] > maxs[i]):
                                maxs[i] = newRectangle[1][i]
                enlargedRectangle = [mins, maxs]
                enlargedRectangleVolume = node.calcVolume(node, enlargedRectangle)
                targetRectangleVolume = node.calcVolume(node, targetRectangle)
                return enlargedRectangleVolume - targetRectangleVolume
        
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

        def split(self,node):
                children = copy.copy(node.childs)
                newNode1 = RTree(node.dim)
                newNode2 = RTree(node.dim)
                if(node.isLeaf==0):
                        newNode1.isLeaf=0
                        newNode2.isLeaf=0
                rectangle_list = [child[0] for child in node.childs]
                seeds = node.pickSeeds(node, rectangle_list)
                newNode2.childs.append(node.childs[seeds[1]])
                newNode2.childCount+=1
                del rectangle_list[seeds[1]]
                del children[seeds[1]]
                newNode1.childs.append(node.childs[seeds[0]])
                newNode1.childCount+=1
                del rectangle_list[seeds[0]]
                del children[seeds[0]]

                if(node.isLeaf==0):
                        node.dirRectangle(newNode1)
                        node.dirRectangle(newNode2)
                else:
                        node.pointsRectangle(newNode1)
                        node.pointsRectangle(newNode2)

                newNode1Tom = node.m-newNode1.childCount
                newNode2Tom = node.m-newNode2.childCount
                while rectangle_list:
                        if (not (len(rectangle_list)==newNode1Tom or len(rectangle_list)==newNode2Tom)):
                                selected_index = node.pickNext(node, rectangle_list, newNode1.rectangle, newNode2.rectangle)
                                newNode1Enlargement = node.calcVolumeEnlargement(node, newNode1.rectangle, rectangle_list[selected_index])
                                newNode2Enlargement = node.calcVolumeEnlargement(node, newNode2.rectangle, rectangle_list[selected_index])
                                del rectangle_list[selected_index]
                                if (newNode1Enlargement < newNode2Enlargement):
                                        newNode1.childs.append(children[selected_index])
                                        del children[selected_index]
                                        newNode1.childCount+=1
                                        newNode1Tom = node.m-newNode1.childCount
                                        if(node.isLeaf==0):
                                                node.dirRectangle(newNode1)
                                        else:
                                                node.pointsRectangle(newNode1)
                                elif (newNode1Enlargement > newNode2Enlargement):
                                        newNode2.childs.append(children[selected_index])
                                        newNode2.childCount+=1
                                        del children[selected_index]
                                        newNode2Tom = node.m-newNode2.childCount
                                        if(node.isLeaf==0):
                                                node.dirRectangle(newNode2)
                                        else:
                                                node.pointsRectangle(newNode2)
                                else:
                                        newNode1Volume = node.calcVolume(node, newNode1.rectangle)
                                        newNode2Volume = node.calcVolume(node, newNode2.rectangle)
                                        if(newNode1Volume < newNode2Volume):
                                                newNode1.childs.append(children[selected_index])
                                                del children[selected_index]
                                                newNode1.childCount+=1
                                                newNode1Tom = node.m-newNode1.childCount
                                                if(node.isLeaf==0):
                                                        node.dirRectangle(newNode1)
                                                else:
                                                        node.pointsRectangle(newNode1)
                                        elif (newNode1Volume > newNode2Volume):
                                                newNode2.childs.append(children[selected_index])
                                                del children[selected_index]
                                                newNode2.childCount+=1
                                                newNode2Tom = node.m-newNode2.childCount
                                                if(node.isLeaf==0):
                                                        node.dirRectangle(newNode2)
                                                else:
                                                        node.pointsRectangle(newNode2)
                                        else:
                                                if(newNode1.childCount < newNode2.childCount):
                                                        newNode1.childs.append(children[selected_index])
                                                        del children[selected_index]
                                                        newNode1.childCount+=1
                                                        newNode1Tom = node.m-newNode1.childCount
                                                        if(node.isLeaf==0):
                                                                node.dirRectangle(newNode1)
                                                        else:
                                                                node.pointsRectangle(newNode1)
                                                else:
                                                        newNode2.childs.append(children[selected_index])
                                                        del children[selected_index]
                                                        newNode2.childCount+=1
                                                        newNode2Tom = node.m-newNode2.childCount
                                                        if(node.isLeaf==0):
                                                                node.dirRectangle(newNode2)
                                                        else:
                                                                node.pointsRectangle(newNode2)
                        elif len(rectangle_list)==newNode1Tom:
                                newNode1.childs.append(children[0])
                                del children[0]
                                newNode1.childCount+=1
                                del rectangle_list[0]
                                newNode1Tom = node.m-newNode1.childCount
                                if(node.isLeaf==0):
                                        node.dirRectangle(newNode1)
                                else:
                                        node.pointsRectangle(newNode1)
                        else:
                                newNode2.childs.append(children[0])
                                del children[0]
                                newNode2.childCount+=1
                                del rectangle_list[0]
                                newNode2Tom = node.m-newNode2.childCount
                                if(node.isLeaf==0):
                                        node.dirRectangle(newNode2)
                                else:
                                        node.pointsRectangle(newNode2)
                #end while :P
                
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
                        node.parent.childs.append((newNode1.rectangle,newNode1))
                        node.parent.childs.append((newNode2.rectangle,newNode2))
                        node.parent.childCount+=1
                        node.parent.childs = [child for child in node.parent.childs if child[1] is not node]
                        node.dirRectangle(node.parent)

        def pickSeeds(self, node, rectangles):
                #rectangles es lista de rectangulos, los cuales vienen en forma [(min1,...,mind), (max1,...,maxd)]
                worstI = -1
                worstJ = -1
                worstD = -1
                for i in range(len(rectangles)):
                        for j in range(i, len(rectangles)):
                                if (i != j):
                                        diff = node.calcVolumeInefficiency(node, rectangles[i], rectangles[j])
                                        if diff > worstD:
                                                worstI = i
                                                worstJ = j
                                                worstD = diff
                return [worstI, worstJ]

        def pickNext(self, node, rectangles, targetRect1, targetRect2):
                #targetRect1 y 2 son los MBR de los grupos 1 y 2
                diffs = []
                max_diff = -1.0
                for rectangle in rectangles:
                        targetRect1Enlargement = node.calcVolumeEnlargement(node, targetRect1, rectangle)
                        targetRect2Enlargement = node.calcVolumeEnlargement(node, targetRect2, rectangle)
                        diff = math.fabs(targetRect1Enlargement - targetRect2Enlargement)
                        diffs.append(diff)
                        if diff > max_diff:
                                max_diff = diff
                return rectangles.index(rectangles[diffs.index(max_diff)])

        def calcRectangle(self,node,point):
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
                        mins.append(node.childs[i][0][0])
                        maxs.append(node.childs[i][0][1])
                minVals= [1]*node.dim
                maxVals= [0]*node.dim
                for j in range(len(mins)):
                        for k in range(node.dim):
                                if(mins[j][k]<minVals[k]):
                                        minVals[k]=mins[j][k]
                                if(maxs[j][k]>maxVals[k]):
                                        maxVals[k] = maxs[j][k]
                
                node.rectangle = (minVals,maxVals)
                                
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
                return None

        def isFull(self):
                return self.childCount == self.M
