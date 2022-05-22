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
uri = "Policies/SecurityRules?location=vsys&vsys=vsys1&name=Python Dev"
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
rule_name = entry_dict.get('@name')
src_zone = entry_dict.get('to').get('member')
dst_zone = entry_dict.get('from').get('member')
src_addr = entry_dict.get('source').get('member')
dst_addr = entry_dict.get('destination').get('member')
app = entry_dict.get('application').get('member')
service = entry_dict.get('service').get('member')
action = entry_dict.get('action')
tag = entry_dict.get('tag').get('member')

print('\nTotal Count: {}\n'.format(total_count))
print('Policy Name: {}'.format(rule_name))
print('Src Zone: {}'.format(src_zone))
print('Dst Zone: {}'.format(dst_zone))
print('Src Address: {}'.format(src_addr))
print('Dst Address: {}'.format(dst_addr))
print('Application: {}'.format(app))
print('Service: {}'.format(service))
print('Action: {}'.format(action))
print('Tag: {}\n'.format(tag))
