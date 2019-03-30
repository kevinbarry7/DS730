import pprint as pp
from itertools import permutations
import timeit
import math

start_time = timeit.default_timer()

def get_perm(ls, start = 0, count = 0, limit = None):
	r = 1
	i = 0
	turn = len(ls)

	while start < turn-1 and i != turn:
		if start != i or count == 0:
			ls_copy = ls.copy()
			start_val = ls[start]
			swap_val = ls[i]
			ls_copy[start] = swap_val
			ls_copy[i] = start_val		
			yield ls_copy

			count += 1

		if r % turn != 0:
			i += 1
		elif r % turn == 0:
			start += 1
		
		if r != turn:
			r += 1

		# print(f"\t\t\t-- after -- start: {start}, i: {i}, count: {count}, r: {r}")

	if count < limit:
		yield from get_perm(ls_copy, 0, count, limit)



a = ['1', '2', '3']
perm_list = []
len_list = len(a)
f = math.factorial(len_list)

for o in get_perm(a, limit = f):
	perm_list.append(tuple(o))
	# print(o)

p1 = set(perm_list)

stop_time = timeit.default_timer()

print(f"{len(p1)}")
print('Time elapsed 1: ', stop_time - start_time)

# start_time2 = timeit.default_timer()

# p2 = set(permutations(a))

# stop_time2 = timeit.default_timer()

# print(f"{len(p2)}")
# print('Time elapsed 2: ', stop_time2 - start_time2)
# print("diff: ", len(p1.difference(p2)))