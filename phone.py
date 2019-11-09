#!/usr/bin/python

###
# 
# This program uses Twilio's API 6.x to lookup who a phone is registered
# to as well as the carrier it is registered with.
# 
# Note: Twilio offers free trials that do not charge. You do not need to enter
# a credit card or anything. All the features in this program can be used with
# the trial account. When you register Twilio will provide you $15.50 worth of credits.
# Each request of my program costs $.03 Cents. This means you can submit 516 requests
# before you have to register another account.
#
# Note: Temp emails work with twilo: uzymav@robot-mail.com
#
# Details about the Twilio trial account can be found here:
# https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account
#
# By prepending cell providers email gateway to cell numbers it is possible to send 
# emails that get routed to cell numbers as sms messages. This is free.
#
# by sho_luv
#
# python -m pdb phone.py # debug program
#
###

import re
import pprint
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
import argparse # Parser for command-line options, arguments and sub-commands
import smtplib	# SMTP protocol client
import sys # used sys to have clean exits of the program
import os # used to call sendEmail because I didn't want to use python smtplib ....
import subprocess # used to call sendEmail because I didn't want to use python's smtplib ....
from termcolor import colored, cprint # used to print colors

parser = argparse.ArgumentParser(description='This program sends text messages to people by using email.')
parser.add_argument('phone', action='store', help='Phone number to lookup or send text message to')
parser.add_argument('-m', action='store', metavar = '"text message"', help='Text message')
parser.add_argument("-n","-notwilio", help='no charge. Do not use Twilio API to lookup information and just send message', action="store_true")

if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

options = parser.parse_args()

# Install Twilo 'pip install twilio'
# Your Account Sid and Auth Token from twilio.com/user/account
# Store them in the environment variables:
# "TWILIO_ACCOUNT_SID" and "TWILIO_AUTH_TOKEN"
# Find these values at https://twilio.com/user/account

# Set Variables ############################################################
# Twilio Account information
############################################################################
account_sid = "" 
auth_token = ""

###########################################################################
# SMTP settings server and credentials
###########################################################################
smtp_server = 'mail.smtp.com'	# gmail smtp: smtp.gmail.com					
smtp_port = '2525'		    # gmail port: 587
email_from = 'your@computer.com'    # set from email
email_subject = 'Alert'             # set subject for email
username = '' # username
password = '' # password 
###########################################################################

# check settings before trying to use
if not username or not password:
    print( "Please set SMTP settings inside %s before using..."%sys.argv[0])
    sys.exit(1)

# Twilio Authentication:
client = Client(account_sid, auth_token)

def valid_number(message):
    try:
        name = client.lookups.phone_numbers(message).fetch(type='caller-name')
        #pprint.pprint(vars(name))
        if name.country_code != 'US':
            cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
            cprint("Sorry this program only works with US numbers ", end='')
            cprint(':( ', 'yellow', attrs=['bold'])  # print success
            sys.exit(1)
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        if e.code == 20008:
            cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
            cprint("Sorry the Twilio test Account_SID and Auth_Token can not be used to run this program ", end='')
            cprint(':( ', 'yellow', attrs=['bold'])  # print success
            sys.exit(1)
        if e.code == 20003:
            cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
            cprint("Sorry the Twilio Account_SID and Auth_Token appear to be invalid.", end='')
            cprint(':( ', 'yellow', attrs=['bold'])  # print success
            sys.exit(1)
        else:
            raise e
            
    # Check for at least two numbers
    countryCode = '+1'
    if bool(re.search(r'\d{2}', message)):
        # Replace %2B with + and assign to variable because strings are immutable in Python
        number = message.replace('%2B', '+', 1)
        # Clean up number
        cleanedUpNumber = re.sub(r'([-() ])', "", number)
        # Check if it's less than 10 digits
        if len(cleanedUpNumber) < 10:
            return False
        elif len(cleanedUpNumber) == 10:
            return countryCode + cleanedUpNumber
        elif len(cleanedUpNumber) > 10:
            # Check for countryCode
            countryCode = '+1'
            if (cleanedUpNumber[0:2] == countryCode):
                return cleanedUpNumber
        else:
            return False
    else:
        return False

