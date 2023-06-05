import streamlit as st
from .funs import frequencies
import pandas as pd
from bs import Liability

"""All forms for my streamlit app"""


#Loan form
def fixedloan_form(on_click):
    form = st.form(key='loan_form', clear_on_submit=True)     
    with form:
        st.markdown('#### Fixed Loan')
        st.write('The interest expense will be transferred to the income statement automatically.')
        row = st.columns(2)
        with row[0]:
            st.text_input('What is loan for?', key='floan_name')
        with row[1]:
            st.number_input('Starting balance', key='floan_total_amount')
        row2 = st.columns(4)
        with row2[0]:
            st.number_input('Rate (in %)' , key='floan_rate', min_value=0.00, max_value=100.00, step=0.01)
        with row2[1]:
            st.number_input('Term', key='floan_term', max_value=35)
        with row2[2]:
            st.number_input('What period are you in?', key='floan_current_period', min_value=1, step=1)
        with row2[3]:
            st.radio('Frequency', options=frequencies, key='floan_frequency')
        st.form_submit_button(label='Add Fixed Loan', on_click=on_click)

#LOC form
def loc_form(on_click):
    form = st.form(key='loc_form', clear_on_submit=True)     
    with form:
        st.markdown('#### Line of Credit')
        row = st.columns(2)
        with row[0]:
            st.text_input('What is line of credit for?', key='loc_name')
        with row[1]:
            st.number_input('Borrowing limit', key='loc_limit')
        row2 = st.columns(3)
        with row2[0]:
            st.number_input('Rate (in %)' , key='loc_rate', min_value=0.00, max_value=100.00, step=0.01)
        with row2[1]:
            st.number_input('What is the current balance?', key='loc_balance', min_value=0.00)
        with row2[2]:
            st.radio('Frequency', options=frequencies, key='loc_frequency')
        st.form_submit_button(label='Add Line of Credit', on_click=on_click)


def car_form(on_click):
    form = st.form(key='car_form', clear_on_submit=True)     
    with form:
        st.markdown('#### Car')
        st.write('The car asset will automatically depreciate linearly.')
        row = st.columns(2)
        with row[0]:
            st.text_input('Car name', key='car_name')
        with row[1]:
            st.number_input('Car price', key='car_price')
        row2 = st.columns(2)
        with row2[0]:
            st.number_input('Useful years' , key='car_life', min_value=0)
        with row2[1]:
            st.number_input('Salvage Value', key='car_salvage', min_value=0)
        st.form_submit_button(label='Add Car Asset', on_click=on_click)

def asset_form(on_click):
    asset_form = st.form(key='asset_form', clear_on_submit=True)
    with asset_form:
        form_columns = st.columns(2)
        with form_columns[0]:
            st.text_input('Asset', key='asset_name')
        with form_columns[1]:
            st.number_input('Value', key='asset_amount')
        st.form_submit_button(label='Add Asset', on_click=on_click)


def liability_form(on_click):
    liability_form = st.form(key='liability_form', clear_on_submit=True)
    with liability_form:
        form_columns = st.columns(2)
        with form_columns[0]:
            st.text_input('Liability', key='liability_name')
        with form_columns[1]:
            st.number_input('Value', key='liability_amount')
        st.form_submit_button(label='Add Liability', on_click=on_click)

def income_form(on_click):
    income_form = st.form(key='income_form', clear_on_submit=True)
    with income_form:
        form_columns = st.columns(3)
        with form_columns[0]:
            st.text_input('Income', key='income_name')
        with form_columns[1]:
            st.number_input('Amount', key='income_amount')
        with form_columns[2]:
            st.selectbox('Frequency', options=frequencies, key='income_frequency')
        st.form_submit_button(label='Add Income', on_click=on_click)


def expense_form(on_click):    
    expense_form = st.form(key='expense_form', clear_on_submit=True)
    with expense_form:
        form_columns = st.columns(3)
        with form_columns[0]:
            st.text_input('Expense', key='expense_name')
        with form_columns[1]:
            st.number_input('Amount', key='expense_amount')
        with form_columns[2]:
            st.selectbox('Frequency', options=frequencies,key='expense_frequency')
        st.form_submit_button(label='Add Expense', on_click=on_click)
