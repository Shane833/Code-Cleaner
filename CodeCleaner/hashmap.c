#undef NDEBUG
#include <stdint.h>
#include <lcthw/hashmap.h>
#include <lcthw/dbg.h>
#include <lcthw/bstrlib.h>
#include <stdbool.h>


// Default compare function which compare the bstrings
static int default_compare(const void * a, const void * b)
{
	return bstrcmp((bstring) a, (bstring) b);
}

// Default compare function for nodes which internally compare the bstrings
static int default_node_compare(const HashmapNode * a, const HashmapNode * b)
{
	if(default_compare(a->key, b->key) == 0 && a->hash == b->hash){
		return 0;
	}else{
		return default_compare(a->key,b->key);
	}
}

// Forward Declaration 
static inline int Hashmap_get_node(Hashmap* map, uint32_t hash, DArray* bucket, void* key);

// Function to get the Threshold
static inline size_t Hashmap_getThreshold(Hashmap * map)
{
	return (size_t)(map->bucket_size * map->load_factor);
}

// Bob Jenkins Hash Algorithm
// Default Hash Function which takes in a bstring value
// and generates an unsigned 32bit integer hash
/* Original Code
static uint32_t default_hash(void* a)
{
	size_t len = blength((bstring) a);
	char* key = bdata((bstring) a);
	uint32_t hash = 0;
	uint32_t i = 0;
	
	for(hash = i = 0;i < len; ++i){
		hash += key[i];
		hash += (hash << 10);
		hash ^= (hash >> 6);
	}
	
	hash += (hash << 3);
	hash ^= (hash << 11);
	hash += (hash << 15);
	
	return hash;
}
*/

// New default hash uses murmur3_32 hash function
static uint32_t default_hash(void * a ,uint32_t seed)
{
	char * key = bdata((bstring)a);
	size_t len = blength((bstring)a);

	return Hashmap_murmur3_32_hash(key, len, seed);
}

//Original Function
// Function to create a Hashmap
Hashmap * Hashmap_create(Hashmap_compare compare, Hashmap_hash hash)
{
	Hashmap* map = calloc(1, sizeof(Hashmap));
	check_mem(map);
	
	// If the values for the compare and hash is not provided we stick with the default functions
	map->compare = compare == NULL ? default_compare : compare; // good of setting defaults
	map->hash = hash == NULL ? default_hash : hash;
	
	// Initializing the additional variable (Part of Improvement)
	map->bucket_size = 0;
	map->load_factor = 0.0;
	map->entries = 0;

	// Then here we allocate a fixed no. of elements in the DArray buckets
	// These elements in turn will be pointers to other DArrays
	map->buckets = DArray_create(sizeof(DArray*), DEFAULT_NUMBER_OF_BUCKETS);

	// Now we have set the end of the DArray = max of the DArray
	// This is done as the no. of elements we have to do deal with are fixed
	// and since we won't be dynamically adding any new keys we won't have to 
	// check if the DArray is expading or not as we will not be pushing any new keys
	map->buckets->end = map->buckets->max; // fake out expanding it // BUT HOW?
	check_mem(map->buckets);

	// Part of improvement 4, it will seed it with everytime we create a new hashmap
	srand(time(NULL));
	// Part of Improvement 4
	map->seed = (uint32_t)rand();

	return map;
error:
	if(map){
		Hashmap_destroy(map);
	}
	return NULL;
}

// Function to create a static Hashmap with user-defined bucket size
Hashmap * Hashmap_createStatic(Hashmap_compare compare, Hashmap_hash hash, size_t bucket_size)
{
	Hashmap* map = calloc(1, sizeof(Hashmap));
	check_mem(map);
	
	// If the values for the compare and hash is not provided we stick with the default functions
	map->compare = compare == NULL ? default_compare : compare; // good way of setting defaults
	map->hash = hash == NULL ? default_hash : hash;
	
	// check if the bucket_size value is valid
	check(bucket_size > 0, "ERROR : Invalid Bucket Size!");
	map->bucket_size = bucket_size;

	// Improvement 2.1 : letting the user decide the buckets in the hashmap
	map->buckets = DArray_create(sizeof(DArray*), map->bucket_size);

	// Now we have set the end of the DArray = max of the DArray
	// This is done as the no. of elements we have to do deal with are fixed
	// and since we won't be dynamically adding any new keys we won't have to 
	// check if the DArray is expading or not as we will not be pushing any new keys
	map->buckets->end = map->buckets->max; // fake out expanding it // BUT HOW?
	check_mem(map->buckets);

	// Part of improvement 4, it will seed it with everytime we create a new hashmap
	srand(time(NULL));
	// Part of Improvement 4
	map->seed = (uint32_t)rand();

	return map;
error:
	if(map){
		Hashmap_destroy(map);
	}
	return NULL;
}

