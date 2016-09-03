from __future__ import unicode_literals
# don't convert to ascii in py2.7 when creating string to return


import donkey_const
import donkeyScraper

import requests
import logging
import time

from slackclient import SlackClient
import os

# establish logging
log_file ='rtmbot.log'
logging.basicConfig(filename=log_file,
                    level=logging.INFO,
                    format='%(asctime)s %(message)s')
logging.info('Initialized in: {}'.format('NOW'))

AVAILABLE_BIKES_CONST = 2
DEFAULT_CHANNEL = 'G1ZVAVC0N'
# Test channel
# DEFAULT_CHANNEL = 'C22GY3D7G'

outputs = []
crontable = []

crontable.append([13*60,'check_hired_interval'])
crontable.append([24*60*60,'daily_update'])
loggedIn = None
ds = donkeyScraper.DonkeyScraper()
while loggedIn == None:
    print('logging in loop')
    loggedIn = ds.login_to_dashboard()

# Use admin token to be able to delete not just Bots messages
# Don't push to git your Token
slack_client = SlackClient(os.environ.get('SLACK-BOT_TOKEN'))

def process_message(data):
    channel = data['channel']
    if 'text' in data.keys():
        text = data['text']
    print('processing message')
    if channel and text:
        if donkey_const.AT_BOT in text:
            print('handling command')
            handle_command(text,channel)

# def catch_all(data):
#     print(data)

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    # logging.info('handle_command running...')
    print('handle_command running...')

    global AVAILABLE_BIKES_CONST
    response = donkey_const.RESPONSE_NO_CLUE

    if command.startswith(donkey_const.EXAMPLE_COMMAND):
        response = "Working...write some more code then I can do whatever you want met to. Wink Wink!"
        print('example command')
    if donkey_const.COMMAND_DELETE_ALL in command:
        del_all_msges(channel)
        response = donkey_const.RESPONSE_DELETED_ALL
    if donkey_const.COMMAND_DAILY in command:
        daily_update()
    if donkey_const.COMMAND_HIRED in command:
        response = get_response_for_hired(check_hired_status())
        print('hired command')
    if donkey_const.COMMAND_REVENUE in command:
        dash = ds.get_dashboard(loggedIn)
        # outputs.append([channel,donkey_const.RESPONSE_REVENUE.format(ds.find_revenue(dash))])
        response = donkey_const.RESPONSE_REVENUE.format(ds.find_revenue(dash))
        print('revenue command')
    if donkey_const.COMMAND_BATTERY_LEVEL in command:
        dash = ds.get_dashboard(loggedIn)
        # outputs.append([channel,donkey_const.RESPONSE_BATTERY.format(a,b,c=ds.check_battery_level(dash))])
        a,b,c = ds.check_battery_level(dash)
        response = donkey_const.RESPONSE_BATTERY.format(a,b,c)
        print('battery level command')

    # logging.info('Adding to outputs list')
    # print(response)
    print('Adding to outputs list')
    outputs.append([channel,response])

def del_all_msges(channel):
    if slack_client.rtm_connect():
        messages = slack_client.api_call('channels.history',channel=channel,count=1000)['messages']
        for msg in messages:
            del_msg(msg['ts'],channel)

def del_msg(ts,channel):
    # FIXME: Why does this differ from Slack documentation?
    slack_client.api_call('chat.delete',channel=channel,ts=ts)

def daily_update():
    print('daily update')
    dash = ds.get_dashboard(loggedIn)
    hired = check_hired_status()
    gd,low,crit = ds.check_battery_level(dash)
    rev = ds.find_revenue(dash)
    if gd == 2:
        # All good battery levels, we don't have to charge battery
        battery_answer = 'No'
    else:battery_answer='Yes'

    outputs.append([DEFAULT_CHANNEL,donkey_const.RESPONSE_DAILY_UPDATE_PREQUEL])
    outputs.append([DEFAULT_CHANNEL,donkey_const.RESPONSE_DAILY_UPDATE.format(hired,rev,battery_answer)])


def check_hired_interval():
    print('Check hired interval')
    global AVAILABLE_BIKES_CONST
    available_bikes = check_hired_status()
    if available_bikes == AVAILABLE_BIKES_CONST:
        # Nothing changed
        return
    else:
        dash = ds.get_dashboard(loggedIn)
        response = donkey_const.STATUS_CHANGED + get_response_for_hired(available_bikes)
        response += donkey_const.RESPONSE_REVENUE.format(ds.find_revenue(dash))
        AVAILABLE_BIKES_CONST = available_bikes
        outputs.append([DEFAULT_CHANNEL,response])

def make_api_call_for_bikes(amount):
    logging.info('make_api_call_for_bikes running...')
    donkey_response = requests.get(donkey_const.DONKEY_API_BASE+donkey_const.DONKEY_API_BIKE_NO.format(amount))
    if donkey_response.status_code == 200:
        json = donkey_response.json()
        for hub in json:
            if hub["id"] == donkey_const.ALTERHUB_ID:
                return amount
    return 0

def check_hired_status():
    """Check if the bikes are hired using DonkeyAPI
    @return returns a num_of_available_bikes (0,1,2)"""
    logging.info('check_hired_status running...')
    num_of_available_bikes = 0
    # Check if there are two bikes available
    if make_api_call_for_bikes(2) == 2:
        return 2
    else:
        if make_api_call_for_bikes(1) == 1:
            num_of_available_bikes = 1
    return num_of_available_bikes

def get_response_for_hired(num_of_available_bikes):
    logging.info('get_response_for_hired running...')
    # If not, check if one
    # If not, two of our bikes are hired
    if num_of_available_bikes == 2:
        return donkey_const.HIRED_NO_BIKES
    if num_of_available_bikes == 1:
        return donkey_const.HIRED_NUM_BIKES.format("one")
    return donkey_const.HIRED_NUM_BIKES.format("two")
