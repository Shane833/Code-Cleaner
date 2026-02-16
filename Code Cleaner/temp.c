#undef NDEBUG
#include <stdint.h>
#include <lcthw/hashmap.h>
#include <lcthw/dbg.h>
#include <lcthw/bstrlib.h>
#include <stdbool.h>



static int default_compare(const void * a, const void * b)
{
	return bstrcmp((bstring) a, (bstring) b);
}


static int default_node_compare(const HashmapNode * a, const HashmapNode * b)
{
	if(default_compare(a->key, b->key) == 0 && a->hash == b->hash){
		return 0;
	}else{
		return default_compare(a->key,b->key);
	}
}


static inline int Hashmap_get_node(Hashmap* map, uint32_t hash, DArray* bucket, void* key);


static inline size_t Hashmap_getThreshold(Hashmap * map)
{
	return (size_t)(map->bucket_size * map->load_factor);
}




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


static uint32_t default_hash(void * a ,uint32_t seed)
{
	char * key = bdata((bstring)a);
	size_t len = blength((bstring)a);

	return Hashmap_murmur3_32_hash(key, len, seed);
}



Hashmap * Hashmap_create(Hashmap_compare compare, Hashmap_hash hash)
{
	Hashmap* map = calloc(1, sizeof(Hashmap));
	check_mem(map);
	
	
	map->compare = compare == NULL ? default_compare : compare; 
	map->hash = hash == NULL ? default_hash : hash;
	
	
	map->bucket_size = 0;
	map->load_factor = 0.0;
	map->entries = 0;

	
	
	map->buckets = DArray_create(sizeof(DArray*), DEFAULT_NUMBER_OF_BUCKETS);

	
	
	
	
	map->buckets->end = map->buckets->max; 
	check_mem(map->buckets);

	
	srand(time(NULL));
	
	map->seed = (uint32_t)rand();

	return map;
error:
	if(map){
		Hashmap_destroy(map);
	}
	return NULL;
}


Hashmap * Hashmap_createStatic(Hashmap_compare compare, Hashmap_hash hash, size_t bucket_size)
{
	Hashmap* map = calloc(1, sizeof(Hashmap));
	check_mem(map);
	
	
	map->compare = compare == NULL ? default_compare : compare; 
	map->hash = hash == NULL ? default_hash : hash;
	
	
	check(bucket_size > 0, "ERROR : Invalid Bucket Size!");
	map->bucket_size = bucket_size;

	
	map->buckets = DArray_create(sizeof(DArray*), map->bucket_size);

	
	
	
	
	map->buckets->end = map->buckets->max; 
	check_mem(map->buckets);

	
	srand(time(NULL));
	
	map->seed = (uint32_t)rand();

	return map;
error:
	if(map){
		Hashmap_destroy(map);
	}
	return NULL;
}


Hashmap * Hashmap_createDynamic(Hashmap_compare compare, Hashmap_hash hash, size_t bucket_size, double load_factor)
{
	Hashmap* map = calloc(1, sizeof(Hashmap));
	check_mem(map);

	
	map->compare = compare == NULL ? default_compare : compare; 
	map->hash = hash == NULL ? default_hash : hash;
	
	
	check(load_factor > 0.0, "ERROR : Invalid Load Factor!");
	map->load_factor = load_factor;

	
	check(bucket_size > 0, "ERROR : Invalid Bucket Size!");
	map->bucket_size = bucket_size;

	
	map->buckets = DArray_create(sizeof(DArray*), map->bucket_size);
	check_mem(map->buckets);

	
	
	
	
	map->buckets->end = map->buckets->max; 
	
	
	srand(time(NULL));
	
	map->seed = (uint32_t)rand();

	return map;
error:
	if(map){
		Hashmap_destroy(map);
	}
	return NULL;
}


void Hashmap_destroy(Hashmap* map)
{
	int i = 0;
	int j = 0;
	
	if(map){
		
		if(map->buckets){
			
			for(i = 0;i < DArray_count(map->buckets); i++){
				DArray* bucket = DArray_get(map->buckets, i);
				
				if(bucket){
					
					for(j = 0;j < DArray_count(bucket); j++){
						free(DArray_get(bucket, j));
					}
					
					DArray_destroy(bucket);
				}
			}
		}
		
		DArray_destroy(map->buckets);

		
		free(map);
	}	
}


static inline HashmapNode* Hashmap_node_create(int hash, void* key, void* data)
{
	
	HashmapNode* node = calloc(1, sizeof(HashmapNode));
	check_mem(node);
	
	node->key = key;
	node->data = data;
	node->hash = hash;
	
	return node;
error:
	return NULL;
}



static inline DArray* Hashmap_find_bucket(Hashmap* map, void* key, int create, uint32_t* hash_out)
{
	check(map != NULL, "ERROR : Invalid map!");
	check(hash_out != NULL, "ERROR : Invalid hash out provided!");

	
	uint32_t hash = map->hash(key, map->seed); 
	/*Original Code
	int bucket_n = hash % DEFAULT_NUMBER_OF_BUCKETS; 
													 
													 
													 
	check(bucket_n >= 0, "Invalid bucket found: %d", bucket_n);
	
	*/

	
	int bucket_n = map->bucket_size == 0 ? hash % DEFAULT_NUMBER_OF_BUCKETS : hash % map->bucket_size;
	check(bucket_n >= 0, "Invalid bucket found : %d", bucket_n);

	
	*hash_out = hash; 
					  
					  
	
	
	DArray* bucket = DArray_get(map->buckets, bucket_n);
	
	if(!bucket && create){ 
						   
		
		bucket = DArray_create(sizeof(void*), DArray_count(map->buckets));
		check_mem(bucket);
		DArray_set(map->buckets, bucket_n, bucket);
	}
	
	return bucket; 
error:
	return NULL;
}

