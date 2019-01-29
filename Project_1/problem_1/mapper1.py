#!/usr/bin/env python

import sys

def main(argv):
    # read in first line
    line = sys.stdin.readline()
    # if line starts with header row, skip it (get next line)
    if line.startswith('InvoiceNo'):
        line = sys.stdin.readline()
    # loop through remaining lines
    for line in sys.stdin:
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
        # if customer_id is not empty and invoice_test is false, print output
        if customer_id != '' and invoice_test is False:
            print('%s\t%s\t%s\t%s' % (month, country, customer_id, amount_spent))
if __name__ == "__main__":
    main(sys.argv)