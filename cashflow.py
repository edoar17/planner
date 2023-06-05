import streamlit as st
from funs.funs import frequencies

class CashFlow():
    """
    This is the parent class of all incomes.
    """
    def __init__(self, name, amount=None, frequency=None, inc_or_exp=None) -> None:
        self.name = name
        self.amount = amount
        self.frequency = frequency
        self.type = inc_or_exp

    def get_input(self):
        col1, col2 = st.columns(2)
        amount = col1.number_input(f"Enter your {self.name} amount:", value=0.0, step=0.01)
        frequency = col2.radio(f"{self.name} frequency", options=frequencies) 
        self.amount = amount
        self.frequency = frequency
        return self

