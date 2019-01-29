# Eli Bolotin
# DS730 Lesson 1
# first.py

# define function
def factorial(val):
	# condition for negative val
	if val < 0:
		return -1

	# if val not negative
	else:
		# loop through range in reverse
		for i in range(val - 1, 0, -1):
			# perform calculation
			val = val * i
			# print(i)

		return val

number = -1
# request user input
while number < 0:
	number = int(input("Enter non-negative integer: "))

else:
	answer = factorial(number)
	print(answer)