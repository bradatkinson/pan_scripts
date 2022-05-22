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
uri = "Objects/Addresses?location=vsys&vsys=vsys1&name=Test_Object_1"
fw_ip = config.paloalto['fw_ip']
url = ("https://{}/restapi/v{}/{}".format(fw_ip, version, uri))

token = config.paloalto['key']
headers = {
    'Accept': 'application/json',
}
headers['X-PAN-KEY'] = token
payload = json.dumps({
  "entry": [
    {
      "@location": "vsys",
      "@vsys": "vsys1",
      "@name": "Test_Object_1",
      "description": "REST API Test Automation Object",
      "ip-netmask": "172.16.5.5"
    }
  ]
})

response = requests.post(url=url, headers=headers, data=payload, verify=False)

json_output = json.loads(response.text)
print(json_output)

# {'@status': 'success', '@code': '20', 'msg': 'command succeeded'}
