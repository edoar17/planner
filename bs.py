import numpy as np
import numpy_financial as npf
from funs.funs import n_frequency
import pandas as pd


class Asset():
    def __init__(self, name, value) -> None:
        self.name = name
        self.value = value

    def __repr__(self):
        out = f"Asset('{self.name}', {self.value})"
        return out
    
    def depreciate(self, salvage, years):
        yearly_dep = (self.value-salvage)/years
        period = []
        value = []
        for i in range(0, years+1):
            period.append(i)
            value.append(i*yearly_dep)
        
        df = pd.DataFrame({'period': period,
                           'value': value})
        return df


class Car(Asset):
    def __init__(self, name, value, salvage, useful_years) -> None:
        super().__init__(name, value)
        self.salvage = salvage
        self.useful_years = useful_years

    def __repr__(self):
        return f"Car('{self.name}', {self.value}, {self.salvage}, {self.useful_years})"

    def depreciate(self, frequency, timeline_periods):
        """
        Return despreciation of asset indexed by period
        """
        #Depreciation per period
        periods = n_frequency(frequency)*self.useful_years
        freq_dep = (self.value-self.salvage)/periods
        #Return dataframe
        period_column = np.arange(0, periods, 1)  
        value_column = [self.value-freq_dep*p for p in range(0, periods)] 
        if timeline_periods > periods:
            period_column = np.arange(0, timeline_periods, 1)
            value_column = value_column + [self.salvage for i in range(periods, timeline_periods)]
        
        out = pd.DataFrame({'period': period_column,
                            'value': value_column})
        return out



class Liability():
    def __init__(self, name, total_amount, frequency) -> None:
        self.name = name
        self.total_amount = total_amount
        self.frequency = frequency


class FixedLoan(Liability):

    def __init__(self, name, total_amount, frequency, rate, term, curr_period) -> None:
        super().__init__(name, total_amount, frequency)
        self.rate = rate
        self.term = term
        self.curr_period = curr_period
        self.extra_pmt = None
        self.lumps = {}

    def __repr__(self):
        out = f"FixedLoan('{self.name}', {self.total_amount}, {self.frequency}, {self.rate}, {self.term}, {self.curr_period})"
        return out

    def pmt(self):
        n = n_frequency(self.frequency)
        rate = self.rate/n
        periods = n*self.term
        pmtn = (self.total_amount*rate)
        pmtd = 1 - (1/((1+rate)**periods))
        pmt = pmtn/pmtd
        if self.extra_pmt:
            pmt = pmt + self.extra_pmt
        return pmt

    def ipmt(self, period):
        n = n_frequency(self.frequency)
        periods = n*self.term
        rate = self.rate/n
        ipmt = npf.ipmt(rate=rate, per=period+1, nper=periods, pv=self.total_amount)
        return -ipmt
    
    def ppmt(self, period):
        n = n_frequency(self.frequency)
        periods = n*self.term
        rate = self.rate/n
        ppmt = npf.ppmt(rate=rate, per=period+1, nper=periods, pv=self.total_amount)
        return -ppmt

    def curr_balance(self):
        schedule = self.payment_schedule(at_current_period=True, extra_pmt_current_period=False, use_extra_pmt=False)
        #Get today's balance
        balance = schedule['starting_balance'].values[0]
        return balance

    def _vanilla_schedule(self):
        n = n_frequency(self.frequency)
        periods = n*self.term
        periods_range = range(0, periods)
        ipmts = [self.ipmt(i) for i in range(periods)]
        ppmts = [self.ppmt(i) for i in range(periods)]
        final_bal = [round(self.total_amount - np.cumsum(ppmts)[i], 6) for i in range(periods)]
        start_bal = [final_bal[i] + ppmts[i] for i in range(periods)]
        data = {'period': periods_range,
                'starting_balance': start_bal, 
                'principal': ppmts,
                'interest': ipmts,
                'final_balance': final_bal}
        df = pd.DataFrame(data)
        return df

    def _row_payment_schedule(self, pmt, start_period, end_period, starting_balance, lump_sums):
        """
        Generate schedule with for loop
        """
        n = n_frequency(self.frequency)
        total_periods = end_period - start_period
        rate = self.rate/n
        # st.write('aqui taa', self.lumps.keys(), self.lumps[150])

        # First row of schedule
        ipmts = [starting_balance*rate]
        ppmts = [pmt-ipmts[0]]
        if 0 in self.lumps and lump_sums:
            ppmts[0] = ppmts[0] + self.lumps['0']
        start_bal = [starting_balance]
        final_bal = [starting_balance - ppmts[0]]

        for i in range(1, total_periods+1):
            start_bal.append(final_bal[i-1])
            ipmt = start_bal[i]*rate
            ipmts.append(ipmt)
            
            ppmt = pmt - ipmts[i]
            
            # st.write(self.lumps)
            lump_period = start_period + i
            if lump_period in self.lumps and lump_sums:
                ext = self.lumps[lump_period]
                # st.write(ext)
                ppmt = ppmt + ext
                

            # If final pmt
            if start_bal[i] < ppmt: 
                ppmts.append(start_bal[i])    
                final_bal.append(start_bal[i]-ppmts[i])
                #End periods
                periods_range = range(start_period+1, i+start_period+2)
                break
            else:
                ppmts.append(ppmt)
                final_bal.append(start_bal[i]-ppmts[i])
                periods_range = range(start_period+1, end_period)


        data = {'period': periods_range,
                'starting_balance': start_bal, 
                'principal': ppmts,
                'interest': ipmts,
                'final_balance': final_bal}
        df = pd.DataFrame(data)
        return df
    

    #Add a lump sum pmt
    def lump_sum(self, amt, period):
        if period in self.lumps:
            self.lumps[period] += amt
        else:
            self.lumps[period] = amt
            

    def payment_schedule(self, at_current_period=False, use_extra_pmt=True, extra_pmt_current_period=True, lump_sums=True):
        """
        at_current_period, returns schedule beginning with current period

        use_extra_pmt, Use an extra pmt. If False use regular annuity formula
        
        extra_pmt_current_period, assumes extra payments start FROM current period. periods before are regular payments 
        
        lump_sums, if True adds one time principal pmt at lump periods
        """
        n = n_frequency(self.frequency)
        total_periods = n*self.term
        pmt = self.pmt()
        # st.write(pmt)
        
        if not use_extra_pmt:
            # Vanilla schedule with no extra payments
            schedule = self._vanilla_schedule()
        
        elif use_extra_pmt:            
            if extra_pmt_current_period:
                #Start paying extra FROM current period
                vanilla = self._vanilla_schedule()
                # Get final balance at current period
                vanilla = vanilla[vanilla['period']<=self.curr_period]
                vanilla_last_bal = vanilla['final_balance'].values[-1]
                #Continue schedule with extra payments
                extra_schedule = self._row_payment_schedule(pmt=pmt,
                                                            start_period=self.curr_period,
                                                            end_period=total_periods,
                                                            starting_balance=vanilla_last_bal,
                                                            lump_sums=lump_sums)
                #Join both schedules
                schedule = pd.concat([vanilla, extra_schedule], axis=0, ignore_index=True)

            else:
                #All periods with extra payment
                schedule = self._row_payment_schedule(pmt=pmt,
                                                      start_period=0,
                                                      end_period=total_periods,
                                                      starting_balance=self.total_amount,
                                                      lump_sums=lump_sums)
        
    
        if at_current_period:
            schedule = schedule[schedule['period']>=self.curr_period]



        return schedule


