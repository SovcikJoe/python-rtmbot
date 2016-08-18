import os
# Commands
EXAMPLE_COMMAND = "test"
COMMAND_REVENUE = "revenue"
COMMAND_DAILY = 'daily update'
COMMAND_HIRED = "hired"
COMMAND_CHECK_HIRED = 'Check status change for hired'
COMMAND_BATTERY_LEVEL = 'battery level'
COMMAND_HELP= "list commands"

BOT_ID = os.environ.get("BOT_ID")
AT_BOT = "<@" + BOT_ID + ">"

DONKEY_API_BASE = "https://www.donkey.bike/api/public/hubs/search"
DONKEY_API_BIKE_NO = "?number_of_bikes={0}"
ALTERHUB_ID = 262
SHERLOCK_ID = 1434
WATSON_ID = 1435
ALTERHUB_NAME = "Halmtorvet"


# Responses
RESPONSE_BATTERY = '''
The battery levels are as follows

        #of bikes
good        *{0}*
low         *{1}*
critical    *{2}*
'''
RESPONSE_REVENUE = '''
Thank you for asking. Our current revenue is {0} Dkk.
Not too bad.\nThough I should mention this is for last 30 days.
Overall Revenue is not Displayed.
That is silly\nSorreeeey'''
RESPONSE_DAILY_UPDATE_PREQUEL ='''
It's time for our Daily Updates....

How are Sherlock and Watson coping?

Is everything all right with our heroes?

Find out:
:expressionless:
'''
RESPONSE_DAILY_UPDATE = '''
How many of our  heroes are in the hub? : *{0}*
What is our revenue for 30 days?        : *{1}*
Do we have to charge the battery?       : *{2}*

Thank you for listening,

Your truely,

badass, Me :)
'''

RESPONSE_NO_CLUE = "Not sure what you mean. Use the *" + COMMAND_HELP + \
           "* command to see help"

RESPONSE_HELP = "I know asking for help can be hard, so I applaud you, well done.\n" +\
                "Here are the commands you can use: {0}, {1},{2}, {3}, {4}".format(COMMAND_HIRED, COMMAND_REVENUE, COMMAND_HELP, COMMAND_BATTERY_LEVEL,COMMAND_DAILY)

HIRED_NUM_BIKES = "DUDE!!! This is *awesome*!!!\n" + \
                    "*{0}* of our bikes are hired right now. You are rich, when do I get paid?"
HIRED_NO_BIKES = "All of our bikes are sound and safe in their hub :). Pretty cool."
STATUS_CHANGED = "Yo, check it. *The bike availability changed.* "
