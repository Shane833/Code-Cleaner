#ifndef _lcthw_Hashmap_h
#define _lcthw_Hashmap_h

#include <stdint.h>
#include <lcthw/darray.h>
#include <lcthw/darray_algos.h>
#include <lcthw/hashmap_algos.h>
#include <time.h>

#define DEFAULT_NUMBER_OF_BUCKETS 100 

typedef int (*Hashmap_compare) (const void* a, const void* b); 
typedef uint32_t (*Hashmap_hash) (void* key, uint32_t seed); 
											  



typedef struct Hashmap{
	DArray * buckets; 
	Hashmap_compare compare; 
	Hashmap_hash hash; 
	
	
	
	
	size_t bucket_size; 
	size_t entries; 
	double load_factor; 
	uint32_t seed; 
}Hashmap;



typedef struct HashmapNode{
	void * key;
	void * data;
	uint32_t hash;
}HashmapNode;



typedef int (*Hashmap_traverse_cb) (HashmapNode* node);




Hashmap * Hashmap_create(Hashmap_compare, Hashmap_hash); 


Hashmap * Hashmap_createStatic(Hashmap_compare, Hashmap_hash, size_t);


Hashmap * Hashmap_createDynamic(Hashmap_compare, Hashmap_hash, size_t, double);


void Hashmap_destroy(Hashmap* map);


int Hashmap_set(Hashmap* map, void* key, void* data);


void * Hashmap_get(Hashmap* map, void* key);


size_t Hashmap_getSize(Hashmap * map);


int Hashmap_traverse(Hashmap* map, Hashmap_traverse_cb traverse_cb);


void * Hashmap_delete(Hashmap* map, void* key);






/* Improvement 1 - Done */
 


/* Some points regarding dynamically sizing the hashmap:
 > When you resize a hashmap you have to also update their positions of elements 
   based on the new size of the buckets and this process is called Re-Hashing.
 > the average number of entries in a bucket (which is the total number of entries 
   divided by the number of buckets) should give a good estimate on when the HashMap 
   should be resized, and the size of individual buckets doesn't need to be checked.
 > To consider a threshold, and if the threshold reaches a certain value then we know
   that its time to resize the map.
*/
/* Improvement 2.1 - Done */ 



/*
static inline size_t Hashmap_getThreshold(Hashmap * map)
{
	return (size_t)(map->bucket_size * map->load_factor);
}
*/

/* Improvement 2.2 - Done */ 





/* Improvement 3 - Done */ 








/* Improvement 4 - Done */ 
                           
													 
													 







/* Improvement 6 - Done */ 

