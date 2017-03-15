from .finEvent import *
import warnings
from numbers import Number
from collections import deque
from inspect import signature


def paramify(func):
    """This is to enable functions to take in any kwargs even if they don't have kwargs"""
    ## Makes it so the function can accept any kwargs and not throw an error if it the function did not expect those, 
    ## This way I can pass more to the function than it expects
    ## It makes **kwargs act like the set of normal key_word arguments that would work
    # If there are no positional only arguments or VAR_POSITIONAL arguments
    
    #TODO: There may be a use in argifying things as well, which would enable passing in as many positional arguments as desired and only having truly pass in the number of arguments it can accept, but that seems to just be asking for untraceable errors so I am shying away from it. If I did want to do it in the future I would need to make sure it doesn't conflict with kwargify so, if and only if there are no positional-only arguments, I can look backwards through the positional arguments to find which can be satisfied by keywords in kwargs, then pass in args sliced until the remaining number of unsatisfied postional arguments, this would be less potential errors in cases where it the function takes positional/keyword and the keyword is unsupplied but assumable via the position (and won't throw errors in cases where all the argument names can be assuemd, as it will be handled by kwargs), but in the case where this version of kwargify could not handle the function to begin with, and the positioning of the arguments is miss_assumed, confusing errors may occur and if may have been better to just tell the user of this module that we didn't expect to give them the argument that they desire. Of course this means it can't handle parameter only arguments, thus the ideal may be to handle it but pass with a warning  
    def new_func(*args, **kwargs):
        acceptable_parms = signature(func).parameters # Should act as a dict
        if "kwargs" not in acceptable_parms:
            new_kwargs = dict((k,v) for k,v in kwargs.items() if k in acceptable_parms and acceptable_parms[k].kind != acceptable_parms[k].POSITIONAL_ONLY)
        else:
            new_kwargs = kwargs
        return func(*args, **new_kwargs)
    return new_func


