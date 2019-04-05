ls_post = ['a','b','c','d']

ls_post_c = ls_post.copy()
for j in range(len(ls_post)):
	swap_val = ls_post_c[j-1]
	ls_post[j] = swap_val

print(ls_post)