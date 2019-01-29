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
        # perform same operations as above, only for the current line
        row = line.split("\t")
        current_month = row[0]
        # if current month is single digit, prepend 0
        if len(current_month) == 1:
            current_month = '0' + current_month
        current_country = row[1]
        current_customer_id = row[2]
        current_amount_spent = float(row[3].strip('\n'))
        # check if month and country is the same.
        if current_month == prev_month and current_country == prev_country:
            # if current customer id is the same as prev customer id, increment amount spent
            if current_customer_id == prev_customer_id:
                prev_amount_spent += current_amount_spent
            else:
                # if most spent is less than incremented amount spent, set new top spender and most spent
                if most_spent < prev_amount_spent:
                    most_spent = prev_amount_spent
                    top_spender = prev_customer_id
                # if there is a tie in top spending, append customer id
                elif most_spent == prev_amount_spent:
                    top_spender = top_spender + ',' + prev_customer_id
                prev_amount_spent = current_amount_spent
                prev_customer_id = current_customer_id
        # if current country/current month is not equal to prev country/prev month
        else:
            # check if prev customer is not None
            if prev_customer_id is not None:
                # if most spent is less than incremented amount spent, set new top spender and most spent
                if most_spent < prev_amount_spent:
                    most_spent = prev_amount_spent
                    top_spender = prev_customer_id
                elif most_spent == prev_amount_spent:
                    top_spender = top_spender + ',' + prev_customer_id
                print('%s,%s:%s' % (prev_month, prev_country, top_spender))
            # reset variables
            prev_country = current_country
            prev_month = current_month
            prev_amount_spent = current_amount_spent
            prev_customer_id = current_customer_id
            most_spent = prev_amount_spent
            top_spender = prev_customer_id
    # if end of file, print results
    if current_country == prev_country:
        print('%s,%s:%s' % (prev_month, prev_country, top_spender))
# Note there are two underscores around name and main
if __name__ == "__main__":
    main(sys.argv)