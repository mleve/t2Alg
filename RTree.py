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
                                #print "se lleno la raiz"
                                #exit
				if(node.parent is None):
                                        return node.chooseLeaf(node,point)
                                else:
                                        return node.chooseLeaf(node.parent,point)
			else:
				#childDir=chooseChild(node,point)
				#return chooseLeaf(loadNode(childDir),point)
                                #return node.chooseLeaf(node.childs[0][1],point)
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
                """print "en calcVolume con rectangle..."
                print rectangle"""
                diffs = [0]*node.dim
                result = 1
                for i in range(node.dim):
                        """print "vamos a calcular diffs[i]!"
                        print "rectangle[1] es:"
                        print rectangle[1]
                        print "rectangle[0] es:"
                        print rectangle[0]
                        print "i es:"
                        print i
                        print "rectangle[1][i]:"
                        print rectangle[1][i]"""
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
                """print "en calcVolumeInefficiency: rectangle 1 y rectangle2 son..."
                print rectangle1
                print rectangle2
                print "llamando calcVolume con boundingRectangle..."
                print boundingRectangle"""
                return node.calcVolume(node, boundingRectangle) - node.calcVolume(node, rectangle1) - node.calcVolume(node, rectangle2)

        def calcVolumeEnlargement(self, node, targetRectangle, newRectangle):
                """print "en calcVolumeEnlargement:"
                print "targetRectangle:"
                print targetRectangle
                print "newRectangle:"
                print newRectangle"""
                mins = []
                maxs = []
                mins.append(targetRectangle[0][0])
                mins.append(targetRectangle[0][1])
                maxs.append(targetRectangle[1][0])
                maxs.append(targetRectangle[1][1])
                """print mins
                print maxs"""
                for i in range(node.dim):
                        """print "i:"
                        print i
                        print "node.dim:"
                        print node.dim
                        print "newRectangle:"
                        print newRectangle
                        print "newRectangle[0]:"
                        print newRectangle[0]"""
                        if (newRectangle[0][i] < mins[i]):
                                mins[i] = newRectangle[0][i]
                        if (newRectangle[1][i] > maxs[i]):
                                maxs[i] = newRectangle[1][i]
                #print "enlargedRectangle:"
                enlargedRectangle = [mins, maxs]
                #print enlargedRectangle
                enlargedRectangleVolume = node.calcVolume(node, enlargedRectangle)
                targetRectangleVolume = node.calcVolume(node, targetRectangle)
                return enlargedRectangleVolume - targetRectangleVolume
        
	def insertar(self,node,point):
                print point
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
                children = copy.copy(node.childs)
                newNode1 = RTree(node.dim)
                newNode2 = RTree(node.dim)
                if(node.isLeaf==0):
                        newNode1.isLeaf=0
                        newNode2.isLeaf=0
                """newNode1.childs.append(node.childs[0])
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
                """
                rectangle_list = [child[0] for child in node.childs]
                print "en split: rectangle_list es..."
                print rectangle_list
                print len(rectangle_list)
                #non_added_indexes = range(node.childCount)
                #print "llamando pickSeeds"
                """print "non_added_indexes inicial:"
                print non_added_indexes
                """
                seeds = node.pickSeeds(node, rectangle_list)
                print "seeds:"
                print seeds
                newNode2.childs.append(node.childs[seeds[1]])
                newNode2.childCount+=1
                #non_added_indexes.remove(seeds[1])
                """print "non_added_indexes luego de remover seeds[1]:"
                print non_added_indexes
                """
                """print "rectangle_list:"
                print rectangle_list"""
                """print "rectangle_list[seeds[1]]"
                print rectangle_list[seeds[1]]"""
                del rectangle_list[seeds[1]]
                del children[seeds[1]]
                """print "rectangle_list luego de remover rectangle_list[seeds[1]]:"
                print rectangle_list"""
                newNode1.childs.append(node.childs[seeds[0]])
                newNode1.childCount+=1
                """print "non_added_indexes es:"
                print non_added_indexes
                print "seeds es:"
                print seeds
                print "rectangle_list es:"
                print rectangle_list
                print "largo de rectangle_list es:"
                print len(rectangle_list)"""
                #non_added_indexes.remove(seeds[0])
                """print "rectangle_list[seeds[0]]"
                print rectangle_list[seeds[0]]"""
                del rectangle_list[seeds[0]]
                del children[seeds[0]]
                print "rectangle_list luego de remover rectangle_list[seeds[0]]:"
                print rectangle_list
                
                if(node.isLeaf==0):
                        node.dirRectangle(newNode1)
                        node.dirRectangle(newNode2)
                else:
                        node.pointsRectangle(newNode1)
                        node.pointsRectangle(newNode2)

                newNode1Tom = node.m-newNode1.childCount
                newNode2Tom = node.m-newNode2.childCount
                """print "newNode1 childs, rectangle:"
                print newNode1.childs
                print newNode1.rectangle
                print "newNode2 childs, rectangle:"
                print newNode2.childs
                print newNode2.rectangle"""
                while rectangle_list:
                        if (not (len(rectangle_list)==newNode1Tom or len(rectangle_list)==newNode2Tom)):
                                selected_index = node.pickNext(node, rectangle_list, newNode1.rectangle, newNode2.rectangle)
                                newNode1Enlargement = node.calcVolumeEnlargement(node, newNode1.rectangle, rectangle_list[selected_index])
                                newNode2Enlargement = node.calcVolumeEnlargement(node, newNode2.rectangle, rectangle_list[selected_index])
                                print "selected_index:"
                                print selected_index
                                """
                                print "non_added_indexes:"
                                print non_added_indexes
                                non_added_indexes.remove(selected_index)"""
                                print "rectangle_list[selected_index]:"
                                print rectangle_list[selected_index]
                                del rectangle_list[selected_index]
                                print "rectangle_list:"
                                print rectangle_list
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

        def pickSeeds(self, node, rectangles):
                #rectangles es lista de rectangulos, los cuales vienen en forma [(min1,...,mind), (max1,...,maxd)]
                worstI = -1
                worstJ = -1
                worstD = -1
                """print "en pickSeeds: rectangles es..."
                print rectangles"""
                for i in range(len(rectangles)):
                        for j in range(i, len(rectangles)):
                                if (i != j):
                                        """print "llamando calcVolumeInefficiency con rectangles[i], rectangles[j].."
                                        print rectangles[i]
                                        print rectangles[j]"""
                                        diff = node.calcVolumeInefficiency(node, rectangles[i], rectangles[j])
                                        if diff > worstD:
                                                worstI = i
                                                worstJ = j
                                                worstD = diff
                return [worstI, worstJ]

        def pickNext(self, node, rectangles, targetRect1, targetRect2):
                #targetRect1 y 2 son los MBR de los grupos 1 y 2
                """print "Estoy en pickNext. rectangles:"
                print rectangles
                print "targetRect1:"
                print targetRect1
                print "targetRect2:"
                print targetRect2"""
                diffs = []
                max_diff = -1.0
                for rectangle in rectangles:
                        """print "rectangle:"
                        print rectangle"""
                        targetRect1Enlargement = node.calcVolumeEnlargement(node, targetRect1, rectangle)
                        targetRect2Enlargement = node.calcVolumeEnlargement(node, targetRect2, rectangle)
                        diff = math.fabs(targetRect1Enlargement - targetRect2Enlargement)
                        """print "diff:"
                        print diff"""
                        diffs.append(diff)
                        if diff > max_diff:
                                max_diff = diff
                """print "diffs:"
                print diffs"""
                return rectangles.index(rectangles[diffs.index(max_diff)])

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
                        print node.childs[i][0]
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
		
				
		
			

