#!/usr/bin/env python3
#
#  AUTHOR: Brad Atkinson
#    DATE: 2/10/2022
# PURPOSE: To test PAN REST API

import requests
import json
import config

requests.packages.urllib3.disable_warnings()

version = "10.0"
uri = "Objects/Tags?location=vsys&vsys=vsys1&name=Xbox"
fw_ip = config.paloalto['fw_ip']
url = ("https://{}/restapi/v{}/{}".format(fw_ip, version, uri))

token = config.paloalto['key']
headers = {
    'Accept': 'application/json',
}
headers['X-PAN-KEY'] = token

response = requests.get(url=url, headers=headers, verify=False)

json_output = json.loads(response.text)
result_dict = json_output.get('result')
entry_dict = result_dict.get('entry')[0]

total_count = result_dict.get('@total-count')
tag_name = entry_dict.get('@name')
color = entry_dict.get('color')

print('\nTotal Count: {}\n'.format(total_count))
print('Tag Name: {}'.format(tag_name))
print('Color: {}\n'.format(color))
