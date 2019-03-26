a = ['a','b','c']
b = ['','','','','','','','','','','','','','','','','','']

count = 1
for i, j in enumerate(b):
	b[i] = a[count-1]
	print("i: ", i)
	print("count: ", count)
	if i % 6 == 0:
		count += 1 

print(b)