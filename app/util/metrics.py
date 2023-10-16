from .data import HelpScoutMethods
from datetime import datetime, timedelta
import pprint


class Metrics:
    
    
    def __init__(self):
      self.data={}
    
### count mail status ######
     
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
    
###


### count incoming mails per day - version 2  ######


    def incoming_mails(self, data,start_date,end_date):
       all_count = []
       current_date = start_date

       while current_date <= end_date:
          
           date = current_date.strftime('%Y-%m-%d')
           count = 0

           for conversation in data:
              
              # filter by createdAt
               if 'createdAt' in conversation:
                   created_at = datetime.strptime(conversation['createdAt'][0], '%Y-%m-%dT%H:%M:%SZ').date()
                   if created_at == current_date.date():
                      
                      # look for createdBy 
                       if 'createdBy' in conversation:
                           for i in conversation['createdBy']:
                               if 'type' in i and i['type'] == 'customer':
                                   # count for the corresponding day
                                   count += 1
 
           all_count.append((date, count))
           
           # Move to the next day
           current_date += timedelta(days=1)

       return all_count




    

    
