#!/usr/bin/python
#
# The purpose of this script is to remove a list of users from a CSV from a specific course
# in TalentLMS.
# 
# As this does updating of live data rather than reporting, caution should be used prior
# to executing the script. Test before running!
#

import requests
import json
import csv

try:
    input = raw_input
except NameError:
    pass

base_url = 'https://{subdomain}.talentlms.com/api/v1'
headers = {
  'Authorization': 'Basic {apikey}',
}

# Define course to delete
course_id = "{courseid}"

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

print("Users not found include: \n")
print(users_not_found)

# Iterate through user_ids to remove all users from course
count = 0
for i in user_id:
    url = base_url + '/removeuserfromcourse/user_id:' + user_id[count] + ',course_id:' + course_id

    response = requests.get(url, headers=headers)
    print(response.text.encode('utf8'))
    count += 1
