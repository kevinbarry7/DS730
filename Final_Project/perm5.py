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

	l = [] # empty list that will store current permutation 
	if level is None:
		level = 1
	
	print(level)
	for i in range(len(lst)): 
		m = lst[i] 
		print("PARENT --- M: ", m)

		remLst = lst[:i] + lst[i+1:] 
		print("PARENT --- remLst: ", remLst)
		level += 1
		for p in get_perm(remLst, level):
			l.append([m] + p)
			print(f"--- sub: {[m]} and {p}") 
		break
	return l

a = ['A', 'B', 'C']
perm_list = []
len_list = len(a)

for o in get_perm(a):
	# perm_list.append(tuple(o))
	print(o)


# p1 = set(perm_list)
# print(f"{len(p1)}")

# stop_time = timeit.default_timer()
# print('Time elapsed 1: ', stop_time - start_time)

# start_time2 = timeit.default_timer()

# p2 = set(permutations(a))
# print(f"{len(p2)}")

# stop_time2 = timeit.default_timer()
# print('Time elapsed 2: ', stop_time2 - start_time2)


# print("diff: ", len(p1.difference(p2)))