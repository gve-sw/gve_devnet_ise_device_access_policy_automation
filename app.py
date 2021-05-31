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
from flask import Flask, render_template, request
import json
import requests
import base64
import urllib3
urllib3.disable_warnings()
app = Flask(__name__)


'''Global variables used to for the request'''
user_id = ''
user_name = ''
current_group_name = ''
list_of_groups = []
new_group_name = ''

''' ISE Environment '''
host = HOST
user = USERNAME
password = PASSWORD

''' Setup ISE credintials '''
creds = str.encode(user+':'+password)
encodedAuth = bytes.decode(base64.b64encode(creds))
payload = {}
headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': 'Basic ' + encodedAuth
}

''' Gathering ISE info, users and groups '''
def collect_ise_info():
    # Getting global variables
    global user_id
    global user_name
    global current_group_name
    global list_of_groups

    print('-'*25+' Collecting ISE info started ' + '-'*25)

    ''' ISE API: Get-All internal users '''
    print('Get-All internal users')
    url = host+":9060/ers/config/internaluser"
    method = "GET"
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)
    # print('-'*50)

    ''' print the list of users '''
    print('List of users:')
    res_dict = json.loads(response.text)
    internal_users = res_dict['SearchResult']['resources']
    for user in internal_users:
        user_name = user['name']
        user_id = user['id']
        print('name: ' + str(user_name) + '\t\tid: ' + str(user_id))
    print('-'*50)

    ''' ISE API: Get-ByID user's details, to store the current group id '''
    # print('User\'s current details:')
    url = host+":9060/ers/config/internaluser/" + user_id
    method = "GET"
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)
    # print('-'*50)

    ''' store the current group's id '''
    res_dict = json.loads(response.text)
    current_group_id = res_dict['InternalUser']['identityGroups']

    ''' ISE API: Get-ByID the group's details, to store its name '''
    # print('User\'s current group details:')
    url = host+":9060/ers/config/identitygroup/" + current_group_id
    method = "GET"
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)
    # print('-'*50)

    ''' store the current group's name '''
    res_dict = json.loads(response.text)
    current_group_name = res_dict['IdentityGroup']['name']
    print('Selected user: ')
    print('User: ' + str(user_name) +
          '\t\tCurrent group: ' + str(current_group_name))
    print('-'*50)

    ''' ISE API: Get-All identitygroup, to list the groups for the user to request the change '''
    # print('Get all groups:')
    url = host+":9060/ers/config/identitygroup"
    method = "GET"
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)
    # print('-'*50)

    ''' reading the list of groups '''
    print('List of groups:')
    res_dict = json.loads(response.text)
    all_groups = res_dict['SearchResult']['resources']
    for group in all_groups:
        print('\tName: ' + group['name'])
        print('\t' + '_'*25)
        list_of_groups.append(group['name'])
    print('-'*50)


''' Updating the user's identity group '''
def change_user_group(user_id, new_group_id):
    ''' ISE API: Get-ByID the group's details, to store its name '''
    # print('User\'s current group details:')
    url = host+":9060/ers/config/identitygroup/" + new_group_id
    payload = {}
    method = "GET"
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)
    # print('-'*50)

    ''' Getting the new group's name '''
    # print('Getting the new group\'s name')
    res_dict = json.loads(response.text)
    new_group_name = res_dict['IdentityGroup']['name']
    print('User: ' + str(user_name) +
          '\t\tMoving to group: ' + str(new_group_name))
    print('-'*50)

    ''' ISE API: Update an internaluser's group '''
    # print('Update the user\'s group')
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
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)

    ''' Checking if the update call has changed any fields '''
    res_dict = json.loads(response.text)
    updated_fields_list = res_dict['UpdatedFieldsList']['updatedField']
    print('Updated Fileds: ' + str(updated_fields_list))
    summary = 'No groups has been changed'
    if(len(updated_fields_list)):
        summary = 'User: ' + user_name + ' \tGroup changed: \nFrom: ' + \
            current_group_name + '\tto: ' + new_group_name

    ''' Print the Summary '''
    print('Summary:')
    print(summary)
    print('-'*50)


''' Getting the group id by passing a group's name '''
def get_group_id(group_name):
    # print('Getting the group id for: ' + group_name)
    ''' ISE API: Get-All identitygroup, to list the groups for the user to request the change '''
    # print('Get all groups:')
    url = host+":9060/ers/config/identitygroup"
    method = "GET"
    response = requests.request(
        method, url, headers=headers, data=payload, verify=False)
    # print('Response Code: ' + str(response.status_code))
    # print(response.text)
    # print('-'*50)

    ''' reading the list of groups '''
    res_dict = json.loads(response.text)
    all_groups = res_dict['SearchResult']['resources']
    for group in all_groups:
        if group['name'] == group_name:
            # print('\tName: ' + group['name'])
            # print('\tid: ' + group['id'])
            # print('\t' + '_'*25)
            return group['id']
    return 'no_id_found'


''' Handling the web application's routes '''
# Default route
@app.route('/')
def index():
    return render_template('index.html', user_name=user_name, current_group_name=current_group_name, list_of_groups=list_of_groups)


# Route when a request is submitted
@app.route('/request_submition', methods=['POST'])
def request_submition():
    global user_id
    global new_group_name
    global current_group_name
    print('Change request has been recieved')
    # Read the request details from the web form
    user = request.form['user_name']
    new_group_name = request.form['new_group_name']
    print('Data:\tUser: ' + user + '\tRequested group: ' + new_group_name)

    new_group_id = get_group_id(new_group_name)

    approve = input('Approve? (Y/N): ')
    # Update the user group, once approved
    if (approve == 'Y') or (approve == 'y'):
        change_user_group(user_id, new_group_id)
        current_group_name = new_group_name
    return 'success'


# Gathering ISE info, users and groups
collect_ise_info()


''' Starting Flask web application '''
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, debug=False, threaded=True)
