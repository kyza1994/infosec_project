#include <math.h>
#include <string.h>
#include <stdio.h>
#include <stdlib.h>

#define SIZE 100000
#define AVRG -10.0
#define DELTA 1.0
#define PATTERN_SIZE 50

int FindGenMax(int a, int b, float *array) {
	int i = a, loci = a;
	double locmax = array[a];
	for (i = a+3; i <= b; i+=3) 
		if (array[i] <= locmax) {
			locmax = array[i];
			loci = i;
		}
	return loci;
}

int main(int argc, char **argv) {
	FILE *data, *ft;
	char* out[20];
	float *arr; 
	
	if ((arr = malloc(SIZE*sizeof(double))) == NULL){
		fprintf(stderr, "Error with allocating memory\n"); 
		exit(1); 
	}
	data = fopen("square.TXT", "r");
	
	int i = 0, j, f = 1;
	int num = 0;
	int p1 = 2, p2 = 0;
	int a, b;
	
	do {	
		while (((f = fscanf(data, "%f", &arr[i])) != EOF)&&((f = fscanf(data, "%f", &arr[i+1])) != EOF)&&((f = fscanf(data, "%f", &arr[i+2])) != EOF)&&(arr[i+2] > AVRG-DELTA)){
			//printf("%f\n", arr[i]);
			i+=3;
			//if (arr[i] > AVRG+DELTA) break;
		}
		a = i+2;
		i+=3;
		if (f != EOF){
			while (((f = fscanf(data, "%f", &arr[i])) != EOF)&&((f = fscanf(data, "%f", &arr[i+1])) != EOF)&&((f = fscanf(data, "%f", &arr[i+2])) != EOF)&&(arr[i+2] < AVRG-DELTA)) {
				i+=3;
			//if (arr[i] < AVRG-DELTA) break;
			}
		}
		b = i+2;
		i+=3;
		p2 = FindGenMax(a, b, arr);	
		//printf("%d\t %d\n", a, b);
		
		if (num % 4 == 0) sprintf((char*)out, "left_%d.txt", (num+3)/4);
			else if (num % 4 == 1) sprintf((char*)out, "up_%d.txt", (num+3)/4);
			else if (num % 4 == 2) sprintf((char*)out, "down_%d.txt", (num+3)/4);
			else if (num % 4 == 3) sprintf((char*)out, "right_%d.txt", (num+3)/4);
		ft = fopen((char*)out, "w");
		for (j = p1-2; j < p2-2; j+=3) 
			fprintf(ft, "%f ", arr[j]);
		for (j = (p2-p1)/3; j < PATTERN_SIZE; j++)
			fprintf(ft, "%f ", 0.0);
		for (j = p1-1; j < p2-2; j+=3) 
			fprintf(ft, "%f ", arr[j]);
		for (j = (p2-p1)/3; j < PATTERN_SIZE; j++)
			fprintf(ft, "%f ", 0.0);
		fclose(ft);
		num++;
		p1 = p2;
	} while (f != EOF);
	
	fclose(data);
	free(arr);
	return 0;
}
