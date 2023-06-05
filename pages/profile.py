"""
In this page the user will input all the information. It will be saved in a csv file to reuse later.

This will be their 'profile'. This way they could create multiple profiles/plans.
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import sys
sys.path.append("../")
from funs.funs import *
from funs.forms import *
from bs import Asset, Liability, LineOfCredit, FixedLoan, Car

#Session state variables
if 'assets' not in st.session_state:
    st.session_state['assets'] = pd.DataFrame(columns=['name', 'amount'])
if 'liabilities' not in st.session_state:
    st.session_state['liabilities'] = pd.DataFrame(columns=['name', 'amount'])
if 'incomes' not in st.session_state:
    st.session_state['incomes'] = pd.DataFrame(columns=['name', 'amount', 'frequency'])
if 'expenses' not in st.session_state:
    st.session_state['expenses'] = pd.DataFrame(columns=['name', 'amount', 'frequency'])
if 'floans' not in st.session_state:
    st.session_state['floans'] = []
if 'cars' not in st.session_state:
    st.session_state['cars'] = []
if 'locs' not in st.session_state:
    st.session_state['locs'] = []


# Add functions
def add_asset():
    asset_df = pd.DataFrame(data={'name': [st.session_state.asset_name], 
                            'amount': [st.session_state.asset_amount],
                            'type': 'asset'})
    st.session_state['assets'] = pd.concat([st.session_state['assets'], asset_df], axis=0)
def add_liability():
    liability_df = pd.DataFrame(data={'name': [st.session_state.liability_name], 
                            'amount': [st.session_state.liability_amount],
                            'type': 'liability'})
    st.session_state['liabilities'] = pd.concat([st.session_state['liabilities'], liability_df], axis=0)
def add_income():
    income_df = pd.DataFrame(data={'name': [st.session_state.income_name], 
                            'amount': [st.session_state.income_amount],
                            'frequency': [st.session_state.income_frequency],
                            'type': 'income'})
    st.session_state['incomes'] = pd.concat([st.session_state['incomes'], income_df], axis=0)
def add_expense():
    expense_df = pd.DataFrame(data={'name': [st.session_state.expense_name], 
                            'amount': [st.session_state.expense_amount],
                            'frequency': [st.session_state.expense_frequency],
                            'type': 'expense'})
    st.session_state['expenses'] = pd.concat([st.session_state['expenses'], expense_df], axis=0)
def add_car():
    car = Car(name=st.session_state['car_name'],
              value=st.session_state['car_price'],
              salvage=st.session_state['car_salvage'],
              useful_years=st.session_state['car_life'])
    st.session_state['cars'].append(repr(car))# = st.session_state['loans'] + [loan]
    #Add to assets
    asset_df = pd.DataFrame(data={'name': [st.session_state['car_name']], 
                            'amount': [st.session_state['car_price']]})
    st.session_state['assets'] = pd.concat([st.session_state['assets'], asset_df])

def add_fixedloan():
    floan = FixedLoan(name=st.session_state['floan_name'], 
                        total_amount=st.session_state['floan_total_amount'],
                        rate = st.session_state['floan_rate']/100,
                        term = st.session_state['floan_term'],
                        frequency=st.session_state['floan_frequency'],
                        curr_period=st.session_state['floan_current_period'])
    st.session_state['floans'].append(repr(floan))

    #Get current liability value
    amort = floan.payment_schedule()
    curr_balance = amort[amort['period']==floan.curr_period]['starting_balance'].values[0]
    liability_df = pd.DataFrame(data={'name': [floan.name], 
                            'amount': [curr_balance]})
    #Add to balance liabilities
    st.session_state['liabilities'] = pd.concat([st.session_state['liabilities'], liability_df], axis=0)

    #Add payments to expenses
    pmt = floan.pmt()
    expense_df = pd.DataFrame(data={'name': [st.session_state.floan_name + ' payment'], 
                            'amount': [pmt],
                            'frequency': [st.session_state.floan_frequency]})
    st.session_state['expenses'] = pd.concat([st.session_state['expenses'], expense_df], axis=0)

def add_lineofcredit():
    loc = LineOfCredit(name=st.session_state['loc_name'],
                       total_amount=st.session_state['loc_limit'],
                       rate=st.session_state['loc_rate'],
                       frequency=st.session_state['loc_frequency'],
                       curr_balance=st.session_state['loc_balance'])
    st.session_state['locs'].append(repr(loc))
    #Add to curr_balance to Liabilities
    liability_df = pd.DataFrame(data={'name': [loc.name], 
                            'amount': [loc.curr_balance]})
    #Add to balance liabilities
    st.session_state['liabilities'] = pd.concat([st.session_state['liabilities'], liability_df], axis=0)




st.header('Welcome!')
if st.file_uploader('Load Profile', key='load_profile'):
    load_file = st.session_state['load_profile'] 
    profile = load_profile(load_file)
    #Reload profile data
    user_name = profile['user_name']
    st.session_state.assets = pd.DataFrame.from_records(profile['assets'])
    st.session_state.liabilities = pd.DataFrame.from_records(profile['liabilities'])
    st.session_state.incomes = pd.DataFrame.from_records(profile['income'])
    st.session_state.expenses = pd.DataFrame.from_records(profile['expenses'])
    st.session_state.floans = [eval(x) for x in profile['floans']]
    st.session_state.cars = [eval(x) for x in profile['cars']]
    # st.session_state.locs = [eval(x) for x in profile['locs']]
else: 
    st.write('OR')
    user_name = st.text_input('Create new profile! Please enter your name', key='user_name')


if user_name:
    st.write(f"Hello {user_name}!")
    st.header('Balance Sheet')
    st.write("To start the financial analysis, we'll begin with the balance sheet")
    
    st.markdown("#### Assets")
    # Assets forms
    # if st.button('Add Home'):
    #     home_form(add_home)
    if st.button('Add car'):
        car_form(add_car)
    if st.button('Add other asset'):
        asset_form(add_asset)
    
    st.markdown("#### Liabilities")
    # Liabilities forms
    if st.button('Add fixed loan'):
        fixedloan_form(add_fixedloan)
    if st.button('Add line of credit'):
        loc_form(add_lineofcredit)
    if st.button('Add other liability'):
        liability_form(add_liability)


    assets = st.session_state.assets
    cars = st.session_state.cars
    liabilities = st.session_state.liabilities
    floans = st.session_state.floans
    locs = st.session_state.locs
    assets['type'] = 'asset'
    liabilities['type'] = 'liability'

    st.header('Income Statement')
    st.write("Note: income is only the periodic cash flows.")

    st.markdown("#### Income")
    if st.button('Add Income'):
        income_form(add_income)

    st.markdown("#### Expenses")
    if st.button('Add Expense'):
        expense_form(add_expense)


    income = st.session_state.incomes
    expenses = st.session_state.expenses
    income['type'] = 'income'
    expenses['type'] = 'expense'





    st.header('Statements')
    st.markdown("#### Your Balance Sheet")

    balance_sheet = pd.concat([assets,liabilities], axis=0).reset_index(drop=True)
    st.dataframe(balance_sheet.style.apply(color_balance_sheet, axis=1), width=700)
    st.markdown("#### Your Income Statement")
    income_statement = pd.concat([income, expenses], axis=0).reset_index(drop=True)
    st.dataframe(income_statement.style.apply(color_income_statement, axis=1), width=700)
    # st.dataframe(assets)
    # st.dataframe(liabilities)
    # st.dataframe(income)
    # st.dataframe(expenses)


    yrs = 10
    assets_tl = assets_timeline(ini_cash=4000, cars=cars, freq='Monthly', years_projection=yrs, home=None, save=500, inflation=True)
    liabilities_tl = liabilities_timeline(floans, years_projection=yrs)

    balance_sheet_tl = pd.concat([assets_tl['total_asset'], liabilities_tl['total_liability']], axis=1)
    balance_sheet_tl = balance_sheet_tl.sort_index()
    balance_sheet_tl['net_worth'] = balance_sheet_tl['total_asset'] - balance_sheet_tl['total_liability']
    balance_sheet_tl = balance_sheet_tl.dropna()
    st.write(balance_sheet_tl)

    fig, ax = plt.subplots()
    sns.lineplot(data=balance_sheet_tl, ax=ax)
    st.pyplot(fig)

    # fig, ax = plt.subplots(2,1)
    # sns.lineplot(data=assets_tl, ax=ax[0])
    # sns.lineplot(data=liabilities_tl, ax=ax[1])
    # st.pyplot(fig)









    profile = {}
    profile['user_name'] = user_name
    profile['assets'] = assets.to_dict(orient='records')
    profile['liabilities'] = liabilities.to_dict(orient='records')
    profile['income'] = income.to_dict(orient='records')
    profile['expenses'] = expenses.to_dict(orient='records')
    profile['locs'] = locs
    profile['floans'] = floans
    profile['cars'] = cars

    # Save user data to a JSON file
    if st.button("Save Profile"):
        save_profile(profile, path=f"profiles/{profile['user_name']}.json")
        st.success("Profile saved!")
        st.success("Now, go to the plan page and upload your file to build a financial plan!")

# # st.write(cash_flow_profile)








