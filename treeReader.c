

#include<stdio.h>


FILE *f1;
FILE *f2;

int main(){
	f1 = fopen("input.bin","rb");

	if (f1 == NULL)
		return -1;

	
	int dimension;
	fread(&dimension,1,4,f1);
	

	int numVectores;
	fread(&numVectores,1,4,f1);

	printf("dimension: %d , vectores: %d \n", dimension,numVectores); 
	printf("Vectores: \n");	

	//valores de 1 vector
	double x, y;

	//Generar y escribir los n vectores, 1 a la vez
	int i=1;
	for(i=1;i<=numVectores;i++){
		fread(&x,1,8,f1);
		fread(&y,1,8,f1);
		printf("x: %f , y: %f \n", x,y); 
	}

	fclose(f1);
	printf("Lector finalizado \n");
}
