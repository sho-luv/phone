# phone.py 

This program uses Twilio's API 6.x to lookup who a phone is registered
to as well as the carrier it is registered with. It can also send text messages to mobile phones 
using the carriers gateway with email to text. To use this program you need a Twilio API key and 
you need to set email settings as well.
 
Note: Twilio offers free trials that do not charge. You do not need to enter
a credit card or anything. All the features in this program can be used with
the trial account. When you register Twilio will provide you $15.50 worth of credits.
Each request of my program costs $.03 Cents. This means you can submit 516 requests
before you have to register another account.

Details about the Twilio trial account can be found here:
https://www.twilio.com/docs/usage/tutorials/how-to-use-your-free-trial-account

By prepending cell providers email gateway to cell numbers, it is possible to send 
emails that get routed to cell numbers as SMS messages. This is free.

by sho_luv

### Usage:
```
phone.py 
usage: phone.py [-h] [-m "text message"] [-n] phone

This program sends text messages to people by using email.

positional arguments:
  phone              Phone number to lookup or send text message to

optional arguments:
  -h, --help         show this help message and exit
  -m "text message"  Text message
  -n, -notwilio      no charge. Do not use Twilio API to lookup information
                     and just send message
```
### Usage Example:
```
root@Id10t:~# phone.py XXXXXXXXXX
[+]  The mobile number +1XXXXXXXXXX is registered to SHO LUV on the PWN Wireless network

root@Id10t:~# phone.py XXXXXXXXXX -m "Hello from the Matrix"
[+] Nov 09 00:54:36 Message sent to mobile number +1XXXXXXXXXX registered to SHO LUV on the PWN Wireless network
```
