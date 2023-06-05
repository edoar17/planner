import streamlit as st
import pickle
import sys
import seaborn as sns
import matplotlib.pyplot as plt 
import numpy as np
import pandas as pd
sys.path.append('../')
from funs.funs import * 
from funs.plots import *
from bs import Liability, Asset, FixedLoan, Car
        

profile_file = st.file_uploader('Upload your profile!')
freq = st.selectbox('Choose the time frequency', options=frequencies, key='plan_freq')

# st.write(st.session_state['profile'])

if profile_file is not None:
    profile = load_profile(file=profile_file)
    st.header(f'Great {profile["user_name"]}, Now lets build your plan!📒🖊️💹')

    #Reload profile data
    assets = pd.DataFrame.from_records(profile['assets'])
    liabilities = pd.DataFrame.from_records(profile['liabilities'])
    income = pd.DataFrame.from_records(profile['income'])
    expenses = pd.DataFrame.from_records(profile['expenses'])
    floans = [eval(x) for x in profile['floans']]
    cars = [eval(x) for x in profile['cars']]

    #Get totals
    total_assets = assets['amount'].sum()
    total_liabilities = liabilities['amount'].sum()
    #Convert cashflows to same frequencies
    income['amount'] = income.apply(lambda x: convert_frequency(x['amount'], x['frequency'], freq), axis=1)
    expenses['amount'] = expenses.apply(lambda x: convert_frequency(x['amount'], x['frequency'], freq), axis=1)
    total_income = income['amount'].sum()
    total_expense = expenses['amount'].sum()

    net_income = total_income-total_expense
    debt_expense = sum([convert_frequency(i.pmt(), i.frequency, freq) for i in floans])

    st.markdown(f"""
    By reading your profile, you earn **\${round(total_income, 2)}** {freq.lower()}. And your expenses total **\${round(total_expense, 2)}**.
    Giving you a net disposable income of **\${round(net_income, 2)}**.

    <br>
    """, unsafe_allow_html=True)
    with st.expander('See breakdown of Balance Sheet'):
        balance_sheet = pd.concat([assets,liabilities], axis=0).reset_index(drop=True)
        st.dataframe(balance_sheet.style.apply(color_balance_sheet, axis=1), width=700)
    with st.expander('See breakdown of Income Statement'):
        income_statement = pd.concat([income, expenses], axis=0).reset_index(drop=True)
        st.dataframe(income_statement.style.apply(color_income_statement, axis=1), width=700)
        
    
    with st.sidebar:
        st.markdown(f'<p style="font-size:1.5em">Gross income: {good_print(total_income)}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:red; font-size:1.0em">Debt expense: {good_print(debt_expense)}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:red; font-size:1.0em">Other expense: {good_print(total_income-debt_expense)}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:red; font-size:1.5em">Total expense: {good_print(total_income-net_income)}</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-size:4em">---------</p>', unsafe_allow_html=True)
        st.markdown(f'<p style="color:green; font-size:1.5em">Net income: {good_print(net_income)}</p>', unsafe_allow_html=True)


    st.markdown('### Set your goals.')
    yrs = st.number_input('Do a projection for how many years?', min_value=0, max_value=20)
    funds = st.multiselect('What are your financial goals? Here is a list of a few.', options=savings_funds)
    desired_fund_size = []
    if funds:
        for fu in funds:
            fcols = st.columns(2)
            with fcols[0]:
                st.markdown(f'**{fu}**')
            with fcols[1]:
                aa = st.number_input(f'What is the desired size of the {fu}?')
            desired_fund_size.append(aa)
        
    st.write(sum(desired_fund_size))
    st.write(debt_expense, net_income)


    # st.markdown('What are your financial goals? Here is a list of a few.', unsafe_allow_html=True)


    st.write(' ')
    st.write(' ')
    st.markdown('### Allocate your net income')
    # st.markdown('Next, what percentage of your disposable income do you want to save?')
    saving_percentage = st.slider('Next, what percentage of your disposable income do you want to save?')
    if saving_percentage:
        save = saving_percentage*net_income/100
        spend = (100-saving_percentage)*net_income/100
        st.markdown(f'You will **save \${round(save, 2)}** and are allowed to spend another \${round(spend, 2)} in lifestyle.')
        st.markdown(f"""
        It is a good idea to transfer these funds monthly into a TFSA before any spending. 
        Once in a savings account, you will not know it exists :)
        """)

        with st.sidebar:
            st.markdown(f'<p style="color:red; font-size:1.0em">Day to day / lifestyle fund: {good_print(net_income-save)}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:4em">---------</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="color:blue; font-size:2em">SAVINGS: {good_print(save)}</p>', unsafe_allow_html=True)
        

        # st.write('[[EXPLAIN SAVINGS APPROACH]] Assume that by continuously investing, you will dollar cost average and earn a 5-7% yield over the long run. Given that you diversify.')
        
        # Start plan to allocate savings
        # st.header('Allocation')
        st.write('With your net income, you can allocate it in an efficient way.')
        st.write('There are multiple options. Repaying debt fast, Maximum savings, etc.')



        st.write('#### How do you want to allocate your savings?')
        inv_percentage = st.slider('Investing Percentage', min_value=0, max_value=100)/100
        debt_percentage = st.slider('Debt Percentage', min_value=0, max_value=100)/100
        if inv_percentage:
            with st.expander('Investments'):
                investment = inv_percentage*save
                st.write(f'{freq}, you will invest ${investment}')
                # st.write(continuous_investing(initial_investment=iinv, 
                #                               annualized_return=irate, 
                #                               contribution=investment, 
                #                               frequency='Monthly', 
                #                               time_horizon_years=2))
                plot_continuous_investing(investment, freq)

        if debt_percentage:
            with st.expander('Debt Repayment'):
                contribution =  debt_percentage*save
                st.write()
                current_debt_pmt = debt_expense
                # st.write(f'{freq}, you will repay in total ${round(current_debt_pmt+contribution, 2)}')
                which_loan = st.selectbox('Contribute for which loan?', options=[l.name for l in floans])
                lump_sum = st.number_input('Lump sum payment?')
                for fl in floans:
                    if which_loan==fl.name:
                        current_pmt = fl.pmt()
                        fl.extra_pmt = convert_frequency(contribution, freq, target_frequency=fl.frequency)
                        st.markdown(f'Your are contributing {freq} an **extra ${(round(contribution, 2))}** for loan {fl.name}')
                        st.write(f'Total payment for {fl.name}: **${round(fl.pmt(), 2)} {fl.frequency}**')
                        
                        #Add lump sum
                        fl.lump_sum(amt=lump_sum, period=fl.curr_period+1)

                        # with st.expander('See breakdown of Debt Repayment'):
                        #Plot debt payoff graph
                        plot_debt_repayment(fixed_loan=fl)
        


        if (inv_percentage or debt_percentage) and yrs:
            inv_save = inv_percentage*save
            liabilities_tl, cash_flow_change = liabilities_timeline(floans, yrs)
            assets_tl = assets_timeline(cars, home=None, 
                                    ini_cash=3000,
                                    save=inv_save, freq=freq, 
                                    years_projection=yrs, 
                                    inflation=True,
                                    cash_flow_change=cash_flow_change)
            # st.write(liabilities_tl)
            # st.write(assets_tl)
            # st.write(floans[2])


            net_worth = pd.concat([assets_tl, liabilities_tl], axis=1).sort_index()
            #GOTTA FIX YEARLY DAYS DO NOT MATCH MONTHLY/BIWEEKLY DAYS (INDEX)
            net_worth = net_worth.dropna()
            net_worth['net_worth'] = net_worth['total_asset'] - net_worth['total_liability']
            # st.write(net_worth)
            
            # Plot net worth
            plot_net_worth(net_worth)
            st.dataframe(net_worth)

            net_worth_avg_growth = net_worth['net_worth'].diff().mean() 
            st.write(f'Average Net worth growth {net_worth_avg_growth} {freq}.')

        # st.write(floans[2].pmt())
        # st.dataframe(floans[2].payment_schedule())

        # floans[2].extra_pmt = contribution
        # floans[2].extra_pmt = contribution
        # st.write(floans[2].pmt())
        # st.dataframe(floans[2].payment_schedule())



    







































