import datetime
import datetime as dt
from dateutil.relativedelta import relativedelta

"""Code for financial event predicted"""
class fin_event(object):
    
    def __init__(self, model, date, model_name, model_number=None, period_n=0):
        self._model = model
        self.date = date 
        self.model_name = model_name
#         self.delta_balance = delta_balance
        self.model_number = model_number
        self.period_n = period_n
    
    def get_next_fin_event(self):
        return self._model.get_next_fin_event()
    
    def apply_fin_event(self):
        self._model.accru(self)
    
    def set_model_number(self, mn):
        self.model_number = mn
    
    def __eq__(self, other_fin_event):
        if not isinstance(other_fin_event,fin_event):
            raise exception("__eq__ of fin_event is only used for comparison with other fin_events ")
        return self.date == other_fin_event.date
    
    def __gt__(self, other_fin_event):
        if not isinstance(other_fin_event,fin_event):
            raise exception("__eq__ of fin_event is only used for comparison with other fin_events ")
        return self.date > other_fin_event.date
    
    def get_model_number(self):
        return self.model_number
    
    def get_model_name(self):
        return self.model_name
    
    def get_date(self):
        return self.date
    
# """There are two account types, abstact account"""
# class fin_holding(object):
#     """This is used to model any account, credit card, bank, morgage, or mutural fund"""
#     unapplied_events = deque([])
    
#     def  __init__(self, percentage_interest, time_period_interest, starting_time, starting_amount=0.0, model_name=None):
#         self.pi = percentage_interest
#         self.tpi = time_period_interest
#         self.balance = starting_amount
#         self.date = starting_time
#         self.model_name = model_name
    
#     def get_name(self):
#         return self.model_name
    
#     def get_balance(self):
#         return self.balance
    
#     def __add__(self, other):
#         return self.balance+other.balance 
    
#     def __iadd__(self, other):
#         self.balance += other.balance
    
#     def __isub__(self, other):
#         self.balance -= other.balance
    
#     def __sub__(self, other):
#         return self.balance-other.balance
    
#     def get_next_fin_event(self):
#         event = [fin_event(self, self.date, self.model_name)]
#         self.unapplied_events.append(event)
#         self.date += self.tpi
#         return event
    
#     def accru(self, fin_event):
#         if len(self.unapplied_events) <= 0:
#             raise exception("No events to accru in " + self.model_name + " number ")
#         if self.unapplied_events[0] is not fin_event:
#             raise exception("Event passed to accru is not the next expected event")
#         event = self.unapplied_events.popleft()
        
#         """Currently every fin_holding works the same, and applies interest to whatever balance it has as the time of expect interest
#         even if money was only recently moving into the account and should not have interest on it
#         -Also there should potentially be different rules for different fin_holdings"""
#         self.balance *= (1+pi)
