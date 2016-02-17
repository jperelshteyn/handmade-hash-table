import sys
import math
import datetime
import random

               
class Hash:
    def __init__(self, key):
        assert key != None
        self.key = key

    def get(self, m):
        int_key = self._to_int(self.key)
        random.seed(int_key)
        return random.randint(0, m-1)
        
    def _to_int(self, key):
		# determine key type and utilize appropriate hashing functions
        key_type = type(key)
        if key_type is tuple:
			# recurse tuple values back into this function
            return sum(i + self._to_int(el) for i, el in enumerate(key))
        if key_type in [str, unicode]:
            return self._from_string(key)
        if key_type is float:
            return abs(self._from_float(key))
        if key_type is long:
            return abs(self._from_long(key))
        if key_type is int:
            return abs(key)
        if isinstance(key, datetime.datetime):
            return self._from_datetime(key)
        raise TypeError(str(key_type) + " is unhashable type")
    
    def _from_string(self, key):
		# utilize string folding technique
		# take four characters at a time multiply their ascii value by exponents of 256
        key = unicode(key)
        string_sum = 0
        try:
            for step in range(0, len(key), 4):
                mult = 1
                for i in range(4):
                    char = key[step+i]
                    string_sum += ord(char) * mult
                    mult *= 256
            return string_sum
        except IndexError:
            return string_sum

    def _from_float(self, key):
		# break float into integer ratio and return their product
        n1, n2 = key.as_integer_ratio()
        return self._from_long(n1 * n2)

    def _from_long(self, key):
        return int(key % sys.maxint)
    
    def _from_datetime(self, key):
        return int((key - datetime.datetime(1970,1,1)).total_seconds())

		
class Tombstone:
	def __init__(self):
		self = self

class HashTable:

	# hashtable utilizing quadratic probing
    def __init__(self, min_size = 1009):
        self.min_size = min_size
        self._m = min_size
        self._key_table = self._make_table()
        self._value_table = self._make_table()
        self.count = 0
        
    def __setitem__(self, key, value):
        idx = self._find_index(key, to_set=True)
        self._key_table[idx] = key
        self._value_table[idx] = value
        self._check_size()
        
    def __getitem__(self, key):
        idx = self._find_index(key)
        return self._value_table[idx]
    
    def __delitem__(self, key):
		# set a list with a None value as a tombstone
        idx = self._find_index(key)
        self._key_table[idx] = Tombstone()
        self._value_table[idx] = None
        self.count -= 1
        self._check_size()
        
    def __iter__(self):
        for key in self._key_table:
            if key != None:
                yield key
        
    def __len__(self):
        return self.count
    
    def __contains__(self, key):
        try:
            self._find_index(key)
            return True
        except KeyError:
            return False
        
    def _find_index(self, key, to_set=False):
		# get hashed index by passing key and m value
        idx = Hash(key).get(self._m)
		# find first key
        saved_key = self._key_table[idx]
		# initialize probe sequence
        probe = self._prob_seq()
		# loop through key array with probe sequence until key matches 
        while saved_key != key:
            if not saved_key:
				# reached empty slot return index if looking to set value else throw exception
                if to_set:
                    self.count += 1
                    return idx
                else:
                    raise KeyError(key)
            idx, saved_key = self._next_key(idx, saved_key, probe)
        return idx
  
    def _next_key(self, idx, key, probe):
		# return next index, key pair according to probing sequence
		# when index runs out reset to 0
        try:
            idx += probe.next()
            key = self._key_table[idx]
        except IndexError:
            idx = 0
            key = self._key_table[0]
        finally:
            return idx, key
    
    def _prob_seq(self):
		# define quadratic probing sequence generator
        for i in xrange(1, self._m):
            yield i + i * i
    
    def _check_size(self):
		# initilize array resize if size to count ratio is below or above preset criteria
        if self._m < self.count * 3 or (self._m != self.min_size and self._m > self.count * 10):
            self._resize(max(self.count * 5, self.min_size))
            
    def _resize(self, size):
		# reset size and count
        self._m = self._next_m(size)
        self.count = 0
		# copy data into temporary arrays
        old_key_table = self._key_table[:]
        old_value_table =  self._value_table[:]
		# initialize new empty arrays
        self._key_table = self._make_table()
        self._value_table = self._make_table()
		# loop through key slots skipping empties and tombstones
        for old_idx, key in enumerate(old_key_table):
            if key != None and not isinstance(key, Tombstone):
				# calculate new hashed index and set key and value
                new_idx = self._find_index(key, to_set=True)
                self._key_table[new_idx] = key
                self._value_table[new_idx] = old_value_table[old_idx]
    
    def _make_table(self):
        return [None for _ in range(self._m)]
    
    def _next_m(self, size):
		# calculate collection size by picking first prime number that is higher than needed size
        n = size
        for p in xrange(n, 2*n):
            top_factor = int(math.ceil(math.sqrt(p)))
            for i in xrange(2, top_factor):
                if p % i == 0:
                    break
            else:
                return p
        return None