class LineOfCredit(Liability):
    def __init__(self, name, total_amount, frequency, rate, curr_balance) -> None:
        """
        curr_balance: Current balance owing on which interets is calculated @ every period
        """
        super().__init__(name, total_amount, frequency)
        self.rate = rate
        self.curr_balance = curr_balance
        self.disbursments = []

    def __repr__(self) -> str:
        out = f"LineOfCredit('{self.name}', {self.total_amount}, '{self.frequency}', {self.rate}, {self.curr_balance})"
        return out

    def ipmt(self):
        rate = self.rate/n_frequency(self.frequency)
        return self.curr_balance * rate

    def borrow(self, amount):
        cupo = self.total_amount-self.curr_balance
        if cupo < amount:
            return ValueError('Cannot borrow over total amount')
        else:
            #Add to borrow history
            self.disbursments.append(amount)
            #Update balance
            self.curr_balance += amount

    def pay_principal(self, amount):
        #Calculate ipmt
        ipmt = self.ipmt()
        ppmt = amount + ipmt
        self.curr_balance = self.curr_balance - ppmt





def deductible_loan(fixed_loan):
    """
    https://www.investopedia.com/articles/mortgages-real-estate/08/tax-deductible-mortgage-canada.asp
    """
    
    # Get a LOC higher than mtg 
    pmt = fixed_loan.pmt()
    disbursements = fixed_loan.payment_schedule().query('period >= @fixed_loan.curr_period')['principal']

    #Total to borrow from LOC    
    loc_amount = disbursements.sum()






# fl = FixedLoan(name='car', total_amount=40000, 
#                frequency='Biweekly', rate=0.06, term=7, 
#                curr_period=20)

# deductible_loan(fl)




# aa = LineOfCredit(10000, 'Monthly', 0.07, 5000)






# aa = Liability('loan', 20000, 0.06, 5, 'Monthly')
# bb = aa.payment_schedule()
# print(eval(repr(aa)))
# print(repr(aa))







