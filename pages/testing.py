import streamlit as st
import sys
sys.path.append('../')
# from funs.funs import deductible_loan
from bs import FixedLoan, LineOfCredit


def deductible_loan(floan):
    """
    Everytime you do a payment on ur fixed loan, you borrow the principal from the 
    interest-tax-deductible loan. 
    
    https://www.investopedia.com/articles/mortgages-real-estate/08/tax-deductible-mortgage-canada.asp
    """
    
    schedule = floan.payment_schedule()
    pmt = floan.pmt()
    
    # Open interest tax deductible line of credit

    loc = LineOfCredit(name='tax-deductible',
                       total_amount=floan.total_amount,
                       frequency=floan.frequency,
                       rate=floan.rate,
                       curr_balance=0)


    print(schedule)
    return schedule    


floan = FixedLoan(name='Mtg', total_amount=350000, frequency='Biweekly',
                  rate=0.05, term=25, curr_period=1)

st.dataframe(deductible_loan(floan))









