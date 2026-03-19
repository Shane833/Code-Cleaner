#ifndef __PQUEUE_H__
#define __PQUEUE_H__

#include <stdlib.h>
#include <lcthw/dbg.h>

/*  A Priority Queue is a special data structure which organize the elements ba- 
	sed on their priority/dominance in the heirarchy. It is basically a complete
	binary tree with the element with the highest priority always at the root. 
   
	It is usually implemented with an array with the ROOT at the 0th index. if a
	PARENT is at Kth index then LEFT child will be at 2K + 1 and the RIGHT child
	will be at 2K + 2 and subsequently the parent will be at (CHILD_INDEX - 1)/2
	
	For Priority Queue containing N elements, the height of the binary tree will
	be log(N), and operation like Insertion and Removal takes O(log(N)) time. S-
	ince it is basically an array, traversal takes O(N) time along with space of
	O(N).
	
	In this tree we are storing 2^l keys on the lth level of a complete binary t-
	-ree in the position (not index) 2^(l - 1) to 2^l - 1.
	
	The best use cases of this data structure is extracting the min/max from the
	given data along with a special case of being used to implement HeapSort.
*/

// Comparison Function - used to organize the data
typedef int (*PQueue_Compare) (const void*, const void* b);

// PQueue Data Structure
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

// Since we mostly work with pointers it and in case of static arrays we don't necessarily
// have any pointers and therefore we store the addresses of each of the elements
PQueue* PQueue_CreateFromStaticArray(void** array, size_t size, PQueue_Compare cmp); 

#define PQueue_Size(A) (A != NULL ? (A)->end + 1 : -1)

void PQueue_Destroy(PQueue* q);

void PQueue_ClearDestroy(PQueue* q);

#define PQueue_Free(E) (free(E))

// TODO: Creating from a static array should use heapify 

#endif