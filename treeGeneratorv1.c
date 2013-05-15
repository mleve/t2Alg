

#include<stdio.h>
#include<stdlib.h>

FILE *f1;
FILE *f2;

int main(){
	f1 = fopen("input.bin","wb");

	if (f1 == NULL)
		return -1;

	
	int dimension = 2;

	int numVectores = 100000;
	//valores de 1 vector
	double x, y;

	fwrite(&dimension,1,4,f1);
	fwrite(&numVectores,1,4,f1);

	//Crear un nuevo generador de numeros aleatorios:
	srand((unsigned)time(NULL));

	//Generar y escribir los n vectores, 1 a la vez
	int i=1;
	for(i=1;i<=numVectores;i++){
		x=((double) rand() / (double) RAND_MAX);
		y=((double) rand() / (double) RAND_MAX);
		fwrite(&x,1,8,f1);
		fwrite(&y,1,8,f1);
	}
	fclose(f1);
	printf("Generador finalizado \n");
}
