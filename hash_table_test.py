import hash_table as ht
import datetime
import random
import string
import numpy
import time

m = 42 

def get_keys():
	float_key = random.random()
	int_key = random.randint(0, 100000)
	string_key = ''.join(random.choice(string.printable) for _ in xrange(10))
	tuple_key = (float_key, int_key, string_key)
	return [float_key, int_key, string_key, tuple_key]

def assert_type_error(case):
	try:
		hash = ht.Hash(case).get(m)
		assert hash == None
	except Exception as e:
		assert isinstance(e, TypeError)


def test_hash_equality():
	for case in get_keys():
		assert ht.Hash(case).get(m) == ht.Hash(case).get(m)

def test_hash_int_return():
	for case in get_keys():
		assert type(ht.Hash(case).get(m)) is int

def test_hash_list_error():
	assert_type_error([4, 2]) 

def test_hash_set_error():
	assert_type_error(set([42])) 

def test_hash_dict_error():
	assert_type_error({42: 42})


def test_hashtable_get_set():
	hashtable = ht.hashtable()
	dictionary = dict()
	for value in xrange(100):
		keys = get_keys()
		for key in keys:
			hashtable[key] = value
			dictionary[key] = value
	assert len(hashtable) == len(dictionary)
	for key in dictionary:
		assert hashtable[key] == dictionary[key]

def test_hashtable_delete():
	hashtable = ht.hashtable()
	dictionary = dict()
	for value in xrange(100):
		keys = get_keys()
		for key in keys:
			hashtable[key] = value
			dictionary[key] = value
	for _ in range(10):
		key = random.choice(dictionary.keys())
		del hashtable[key]
		del dictionary[key]
	assert len(hashtable) == len(dictionary)
	for key in dictionary:
		assert hashtable[key] == dictionary[key]
		
def test_hashtable_less_than_linear_time_complexity():
	test_cases = dict()
	Ns = [n for n in xrange(100, 5000, 100)]
	for n in Ns:
		hashtable = ht.hashtable()
		for value in xrange(n):
			for key in get_keys():
				hashtable[key] = value
		test_cases[n] = hashtable

	execution_times = []
	for n in Ns:
		time1 = time.clock()
		for key in test_cases[n]:
			_ = test_cases[n][key]
		average_time = (time.clock() - time1) / n
		execution_times.append(average_time)
			
	correlation = numpy.corrcoef(Ns, execution_times)[0, 1]
		 
	assert correlation < 0.5		