// Creates a dynamic hashmap which grows as per the given load factor
Hashmap * Hashmap_createDynamic(Hashmap_compare compare, Hashmap_hash hash, size_t bucket_size, double load_factor)
{
	Hashmap* map = calloc(1, sizeof(Hashmap));
	check_mem(map);

	// If the values for the compare and hash is not provided we stick with the default functions
	map->compare = compare == NULL ? default_compare : compare; // good of setting defaults
	map->hash = hash == NULL ? default_hash : hash;
	
	// check if the load factor is valid
	check(load_factor > 0.0, "ERROR : Invalid Load Factor!");
	map->load_factor = load_factor;

	// check if the bucket_size value is valid
	check(bucket_size > 0, "ERROR : Invalid Bucket Size!");
	map->bucket_size = bucket_size;

	// Improvement 2.1 : letting the user decide the buckets in the hashmap
	map->buckets = DArray_create(sizeof(DArray*), map->bucket_size);
	check_mem(map->buckets);

	// Now we have set the end of the DArray = max of the DArray
	// This is done as the no. of elements we have to do deal with are fixed
	// and since we won't be dynamically adding any new keys we won't have to 
	// check if the DArray is expading or not as we will not be pushing any new keys
	map->buckets->end = map->buckets->max; // fake out expanding it // BUT HOW?
	
	// Part of improvement 4, it will seed it with everytime we create a new hashmap
	srand(time(NULL));
	// Part of Improvement 4
	map->seed = (uint32_t)rand();

	return map;
error:
	if(map){
		Hashmap_destroy(map);
	}
	return NULL;
}

// Function to deallocate memory from the map
void Hashmap_destroy(Hashmap* map)
{
	int i = 0;
	int j = 0;
	// First we check for the validity of the map
	if(map){
		// then vaildity of the content
		if(map->buckets){
			// Now we loop through all the buckets
			for(i = 0;i < DArray_count(map->buckets); i++){
				DArray* bucket = DArray_get(map->buckets, i);
				// If the bucket exists
				if(bucket){
					// We free the nodes within that bucket
					for(j = 0;j < DArray_count(bucket); j++){
						free(DArray_get(bucket, j));
					}
					// Now we destroy that bucket
					DArray_destroy(bucket);
				}
			}
		}
		// Then destroy the main buckets DArray
		DArray_destroy(map->buckets);

		// and finally deallocate memory from the map
		free(map);
	}	
}

// Function to create a Hashmap Node
static inline HashmapNode* Hashmap_node_create(int hash, void* key, void* data)
{
	// As simple as it gets
	HashmapNode* node = calloc(1, sizeof(HashmapNode));
	check_mem(node);
	
	node->key = key;
	node->data = data;
	node->hash = hash;
	
	return node;
error:
	return NULL;
}

// This function is the most important as it is responsible for finding
// as well creating a new bucket corresponding to specific hash value
static inline DArray* Hashmap_find_bucket(Hashmap* map, void* key, int create, uint32_t* hash_out)
{
	check(map != NULL, "ERROR : Invalid map!");
	check(hash_out != NULL, "ERROR : Invalid hash out provided!");

	// Improvement 4 : Now the hash function takes in an additional seed
	uint32_t hash = map->hash(key, map->seed); // Here we take the key and generate a u32 bit hash
	/*Original Code
	int bucket_n = hash % DEFAULT_NUMBER_OF_BUCKETS; // It generate an index to the DArray within the buckets DArray
													 // We are simple limiting the index to [0, Default no. of buckets - 1]
													 // In this case 0 to 99
													 // This will ensure that all the key-value pairs reside within these buckets only
	check(bucket_n >= 0, "Invalid bucket found: %d", bucket_n);
	// Improvement : Hashing with the new size of the buckets
	*/

	// Improvement : Based on if size is given or not we will hash differently
	int bucket_n = map->bucket_size == 0 ? hash % DEFAULT_NUMBER_OF_BUCKETS : hash % map->bucket_size;
	check(bucket_n >= 0, "Invalid bucket found : %d", bucket_n);

	// store it for the return so the caller can use it
	*hash_out = hash; // Then we store this generated hash into pointer provided
					  // also make sure than the types of both the values is same
					  // else compiler will throw an error as they would have different memory layouts
	
	// Now we find the bucket correspoding to the calculated index
	DArray* bucket = DArray_get(map->buckets, bucket_n);
	
	if(!bucket && create){ // If the buckets does not exists and the create flag in on then we create
						   // a new DArray and add it at the generated index
		// new bucket, set it up
		bucket = DArray_create(sizeof(void*), DArray_count(map->buckets));
		check_mem(bucket);
		DArray_set(map->buckets, bucket_n, bucket);
	}
	
	return bucket; // Now we simply return the pointer to the DArray
error:
	return NULL;
}

