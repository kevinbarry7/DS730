import pprint as pp
from itertools import permutations
import timeit

start_time = timeit.default_timer()

# print(len(p2.difference(p1)))

def get_perm(lst, level = None): 
	if len(lst) == 0: 
		return [] 

	if len(lst) == 1: 
		return [lst] 

	l = []
	
	for i in range(len(lst)): 
		m = lst[i] 

		remLst = lst[:i] + lst[i+1:] 

		for p in get_perm(remLst):
			l.append([m] + p)
	return l

a = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
perm_list = []
len_list = len(a)

for o in get_perm(a):
	perm_list.append(tuple(o))

p1 = set(perm_list)
stop_time = timeit.default_timer()

print(f"{len(p1)}")
print('Time elapsed 1: ', stop_time - start_time)

start_time2 = timeit.default_timer()

p2 = set(permutations(a))

stop_time2 = timeit.default_timer()

print(f"{len(p2)}")
print('Time elapsed 2: ', stop_time2 - start_time2)
print("diff: ", len(p1.difference(p2)))