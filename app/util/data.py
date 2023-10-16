import pprint
import datetime as dt
from access_token import HelpScout
from map import RECORD, \
                FIELD, \
                MAILBOXES_MAP, \
                CONV_MAP, \
                USERS_MAP, \
                TAGS_MAP

URL_MAIN = 'https://api.helpscout.net/v2/'

STATUS_ALL = '?status=all'


class HelpScoutMethods:
    def __init__(self, start='', end=''):

        self.helpscout_obj = HelpScout()
        self.start = dt.datetime.strptime(start, '%Y-%m-%d')
        self.end = dt.datetime.strptime(end, '%Y-%m-%d')

        if self.start != '' and self.end != '':
            self.query = '&query=(createdAt:[{}T00:00:00Z TO {}T00:00:00Z])'.format(
                self.start.strftime('%Y-%m-%d'),
                self.end.strftime('%Y-%m-%d')
            )



    @staticmethod
    def generate_json(l,mapping):
        
        results = dict()
        for item in list(mapping.keys()):
                if item in l.keys():
                    if l[item] == []:
                        pass  
                    else:
                        if type(l[item]) != list:
                            results[item] = [l[item]]
                        else:
                            results[item] = l[item]
                else:
                    pass
        return results
    


    def filter(self, d, keys):
        'filter: remove specific keys'
        return {x: d[x] for x in d if x not in keys}
    


    def customers(self):

        url_customers = URL_MAIN + 'customers'
        data = self.helpscout_obj.get_helpscout_data(url=url_customers)
        data = data['_embedded']['customers']        
        
        return data



    def mailboxes(self):

        mailbox_list = self.helpscout_obj.get_helpscout_data(url=self.url_mailboxes)['_embedded']['mailboxes']

        d = list()

        exclude = {"_embedded", "_links",}
        for item in mailbox_list:
            __dict = self.filter(item, exclude)

            results = self.generate_json(__dict,MAILBOXES_MAP)
            d.append(results)
        return d
    


    def conversations(self):

        url_conversations = URL_MAIN + 'conversations' + STATUS_ALL + self.query
        conversation_list = self.helpscout_obj.get_helpscout_data(url=url_conversations)['_embedded']['conversations']
        d = list()

        for j in range(len(conversation_list)):
           
            results = self.generate_json(conversation_list[j], CONV_MAP)
            d.append(results)
            
        return d
    


    def count(self, data, location, term):
        count = 0

        for conversation in data:
           if 'status' in conversation and conversation[location][0] == term:
               count += 1

        return count



    def tags(self):

        url_tags= URL_MAIN + 'tags'
        tag_list = self.helpscout_obj.get_helpscout_data(url=url_tags)['_embedded']['tags']
        
        data=list()
            
        for tag in tag_list:
            tag_name = tag['name'] if tag['name'] else ''  # Extract the tag name
            ticket_count = tag['ticketCount'] if tag['ticketCount'] else None  # Extract the ticket count
            formatted_tag = {tag_name: ticket_count}  # Create a dictionary
            data.append(formatted_tag)

        return data
    


    def users(self):
        """
        The method for getting data from the 'users' HelpScout endpoint
        :return: list of dictionaries with the users data
        """

        user_list = self.helpscout_obj.get_helpscout_data(url=URL_MAIN + 'users')['_embedded']['users']
        d = list()

        for j in user_list:
          username = j['firstName']
          d.append(username)
        return d

                   
source=HelpScoutMethods('2023-10-01','2023-10-14')
data=source.conversations()
pprint.PrettyPrinter(width=10).pprint(data)

