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

Hey there!                           
