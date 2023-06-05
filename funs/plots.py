import streamlit as st
import numpy as np
import pandas as pd
from .funs import continuous_investing, n_frequency, convert_frequency, good_print
import seaborn as sns
sns.set(style="whitegrid")
import matplotlib.pyplot as plt

def plot_continuous_investing(savings, freq):
        st.write(f'Continuosly compunding it...')

        box = st.columns(2)

        initial_investment = box[0].number_input(label='Any intial savings?', min_value=0)
        time_horizon_years = box[1].number_input(label='Years', min_value=1)

        box2 = st.columns(2)
        apr = box2[0].number_input(label='Annual rate', max_value=1.00)


        compounded_savings = continuous_investing(initial_investment=initial_investment, 
                                                  annualized_return=apr,
                                                  contribution=savings, 
                                                  frequency=freq, 
                                                  time_horizon_years=time_horizon_years)
        
        contributions = np.full(len(compounded_savings), savings)
        contributions[0] = initial_investment #Add initial investment
        cumulative_contributions = np.cumsum(contributions)
        #Plot compounded interest
        time_axis = list(range(0, len(compounded_savings)))


        fig, ax = plt.subplots(figsize=(10,4))
        # figure(figsize=(10, 4))
        sns.lineplot(x=time_axis, y=compounded_savings, label='Investment value', ax=ax)
        sns.barplot(x=time_axis, y=cumulative_contributions, label='Total contributions / Not compounded', ax=ax)
        ax.set_title('Compounding Over Time')
        ax.set_xticks([])
        ax.set_xlabel('Time')
        ax.set_ylabel('Value')

        final_compsav = round(compounded_savings[-1], 2)
        final_cumcontrib = round(cumulative_contributions[-1], 2)

        textstr = f"""Terminal values:\nCompounded savings: ${final_compsav}
                        \nCumulative contributions: ${final_cumcontrib}"""
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text(0.02, 0.85, textstr, transform=ax.transAxes, fontsize=12,
        verticalalignment='top', bbox=props)
        st.pyplot(fig)
        st.write(f'Difference of fund value vs total contributions: **{good_print(final_compsav-final_cumcontrib)}**')

        #Investment profit
        #Yearly gains (avg)
        n = n_frequency(freq)
        yearly_returns = compounded_savings[::n]
        yearly_contributions = cumulative_contributions[::n]

        # st.write(yearly_returns)
        # st.write(yearly_contributions)

        #Table info
        tbl = pd.DataFrame(data={'ret': yearly_returns, 'con': yearly_contributions}, index=range(0,time_horizon_years+1))
        tbl.iloc[0:1,:] = 0
        tbl.index.name = 'End of Year #'
        
        tbl['ret_diff'] = tbl['ret'].diff()
        tbl['con_diff'] = tbl['con'].diff()
        
        tbl['inv_profit'] = tbl['ret_diff']-tbl['con_diff']
        

        st.write(tbl)
        # st.write(yearly_contributions)


def plot_debt_repayment(fixed_loan):
        old_schedule = fixed_loan.payment_schedule(at_current_period=True, 
                                                   use_extra_pmt=False)
        old_interest = old_schedule['interest'].sum()

        new_schedule = fixed_loan.payment_schedule(at_current_period=True, 
                                                   use_extra_pmt=True)
        new_interest = new_schedule['interest'].sum()

        # st.dataframe(old_schedule)
        # st.dataframe(new_schedule)
        x = old_schedule['period']
        old_bal = old_schedule['final_balance']
        new_bal = new_schedule['final_balance']

        fig, ax = plt.subplots(figsize=(10,4))
        sns.lineplot(x=x, y=old_bal, label='Current', ax=ax)
        sns.lineplot(x=x, y=new_bal, label='With new contribution', ax=ax)
        ax.set_title('Debt repayment')
        ax.set_ylim(ymin=0)
        ax.set_xlabel('Periods')
        ax.set_ylabel('Value')

        st.pyplot(fig)

        # Get final balance at end of period
        old_last_period = x.values[-1]
        new_last_period = new_schedule['period'].values[-1]

        interest_diff = round(old_interest-new_interest, 2)
        periods_diff =  old_last_period - new_last_period

        st.write(f'In total, you will pay ${interest_diff} less in interests and pay your debt {periods_diff} periods sooner')
        st.write(f'New last period: {old_last_period}')
        st.write(f'New last period: {new_last_period}')


def plot_net_worth(net_worth_df, asset=True, liab=True):
    fig, ax = plt.subplots()
    x = net_worth_df['period']
    if asset:
        sns.lineplot(x=x, y=net_worth_df['total_asset'], color='green', label='Assets')
    if liab:
        sns.lineplot(x=x, y=net_worth_df['total_liability'], color='red', label='Liabilities')
    sns.lineplot(x=x, y=net_worth_df['net_worth'], color='blue', label='Net worth')
    ax.axhline(y=0, color='gray', linestyle='--')
    ax.legend(loc=0)

    st.pyplot(fig)