class limited_value(object):

    def __init__(self, starting_value=0.0, lower_limit=float("-inf"), upper_limit=float("inf"), violation_responce="corrected"):
        self.lower_limit = lower_limit
        self.upper_limit = upper_limit
        self.violation_responce = violation_responce
        if self.upper_limit < self.lower_limit:
            raise Exception("Upper limit must be GTE to lower limit")
        # self.set_value(starting_value)
        self._value = None
        self.value = starting_value

    @property
    def value(self):
        return self._value

    def valid_value(self, value):
        return self.lower_limit <= value and value <= self.upper_limit
    
    @value.setter     
    def value(self, value):
        # print ("trying to set value to ", value)
        if self.valid_value(value):
            self._value = value
        elif self.lower_limit > value:
            self._violated(value, self.lower_limit, "greater")
        elif self.upper_limit < value:
            self._violated(value, self.upper_limit, "less")
        else:
            raise Exception("Unexpected part of code reached...")

    def _violated(self, real, limit, direction):
        if self.violation_responce == "silenced":
            return
        elif self.violation_responce == "corrected":
            self.value = limit
        else:
            raise Exception("Limited_value Cannot be {}, it must be {} than or equal to {}".format(real, direction, limit)) 

    def transfer(self, other, amount):
        # print("trying to transfer ", amount )
        ## Transfers however much of the amount it can between two limited values, and returns the amount untransfered
        if isinstance(other, fin_cause):
            other = other._balance
        ## Cache current values and violation_responce

        # can_remove = valid_value(self.value-amount)
        # can_add = other.valid_value(other.value+amount)
        # if can_remove and can_add:
        #     self.value = self.value - amount
        #     other.value = other.value + amount
        #     return 0.0

        if amount > 0:
            # the amount this account can handle is based on the min value, so value-min  and
            this_value = self.value - self.lower_limit
            other_value = other.upper_limit - other.value
            transfer_min = min(this_value, other_value)
            transfer_amount = min(transfer_min, amount)

        if amount <= 0:
            # the amount the accound can add is based on max value-max
            this_value = self.value - self.upper_limit
            other_value = other.lower_limit - other.value  #upper_limit 
            transfer_max = max(this_value, other_value)
            transfer_amount = max(transfer_max, amount)

        self.value = self.value - transfer_amount
        other.value = other.value + transfer_amount
        transfered = amount-transfer_amount
        # pre_value = self.value
        # pre_value_2 = other.value
        # pre_violation_responce = self.violation_responce
        # pre_violation_responce2 = other.violation_responce
        # ## Set the violation_responces to correct the transfer
        # self.violation_responce = "corrected"
        # other.violation_responce = "corrected"
        # self.value = self.value - amount
        # other.value = other.value + amount
        # # check how much was transfered. 
        # t_1 = pre_value - self.value 
        # t_2 = other.value - pre_value_2 
        # transfered = min(abs(t_1), abs(t_2))
        # if t_1 != transfered:
        #     # print ("readding {} to self.value ".format(amount-transfered))
        #     self.value = self.value + amount- other.value - pre_value_2
        # elif t_2 != transfered:
        #     other.value = other.value - amount- self.value - pre_value
        # # Return the violation responces to their previous values
        # self.violation_responce = pre_violation_responce
        # other.violation_responce = pre_violation_responce2
        # print("in transfer {} succeeded in transfering {}, pre1: {}, pre2:{}, pos1:{}, pos2:{}, t1:{}, t2:{}".format(amount, transfered, pre_value, pre_value_2, self.value, other.value, t_1, t_2))
        return transfered

    def __iadd__(self, other):
        try:
            new_value = self.value + other.value
        except:
            try:
                new_value = self.value + other
            except e:
                raise e
        self.value = new_value
    
    def __isub__(self, other):
        try:
            new_value = self.value - other.value
        except:
            try:
                new_value = self.value - other
            except e:
                raise e
        self.value = new_value

    def __imul__(self, other):
        try:
            new_value = self.value * other.value
        except:
            try:
                new_value = self.value * other
            except e:
                raise e
        self.value = new_value

    def __idiv__(self, other):
        try:
            new_value = self.value / other.value
        except:
            try:
                new_value = self.value / other
            except e:
                raise e
        self.value = new_value

    def __ifloordiv__(self, other):
        try:
            new_value = self.value // other.value
        except:
            try:
                new_value = self.value // other
            except e:
                raise e
        self.value = new_value

    def __imod__(self, other):
        try:
            new_value = self.value % other.value
        except:
            try:
                new_value = self.value % other
            except e:
                raise e
        self.value = new_value

    def __ipow__(self, other):
        try:
            new_value = self.value ** other.value
        except:
            try:
                new_value = self.value ** other
            except e:
                raise e
        self.value = new_value

    def __ilshift__(self, other):
        try:
            new_value = self.value << other.value
        except:
            try:
                new_value = self.value << other
            except e:
                raise e
        self.value = new_value

    def __irshift__(self, other):
        try:
            new_value = self.value >> other.value
        except:
            try:
                new_value = self.value >> other
            except e:
                raise e
        self.value = new_value

    def __iand__(self, other):
        try:
            new_value = self.value & other.value
        except:
            try:
                new_value = self.value & other
            except e:
                raise e
        self.value = new_value

    def __ixor__(self, other):
        try:
            new_value = self.value ^ other.value
        except:
            try:
                new_value = self.value ^ other
            except e:
                raise e
        self.value = new_value
        
    def __ior__(self, other):
        try:
            new_value = self.value | other.value
        except:
            try:
                new_value = self.value | other
            except e:
                raise e
        self.value = new_value
   
    def __add__(self, other):
        try:
            return self.value + other.value
        except:
            try:
                return self.value + other
            except e:
                raise e
    
    def __sub__(self, other):
        try:
            return self.value - other.value
        except:
            try:
                return self.value - other
            except e:
                raise e

    def __mul__(self, other):
        try:
            return self.value * other.value
        except:
            try:
                return self.value * other
            except e:
                raise e

    def __floordiv__(self, other):
        try:
            return self.value // other.value
        except:
            try:
                return self.value // other
            except e:
                raise e
   
    def __div__(self, other):
        try:
            return self.value / other.value
        except:
            try:
                return self.value / other
            except e:
                raise e

    def __mod__(self, other):
        try:
            return self.value % other.value
        except:
            try:
                return self.value % other
            except e:
                raise e

    def __pow__(self, other):
        try:
            return self.value * other.value
        except:
            try:
                return self.value * other
            except e:
                raise e

    def __lshift__(self, other):
        try:
            return self.value << other.value
        except:
            try:
                return self.value << other
            except e:
                raise e

    def __rshift__(self, other):
        try:
            return self.value >> other.value
        except:
            try:
                return self.value >> other
            except e:
                raise e

    def __and__(self, other):
        try:
            return self.value & other.value
        except:
            try:
                return self.value & other
            except e:
                raise e

    def __xor__(self, other):
        try:
            return self.value ^ other.value
        except:
            try:
                return self.value ^ other
            except e:
                raise e

    def __or__(self, other):
        try:
            return self.value | other.value
        except:
            try:
                return self.value | other
            except e:
                raise e

    def __neg__(self):
        try:
            return -self.value
        except:
            raise e

    def __pos__(self):
        try:
            return +self.value
        except:
            raise e

    def __abs__(self):
        try:
            return abs(self.value)
        except:
            raise e

    def __invert__(self):
        try:
            return ~self.value
        except:
            raise e

    def __complex__(self):
        try:
            return complex(self.value)
        except:
            raise e

    def __int__(self):
        try:
            return int(self.value)
        except:
            raise e

    def __long__(self):
        try:
            return long(self.value)
        except:
            raise e

    def __float__(self):
        try:
            return float(self.value)
        except:
            raise e

    def __oct__(self):
        try:
            return oct(self.value)
        except:
            raise e

    def __hex__(self):
        try:
            return hex(self.value)
        except:
            raise e

    def __lt__(self, other):
        try:
            return self.value < other.value
        except:
            try:
                return self.value < other
            except e:
                raise e

    def __le__(self, other):
        try:
            return self.value <= other.value
        except:
            try:
                return self.value <= other
            except e:
                raise e

    def __eq__(self, other):
        try:
            return self.value == other.value
        except:
            try:
                return self.value == other
            except e:
                raise e
                
    def __ne__(self, other):
        try:
            return self.value != other.value
        except:
            try:
                return self.value != other
            except e:
                raise e

    def __ge__(self, other):
        try:
            return self.value >= other.value
        except:
            try:
                return self.value >= other
            except e:
                raise e

    def __gt__(self, other):
        try:
            return self.value > other.value
        except:
            try:
                return self.value > other
            except e:
                raise e                                                            


