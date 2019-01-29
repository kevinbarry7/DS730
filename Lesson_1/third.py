# Eli Bolotin
# DS730 Lesson 1
# third.py

import sys

# list for input strings
input_list = []

# loop through sequence of length 2, ask for input numbers, and append both numbers to list.
for i in range(1, 3):
	num = input(f"Enter number {i}: ")
	input_list.append(num)

# convert numbers (in string form from input_list) to integers
input_integers = list(map(int, input_list))

# find min integer and add 1 to specify range "strictly"
num_min = min(input_integers) + 1

# find max integer
num_max = max(input_integers)

# create range of min/max integer
num_range = range(num_min, num_max)
prime_numbers = []

# loop through every number (int) in num_range
for num in num_range:
	# define count of factors
	count_factors = 0

	# for every integer greater than 1
	for i in range(2, num):

		# check that the remainder of dividing num by i is 0
		if num % i == 0:
			# if true, then this is a factor. add count.
			count_factors += 1

	# if count factors is 0, then we have identified a prime.
	if count_factors is 0:
		prime_numbers.append(num)

# condition for 0 primes
if len(prime_numbers) is 0:
	print("No Primes")

# condition for 1 prime
elif len(prime_numbers) is 1:
	print(prime_numbers[0])

# condition for > 1 prime
else:
	# define delimiters
	delimiters = [':', '!', '&']

	# get end of list index
	end_index = len(prime_numbers) - 1

	i = 0

	# loop through (enumerated) prime numbers
	for j, num in enumerate(prime_numbers):
		if j != end_index:
			# prime primes with delimiter
			print(f'{num}{delimiters[i]}', end = '')

			# increment delimiter index
			if i < 2:
				i += 1

			else:
				i = 0
		else:
			# if end of list, just print the prime
			print(f'{num}', end = '')

	# carriage return
	print("\r")