#!/usr/bin/env python

import sys
import operator

def main(argv):
    # read in first line
    for line in sys.stdin:
        # get line values
        prev_month, prev_country, prev_customer_id, prev_amount_spent =  _get_row_values(line)
        # define most spent and top spender (customer id)
        top_spent = prev_amount_spent
        top_spender = prev_customer_id
        
        # loop through every line in standard input
        for line in sys.stdin:
            # get line values
            current_month, current_country, current_customer_id, current_amount_spent =  _get_row_values(line)

            # check if current country and month vary from previous country/month
            if prev_country == current_country and prev_month == current_month:
                # check if prev customer id is equal to current customer id
                if prev_customer_id == current_customer_id:
                    prev_amount_spent += current_amount_spent
                
                # if they are not equal to eachother
                elif prev_customer_id != current_customer_id:
                    # then check to see if incremented amount spent is greater than top spent
                    if top_spent < prev_amount_spent:
                        # if so, set top spent to (new) amount spent, and save top spender
                        top_spent = prev_amount_spent
                        top_spender = prev_customer_id

                    # if there is a tie, then append customer_id to top_spender
                    elif top_spent == prev_amount_spent:
                        top_spender = top_spender + "," + prev_customer_id
                    
                    prev_amount_spent = current_amount_spent
                    prev_customer_id = current_customer_id

            # if previous country/month are not the same as current country/month
            else:
                # check if incremented amount spent is greater than top_spent
                if top_spent < prev_amount_spent:
                    # set new top spent/spender
                    top_spent = prev_amount_spent
                    top_spender = prev_customer_id

                # if there is a tie
                elif top_spent == prev_amount_spent:
                    # append tied customer_id to top spender
                    top_spender = top_spender + "," + prev_customer_id

                # print month, country, and top spender
                print('%s,%s:%s' % (prev_month, prev_country, top_spender))
                
                # update variables for next iteration
                prev_amount_spent = current_amount_spent
                prev_country = current_country
                prev_customer_id = current_customer_id
                prev_month = current_month
                top_spender = prev_customer_id
                most_spent = prev_amount_spent

        # print final line
        print('%s,%s:%s' % (prev_month, prev_country, top_spender))

# function performs activites related to line splitting & value formatting
def _get_row_values(line):
    try:
        row = line.split("\t")
        del row[2]
        del row[1]
        key = row[0].split(",")
        value = row[1].strip("\n")
        month = key[0]
        # if current month is single digit, prepend 0
        if len(month) == 1:
            month = '0' + month

        country = key[1]
        customer_id = key[2]
        amount_spent = float(value)
        return(month, country, customer_id, amount_spent)

    except Exception as error:
        print(error)
# Note there are two underscores around name and main
if __name__ == "__main__":
    main(sys.argv)