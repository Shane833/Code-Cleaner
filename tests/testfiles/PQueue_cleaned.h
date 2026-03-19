#ifndef __PQUEUE_H__
#define __PQUEUE_H__

#include <stdlib.h>
#include <lcthw/dbg.h>

typedef int (*PQueue_Compare) (const void*, const void* b);

typedef struct PQueue{
	int end;
	size_t max;
	void** array;
	PQueue_Compare cmp;
}PQueue;

PQueue* PQueue_Create(size_t size, PQueue_Compare cmp);

void PQueue_Enqueue(PQueue* q, void* element);

void* PQueue_Dequeue(PQueue* q);

PQueue* PQueue_CreateFromArray(void** array, size_t size, PQueue_Compare cmp);

PQueue* PQueue_CreateFromStaticArray(void** array, size_t size, PQueue_Compare cmp); 

#define PQueue_Size(A) (A != NULL ? (A)->end + 1 : -1)

void PQueue_Destroy(PQueue* q);

void PQueue_ClearDestroy(PQueue* q);

#define PQueue_Free(E) (free(E))

#endif