/* Commented out for testing for now
// Part of Improvement 2.2
static inline double Hashmap_getThreshold(Hashmap * map)
{
	return map->bucket_size * map->load_factor; // Lets us decide when to resize
}
*/

static bool Hashmap_rehash(Hashmap * map, DArray * new_buckets)
{
	// Just use the existing
	for(int i = 0;i < DArray_count(map->buckets); i++){ // Looping through the buckets
		// Get the pointer to the underlying bucket
		DArray * bucket = DArray_get(map->buckets, i);
		
		if(bucket){ // if the bucket exists

			for(int i = 0;i < DArray_count(bucket);i++){ // Go through individual bucket
				// Get the node from the bucket
				HashmapNode * node = DArray_get(bucket, i);
				// I want to add this node into the new bucket
				// Rehashing the value from previous buckets to new buckets
				int bucket_n = node->hash % (map->bucket_size * 2);
				check(bucket_n >= 0, "Invalid bucket found : %d", bucket_n);

				// Now we check if that bucket exists in the map
				DArray* new_bucket = DArray_get(new_buckets, bucket_n);
				
				if(!new_bucket){ // If the buckets does not exists
									   // a new DArray and add it at the generated index
					// new bucket, set it up
					new_bucket = DArray_create(sizeof(void*), DArray_count(map->buckets)); // I keep the size of the individual bucket small or half the current size of bucekts
					check_mem(new_bucket);												   // Since really we will be having 2-3 keys per bucket if the hash function is good.
					DArray_set(new_buckets, bucket_n, new_bucket);
				}

				// Improvement - Addes by sorting the data
				DArray_sort_add(new_bucket, node, (DArray_compare)default_node_compare, DARRAY_HEAPSORT);
			}

			// Deallocate memory from that bucket
			DArray_destroy(bucket);
			bucket = NULL;
		}
	}

	// Deallocate memory from the existing buckets
	DArray_destroy(map->buckets);

	return true;
error:
	return false;
}

// Part of Improvement 2.2
// Function to resize the hashamp
static bool Hashmap_resize(Hashmap * map)
{
	// Revision 1 : We want to double the size and rehash the value in the new array

	// QUESTION : Why didn't I just use a realloc call on the existing arrays and then rehash it with the new size
	
	// Now first create a new DArray of double the size
	DArray * new_buckets = DArray_create(sizeof(DArray*), 2 * map->bucket_size); // doubling the size
	check(new_buckets != NULL, "ERROR : Failed to create new buckets!");
	// making it behave more like a regular array
	new_buckets->end = new_buckets->max;

	// Rehash the values
	bool r = Hashmap_rehash(map, new_buckets);
	check_debug(r == true, "ERROR : Failed to rehash the map!");
	
	// Update the pointer to the new buckets
	map->buckets = new_buckets;

	// Update the map bucket size
	map->bucket_size *= 2;


	return true;
error:
	return false;
}

// This function helps to add a Node with Key-Value Pair
int Hashmap_set(Hashmap* map, void* key, void* data)
{
	check(map != NULL, "ERROR : Invalid Map!");

	uint32_t hash = 0; // This will store the generated hash from the key
	DArray* bucket = Hashmap_find_bucket(map, key, 1, &hash); // Then we find/create a bucket corresponding to the hash
	check(bucket, "Error can't create bucket.");
	
	// pointer value changes depending if we find the node or not
	HashmapNode* node = NULL;

	// Improvemet : Check if the key already exists then overwrite respective value else add a new node
	int r = Hashmap_get_node(map, hash, bucket, key);

	if(r < 0){ // No existing node was found
		// Now we simply create a Node with the given key-value and store the generated hash
		node = Hashmap_node_create(hash, key, data);
		check_mem(node);

		// First check if the size is equal to threshold
		// if load_factor is 0, means we don't want to resize
		// which will be true for static and default create functions
		if( (map->load_factor) && (Hashmap_getSize(map) == Hashmap_getThreshold(map)) ){
			// call the function for resizing
			check(Hashmap_resize(map) == true, "ERROR : Failed to resize the map!");

			// Now I have to find the bucket again when the map gets resized
			bucket = Hashmap_find_bucket(map, key, 1, &hash); // Then we find/create a bucket corresponding to the hash
			check(bucket, "Error can't create bucket.");
		}

		// Improvement - Adds by sorting the data
		DArray_sort_add(bucket, node, (DArray_compare)default_node_compare, DARRAY_HEAPSORT);
		// Update the entries
		map->entries++; // this doesn't take into 
	}
	else{ // If an existing node is found, then we simply get its pointer and overwrite the value
		node = DArray_get(bucket, r);
		node->data = data;
	}

	/* Original code
	// Now we simply create a Node with the given key-value and store the generated hash
	HashmapNode* node = Hashmap_node_create(hash, key, data);
	check_mem(node);
	// and finally push that value into the bucket
		Original Code 
		DArray_push(bucket, node);
	*/

	return 0;
error:
	return -1;
}

