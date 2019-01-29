# Eli Bolotin
# DS730 Lesson 1
# second.py

import sys

# read standard input and split standard input at space
input_list = sys.stdin.read().split(" ")

# apply int to input list, then convert this object to list
integer_list = list(map(int, input_list))

# find mean
mean_list = sum(integer_list) / len(integer_list)

# print mean
print(mean_list)