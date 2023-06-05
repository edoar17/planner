import streamlit as st




st.header('Hello!')

st.write('')


explanation_md = """
The way this app works is that you enter your assets, liabilities to calculate your net worth.
Then you enter your cash flow incomes and expenses to get an income statement.


This will help you to assess what you could to with your net income (income-expenses). 
This app can also help you to improve your net worth. A positive net worth is good because it allows you to borrow more later on,
and to be prepared for emergencies.

To start the financial analysis, go to the profile page to build your profile.

Once you enter all the information you can start allocation your net income into multiple saving funds to accomplish your financial goals!

#### Net worth
The higher your net worth, the more potential stability you have during times of ecnonomic upheaval,
and the better positioned you are to take advantage of opportunities that come your way.
A positive net worth is important for several reasons:

- Financial stability: Having a positive net worth indicates that you have more assets than liabilities, which means you are in a financially stable position. This gives you a sense of security and helps you to weather financial storms, such as job loss or unexpected expenses.
- Investment opportunities: A positive net worth opens up opportunities for investment in various assets, such as stocks, real estate, and businesses. This can help you to grow your wealth over time.
- Creditworthiness: A positive net worth improves your creditworthiness, which means that lenders are more likely to approve you for loans or credit cards. This can help you to access credit when you need it and at better terms.
- Retirement planning: A positive net worth is an important factor in retirement planning. It indicates that you have accumulated enough wealth to support yourself in retirement and maintain your standard of living.

In summary, a positive net worth is an important financial indicator that can provide financial stability, open up investment opportunities, improve creditworthiness, and support retirement planning.


"""

st.markdown(explanation_md)