class fin_cause(object):
    """The class is used to model reoccuring (potentially disregular but dependant) cost or income structures
    For example it should be used to model salary, household expenses, car expenses...
    It keeps track of the balance (to do analysis on how much each cause effects), but it primarily places the 
    accrued balance into the connected account. 
    """
    
    
    """TO COMPLETE, BEST WAY TO MAKE THIS OBJECT SO IT HANDLES DISREGULARITY WELL"""
    # cost_structure looks like [(time period, cost_increase_function/new_cost, repitions/timeDelta/relativeTimeDelta/endDate)]
    """
    TODO: To make life much easier for the program, use
    from inspect import signature
    to inspect the cost_increase_function parameters and the like and include cost, balance, and time till repeat changes
    within the function, so each time period can have a truly flexable time/cost structure
    This could then be used for modeling any individual account/system of costs
    
    Then I want to make a decorator that handles transforming any function into a cost or balance function
    """
    #     def default_balance
    def  __init__(self, starting_time, linked_accounts=[], cost_structure=[
        ("time period till repeat", "cost_increase_function or new_cost",
         " # of repitions or timeDelta or relativeTimeDelta or endDate", "[accounts transfer functions]")], 
                  # Accounts transfer functions should take in: pre_disbersal_cost, after_disberal_cost, pre_disbersal_balance, after_disberal_balance, # aka before and after the money was transfered to other accounts during this update
        model_name=None, starting_amount=0.0, balance_function=lambda x:x, starting_cost=0.0, interest_start_date=None,
        min_balance=float("-inf"), max_balance=float("inf") ):
        self.unapplied_events = deque([])
        self.interest_start_date = interest_start_date
        self.min_balance = min_balance
        self.max_balance = max_balance
        self.more_events = True
        self.date = starting_time
        self._last_date = None
        self.cost = starting_cost
        self.period_n = 0
        self.start_period_n = 0
        self.cost_structures = cost_structure
        self.model_name = model_name
        self.set_period_date()
        self.set_period_details(0)   
        # self.__balance = limited_value(starting_amount, min_balance, max_balance)                                
        # self._balance = 
        self.balance = starting_amount
        self.balance_f = paramify(balance_function)#lambda *args, **kwargs : paramify(balance_function(*args, **kwargs))#lambda **kwargs: raise Exception
    #         paramify()
        self.balance_f_cost_total = 0.0
        self.accounts = linked_accounts
        
        
    #         self.intra_period_rounds = 0
    #         self.ttr = relativedelta(seconds=1)
    #         self.end_of_period = starting_time+relativedelta(seconds=1)
        
    def get_name(self):
        return self.model_name
    
    @property
    def balance(self):
        return self._balance.value

    @balance.setter
    def balance(self, x):
        # print("trying to set balance to ", x)
        self._balance = x
        # return self.balance
    
    @property
    def _balance(self):
        return self.__balance

    @_balance.setter
    def _balance(self, x):
        self.__balance = limited_value(x, self.min_balance, self.max_balance)

    @property 
    def ttr(self):  
        if self.date is not self._last_date:
            kwargs={"date":self.date}
            self._last_ttr = self.ttr_f(**kwargs)
            self._last_date = self.date
        return self._last_ttr

    @ttr.setter 
    def ttr(self, value):
        if not callable(value):
            a = value
            value = lambda : a
        self.ttr_f = paramify(value)

    def set_period_date(self):
    #         print( "setting period date for model {}".format(self.model_name))
        ## PERIOD DATE and TTR IS used by get_fin_events, and disconnected from the period used in the cost which is parameter based
        self.start_of_period = self.date
        self.start_period_n = self.period_n
        self.intra_period_rounds = 0    
        try:
            self.ttr, self.end_of_period =  self.cost_structures[self.period_n][0], self.cost_structures[self.period_n][2]
        except:
            print("ERROR: model ", self.model_name)
            print("ERROR: period_n", self.period_n)
            print("ERROR: self.cost_structures", self.cost_structures)
            raise exception("ERROR!!")
        self._valid_ttr()
        self._valid_end_of_period()

    
    def reset_period_date(self):
        self.set_period_date()
        self.period_n += 1
        if self.period_n >= len(self.cost_structures):
            self.more_events = False
     
    def set_period_details(self, period_n):
    #         for i,c in enumerate(self.cost_structures):
    #             print("c , ", i, " :", c[1])
        period_n = min(period_n, len(self.cost_structures)-1) ##TODO:: I need to confirm that the correct period is being passed on the correct dates. 
    #         print ("period_n is ", period_n, " out of ", len(self.cost_structures))
        self.cost_f, self.account_fs =  self.cost_structures[period_n][1], self.cost_structures[period_n][3] 
    #         print(" new? cost_f : ", self.cost_f)
        self._valid_cost_f()
        
        self._valid_account_fs()
    
    def _refresh_cost(self, **kwargs):
        ## TODO::
        other_info = {"account":self, "x": self.cost, "cost":self.cost, "previous_cost":self.cost, "pre_cost":self.cost}
    #         print("_refresh_cost self.cost_f is {}, self.cost_f(**other_info) is {}".format(self.cost_f, self.cost_f(**other_info)))
        kwargs.update(other_info)
        self.cost = self.cost_f(**kwargs)

    def _refresh_balance(self, **kwargs):
        if self.interest_start_date is None or kwargs["event_date"] >= self.interest_start_date:
            other_info = {"x":self.balance, "balance":self.balance, "pre_balance":self.balance, "previous_balance":self.balance}
            kwargs.update(other_info)
            old_balance = self.balance
    #         print("balance_f is {}".format(self.balance_f))
    #         print("new balance for model {} is {}".format(self.model_name, new_balance))
            self.balance = self.balance_f(**kwargs)
            self.balance_f_cost_total += self.balance - old_balance
             
    
    def _transfer_to_account(self, **kwargs):
        pre_disbersal_cost = self.cost
        pre_disbersal_balance = self.balance
        sum_transfer= 0.0
        for a, af in zip(self.accounts, self.account_fs):
            if af is not None:
    #                  pre_disbersal_cost, after_disberal_cost, pre_disbersal_balance, after_disberal_balance
                ##TODO: Add amount recieved on intrest of balance function
                other_info = {"x":self.balance, "previous_cost":self.cost, "pre_cost":self.cost, "cost":self.cost, "pre_balance":self.balance, "previous_balance":self.balance, "transfer_amount":sum_transfer,
                         "remaining_balance":self.balance, "account_to":a, "account_from":self
                        }
                kwargs.update(other_info)

                transfer_amount = af(**kwargs)
                transfer_amount2 = transfer_amount
                remaining = self._balance.transfer(a, transfer_amount)
                transfer_amount -= remaining
                sum_transfer += transfer_amount
                # print("Tried to transfer {} from {} to {} succeeded in transfering {}".format(transfer_amount2, self.model_name, a.model_name, transfer_amount))

                # transfer_amount = af(**kwargs)
                # self.old_balance
                # # 
                # self.balance -= transfer_amount
                # a += transfer_amount
        # print("value:{}, cost:{}, balance+cost:{}".format(self.balance, self.cost, self.balance+self.cost))
        self.balance += self.cost # self.balance+
    
    def get_next_fin_event(self):
    #         p = self.period_n
        p = self.period_n if self._period_past_over() else self.start_period_n
    #         print("\t making an event on {} with period_n {}".format(self.date,p ))
        event = fin_event(self, self.date, self.model_name, period_n=p)
    #         if self._period_over():
    #             event = fin_event(self, self.date, self.model_name, period_n=self.period_n)
        
        if (not self.more_events) and self._period_past_over(): # and (len(self.unapplied_events)==0 or event.date == self.unapplied_events[-1].date) # ((not len(self.unapplied_events)==0) and event.date == self.unapplied_events[-1].date))
    #             print("RETURNING NONE!! self.more_events: {},  len(self.unapplied_events): {}, event.date == self.unapplied_events[-1].date:{} ".format(self.more_events, len(self.unapplied_events), event.date == self.unapplied_events[-1].date))
            return None
        self.unapplied_events.append(event)
        self.intra_period_rounds += 1
        while self._period_past_over() and self.more_events:
    #             print("self.more_events ", self.more_events) 
            self.reset_period_date()
    #             if not self.more_events:
    #                 print("NO more EVENTS a ")
    #                 return None
    #       if self.more_events and not self._period_over():
        self._update_date()
        return event
    #         else:
    #             print("NO more EVENTS b ")
    #             return None
    
    def __intra_period_update(self, period_n, **kwargs):
        """This function updates the cost and/or balance and moves funds according to rules set
        """  
        self.set_period_details(period_n)
        self._refresh_cost(**kwargs)
    #         if self.intra_period_rounds > 1 or period_n > 0:
        self._refresh_balance(**kwargs)
        ## cost is transfered to balance during _transfer_to_account, such that balance function is not applied on brand new costs
        self._transfer_to_account(**kwargs)
        
    def accru(self, fin_event):
    #         print ("\n{} ACCURING at date {}".format(self.model_name, fin_event.date))
    #         print ("unapplied events {}".format([e.date for e in self.unapplied_events]))
        if len(self.unapplied_events) <= 0:
            raise exception("No events to accru in " + self.model_name + " number ")
        if self.unapplied_events[0] is not fin_event:
    #             print("ue: {}, fe: {}, ue_date: {}, fe_date: {}".format(self.unapplied_events[0], fin_event, self.unapplied_events[0].date, fin_event.date))
            raise exception("Event passed to accru is not the next expected event")
        event = self.unapplied_events.popleft()
        period_n = event.period_n
    #         print (" EVENT PERIOD_N BEFORE UPDATE IS ", period_n )
        """Currently every fin_holding works the same, and applies interest to whatever balance it has as the time of expect interest
        even if money was only recently moving into the account and should not have interest on it
        -Also there should potentially be different rules for different fin_holdings"""
        other_info = {"event":event, "accural_date":event.date, "event_date":event.date}
        self.__intra_period_update(period_n, **other_info)
    
    def _valid_ttr(self):
        """Issues a warning if time_period_till_repeat is not of the right types"""
        if not isinstance(self.ttr, datetime.timedelta) and not isinstance(self.ttr, relativedelta):
            warnings.warn("Time_period_till_repeat is not of known type, this may mean it won't work right")
    
    def _valid_cost_f(self):
        """Issues a warning if cost is not of the right types, and converts it into a function"""
        if not callable(self.cost_f) and not isinstance(self.cost_f, Number):
            warnings.warn("Unrecognized type {} for cost/cost_function in fin_cause object".format(type(self.cost_f)))
        if not callable(self.cost_f):
    #             print("setting _valid_cost_f cost_f to {}".format(self.cost_f))
            v = self.cost_f
            self.cost_f = lambda *args, **kwargs: v
    #             print("cost function is now {}, and self.cost_f() is now {}".format(self.cost_f, self.cost_f()))
        else:
            f = self.cost_f
            self.cost_f = paramify(f)
    
    def _valid_account_fs(self):
        for i, af in enumerate(self.account_fs):
            if not callable(af) and not isinstance(af, Number):
                warnings.warn("Unrecognized type {} for cost/cost_function in fin_cause object".format(af))
            if not callable(af):
                f = af
                self.account_fs[i] = lambda *args, **kwargs: f
            else:
                f = self.account_fs[i]
                self.account_fs[i] = paramify(f)
            
    def _valid_end_of_period(self):
        # of repitions or timeDelta or relativeTimeDelta or endDate"
        """Issues a warning if end_of_period is not of a known type"""
        if not isinstance(self.end_of_period, datetime.timedelta) and not isinstance(self.end_of_period, relativedelta)\
        and not isinstance(self.end_of_period, datetime.datetime) and not isinstance(self.end_of_period, Number):
            warnings.warn("End_of_period is not of known type, this may mean it won't work right")
        if isinstance(self.end_of_period, datetime.timedelta) or isinstance(self.end_of_period, relativedelta):
            self.end_of_period = self.start_of_period + self.end_of_period
    #         elif isinstance(self.end_of_period, Number):
    #             end = self.start_of_period
    #             for x in range(self.end_of_period):
    #                 end += self.ttr
    #             self.end_of_period = end
            
    def _period_over(self):
        # Returns true of false
        if isinstance(self.end_of_period, Number):
    #             print("in _period_over, end_date is {}, intra_period_rounds is {}".format(self.end_of_period, self.intra_period_rounds))
            return self.end_of_period <= self.intra_period_rounds-1
        else:
    #             print("in _period_over, end_date is {}, self.date + self.ttr is {}".format(self.end_of_period, self.date + self.ttr))
            return self.date + self.ttr > self.end_of_period
    
    def _period_past_over(self):
        if isinstance(self.end_of_period, Number):
    #             print("in _period_over, end_date is {}, intra_period_rounds is {}".format(self.end_of_period, self.intra_period_rounds))
            return self.end_of_period <= self.intra_period_rounds
        else:
    #             print("in _period_over, end_date is {}, self.date + self.ttr is {}".format(self.end_of_period, self.date + self.ttr))
            return self.date > self.end_of_period
    
    def _update_date(self):
    #         print ("\n {} _update_date unapplied events {}".format(self.model_name, [e.date for e in self.unapplied_events]))
        self.date += self.ttr

    def __add__(self, other):
        try:
            return self.balance+other.balance 
        except:
            try: 
                return self.balance+other
            except e:
                raise e
                
    def __iadd__(self, other):
        try:
            self.balance += other.balance
        except:
            try:
                self.balance += other
            except e:
                raise e
    
    def __isub__(self, other):
        try:
            self.balance -= other.balance
        except:
            try:
                self.balance -= other
            except e:
                raise e
                
    def __sub__(self, other):
        try:
            return self.balance - other.balance
        except:
            try:
                return self.balance - other
            except e:
                raise e


