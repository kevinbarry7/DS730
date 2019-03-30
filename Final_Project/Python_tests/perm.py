import pprint as pp
from itertools import permutations


def get_perm(ls, len_list, start = None):
	if start is None:
		yield ls
		start = 0
	else:
		start += 1

	for i in range(start, len_list):
		ls_pre = ls.copy()
		ls_post = ls_pre.copy()
		start_val = ls_post[start]
		swap_val = ls_post[i]
		ls_post[start] = swap_val
		ls_post[i] = start_val
		print(f"Start: {start}, i: {i}")
		if ls_pre != ls_post:
			yield ls_post

		for np in get_perm(ls_post, len_list, start):
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

