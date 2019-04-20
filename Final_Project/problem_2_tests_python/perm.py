import pprint as pp
from itertools import permutations
import timeit

start_time = timeit.default_timer()
def get_perm(ls, len_list, start = None):
	if start is None:
		yield ls
		start = 0
	else:
		start += 1

	for i in range(start, len_list):
		ls_post = ls.copy()
		start_val = ls_post[start]
		swap_val = ls_post[i]
		ls_post[start] = swap_val
		ls_post[i] = start_val
		# print(f"\t\t\ti: {i}, start: {start}")
		if ls != ls_post:
			yield ls_post

		for np in get_perm(ls_post, len_list, start):
			yield np

a = ['A', 'B', 'C','D','E','F','G','H']

perm_list = []
len_list = len(a)

for o in get_perm(a, len_list):
	perm_list.append(tuple(o))

stop_time = timeit.default_timer()

### p1

print('Time elapsed 1: ', stop_time - start_time)

p1 = set(perm_list)
print(f"{len(p1)}")

### p2

start_time2 = timeit.default_timer()
p2 = set(permutations(a))
print(f"{len(p2)}")
stop_time2 = timeit.default_timer()

print('Time elapsed 2: ', stop_time2 - start_time2)

# print(len(p2.difference(p1)))

