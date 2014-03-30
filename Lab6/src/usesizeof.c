/*
 * usesizeof.c
 * by Hawk Weisman
 * for CMPSC440 Lab 6
 * at Allegheny College
 *
 * Determines the size of various C data types.
 */

#include	<stdio.h>
#include	<stdbool.h>
#include	<string.h>
#include	<limits.h>

#define		TABLE_FMT	"%-12s%8lu%8lu\n"
#define		HEAD_FMT	"%-12s%8s%8s\n"
#define		TEX_FMT     "%-12s & %lu & %8lu \\\\ \n"

#define		MAKETABLE(name, type, fmt) printf(fmt, name, sizeof(type), bits(sizeof(type)))

unsigned long bits (unsigned long bytes) {
	return bytes * CHAR_BIT;
}

// Struct representing a point on a 2D plane
struct int_2d{
	int x;
	int y;
};

// Struct representing a point on a 3D plane
struct int_3d{
	int x;
	int y;
	int z;
};

// Struct representing a point on a 2D plane
// (with doubles)
struct double_2d{
	double x;
	double y;
};

// Struct representing a point on a 3D plane
// (with doubles)
struct double_3d{
	double x;
	double y;
	double z;
};

int main (int argc, const char* argv[]) {
	printf("Sizes of data types in C:\n\n");

	// print the header of the table
	printf(HEAD_FMT, "data type", "bytes", "bits");
	printf(HEAD_FMT, "---- ----", "-----", "----");

	// if we are in tex-mode...
	if (argc > 1  && (strcmp(argv[1], "-t") || strcmp(argv[1], "--tex"))) {
		//...print the tex-friendly table
		MAKETABLE("short", short, TEX_FMT);
		MAKETABLE("int", int, TEX_FMT);
		MAKETABLE("long", long, TEX_FMT);
		MAKETABLE("long long", long long, TEX_FMT);
		MAKETABLE("float", float, TEX_FMT);
		MAKETABLE("double", double, TEX_FMT);
		MAKETABLE("long double", long double, TEX_FMT);
		MAKETABLE("char", char, TEX_FMT);
		MAKETABLE("char*", char*, TEX_FMT);
		MAKETABLE("_Bool", _Bool, TEX_FMT);

		printf("\n");

		MAKETABLE("int_2d", struct int_2d, TEX_FMT);
		MAKETABLE("int_3d", struct int_3d, TEX_FMT);
		MAKETABLE("double_2d", struct double_2d, TEX_FMT);
		MAKETABLE("double_3d", struct double_3d, TEX_FMT);
	}
	// otherwise...
	else {
		// ...print the standard table
		MAKETABLE("short", short, TABLE_FMT);
		MAKETABLE("int", int, TABLE_FMT);
		MAKETABLE("long", long, TABLE_FMT);
		MAKETABLE("long long", long long, TABLE_FMT);
		MAKETABLE("float", float, TABLE_FMT);
		MAKETABLE("double", double, TABLE_FMT);
		MAKETABLE("long double", long double, TABLE_FMT);
		MAKETABLE("char", char, TABLE_FMT);
		MAKETABLE("char*", char*, TABLE_FMT);
		MAKETABLE("_Bool", _Bool, TABLE_FMT);

		printf("\n");

		MAKETABLE("int_2d", struct int_2d, TABLE_FMT);
		MAKETABLE("int_3d", struct int_3d, TABLE_FMT);
		MAKETABLE("double_2d", struct double_2d, TABLE_FMT);
		MAKETABLE("double_3d", struct double_3d, TABLE_FMT);
	}
	return 0;
}
