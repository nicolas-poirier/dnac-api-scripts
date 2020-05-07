"""
dnac_get-all-configs.py: Backup all configuration files from equipments in Cisco DNA Center inventory
Author: Nicolas Poirier - @NicolasPoirie19
GitHub: https://github.com/nicolas-poirier
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

from requests import get, post
import json
from base64 import b64encode
from argparse import ArgumentParser
from re import search, MULTILINE

if __name__ == '__main__':

    # script arguments
    parser: ArgumentParser = ArgumentParser(description='Backup all configuration files from equipments in Cisco DNA Center inventory')
    parser.add_argument('--dnac', help='IP Address or FQDN of DNA Center Server', type=str, required=True)
    parser.add_argument('-u', '--user', help='username to authenticate on DNA Center', type=str, required=True)
    parser.add_argument('-p', '--password', help='password to authenticate on DNA Center', type=str, required=True)
    parser.add_argument('-v', '--verify', help='enable HTTPS certificate verification (Optional, Default=True)', default="True", choices=["True","False"], type=str, required=False)
    args = parser.parse_args()

    # Basic Authentication is required in order to obtain an authentication token
    credentials = b64encode((args.user + ":" + args.password).encode()).decode()
    headers = {"Content-Type": "application/json", 'Authorization': "Basic "+ credentials}
    if args.verify:
        response = post(f"https://{args.dnac}/dna/system/api/v1/auth/token", data="", headers=headers)
    else:
        response = post(f"https://{args.dnac}/dna/system/api/v1/auth/token", data="", headers=headers, verify=False)

    # if the authentication is successful, the Token is saved
    if response.status_code != 200:
        raise ConnectionError(f'POST /dna/api/system/v1/auth/token {response.status_code}')
    else:
        dnac_token = response.json()["Token"]
    
    # New header with authentication Token
    headers = {"Content-Type": "application/json", "x-auth-token": dnac_token}
    # GET Request to get device configuration from DNA Center
    if args.verify:
        response = get(f"https://{args.dnac}/dna/intent/api/v1/network-device/config", data="", headers=headers)
    else:
        response = get(f"https://{args.dnac}/dna/intent/api/v1/network-device/config", data="", headers=headers, verify=False)
    
    if response.status_code == 200:
        counter = 1
        for device in response.json()["response"]:
            # Find device hostname with classic IOS syntax
            hostname = search(r"^hostname ([a-zA-Z0-9\-_]*$)",device["runningConfig"], MULTILINE)
            if hostname:
                hostname = hostname.group(1)
            # if hostname not found, the device is called "UNKNOWN-xx"
            else:
                hostname = f"UNKNOWN-{str(counter).zfill(2)}"
                counter += 1
            # Create configuration file     
            with open(f"{hostname}.txt", "w") as config_file:
                config_file.write(device["runningConfig"])