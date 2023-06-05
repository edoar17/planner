# Income is divided in wages and savings.
# Assume savings can be invested in a risk-free rate savings account.

# Global variables
RF = 0.05
YEARS = 7
inflation = 0.06






# Assets
cash = 3000
investments = 1000
# car
car = 30000
years_to_use = 7
salvage_value = 7000
def car_value(initial_price, years_to_use, salvage_value, discount_rate):
    annual_depreciation = (car-salvage_value)/years_to_use
    remaining_value = []
    discounted_value = []
    for year in range(1, years_to_use+1):
        value = initial_price - (year * annual_depreciation)
        remaining_value.append(value)
        discounted = value / (1 + discount_rate) ** year
        discounted_value.append(discounted)
    return remaining_value, discounted_value
# remaining_value, discounted_value = car_value(initial_price=car, discount_rate=RF, salvage_value=salvage_value, years_to_use=years_to_use)
# for year in range(1, years_to_use + 1):
#     print(f"Year {year}: Remaining value: ${remaining_value[year-1]:,.2f}, Discounted value: ${discounted_value[year-1]:,.2f}")

#investments
def investments_value(initial_investments, years, risk_free):
    investments = {}
    for year in range(1, years+1):
        investments[year] = initial_investments*(1+risk_free)**year
    return investments

#cash
def cash_value(initial_cash, years, inflation):
    cash = {}
    for year in range(1, years+1):
        cash[year] = initial_cash*(1-inflation)**year
    return cash




