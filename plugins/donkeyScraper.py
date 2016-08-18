import requests
from bs4 import BeautifulSoup
import re
import os
class DonkeyScraper():
    def __init__(self):
        USERNAME = os.environ.get('DONKEY_USER')
        PASS = os.environ.get('DONKEY_PASS')

        self.BATTERY_LOW = 'low battery'
        self.BATTERY_CRITICAL = 'critical battery'
        self.BATTERY_GOOD = 'good battery'
        self.admin_signin = 'https://www.donkey.bike/admins/sign_in'

        self.admin_password = 'admin[password]'
        self.admin_name = 'admin[email]'
        self.auth_token = 'authenticity_token'

        self.PAYLOAD ={
            self.admin_name:USERNAME,
            self.admin_password:PASS,
            self.auth_token:""
        }

        self.session_requests = requests.session()

    def login_to_dashboard(self):
        '''Logs in
        returns response or None if error
        '''
        response = self.session_requests.get(self.admin_signin)
        if response.ok:
            # Get auth_token first before logging in
            soup = BeautifulSoup(response.text,'html.parser')
            for tag in soup.find_all('input'):
                if tag['name'] == self.auth_token:
                    self.PAYLOAD[self.auth_token] = tag['value']
                    response = self.session_requests.post(self.admin_signin,self.PAYLOAD)
                    if response.ok:
                        return response
        return None


    def find_revenue(self,dashboard):
        ''' Checks the revenue
        @RETURN string'''
        txt = dashboard.find_all('div','well','h3')[0].text.strip()
        return re.findall('(?:\d+,)?[0-9]*[.][0-9]*',txt)[0]


    def check_battery_level(self,dashboard):
        '''Checks battery level of locks
        and returns number of locks that are in which level
        for all battery levels

        RETURN good, low,
        RETURN int,int,int
        '''
        for battery in dashboard.find_all('div','progress-bar'):
            if self.BATTERY_LOW in battery['title']:
                low_battery_bikes = int(battery.text.strip())
            if self.BATTERY_CRITICAL in battery['title']:
                critical_battery_bikes = int(battery.text.strip())
            if self.BATTERY_GOOD in battery['title']:
                good_battery_bikes = int(battery.text.strip())
        return good_battery_bikes,low_battery_bikes,critical_battery_bikes

    def get_dashboard(self,response):
        return BeautifulSoup(response.text,'html.parser')




if __name__ == "__main__":
    ds = DonkeyScraper()
    dash = ds.get_dashboard(ds.login_to_dashboard())
    print(ds.find_revenue(dash))
    print(ds.check_battery_level(dash))