def name_lookup(number_to_lookup):
    try:
        name = client.lookups.phone_numbers(number_to_lookup).fetch(type='caller-name')
        if name:
            return (name.caller_name)['caller_name']
        else:
            return False
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e

def carrier_lookup(number_to_lookup):
    try:
        carrier = client.lookups.phone_numbers(number_to_lookup).fetch(type='carrier')
        if carrier:
            return (carrier)
        else:
            return False
    except TwilioRestException as e:
        if e.code == 20404:
            return False
        else:
            raise e

# Main program starts here.
number = valid_number(options.phone)
if number:
    name = name_lookup(number)
    carrier_info = carrier_lookup(number)
    carrier = carrier_info.carrier['name']
    carrier_type = carrier_info.carrier['type']
    if 'AT&T' in carrier:    # determine carrier email to send to and color output
            carrier_email = 'txt.att.net'
            color_carrier = colored(carrier, 'blue')
    elif 'Verizon' in carrier:
            carrier_email = 'vtext.com'
            color_carrier = colored(carrier, 'red')
    elif 'T-Mobile' in carrier:
            carrier_email = 'tmomail.net'
            color_carrier = colored(carrier, 'magenta')
    elif 'Sprint' in carrier:
            carrier_email = 'messaging.sprintpcs.com'
            color_carrier = colored(carrier, 'yellow')
    elif 'Google' in carrier:
            carrier_email = 'txt.voice.google.com'
            color_carrier = colored(carrier, 'white')
    elif 'Cricket' in carrier:
            carrier_email = 'sms.cricketwireless.net'
            color_carrier = colored(carrier, 'green')
    else:
            carrier_email = 'Uknown'
            color_carrier = colored(carrier, 'green')
    
    green_name = colored(name, 'green')
    yellow_phone = colored(number, 'yellow')
    color_carrier_type = colored(carrier_type, 'yellow')
    if options.m is not None:

        if carrier_email == 'Uknown':
            cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
            response = " Unable to send message to %s number %s registered to %s on the %s network" % (color_carrier_type, yellow_phone, green_name, color_carrier) 
            print(response)
        else:
            email = "sendEmail -f %s -t %s@%s -u %s "\
                     "-s %s:%s -o tls=no -xu %s -xp %s -m %s media_url=http://sholuv.net/smile.jpg"\
                     % (email_from, options.phone, carrier_email, email_subject, smtp_server, smtp_port, username, password, options.m)

            output = subprocess.check_output(email, shell=True) # call to os to run command and save ouput
            output = output.decode("utf-8")
            if 'successfully' in output:
                    cprint('[+] ', 'green', attrs=['bold'], end='')  # print success
                    cprint(output[0:16], end='')    # print out date and timestamp of message sent
                    response = "Message sent to %s number %s registered to %s on the %s network" % (color_carrier_type, yellow_phone, green_name, color_carrier)
                    print(response)
                    sys.exit(0)
            else:
                    cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
                    response = " Error sending message to %s number %s registered to %s on the %s network" % (color_carrier_type, yellow_phone, green_name, color_carrier) 
                    print(response)
                    cprint("Sorry unable to send message...", 'red', attrs=['bold'])
                    sys.exit(1)
    else:
        cprint('[+] ', 'green', attrs=['bold'], end='')  # print success
        response = " The %s number %s is registered to %s on the %s network" % (color_carrier_type, yellow_phone, green_name, color_carrier) 
        print(response)
    sys.exit(0)
else:
    cprint('[+] ', 'red', attrs=['bold'], end='')  # print success
    cprint("Sorry that phone number isn't valid ", end='')
    cprint(':( ', 'yellow', attrs=['bold'])  # print success
    sys.exit(1)
