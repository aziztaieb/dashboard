from .data import HelpScoutMethods


class Metrics:
    def __init__(self):
      self.data={}
    def search_status(self, data):
        active = 0
        pending = 0
        closed = 0

        for conversation in data:
           if 'status' in conversation :
              if conversation['status'][0] == 'active': 
                active += 1
              elif conversation['status'][0] == 'pending': 
               pending += 1
              elif conversation['status'][0] == 'closed': 
               closed += 1
                 
        return active,pending,closed
    
