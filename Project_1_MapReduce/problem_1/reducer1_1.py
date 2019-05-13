#!/usr/bin/env python

import sys

def main(argv):
    # read in first line
    line = sys.stdin.readline()
    # define variables for first line
    prev_month = None
    prev_country = None
    prev_customer_id = None
    prev_amount_spent = 0
    top_spender = ''
    most_spent = 0
    # iterate through remaining lines
    for line in sys.stdin:
        # get current line values
        current_month, current_country, current_customer_id, current_amount_spent =  _get_row_values(line)
        if current_customer_id == prev_customer_id:
            prev_amount_spent += current_amount_spent
        else:
            if prev_customer_id is not None:
                # if most spent is less than incremented amount spent, set new top spender and most spent
                if most_spent < prev_amount_spent:
                    most_spent = prev_amount_spent
                    top_spender = prev_customer_id
                # if there is a tie in top spending, append customer id
                elif most_spent == prev_amount_spent:
                    top_spender = top_spender + ',' + prev_customer_id
                print('%s,%s:%s' % (prev_month, prev_country, top_spender))
            prev_amount_spent = current_amount_spent
            prev_customer_id = current_customer_id
            prev_month = current_month
            prev_country = current_country
    # if end of file, print results
    if current_country == prev_country:
        print('%s,%s:%s' % (prev_month, prev_country, top_spender))
def _get_row_values(line):
    try:
        row = line.split("\t")
        key = row[0].split(",")
        value = row[1].split(",")
        month = key[0]
        # if current month is single digit, prepend 0
        if len(month) == 1:
            month = '0' + month
        country = key[1]
        customer_id = value[0]
        amount_spent = float(value[1])
        return(month, country, customer_id, amount_spent)
    except Exception as error:
        print(error)
# Note there are two underscores around name and main
if __name__ == "__main__":
    main(sys.argv)