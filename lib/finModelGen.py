from .finCause import *
from heapq import heappush, heappop, heapreplace
from collections import OrderedDict
# class fin_cause_pipeline(fin_cause):
#     """This class is used to model costs """
        
#     __lt__(a, b)
# operator.__le__(a, b)
# operator.__eq__(a, b)
# operator.__ne__(a, b)
# operator.__ge__(a, b)
# operator.__gt__(a, b)
        
""" CODE FOR THE FULL MODEL GENERATOR
class full_model_setup(object):
    
    def __init__(self,model_end_date, model_start_date=datetime.datetime.now(), extra_models=[] ):
        self.models += extra_models
        self.model_end_date = model_end_date
        self.model_start_date = model_start_date
        
    def balance_transfers(self):
        
"""      
        
def fin_mod_gen(models, model_end_date):
    """ Since each model should be depenant upon other models and the current situation, and things can happen simultaniously, 
    fin_events are only dates linked back to models, only when the date is processed as the current date are the values calculated"""
    
    fin_event_heap = []
#     date-> [ [monitary_events], [sub_gen_number]] .
    for model in models:
        heappush(fin_event_heap, model.get_next_fin_event() )
    
#     print("fin_event_heap ", [e.date for e in fin_event_heap])

    current_date = fin_event_heap[0].date
    while len(fin_event_heap) > 0 and current_date <= model_end_date:
#         print("UP TO: ", current_date, " HEAP has ",len(fin_event_heap) )
        next_events = []
        next_e = fin_event_heap[0].get_next_fin_event() 
        if next_e is not None:
#             print ("next_e is ", next_e.date)
            next_events.append(heapreplace(fin_event_heap, next_e))
        else:
#             print ("next_e is None a")
            next_events.append(heappop(fin_event_heap))
    
        current_date = next_events[0].date
        while len(fin_event_heap)>0 and fin_event_heap[0].date == current_date:
            ## Populate the next_events to be returned by taking all events that occur at the given time and replacing what is lost in the heap with a new event from the given model
#             print("\n replace in  fin_event_heap: ", [e.date for e in fin_event_heap])
            next_e = fin_event_heap[0].get_next_fin_event()
            if next_e is not None:
#                 print ("next_e is ", next_e.date)
                next_events.append(heapreplace(fin_event_heap, next_e))
            else:
#                 print ("next_e is None b")
                next_events.append(heappop(fin_event_heap))
        ## APPLY EVENTS
        event_names = []
        for event in next_events:
            event.apply_fin_event() ## Actually accru interest on each account
            event_names.append(event.get_model_name() )
        ## Transfer Balances
#         print("UP TO: ", current_date, " of " , model_end_date,  " Next events are ", [e.date for e in next_events], " len(fin_event_heap) is ", len(fin_event_heap), " len(fin_event_heap) > 0 : ", len(fin_event_heap) > 0)
        # Create an Ordered Dictionary of balances
        balances = OrderedDict([("{}_balance".format(model.get_name()), model.balance ) for model in models]+[("{}_cost".format(model.get_name()), model.cost ) for model in [e._model for e in next_events] ] )
#         , ('Income', i)
        
        balances["Index"] = current_date
        balances["Recent Events"] = tuple(event_names)
        
#         print ("Index: ", balances["Index"] , " vs. current_date: ", current_date)
        yield balances
#         next_events = {}
#         next_events
    