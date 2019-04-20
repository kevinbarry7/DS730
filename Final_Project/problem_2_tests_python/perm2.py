import pprint as pp
from itertools import permutations


def get_perm(ls, len_list, start = None):
	if start is None:
		start = 0
	else:
		start += 1

	for i in range(start, len_list):
		ls_copy = ls.copy()
		start_val = ls[start]
		swap_val = ls[i]
		ls_copy[start] = swap_val
		ls_copy[i] = start_val
		# print(f"Start: {start}, i: {i}")
		yield ls_copy

		for np in get_perm(ls_copy, len_list, start):
			yield np

a = ['A', 'B', 'C']
# a = [1,2,3]
perm_list = []
len_list = len(a)

for o in get_perm(a, len_list):
	print("\t", o)
	perm_list.append(tuple(o))

p1 = set(perm_list)
print(f"{len(p1)}")
p2 = set(permutations(a))
print(f"{len(p2)}")
print(len(p2.difference(p1)))

