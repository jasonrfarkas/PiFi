# PiFi
Personal Finance Modeling

The purpose of this project is to enable complex personal financial modeling senarios. 
To get it running ```pip install jupyter-notebook```
Navigate to Personal_Finances.ipynb and modify the code as needed to model your own financial future.

The backbone behind this code is a model generator that uses a list of Financial Causes to generate Financial Events.
It will walk through these events, and use the financial causes to generate more events, until a given end date. 
It will produce a pandas dataframe with all important dates and all account balances on those dates.

Financial Causes have a very flexable structure for defining how they should be treated over time. 
A financial cause can be anywhere from a Bank Account or Credit Card to a Salary (that changes over time), to a tax calculation, to a one time life event. 
Each Financial cause has a cost structure - a list of rules for how financial events should be generated from this Financial cause (within a specified time period, or number of repitions)
So one financial cause can naturally change over time. (This is useful for expressing cases of children who cause a different financial amount over time)
In order to represent various concepts, a financial cause can have both a balance and/or a cost. Balance changes over time via a balance function, while cost changes via the cost structure.

Financial causes can also interact with one other such that they can naturally transfer over thier balances from one account to another.
