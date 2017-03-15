"""
The goal of this notebook  (backend) is to be able to forcast and model various budgeting senarios. 

I should be able to see with a min and max on all of the following. 

Salary. 
Debt.
expected Cost per unit of time (at a future time)
Cumilative costs
Total Savings per day
Cumilative Savings

Cost of 
Net Worth.


----

salary is assumed to go up by a certain percentage of a previous salary every period until salary maxes out. 
to model this one way is to make a generator that does the calculation and place the data in a pd df with a dt index
when doing calculations with salary at arbitrary dates I need to do an an outer join then fill foward then potentially fil backwards and then grab only the dates in the desired dt_index

In order to do income calcuations, the salary needs to be divided per number of pay periods until the next salary increase and then each period between needs to get that value


-----
In order to generate the dataframe appropriarely I plan to have one generatator called the model generator which is used to make the dataframe, 
this model generator takes the parameters for all submodels. 

It has at least a single instance of each important submodel. 
Then it has a DS, lets say a heap of date-> [ [monitary_events], [sub_gen_number]] .
every itteration of the generator it pops the top dateTime off the top and refreshes whichever model numbers were used
it then yields what it popped off as a dictionary. 



"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Local imports
from .finModelGen import *



# ----------- old code -------
# default_model_end_date=datetime.datetime(2027, 6, 19, 0, 0)
# def salary_gen(start_date, start_salary, time_till_raise, percentage_raise, max_salary=float("inf"), retire_date=None):
#     current_date = start_date
#     current_salary = start_salary
#     while current_salary < max_salary and (retire_date is None or start_date < retire_date):
#         yield current_date, current_salary
#         current_date += time_till_raise
#         current_salary *= (1+percentage_raise)
#     while retire_date is None or start_date < retire_date:
#         yield current_date, max_salary
#         current_date += time_till_raise
#     while True:
#         yield current_date, 0.0
#         current_date += time_till_raise

# def income_gen(first_payment_date, starting_yearly_salary, time_till_raise, percentage_raise, max_salary=float("inf"), model_end_date=default_model_end_date, retire_date=None, increments="biMonthly"):
#     if increments is not "biMonthly":
#         raise ValueError('increments has not been programmed for anything not biMonthly')
#     current_date = first_payment_date
#     onFirst = True if current_date.day == 1 else False
#     current_salary = starting_yearly_salary 
#     next_raise_date = current_date+time_till_raise
# #   TODO: CALCULATE HOW TAX IS TAKEN OFF AND OR PUT BACK ON AFTERWORDS
#     bioMonthly_salary = current_salary/24
    
#     while current_salary < max_salary and (retire_date is None or current_date < retire_date) and current_date < model_end_date :
#         yield current_date, bioMonthly_salary
#         current_date += (relativedelta(months=1)-relativedelta(days=14)) if not onFirst else relativedelta(days=14)
#         onFirst = not onFirst
#         if current_date > next_raise_date:
#             current_salary *= (1+percentage_raise)
#             bioMonthly_salary = current_salary/24
#             next_raise_date += time_till_raise
        
#     while retire_date is None or current_date < retire_date and current_date < model_end_date:
#         bioMonthly_salary = max_salary/24
#         yield current_date, bioMonthly_salary
#         current_date += (relativedelta(months=1)-relativedelta(days=14)) if not onFirst else relativedelta(days=14)
#     while current_date < model_end_date:
#         yield current_date, 0.0
#         current_date += (relativedelta(months=1)-relativedelta(days=14)) if not onFirst else relativedelta(days=14)

# def df_income_gen(first_payment_date, starting_yearly_salary, time_till_raise, percentage_raise, max_salary=float("inf"), model_end_date=default_model_end_date, retire_date=None, increments="biMonthly"):
#     gen = income_gen(first_payment_date, starting_yearly_salary, time_till_raise, percentage_raise, max_salary, model_end_date, retire_date, increments)
#     for d, i in gen:
#         yield OrderedDict([('Index', d), ('Income', i)])
                           
# #         yield OrderedDict([('Index',start_date),
# #                            ('Period', p),
# #                            ('Begin Balance', beg_balance),
# #                            ('Payment', pmt),
# #                            ('Principal', principal),
# #                            ('Interest', interest),
# #                            ('Additional_Payment', addl_principal),
# #                            ('End Balance', end_balance)])




