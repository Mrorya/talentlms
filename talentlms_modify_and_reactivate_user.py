#!/usr/bin/python
#
# The purpose of this script is to be able to update user profile data from a spreadsheet.
# This script has been configured to update a user's username and reactivate their account 
# but can be modified easily to update other attributes.
#
# As this does updating of live data rather than reporting, caution should be used prior
# to executing the script. Test before running!
#

import requests
import json
import csv

base_url = 'https://{subdomain}.talentlms.com/api/v1'
headers = {
  'Authorization': 'Basic {apikey}',
}

# Ask user for name of csv file
print("Please make sure your csv file is formatted to only contain one column of email addresses and no additional data. \n")
csv_input = raw_input("Enter the filename of the csv: ")

email_address = []

# Pull User IDs
# Open Email CSV and append all rows to array for emailAddress
with open(csv_input, 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        email_address.append(row)
csvfile.close()

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

count = 0

for i in user_id:
    url = base_url + '/edituser'

    payload = {
        'user_id' : user_id[count],
        'login' : user_email[count],
    }
    print('Setting user ' + user_id[count] + ' login to ' + user_email[count])
    requests.post(url, data=payload, headers=headers)
    count += 1

count = 0

for i in user_id:
    url = base_url + '/usersetstatus/user_id:' + user_id[count] + ',status:active'

    print('Reactivating user: ' + user_email[count])
    requests.get(url, headers=headers)
    count +=1