static inline int Hashmap_get_node(Hashmap* map, uint32_t hash, DArray* bucket, void* key)
{
	check(map != NULL, "ERROR : Invalid map!");
	check(bucket != NULL, "ERROR : Invalid bucket!");

	// Ok so after implementing the hashing algorithms and
	// dynamic resizing of the hashmap I realized that the buckets
	// usually contains at max 2-3 elements and using binary search
	// to search for 2-3 elements is not really efficient.
	// However, If we keep the buckets size fixed and store a lot of elements
	// say 30-40 per bucket then using binary search would be beneficial HOWEVER we also 
	// have one problem while deleting the nodes we don't really resort them so again 
	// If we apply binary search we would be doing so on unsorted data.
	// So, in my opinion using linear searching would be just as good without all of the overhead
	// of continuous sorting and for searching the data.



	// This assumes that all the Keys are unique
	// Here we traverse the DArray which is provided and compare the keys and hash values
	// and simply return the index to that element in the DArray at the end and -1 on failure
	
	
	//Original Code
	int i = 0;
	for(i = 0;i < DArray_end(bucket); i++){
		debug("TRY : %d", i);
		HashmapNode* node = DArray_get(bucket, i);
		if(node->hash == hash && map->compare(node->key, key) == 0){
			return i;
		}
	}
	

	/* Commenting this part out and sticking with the original
	// Updated 
	// Ideas : How about I create new node with the same has and key values
	// and then search it within the array
	HashmapNode node = {key, NULL, hash};
	// Then we pass this element into DArray_find function
	int r = DArray_find(bucket, &node, (DArray_compare)default_node_compare);
	
	return r;
	*/

error:
	return -1;
}

void* Hashmap_get(Hashmap* map, void* key)
{
	uint32_t hash = 0; // Used for finding the Node
	DArray* bucket = Hashmap_find_bucket(map, key, 0, &hash); // We obtain the bucket corresponding to the hash
	if(!bucket) return NULL;
	
	int i = Hashmap_get_node(map, hash, bucket, key); // Then we get the index of the node within that bucket
	if(i == -1) return NULL;
	
	HashmapNode* node = DArray_get(bucket, i); // Now we obtain the node from the bucket if it exists
	check(node != NULL, "Failed to get node from bucket when it should exist");
	// and simply return the data associated with it
	return node->data;
error:
	return NULL;
}

// Part of Improvment 2.2
size_t Hashmap_getSize(Hashmap * map)
{
	// Function can be called by user so check 
	check(map != NULL, "ERROR : Invalid map!");

	return map->entries;
error:
	return 0;
}

int Hashmap_traverse(Hashmap* map, Hashmap_traverse_cb traverse_cb)
{
	check(map != NULL, "ERROR : Invalid Map!");

	int i = 0;
	int j = 0;
	int rc = 0 ;
	// We enter the buckets
	for(i = 0; i < DArray_count(map->buckets); i++){
		DArray* bucket = DArray_get(map->buckets, i);
		// Check if the bucket is valid, i.e. if it contains any data
		if(bucket){
			for(j = 0; j < DArray_count(bucket); j++){
				HashmapNode* node = DArray_get(bucket, j); // fetches the node and traverses it
				check(node != NULL, "ERROR : Invalid Node"); // check for valid node
				rc = traverse_cb(node);
				if(rc != 0)
					return rc; // any value other than 0 is considered an error
			}
		}
	}
	
	return 0;
error:
	return 1;
}

// Function to remove a Node from the map
void* Hashmap_delete(Hashmap* map, void* key)
{
	// First we will find the bucket associated with the hash
	uint32_t hash = 0;
	DArray* bucket = Hashmap_find_bucket(map, key, 0, &hash);
	if(!bucket)
		return NULL;
	
	// Then we find the node itself
	int i = Hashmap_get_node(map, hash, bucket, key);
	if(i == -1)
		return NULL;
	
	// Now we get that node from the bucket
	HashmapNode* node = DArray_get(bucket, i);
	void* data = node->data;
	free(node); // deallocate memory from that node
	
	HashmapNode* ending = DArray_pop(bucket); // Now we get Node which is situated at the end
	
	if(ending != node){ // If the node we deleted and the node at the end were same then it okay
		// alright looks like its not the last one swap it
		// as they are not same we simply overwrite the value in the bucket 
		// associated with the index of our deleted node with the popped node
		DArray_set(bucket, i, ending);
	}
	
	// Update the size;
	map->entries--;

	// and we return the data of the deleted node
	return data;
}
