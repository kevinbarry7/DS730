from functools import reduce
# product = reduce((lambda x, y: x * y), [1, 2, 3, 4])

# l = [15, 18, 2, 36, 12, 78, 5, 6, 9, 10]
l = [1, 2, 3, 4, 5, 6]
test = reduce(lambda x, y: x * y, l)
print(test)