class Bank(fin_cause):

    def __init__(self, starting_time, linked_accounts=[], cost_structure=[
        ("time period till repeat", "cost_increase_function or new_cost",
         " # of repitions or timeDelta or relativeTimeDelta or endDate", "[accounts transfer functions]")], 
                  # Accounts transfer functions should take in: pre_disbersal_cost, after_disberal_cost, pre_disbersal_balance, after_disberal_balance, # aka before and after the money was transfered to other accounts during this update
        model_name="Bank", starting_amount=0.0, balance_function=lambda x:x, starting_cost=0.0, interest_start_date=None, max_balance=float("inf")):
        super().__init__(starting_time, linked_accounts, cost_structure, model_name, starting_amount, balance_function, starting_cost, interest_start_date, 0.0, max_balance)

class CreditCard(fin_cause):

    def __init__(self, starting_time, linked_accounts=[], cost_structure=[
        ("time period till repeat", "cost_increase_function or new_cost",
         " # of repitions or timeDelta or relativeTimeDelta or endDate", "[accounts transfer functions]")], 
                  # Accounts transfer functions should take in: pre_disbersal_cost, after_disberal_cost, pre_disbersal_balance, after_disberal_balance, # aka before and after the money was transfered to other accounts during this update
        model_name="Credit_card", starting_amount=0.0, balance_function=lambda x:x, starting_cost=0.0, interest_start_date=None, min_balance=float("-inf")):
        super().__init__(starting_time, linked_accounts, cost_structure, model_name, starting_amount, balance_function, starting_cost, interest_start_date, min_balance, 0.0)


