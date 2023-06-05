import streamlit as st
import pandas as pd
import sys
sys.path.append('../')
from bs import FixedLoan, LineOfCredit
from funs.plots import plot_debt_repayment
from funs.funs import continuous_investing

mtg = FixedLoan('mortgage', 40000, 'Biweekly', 0.06, 7, curr_period=25)
loc = LineOfCredit('heloc', 40000, 'Biweekly', 0.03, 0)

# st.write(mtg.pmt())

tax_rate = 0.30

mtg.lump_sum(5000, 30)
mtg.lump_sum(0, 30)
mtg.lump_sum(0, 150)
mtg.extra_pmt = 100

st.write(plot_debt_repayment(mtg))
st.write(mtg.pmt())

# st.write(mtg.lumps)

schedule = mtg.payment_schedule(at_current_period=True, lump_sums=True)
#First 5 years
schedule = schedule[schedule['period']<=156]
st.write(schedule)

rows = []
tax_savings = []
for i in schedule.to_dict('records'):
    borrow = i['principal']
    loc.borrow(borrow)
    # st.write(loc.curr_balance)

    i['loc_balance'] = loc.curr_balance
    i['loc_interest'] = loc.ipmt()
    i['tax_savings'] = i['loc_interest']*tax_rate
    rows.append(i)



df = pd.DataFrame.from_records(rows)

st.write(df)
st.write(df['loc_interest'].sum())
st.write(df['tax_savings'].sum())

ret = 0.05
aa = continuous_investing(0, ret, df['principal'], 'Biweekly', 7)
st.wrtie(aa)











def smith_manoeuvre(fixed_loan, line_of_credit):
    """
    Take Equity off home, and invest it.
    The equity loc's interest payments are tax-deductible.

    Get total interest expense and deduct the tax savings

    """

    






    



    return None


