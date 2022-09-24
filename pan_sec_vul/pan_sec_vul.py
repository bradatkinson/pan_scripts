#!/usr/bin/env python3
#
#  AUTHOR: Brad Atkinson
#    DATE: 9/23/2022
# PURPOSE: To display security vulnerability info

import json
import argparse
import requests
import prettytable
import colorama
from colorama import Fore

colorama.init(autoreset=True)


def get_request(cve):
    """Get Request

    Args:
        cve (str): A string containing the CVE ID

    Returns:
        response (str): A string containing the response
    """
    url = ('https://security.paloaltonetworks.com/json/{}'.format(cve))
    response = requests.get(url, timeout=10)
    return response


def process_results(response):
    """Process Results

    Args:
        response (str): A string containing the response
    """
    table = prettytable.PrettyTable(['Versions', 'Affected', 'Unaffected'])
    table.align = 'l'

    json_output = json.loads(response.text)

    cve_id = json_output.get('CVE_data_meta').get('ID')
    title = json_output.get('CVE_data_meta').get('TITLE')
    description = json_output.get('description').get('description_data')[0].get('value')
    solution = json_output.get('solution')[0].get('value')
    severity = json_output.get('impact').get('cvss').get('baseSeverity')
    severity_score = json_output.get('impact').get('cvss').get('baseScore')

    versions_dict = version_processing(json_output)

    for version_name in versions_dict.keys():
        version = 'PAN-OS ' + version_name
        affected = versions_dict.get(version_name).get('affected')
        unaffected = versions_dict.get(version_name).get('unaffected')
        table.add_row([version, affected, unaffected])

    print(Fore.RED+'\nTITLE: '+Fore.WHITE+'{}'.format(title))
    print(Fore.RED+'CVE ID: '+Fore.WHITE+'{}'.format(cve_id))
    print(Fore.RED+'SEVERITY & SCORE: '+Fore.WHITE+'{} - {}'.format(severity, severity_score))
    print(Fore.RED+'\nDESCRIPTION:')
    print(description)
    print(Fore.RED+'\nAFFECTS:')
    print(table)
    print(Fore.RED+'\nSOLUTION:')
    print(solution)


def version_processing(json_output):
    """Version Processing

    Args:
        json_output (dict): A dictionary of the results

    Returns:
        versions_dict (dict): A dictionary of the affected/unaffected versions
    """
    versions_dict = {}
    version_list = json_output.get('affects').get('vendor').get('vendor_data')[0].get('product').get('product_data')[0].get('version').get('version_data')
    for item_dict in version_list:
        version_name = item_dict.get('version_name') 
        version_affected = item_dict.get('version_affected')
        version_value = item_dict.get('version_value')
        if '!' in version_affected:
            version_affected = version_affected.strip('!')
            unaffected = version_affected + ' ' + version_value
            affected = 'N/A'
            if version_name in versions_dict:
                versions_dict[version_name]['unaffected'] = unaffected
            else:
                versions_dict[version_name] = {'unaffected': unaffected}
        else:
            affected = version_affected + ' ' + version_value
            unaffected = 'N/A'
            if version_name in versions_dict:
                versions_dict[version_name]['affected'] = affected
            else:
                versions_dict[version_name] = {'affected': affected}
    return versions_dict


def main():
    """Function Calls
    """
    parser = argparse.ArgumentParser(
        description='To display security vulnerability info')
    parser.add_argument('-c', '--cve',
                        required=True,
                        dest='cve_var',
                        help='CVE ID')
    args = parser.parse_args()

    response = get_request(args.cve_var)
    process_results(response)


if __name__ == '__main__':
    main()
