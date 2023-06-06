
"""All useful lists, functions, etc."""

import json
import numpy as np
import pandas as pd
import streamlit as st
import numpy_financial as npf

income_list = ['wages']
expense_list = ['housing', 'car', 'food', 'gas', 'car insurance', 'parking', 'phone', 'gym', 'other insurance', 'student loan']
assets_list = ['car', 'cash']
liabilities_list = ['car', 'credit card', 'student loan']
frequencies = ['Weekly', 'Biweekly', 'Monthly', 'Yearly'] 


financial_goals = ['debt repayment', 'max savings']

savings_funds = ['Vacation Fund', 'Health Fund', 'Education Fund', 'Emergency Fund', 'Fast debt repayment']



def n_frequency(frequency):
    if frequency=='Weekly':
        n = 52
    elif frequency=='Biweekly':
        n = 26
    elif frequency=='Monthly':
        n = 12
    elif frequency=='Yearly':
        n = 1
    return n

def days_frequency(frequency):
    if frequency=='Weekly':
        n = 7
    elif frequency=='Biweekly':
        n = 14
    elif frequency=='Monthly':
        n = 30
    elif frequency=='Yearly':
        n = 365
    return n
    

def color_balance_sheet(df):
    green = ['background-color: rgba(0, 128, 0, 0.25)']
    red = ['background-color: rgba(255, 0, 0, 0.25)']
    return green*len(df) if df['type']=='asset' else red*len(df)
def color_income_statement(df):
    green = ['background-color: rgba(0, 128, 0, 0.25)']
    red = ['background-color: rgba(255, 0, 0, 0.25)']
    return green*len(df) if df['type']=='income' else red*len(df)


def continuous_investing(initial_investment, annualized_return, contribution, frequency, time_horizon_years=1) -> list:
    """
    Returns the value of the investment per period in a python list
    Compounds interest per frequency
    """
    #nper per year
    n = n_frequency(frequency)
    period_rate = (1 + annualized_return)**(1/n) - 1
    periods = n*time_horizon_years

    # Calculate compounded value
    contributions = np.full(periods+1, contribution)
    contributions[0] = initial_investment #Add initial investment

    
    if not initial_investment:
        periodic_values = [-npf.fv(rate=period_rate, nper=p, pmt=contribution, pv=0, when=1) for p in range(periods+1)]
        
    elif initial_investment:    
        periodic_values = [contributions[0]]
        for i in range(1, len(contributions)+1):
            new_value = (periodic_values[i-1] + contribution)*(1+period_rate)
            periodic_values.append(new_value)
        # st.write(compounded_returns)
        # st.write(periodic_values)
        # st.write(periodic_total_values)

    return periodic_values


def save_profile(profile, path):
    with open(path, 'w') as f:
        json.dump(profile, f)

def load_profile(file):
    profile = json.load(file)
    return profile



def liabilities_timeline(floans, years_projection):
    """
    Timeline of the balances of liabilities in one dataframe. 
    Due to different frequencies, all liabilities are indexed by # of days
    """    
    total_days = 365*years_projection+1
    # To
    dfs = []
    cash_flow_change = []

    # Fixed loans
    for fl in floans:
        fl = eval(fl)
        freq = fl.frequency
        #freq converted to days
        timeline_days = np.arange(0, total_days, days_frequency(freq))
        periods = len(timeline_days)
        #Balances starting from current period
        balances = fl.payment_schedule(at_current_period=True, 
                                       use_extra_pmt=True, 
                                       extra_pmt_current_period=True)
        balances = balances['starting_balance'].head(periods)

        if len(balances) < periods:
            #Append extra income when finish debt pmts
            cash_flow = {'name': fl.name,
                'after_days': timeline_days[len(balances)],
                'extra_save': fl.pmt(),
                'freq': fl.frequency}
            cash_flow_change.append(cash_flow)
            # If loan is paid off before end of projection, set balance to zero.
            how_many = periods - len(balances)
            to_append = pd.Series(np.linspace(0, 0, how_many))
            #Append zero balances at the end 
            balances = pd.concat([balances, to_append], axis=0)
            

        timeline = pd.DataFrame({'day': timeline_days,
                                f'{fl.name} balance': balances})
        timeline = timeline.set_index('day')
        dfs.append(timeline)

    df = pd.concat(dfs,axis=1).sort_index()
    #Fill nas with previous balance.
    df = df.fillna(method='ffill')
    #Sum total liability
    df['total_liability'] = df.sum(axis=1)
    return df, cash_flow_change


