import requests
import time
import json

URL_AUTH = 'https://api.helpscout.net/v2/oauth2/token'


class HelpScout:
    def __init__(self):
        """
        The connection with the HelpScout API.
        """


        self.data = {
        'grant_type': 'client_credentials',
        'client_id': 'RNvLHFpooBZD2isCwxB2VtrY2muvXYC7',
        'client_secret': '7muvT242WRiNMcpWk3mmATk46AEBQh0w'
        }

        self.token = requests.post(URL_AUTH, data=self.data)

        self.headers = {'Authorization': 'Bearer {}'.format(self.token.json()['access_token'])}


    def get_helpscout_data(self, url,  start='', end=''):
        """
        request data from HelpScout API
        """


        params = {
            'start': '{}T00:00:00Z'.format(start),
            'end': '{}T00:00:00Z'.format(end)
        }

        helpscout_data = requests.get(url, headers=self.headers, params=params)
        time.sleep(1)
        
        return helpscout_data.json()

    def get_pages_breakdown(self, url, page, start='', end=''):

        params = {
                'start': '{}T00:00:00Z'.format(start),
                'end': '{}T00:00:00Z'.format(end),
                'page': '{}'.format(page)
        }

        pages_breakdown = requests.get(url, headers=self.headers, params=params)
        time.sleep(1)
        return pages_breakdown.json()

