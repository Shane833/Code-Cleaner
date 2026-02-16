#ifndef _lcthw_Hashmap_h
#define _lcthw_Hashmap_h

#include <stdint.h>
#include <lcthw/darray.h>
#include <lcthw/darray_algos.h>
#include <lcthw/hashmap_algos.h>
#include <time.h>

#define DEFAULT_NUMBER_OF_BUCKETS 100 // Macro defining the default size of the Hashmap Keys

typedef int (*Hashmap_compare) (const void* a, const void* b); // Pointer to Function for comparing Keys 
typedef uint32_t (*Hashmap_hash) (void* key, uint32_t seed); // Pointer to a Function for generating the hash from a key		
											  // Returns an unsigned 32 bit integer hash value

// This is our Hashmap which contains pointer to compare function and pointer to hash generating function
// and a Dynamic Array called bucket for storing the Nodes corresponding to a specific hash
typedef struct Hashmap{
	DArray * buckets; 
	Hashmap_compare compare; // Pointer to a function for comparing keys
	Hashmap_hash hash; // Pointer to a function for generating the hash
	// Improvement : For Dynamic Growth
	// We will maintain 2 more variables
	// 1. entries, to know the no. of currently added elements
	// 2. load factor, to decide the condition for resizing elements
	size_t bucket_size; // or called capacity in someplaces
	size_t entries; // current no. of elements in the map, updated at every add / delete function call
	double load_factor; // helps us determine a threshold for resizing
	uint32_t seed; // This will be initialized once and then used for the lifetime of the program
}Hashmap;

// This is our single Node which is a pair of keys and values
// and also stores a unique has code within it
typedef struct HashmapNode{
	void * key;
	void * data;
	uint32_t hash;
}HashmapNode;

// This is a function for traversing the Node and displaying all the data associated with it
// This is a user-defined function which tells how to display the data within the node
typedef int (*Hashmap_traverse_cb) (HashmapNode* node);

// Original Function
// Function to create a Hashmap and you have to provide a compare and hash generating function
// for the specific datatype that you wish to use as a key
Hashmap * Hashmap_create(Hashmap_compare, Hashmap_hash); // Default Implementation

// Improvement 2.1 : Lets the user specificically decide the size of the buckets (non-resizable)
Hashmap * Hashmap_createStatic(Hashmap_compare, Hashmap_hash, size_t);

// Improvement 2.2 : Lets the user define an initial capacity / bucket size and a load factor
Hashmap * Hashmap_createDynamic(Hashmap_compare, Hashmap_hash, size_t, double);

// Destroys the data in the hashmap
void Hashmap_destroy(Hashmap* map);

// Function to set/add a specific key value pair assuming that the keys are unique
int Hashmap_set(Hashmap* map, void* key, void* data);

// Function to get the value for a corresponding key from the hashmap
void * Hashmap_get(Hashmap* map, void* key);

// Function to get the size of the hashmap
size_t Hashmap_getSize(Hashmap * map);

// Function to traverse the hashmap and you have to provide how each of the node gets traversed
int Hashmap_traverse(Hashmap* map, Hashmap_traverse_cb traverse_cb);

// Function to remove a key value pair from the map
void * Hashmap_delete(Hashmap* map, void* key);

// Improvements

// 1. Sort each of the bucket so that we can use binary search to find the element, this would increase
// insertion time but decreases the searching time since currently it used linear search to find the keys
// include the darray_algos header file and use the required functions
/* Improvement 1 - Done */
 
// 2. To dynamically size the number of buckets or let the caller specify the number of buckets
// for each hashmap created
/* Some points regarding dynamically sizing the hashmap:
 > When you resize a hashmap you have to also update their positions of elements 
   based on the new size of the buckets and this process is called Re-Hashing.
 > the average number of entries in a bucket (which is the total number of entries 
   divided by the number of buckets) should give a good estimate on when the HashMap 
   should be resized, and the size of individual buckets doesn't need to be checked.
 > To consider a threshold, and if the threshold reaches a certain value then we know
   that its time to resize the map.
*/
/* Improvement 2.1 - Done */ // Lets the user decide the default no. of buckets

// don't define functions in your header if you don't want multiple definitions
// rather just define them static inline or just static so they are local to the Translation Units
/*
static inline size_t Hashmap_getThreshold(Hashmap * map)
{
	return (size_t)(map->bucket_size * map->load_factor);
}
*/

/* Improvement 2.2 - Done */ // Now the map gets resized automatically after the entries exceed the threshold

// 3. Use a better default hash: Some options are : murmur3, cityhash

// Going to be using murmur3 hash as a better defult hash

/* Improvement 3 - Done */ 

// 4. This (and nearly every Hashmap) is vulnerable to someone picking keys that will fill
// only one bucket, and then tricking your program into processing them. This then makes
// you program run slower because it changes from processing a Hashmap to effectively processing
// a single DArray. If you sort the nodes in the bucket, this helps but you can also use better
// hashing functions, and for the really paranoid programmer, add a random salt so that keys can't
// be predicted 

/* Improvement 4 - Done */ // The nodes are stored in sorted fashion, then we resize after reaching a threshold
                           // So it is difficult to store a lot of nodes in a single DArray and finally I add 
													 // generate a random seed everytime we create a new hashmap which means the hash generated
													 // by one hashmap will be slightly different than other

// 5. You could have it delete buckets that are empty of nodes to save space, or put empty buckets into a cache so you can
// save time lost creating and destroying them.

// 6. Right now, it just adds elements even if they already exits. Write an alternative set method that only adds an 
// element if it isn't set already

/* Improvement 6 - Done */ // Along with not adding an element, the value of that element gets overwritten

