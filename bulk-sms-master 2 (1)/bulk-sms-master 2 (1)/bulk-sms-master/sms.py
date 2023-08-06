#!/usr/bin/env python3
# Download the helper library from https://www.twilio.com/docs/python/install
import csv, sys, os 
from twilio.rest import Client
import numpy as np 

MESSAGE_FILE = 'message.txt'     # File containing text message
CSV_FILE = 'Book4.csv'
LOG_FILE = 'newlog.csv'
PEOPLE_FILE = 'test.csv'    # File containing participant numbers
LOG_CSV = 'newlog.csv'    # File containing sent numbers
SMS_LENGTH = 160                 # Max length of one SMS message
MSG_COST = 0.015                  # Cost per message

# Twilio: Find these values at https://twilio.com/user/account
account_sid = "AC1d82e07c778ab632fd70029df76a0aa4"   # Ensure you remove the angle brackets! < >
auth_token = "71582149684ea2dbe67dcab72b63589c"
from_num = "6475600321"# 'From' number in Twilio

# Now put your SMS in a file called message.txt, and it will be read from there.
with open(MESSAGE_FILE, 'r') as content_file:
    sms = content_file.read()

# Check we read a message OK
if len(sms.strip()) == 0:
    print("SMS message not specified- please make a {}' file containing it. \r\nExiting!".format(MESSAGE_FILE))
    sys.exit(1)
else:
    print("> SMS message to send: \n\n{}".format(sms))

# How many segments is this message going to use? 
segments = int(len(sms.encode('utf-8')) / SMS_LENGTH) +1

# Open the people CSV and get all the numbers out of it
with open(CSV_FILE, 'r') as csvfile:
    peoplereader = csv.reader(csvfile)
    numbers = set([p[0] for p in peoplereader]) # remove duplicate numbers

with open(LOG_CSV, 'r') as csvfile: 
    logreader = csv.reader(csvfile)
    new_numbers = set([p[0] for p in logreader])

log_nums = []

for i in new_numbers: 
    x = i.replace(" ", "")
    log_nums.append(x)

#with open(PEOPLE_FILE, 'r') as csvfile:
#    namereader = csv.reader(csvfile)
#   for k in namereader:
#        names.append(k)

#print(names)
better_numbers = []

for j in numbers: 
    i = j.replace(" ", "")
    if len(i) == 11:
        better_numbers.append(i)

better_numbers = [num for num in better_numbers if num.startswith("1")]

count = 0 

for i in log_nums: 
    if i in log_nums and i in better_numbers: 
        count+=1 
        better_numbers.remove(i)

print("You have already texted " + str(count) + " phone numbers previously, they have been removed from the list and will not be texted")
#testing 
#for i in better_numbers:
#    print(i)

# Calculate how much it's going to cost
messages = len(better_numbers)
print(messages)
cost = MSG_COST * segments * messages

#texts = []
#for i in names: 
#    text = "Hi "+ str(i) + " This is a test!!"
#    print(text)
#    texts.append(text)

print("> {} messages of {} segments each will be sent, at a cost of ${} ".format(messages, segments, cost))

# Check you really want to send them
confirm = input("Send these messages? [Y/n]")
if confirm[0].lower() == 'y':
    # Set up Twilio client
    client = Client(account_sid, auth_token)
    # Send the messages
    for num in better_numbers:    
        # Send the sms text to the number from the CSV file:
        print("Sending to " + num)
        with open(LOG_CSV,'a', newline='') as logging:
            wr = csv.writer(logging, quoting=csv.QUOTE_ALL)
            wr.writerow([num])
        message = client.messages.create(to=num, from_=from_num, body = sms)
        

print("Exiting!")