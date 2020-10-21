#!/usr/bin/python
#
# The purpose of this script is to be able to deactivate a user from a csv.
# This script has been configured to update a user's status but
# can be modified easily to update other attributes.
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

# Modify this with the date to disable - cannot deactivate in the past
deactivation_date = '{date}'

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
        'deactivation_date' : deactivation_date
    }
    print('Disabled user ' + user_id[count] + ' - ' + user_email[count])
    requests.post(url, data=payload, headers=headers)
    count += 1
