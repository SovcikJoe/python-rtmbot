import os
# Commands
EXAMPLE_COMMAND = "test"
COMMAND_REVENUE = "revenue"
COMMAND_DAILY = 'daily update'
COMMAND_HIRED = "hired"
COMMAND_CHECK_HIRED = 'Check status change for hired'
COMMAND_BATTERY_LEVEL = 'battery level'
COMMAND_HELP= "list commands"
COMMAND_DELETE_ALL = "delete all messages"

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

DONKEY_API_BASE = "https://www.donkey.bike/api/public/hubs/search"
DONKEY_API_BIKE_NO = "?number_of_bikes={0}"
ALTERHUB_ID = 262

# Responses
RESPONSE_DELETED_ALL = 'Whoa, what a mess. All messages are deleted'
RESPONSE_BATTERY = '''
The battery levels are as follows

        #of bikes
good        *{0}*
low         *{1}*
critical    *{2}*
'''
RESPONSE_REVENUE = '''
Our current revenue is {0} Dkk.
Not too bad.\nThough I should point out this is only for last 30 days.
Overall Revenue is not displayed which is silly :/
'''
RESPONSE_DAILY_UPDATE_PREQUEL ='''
\nIt's time for our Daily Update....
'''
RESPONSE_DAILY_UPDATE = '''
__________________________________________________
How many of our  heroes are in the hub? : *{0}*
What is our revenue for 30 days?        : *{1}*
Do we have to charge the battery?       : *{2}*
__________________________________________________
'''

RESPONSE_NO_CLUE = "Not sure what you mean. Use the *" + COMMAND_HELP + \
           "* command to see help"

RESPONSE_HELP = "I know asking for help can be hard, so I applaud you, well done.\n" +\
                "Here are the commands you can use: {0}, {1},{2}, {3}, {4}".format(COMMAND_HIRED, COMMAND_REVENUE, COMMAND_HELP, COMMAND_BATTERY_LEVEL,COMMAND_DAILY)

HIRED_NUM_BIKES = "DUDE!!! This is *awesome*!!!\n" + \
                    "*{0}* of our bikes are hired right now. You are rich, when do I get paid?"
HIRED_NO_BIKES = "All of our bikes are sound and safe in their hub :). Pretty cool."
STATUS_CHANGED = "Yo, check it. *The bike availability changed.* "