/* Commented out for testing for now

static inline double Hashmap_getThreshold(Hashmap * map)
{
	return map->bucket_size * map->load_factor; 
}
*/

static bool Hashmap_rehash(Hashmap * map, DArray * new_buckets)
{
	
	for(int i = 0;i < DArray_count(map->buckets); i++){ 
		
		DArray * bucket = DArray_get(map->buckets, i);
		
		if(bucket){ 

			for(int i = 0;i < DArray_count(bucket);i++){ 
				
				HashmapNode * node = DArray_get(bucket, i);
				
				
				int bucket_n = node->hash % (map->bucket_size * 2);
				check(bucket_n >= 0, "Invalid bucket found : %d", bucket_n);

				
				DArray* new_bucket = DArray_get(new_buckets, bucket_n);
				
				if(!new_bucket){ 
									   
					
					new_bucket = DArray_create(sizeof(void*), DArray_count(map->buckets)); 
					check_mem(new_bucket);												   
					DArray_set(new_buckets, bucket_n, new_bucket);
				}

				
				DArray_sort_add(new_bucket, node, (DArray_compare)default_node_compare, DARRAY_HEAPSORT);
			}

			
			DArray_destroy(bucket);
			bucket = NULL;
		}
	}

	
	DArray_destroy(map->buckets);

	return true;
error:
	return false;
}



static bool Hashmap_resize(Hashmap * map)
{
	

	
	
	
	DArray * new_buckets = DArray_create(sizeof(DArray*), 2 * map->bucket_size); 
	check(new_buckets != NULL, "ERROR : Failed to create new buckets!");
	
	new_buckets->end = new_buckets->max;

	
	bool r = Hashmap_rehash(map, new_buckets);
	check_debug(r == true, "ERROR : Failed to rehash the map!");
	
	
	map->buckets = new_buckets;

	
	map->bucket_size *= 2;


	return true;
error:
	return false;
}


int Hashmap_set(Hashmap* map, void* key, void* data)
{
	check(map != NULL, "ERROR : Invalid Map!");

	uint32_t hash = 0; 
	DArray* bucket = Hashmap_find_bucket(map, key, 1, &hash); 
	check(bucket, "Error can't create bucket.");
	
	
	HashmapNode* node = NULL;

	
	int r = Hashmap_get_node(map, hash, bucket, key);

	if(r < 0){ 
		
		node = Hashmap_node_create(hash, key, data);
		check_mem(node);

		
		
		
		if( (map->load_factor) && (Hashmap_getSize(map) == Hashmap_getThreshold(map)) ){
			
			check(Hashmap_resize(map) == true, "ERROR : Failed to resize the map!");

			
			bucket = Hashmap_find_bucket(map, key, 1, &hash); 
			check(bucket, "Error can't create bucket.");
		}

		
		DArray_sort_add(bucket, node, (DArray_compare)default_node_compare, DARRAY_HEAPSORT);
		
		map->entries++; 
	}
	else{ 
		node = DArray_get(bucket, r);
		node->data = data;
	}

	/* Original code
	
	HashmapNode* node = Hashmap_node_create(hash, key, data);
	check_mem(node);
	
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

	
	
	
	
	
	
	
	
	
	



	
	
	
	
	
	
	int i = 0;
	for(i = 0;i < DArray_end(bucket); i++){
		debug("TRY : %d", i);
		HashmapNode* node = DArray_get(bucket, i);
		if(node->hash == hash && map->compare(node->key, key) == 0){
			return i;
		}
	}
	

	/* Commenting this part out and sticking with the original
	
	
	
	HashmapNode node = {key, NULL, hash};
	
	int r = DArray_find(bucket, &node, (DArray_compare)default_node_compare);
	
	return r;
	*/

error:
	return -1;
}

void* Hashmap_get(Hashmap* map, void* key)
{
	uint32_t hash = 0; 
	DArray* bucket = Hashmap_find_bucket(map, key, 0, &hash); 
	if(!bucket) return NULL;
	
	int i = Hashmap_get_node(map, hash, bucket, key); 
	if(i == -1) return NULL;
	
	HashmapNode* node = DArray_get(bucket, i); 
	check(node != NULL, "Failed to get node from bucket when it should exist");
	
	return node->data;
error:
	return NULL;
}


size_t Hashmap_getSize(Hashmap * map)
{
	
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
	
	for(i = 0; i < DArray_count(map->buckets); i++){
		DArray* bucket = DArray_get(map->buckets, i);
		
		if(bucket){
			for(j = 0; j < DArray_count(bucket); j++){
				HashmapNode* node = DArray_get(bucket, j); 
				check(node != NULL, "ERROR : Invalid Node"); 
				rc = traverse_cb(node);
				if(rc != 0)
					return rc; 
			}
		}
	}
	
	return 0;
error:
	return 1;
}


void* Hashmap_delete(Hashmap* map, void* key)
{
	
	uint32_t hash = 0;
	DArray* bucket = Hashmap_find_bucket(map, key, 0, &hash);
	if(!bucket)
		return NULL;
	
	
	int i = Hashmap_get_node(map, hash, bucket, key);
	if(i == -1)
		return NULL;
	
	
	HashmapNode* node = DArray_get(bucket, i);
	void* data = node->data;
	free(node); 
	
	HashmapNode* ending = DArray_pop(bucket); 
	
	if(ending != node){ 
		
		
		
		DArray_set(bucket, i, ending);
	}
	
	
	map->entries--;

	
	return data;
}
