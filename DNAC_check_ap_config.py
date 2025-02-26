"""
dnac_check_ap_config.py: Collect configuration and state of Access Points from Catalyst Center
Author: Nicolas Poirier - @NicolasPoirie19
GitHub: https://github.com/nicolas-poirier
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

import requests
from requests.packages import urllib3
from requests.auth import HTTPBasicAuth
from argparse import ArgumentParser
from alive_progress import alive_bar

# Désactivation des warnings liés à l'usage d'un certificat auto-signé sur Catalyst Center
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Info DNAC utilisées par défaut si rien de fourni en entrée du script
# Ici les infos de la sandbox Devnet Cisco (voir https://developer.cisco.com/)
default_dnac_url = "198.18.129.100"
default_dnac_username = "admin"
default_dnac_password = "C1sco12345"

# Récupération du token de connexion DNAC
def get_token(dnac_url, dnac_username, dnac_password):
    print("[+] Getting a token from the Catalyst Center")
    token = requests.post(
       f'https://{dnac_url}/dna/system/api/v1/auth/token',
       auth=HTTPBasicAuth(
           username=dnac_username,
           password=dnac_password
       ),
       headers={'content-type': 'application/json'},
       verify=False,
    )
    data = token.json()
    return data['Token']

# Collecte des UUID de toutes les bornes Wi-Fi présentes sur le Catalyst Center
def get_ap_uuid(dnac_url, token):
    print("[+] Retrieving the list of Access Points' UUIDs from Catalyst Center")
    response = requests.get(
        f'https://{dnac_url}/dna/intent/api/v1/network-device?family=Unified AP',
        headers={
            'X-Auth-Token': '{}'.format(token),
            'Content-type': 'application/json',
        },
        verify=False
    )
    # On créé une liste de liste contenant les uuid et hostname de chaque équipement
    uuid_list = []
    for device in response.json()['response']:
        uuid_list.append([device['id'], device['hostname']])
        print(f"     Device Found: {device['hostname']} with the UUID {device['id']}")
    return uuid_list

def get_all_ap_info(dnac_url, dnac_token, list_of_device_uuids):
    print("[+] Collecting info about the Managed Access Points")
    all_ap_info = []
    with alive_bar(total=(len(list_of_device_uuids)), bar="filling", spinner="waves", dual_line="true", title="Getting devices UUID") as bar:
        for device_uuid in list_of_device_uuids:            
            #print(f"[--] Searching device UUID {device_uuid[0]}")            
            response = requests.get(
        f'https://{dnac_url}/dna/intent/api/v1/device-detail?identifier=uuid&searchBy={device_uuid[0]}',
        headers={
            'X-Auth-Token': '{}'.format(dnac_token),
            'Content-type': 'application/json',
        },
        verify=False
    )
            if response.status_code != 200:
                print(f"No valid response for UUID {device_uuid[0]}")                     
            else:
                cfs_ap_info = response.json()['response']                
                all_ap_info.append(cfs_ap_info)
            bar()
        return all_ap_info

if __name__ == '__main__':

    # script arguments
    parser: ArgumentParser = ArgumentParser(description='Display the last provisioned date of all devices in Catalyst Center')
    parser.add_argument('--dnac', help='IP Address or FQDN of Catalyst Center Server', type=str, default=default_dnac_url, required=False)
    parser.add_argument('-u', '--user', help='username to authenticate on Catalyst Center', type=str, default=default_dnac_username, required=False)
    parser.add_argument('-p', '--password', help='password to authenticate on Catalyst Center', type=str, default=default_dnac_password, required=False)
    parser.add_argument('-v', '--verify', help='enable HTTPS certificate verification (Optional, Default=True)', default="True", choices=["True","False"], type=str, required=False)
    args = parser.parse_args()

    dnac_token = get_token(args.dnac, args.user, args.password)
    UUID_list = get_ap_uuid(args.dnac, dnac_token)    
    
    all_ap_info = get_all_ap_info(args.dnac, dnac_token, UUID_list)
    for result in all_ap_info:
        try:
            ap_name = result['nwDeviceName']
            ap_serial = result['serialNumber']
            ap_ip_address = result['ip_addr_managementIpAddr']
            site_tag = result['siteTagName']
            policy_tag = result['policyTagName']
            ap_state = result['communicationState']
            print(f"[--] Access Point {ap_name} with Serial Number {ap_serial} state is {ap_state}")
            print(f"\tIP Address: {ap_ip_address}")
            print(f"\tPolicy Tag: {policy_tag}")
            print(f"\tSite Tag: {site_tag}\n")
        except IndexError:
            continue

