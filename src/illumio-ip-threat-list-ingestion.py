#!/usr/bin/env python3
#
#   Copyright 2019 Illumio, Inc.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import getopt
import os
import sys
import requests
import urllib.request
import config


def pce_request(pce, org_id, key, secret, verb, path, params=None,
                data=None, json=None, extra_headers=None):
    url = os.path.join(pce, 'orgs', org_id, path)
    headers = {
        'user-agent': 'illumio-ip-threat-list-ingestion',
        'accept': 'application/json',
    }
    response = requests.request(verb, url, auth=(key, secret), headers=headers, params=params, json=json, data=data)
    return response


def update_illumio_policies(malicious_ips):
    pce_api = int(os.getenv('ILO_API_VERSION', 2))
    pce = os.path.join('https://' + os.environ['ILO_SERVER'] + ':' + os.environ['ILO_PORT'], 'api', 'v%d' % pce_api)
    org_id = os.environ['ILO_ORG_ID']
    key = 'api_' + os.environ['ILO_API_KEY_ID']
    secret = os.environ['ILO_API_KEY_SECRET']
    ip_list = os.environ['THREAT_LIST_KEY']
    ip_list_href = 'sec_policy/draft/ip_lists/' + str(ip_list)
    response = pce_request(pce, org_id, key, secret, 'GET', ip_list_href).json()
    pce_ip_list = []
    for ip_obj in response['ip_ranges']:
        pce_ip_list.append(ip_obj.get('from_ip', None))
        pce_ip_list.append(ip_obj.get('to_ip', None))
    if len(response['ip_ranges']) > 3:
        print('current pce ip threat list: [', response['ip_ranges'][0]['from_ip'], ',', response['ip_ranges'][1]['from_ip'],
              '...<snip>...', response['ip_ranges'][-1]['from_ip'], ']')
    else:
        print('current pce ip threat list: ', [x.get('from_ip') for x in response['ip_ranges']])
    duplicate_ip_list = []

    for ip in malicious_ips:
        exclude_ip = {
            'from_ip': ip,
            'exclusion': True
        }
        if exclude_ip not in response['ip_ranges'] and exclude_ip['from_ip'] not in pce_ip_list:
            response['ip_ranges'].append(exclude_ip)
        else:
            duplicate_ip_list.append(exclude_ip['from_ip'])
    if len(duplicate_ip_list) > 3:
        print('duplicate ips found in new list: [', duplicate_ip_list[0], ',', duplicate_ip_list[1],
              '...<snip>...', duplicate_ip_list[-1], ']')
    elif len(duplicate_ip_list) > 0:
        print('duplicate ips found in new list: ', duplicate_ip_list)
    else:
        print('No duplicate ips found in new list')
    request_body = {
        'name': response['name'],
        'description': response['description'],
        'ip_ranges': response['ip_ranges']
    }
    resp = pce_request(pce, org_id, key, secret, 'PUT', ip_list_href, json=request_body)
    if resp.status_code == 204:
        print('ip threat list successfully updated in draft version, trying to provision now.')
        policy_href = '/orgs/' + str(org_id) + '/' + ip_list_href
        body = {
            "update_description": "Adding IPs to threat list",
            "change_subset": {
                "ip_lists": [{
                    "href": policy_href
                }]
            }
        }
        res = pce_request(pce, org_id, key, secret, 'POST', 'sec_policy', json=body)
        if res.status_code == 201:
            print('ip threat list successfully provisioned.')
        else:
            print('ip threat list provisioning failed, returned http code: ', res.status_code)
    else:
        print('ip threat list failed to update, returned http code: ', resp.status_code)


def get_malicious_ips(ip_threat_list_url):
    malicious_ips = []
    malicious_data = urllib.request.urlopen(ip_threat_list_url)
    for line in malicious_data:
        if str(line.decode("utf-8").split()[0]) != "#" and str(line.decode("utf-8").split()[0]) != '\n':
            malicious_ips.append(line.decode("utf-8").split()[0])
    if malicious_ips != []:
        print("Successfully fetched threat list")
    else:
        print('Error while fetching IP threat list ', urllib.error.URLError)
        sys.exit(4)
    return malicious_ips


def main():
    ip_threat_list_url = ''
    for ip_threat_list_url in config.threat_list:
        print('ip threat list url is: ', ip_threat_list_url)
        malicious_ips = get_malicious_ips(ip_threat_list_url)
        update_illumio_policies(malicious_ips)


if __name__ == "__main__":
    main()
