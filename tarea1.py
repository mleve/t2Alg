import random
import time

#------------------------------------------------------------------------
#Auxiliar de intercambio de valores--------------------------------------
def swap(arreglo, pos1, pos2):
	aux = arreglo[pos1]
	arreglo[pos1] = arreglo[pos2]
	arreglo[pos2] = aux;


#------------------------------------------------------------------------
#QuickSelect-------------------------------------------------------------
def quickSelect(arreglo, inicio, fin):
	posMediana = len(arreglo)/2
	posPivote = particionQuickSelect(arreglo, inicio, fin)
	#recursividad
	if posPivote==posMediana:
		return arreglo[posPivote]
	if posPivote<posMediana:
		return quickSelect(arreglo, posPivote+1, fin)
	if posPivote>posMediana:
		return quickSelect(arreglo, inicio, posPivote-1)

def particionQuickSelect(arreglo, inicio, fin):
	#eleccion del pivote
	pivote = arreglo[fin]
	#particionamiento
	indice = inicio-1
	for i in range(inicio, fin, 1):
		if arreglo[i] <= pivote:
			indice+=1
			swap(arreglo, indice, i)
	swap(arreglo, indice+1, fin);
	return indice+1;


#------------------------------------------------------------------------
#Mediana de medianas-----------------------------------------------------
def medianaDeMedianas(arreglo, k, inicio, fin):
	elemPorGrupo = 2*k+1
	pivote = obtenerMedianaDeMedianas(arreglo, elemPorGrupo, inicio, fin)
	posPivote = particionMedianaDeMedianas(arreglo, pivote, inicio, fin)
	posMediana = len(arreglo)/2
	#print "medianaDeMedianas: para ",arreglo," el pivote dio ",pivote," en la pos ",posPivote
	if posPivote==posMediana:
		return arreglo[posPivote]
	if posPivote<posMediana:
		#print "recursion sobre ",arreglo[posPivote+1: fin]
		return medianaDeMedianas(arreglo, k, posPivote+1, fin)
	if posPivote>posMediana:
		#print "recursion sobre ",arreglo[inicio: posPivote]
		return medianaDeMedianas(arreglo, k, inicio, posPivote)

def obtenerMedianaDeMedianas(arreglo, elemPorGrupo, inicio, fin):
	medianas = []
	#trabajo sobre cada grupo
	for paso in range(inicio,fin,elemPorGrupo):
		limite = paso+elemPorGrupo
		if limite > fin:
			limite = fin
		#el grupo parte en "paso" y termina en "limite"
		#usamos insertion sort sobre el grupo
		for i in range(paso, limite, 1):
			aux = arreglo[i]
			indice = i-1
			while (indice >= paso and arreglo[indice] > aux):
				arreglo[indice+1] = arreglo[indice]
				indice = indice-1
			arreglo[indice+1] = aux
		#agregamos la mediana del grupo al arreglo de medianas
		medianas.append(arreglo[(paso+limite)/2])
	if len(medianas)==1:
		return medianas[0]
	else:
		return obtenerMedianaDeMedianas(medianas,elemPorGrupo,0,len(medianas))
		
def particionMedianaDeMedianas(arreglo, pivote, inicio, fin):
	fin-=1
	while inicio<fin:
		while arreglo[inicio]<pivote and arreglo[inicio]!=pivote:
			inicio+=1
		while arreglo[fin]>pivote and arreglo[fin]!=pivote:
			fin-=1
		swap(arreglo, inicio, fin)
	indice = inicio-1
	for i in range(inicio, fin, 1):
		if arreglo[i] <= pivote:
			indice+=1
			swap(arreglo, indice, i)
	swap(arreglo, indice+1, fin)
	return indice+1;
		
#musser
def musser(arreglo, t, alfa):
	#print "musser: quickSelectMusser antes", arreglo
	res = quickSelectMusser(arreglo, 0, len(vEjemplo)-1, t)
	#print "musser: quickSelectMusser despues", arreglo
	if res[0]!=None:
		return res[0]
	inicio = res[1]
	fin = res[2]
	#print "fallamos con ",res
	tamSubproblema = (fin-inicio+1)
	if tamSubproblema*alfa > len(arreglo):
		#NECESITO DETERMINAR EL K OPTIMO!
		#print "musser: usamos medianaDeMedianas: "
		return medianaDeMedianas(arreglo, 2, inicio, fin+1)
	else:
		#print "musser: usamos quickSelect"
		return quickSelect(arreglo, inicio, fin)
	

def quickSelectMusser(arreglo, inicio, fin, t):
	if(t <= 0):
		return [None, inicio, fin]
	posMediana = len(arreglo)/2
	posPivote = particionQuickSelect(arreglo, inicio, fin)
	if posPivote==posMediana:
		return [arreglo[posPivote], inicio, fin]
	if posPivote<posMediana:
		t-=1
		return quickSelectMusser(arreglo, posPivote+1, fin, t)
	if posPivote>posMediana:
		t-=1
		return quickSelectMusser(arreglo, inicio, posPivote-1, t)

#construimos arreglos
vEjemplo = range(100000)
random.shuffle(vEjemplo)
v1 = list(vEjemplo)
v2 = list(vEjemplo)
v3 = list(vEjemplo)

print "a probar el algoritmo d medianas"
#print vEjemplo
#a=quickSelect(v1, 0, len(v1)-1)
#print "quickselect ",a
#b=medianaDeMedianas(v2, len(v2)/2, 0, len(v2))
#print "meidanas ",b
#c=musser(v3, 5, 3)
#print "musser ",c
for i in range(1,20):
	inicio = time.time()
	ret = medianaDeMedianas(list(v2), i, 0, len(v2))
	fin = time.time()
	print "k: ",i, "grupos de: ",2*i+1," da tiempo de: ",fin-inicio