def assets_timeline(cars, home, ini_cash, save, freq, years_projection, inflation, cash_flow_change):
    """
    Timeline of the balances of assets. 
    Depreciate / Appreciate all assets with the same frequency
    
    cars: list of Car
    save: Extra cash saved per frequency

    """    
    total_days = 365*years_projection+1
    timeline_days = np.arange(0, total_days, days_frequency(freq))
    inflation_rate = 0.05
    inflation_rate_freq = inflation_rate/n_frequency(freq)
    periods = len(timeline_days)

    # Depreciating assets
    # Car
    depre = []
    for car in cars:
        df_dep = car.depreciate(frequency=freq, timeline_periods=periods)
        df_dep['day'] = df_dep['period']*days_frequency(freq)
        df_dep = df_dep.rename(columns={'value': f'{car.name}_value'})
        df_dep = df_dep.set_index('day')
        depre.append(df_dep)

    # Cash (inflation)
    cash_dep = pd.DataFrame({'day': timeline_days,
                             'cash_value': save})
    # Initial cash 
    cash_dep['cash_value'].iloc[0] = save+ini_cash

    #Add income from debts paid off
    for i in cash_flow_change:
        after_day = i['after_days']
        extra_save = i['extra_save']
        save_freq = i['freq']
        #Conver cash flow desired freq
        extra_save = convert_frequency(extra_save, save_freq, target_frequency=freq)
        #Add to DF
        mask = (cash_dep['day']>=after_day)
        cash_dep.loc[mask, 'cash_value'] = cash_dep.loc[mask, 'cash_value'] + extra_save
        
    cash_dep['cash_value'] = cash_dep['cash_value'].cumsum()

    cash_dep = cash_dep.set_index('day')
    depre.append(cash_dep)

    # DF of all depreciating assets
    df = pd.concat(depre, axis=1)
    #Apply inflation
    if inflation:   
        df['cash_value'] = ((df['cash_value']-save)*((1-inflation_rate_freq)**df['period']))+save

    # Appeciating assets
    # Home, Investment accounts
    ### Empty for now ###

    # Total value fo assets
    df['total_asset'] = df.sum(axis=1)
    df = df.head(periods)
    return df


def generate_new_key(name, key_list):
    if len(key_list) == 0:
        key_name = f'{name}_0'
        # key_list.append(key_name)
        return key_name 
    else:
        i = len(key_list)
        key_name = f'{name}_{i}'
        # key_list.append(key_name)
        return key_name
    




def convert_frequency(amount, frequency, target_frequency):
    """
    Converts any amount-frequency pair to a normal monthly, yearly, or biweekly frequency.
    """
    if target_frequency == 'Weekly':
        if frequency == "Weekly":
            return amount
        if frequency == "Biweekly":
            return amount / 2
        elif frequency == "Monthly":
            return amount * 12 / 52    
        elif frequency == "Yearly":
            return amount / 52
        
    elif target_frequency == "Biweekly":
        if frequency == "Weekly":
            return amount * 2
        elif frequency == "Biweekly":
            return amount
        elif frequency == "Monthly":
            return amount * 12 / 26
        elif frequency == "Yearly":
            return amount / 26
        
    elif target_frequency == "Monthly":
        if frequency == "Weekly":
            return amount * 52 / 12
        elif frequency == "Biweekly":
            return amount * 26 / 12
        elif frequency == "Monthly":
            return amount
        elif frequency == "Yearly":
            return amount / 12
        

    elif target_frequency == "Yearly":
        if frequency == "Weekly":
            return amount * 52
        elif frequency == "Biweekly":
            return amount * 26
        elif frequency == "Monthly":
            return amount * 12
        elif frequency == "Yearly":
            return amount
    else:
        raise ValueError("Invalid target frequency specified.")
    

def good_print(amt):
    out = round(amt, 2)
    out = '$' + str(out)
    return out