def pay_cc(**kwargs):
#     kwarg = {"pre_cost":self.cost, "pre_balance":self.balance, "transfer_amount":sum_transfer,
#     "remaining_balance":self.balance, "account_to":a, "account_from":self}
    if kwargs["remaining_balance"] > 0:
        raise Exception("Credit Card balance can't be positive") 
    account_to = kwargs["account_to"]
    if kwargs["remaining_balance"] < 0 and account_to.balance > 0:
        return -min(account_to.balance, -kwargs["remaining_balance"])
    return 0.0

def bi_monthly(date):
    return (relativedelta(months=1)-relativedelta(days=14)) if not date.day == 1 else relativedelta(days=14)

# def income_gen(first_payment_date, starting_yearly_salary, time_till_raise, percentage_raise, max_salary=float("inf"), model_end_date=default_model_end_date, retire_date=None, increments="biMonthly"):
#     if increments is not "biMonthly":
#         raise ValueError('increments has not been programmed for anything not biMonthly')
#     current_date = first_payment_date
    
#     current_salary = starting_yearly_salary 
#     next_raise_date = current_date+time_till_raise
# #   TODO: CALCULATE HOW TAX IS TAKEN OFF AND OR PUT BACK ON AFTERWORDS
#     bioMonthly_salary = current_salary/24
    
#     while current_salary < max_salary and (retire_date is None or current_date < retire_date) and current_date < model_end_date :
#         yield current_date, bioMonthly_salary
#         onFirst = True if current_date.day == 1 else False
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



