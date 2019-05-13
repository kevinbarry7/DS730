#!/usr/bin/env python

import sys

def main(argv):
	# read in first line
	line = sys.stdin.readline()
	# if line starts with header row, skip it (get next line)
	if line.startswith('InvoiceNo'):
		line = sys.stdin.readline()

	# call function to get row values
	prev_invoice_test, prev_month, prev_country, prev_customer_id, prev_amount_spent = _get_row_values(line)

	if prev_customer_id != '' and prev_invoice_test is False:
		for line in sys.stdin:
			current_invoice_test, current_month, current_country, current_customer_id, current_amount_spent = _get_row_values(line)	
			
			if current_customer_id != '' and current_invoice_test is False:
				# check if month and country is the same.
				if current_month == prev_month and current_country == prev_country and current_customer_id == prev_customer_id:
						prev_amount_spent += current_amount_spent
			
				# if current country/current month is not equal to prev country/prev month
				else:
					print('%s\t%s\t%s\t%s' % (prev_month, prev_country, prev_customer_id, prev_amount_spent))

					prev_country = current_country
					prev_month = current_month
					prev_amount_spent = current_amount_spent
					prev_customer_id = current_customer_id
					prev_invoice_test = current_invoice_test

			else:
				pass

		if current_country == prev_country:
			print('%s\t%s\t%s\t%s' % (prev_month, prev_country, prev_customer_id, prev_amount_spent))
def _get_row_values(line):
	try:
		# split line into list at commas
		row = line.split(',')
		# check if invoice starts with upper or lowercase C
		invoice_test = row[0].startswith(('C','c'))
		# get month
		month = row[4].split("/",1)[0]
		# strip whitespace from country
		country = row[7].strip()
		# get other column values
		customer_id = row[6]
		quantity = int(row[3])
		unitprice = float(row[5])
		amount_spent = quantity * unitprice
		return(invoice_test, month, country, customer_id, amount_spent)
	
	except Exception as error:
		print(error)
		return(error)

if __name__ == "__main__":
	main(sys.argv)