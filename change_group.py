# Copyright (c) 2021 Cisco and/or its affiliates.

# This software is licensed to you under the terms of the Cisco Sample
# Code License, Version 1.1 (the "License"). You may obtain a copy of the
# License at

#                https://developer.cisco.com/docs/licenses

# All use of the material herein must be in accordance with the terms of
# the License. All rights not expressly granted by the License are
# reserved. Unless required by applicable law or agreed to separately in
# writing, software distributed under the License is distributed on an "AS
# IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
# or implied.


from config import HOST, USERNAME, PASSWORD
import requests
import base64
import json
import urllib3
urllib3.disable_warnings()


''' ISE Environment '''
host = HOST
user = USERNAME
password = PASSWORD

''' Setup credintials '''
creds = str.encode(user+':'+password)
encodedAuth = bytes.decode(base64.b64encode(creds))

payload = {}
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Basic ' + encodedAuth
}

print('-'*25+' Start ' + '-'*25)
''' ISE API calls '''

''' Get-All internal users '''
print('Get-All internal users')
url = host+":9060/ers/config/internaluser"
method = "GET"
response = requests.request(
    method, url, headers=headers, data=payload, verify=False)
print('Response Code: ' + str(response.status_code))
# print(response.text)
print('-'*50)


''' Printing List of users '''
print('List of users:')
res_dict = json.loads(response.text)
internal_users = res_dict['SearchResult']['resources']
for user in internal_users:
    user_name = user['name']
    user_id = user['id']
    print('name: ' + str(user_name) + '\t\tid: ' + str(user_id))
print('-'*50)

''' Printing user's current details '''
print('Selected user\'s details:')
url = host+":9060/ers/config/internaluser/" + user_id
method = "GET"
response = requests.request(
    method, url, headers=headers, data=payload, verify=False)
print('Response Code: ' + str(response.status_code))
# print(response.text)
# print('-'*50)

''' Getting the group id '''
res_dict = json.loads(response.text)
user_group_id = res_dict['InternalUser']['identityGroups']
print('Current user_group_id: ' + str(user_group_id))
print('-'*50)


''' Get user's group details '''
print('User\'s current group name:')
url = host+":9060/ers/config/identitygroup/" + user_group_id
method = "GET"
response = requests.request(
    method, url, headers=headers, data=payload, verify=False)
print('Response Code: ' + str(response.status_code))
# print(response.text)
# print('-'*50)

''' Getting the group's name '''
res_dict = json.loads(response.text)
current_group_name = res_dict['IdentityGroup']['name']
print('User: ' + str(user_name) + '\t\tCurrent group: ' + str(current_group_name))
print('-'*50)

''' Get-All identitygroup '''
print('Get all groups:')
url = host+":9060/ers/config/identitygroup"
method = "GET"
response = requests.request(
    method, url, headers=headers, data=payload, verify=False)
print('Response Code: ' + str(response.status_code))
# print(response.text)

''' Printing all the found groups ''' 
res_dict = json.loads(response.text)
groups = res_dict['SearchResult']['resources']

for group in groups:
    print('\tName: ' + group['name'])
    print('\tid: ' + group['id'])
    print('\t' + '_'*25)

print('-'*50)
''' Select the new group by entering its id '''
new_group_id = input('Enter the new group\'s id to move the user to:\n')


''' Get user's new group's details '''
print('User\'s current group details:')
url = host+":9060/ers/config/identitygroup/" + new_group_id
method = "GET"
response = requests.request(
    method, url, headers=headers, data=payload, verify=False)
print('Response Code: ' + str(response.status_code))
# print(response.text)
print('-'*50)

''' Getting the new group's name '''
print('Getting the new group\'s name')
res_dict = json.loads(response.text)
new_group_name = res_dict['IdentityGroup']['name']
print('User: ' + str(user_name) + '\t\tNew group: ' + str(new_group_name))
print('-'*50)


''' Update the user's group '''
print('Update the user\'s group')
url = host+":9060/ers/config/internaluser/" + user_id
method = "PUT"
payload = {
    "InternalUser": {
        "id": user_id,
        "name": user_name,
        "identityGroups": new_group_id
    }
}
response = requests.request(
    method, url, headers=headers, data=json.dumps(payload), verify=False)
print('Response Code: ' + str(response.status_code))
# print(response.text)


res_dict = json.loads(response.text)

''' Checking if the update call has changed any fields '''
updated_fields_list = res_dict['UpdatedFieldsList']['updatedField']
print('Updated Fileds: ' + str(updated_fields_list))
summary = 'No groups has been changed'
if(len(updated_fields_list)):
    summary = 'User: ' + user_name + ' \tGroup changed: \nFrom: ' + \
        current_group_name + '\tto: ' + new_group_name
print('-'*50)


''' Print the Summary '''
print('Summary:')
print(summary)
print('-'*50)
