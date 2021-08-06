#!/usr/bin/python
#
# TalentLMS' SAML assertion comes preconfigured with their username as their email address. This script's
# goal is to take a CSV of user emails, look up their IDs in TalentLMS, and modify the usernames accordingly 
# to match their email address.
#
#

import requests
import json
import csv

try:
    input = raw_input
except NameError:
    pass

base_url = 'https://{domain}.talentlms.com/api/v1'
headers = {
  'Authorization': 'Basic {{apikey}}',
}

# Ask user for name of csv file
print("Please make sure your csv file is formatted to only contain one column of email addresses and no additional data. \n")
csv_input = input("Enter the filename of the csv: ")

email_address = []

# Pull User IDs
# Open Email CSV and append all rows to array for emailAddress
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        email_address.append(row)
csvfile.close()

print(email_address)

# Create empty variables for USER IDs 
user_id = []
user_email = []
users_not_found = []

# Lookup and store userIds for all users in email array
for i in email_address:
    try:
        url = base_url + '/users/email:' + str(i[0])
        req = requests.get(url, headers=headers)
        json_obj = req.json()
        user_id.append(json_obj["id"])
        user_email.append(json_obj["email"])
    except KeyError:
        users_not_found.append(i)
        pass

# Iterate through user email IDs and set login as user's email
count = 0
for i in user_id:
    url = base_url + '/edituser'

    payload = {
        'user_id' : user_id[count],
        'login' : user_email[count]
    }
    print('Setting user ' + user_id[count] + ' login to ' + user_email[count])
    requests.post(url, data=payload, headers=headers)
    count += 1
