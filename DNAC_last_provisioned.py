"""
dnac_last_provisioned.py: Display the last provisioned date of all devices in Catalyst Center
Author: Nicolas Poirier - @NicolasPoirie19
GitHub: https://github.com/nicolas-poirier
License: GNU GENERAL PUBLIC LICENSE Version 3
"""

import time
import datetime
import requests
from requests.packages import urllib3
from requests.auth import HTTPBasicAuth
from argparse import ArgumentParser
from alive_progress import alive_bar

# Désactivation des warnings liés à l'usage d'un certificat auto-signé sur Catalyst Center
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Info DNAC utilisées par défaut si rien de fourni en entrée du script
# Ici les infos de la sandbox Devnet Cisco (voir https://developer.cisco.com/)
default_dnac_url = "10.10.20.85"
default_dnac_username = "admin"
default_dnac_password = "Cisco1234!"

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

# Fonction filtre dispo, pas utilisé ici, mais permet de ne pas collecter tous les équipements du DNAC à chaque fois
def get_device_uuid(dnac_url, token, filter="."):
    print("[+] Retrieving the list of devices UUID from Catalyst Center")
    response = requests.get(
        f'https://{dnac_url}//dna/intent/api/v1/network-device',
        headers={
            'X-Auth-Token': '{}'.format(token),
            'Content-type': 'application/json',
        },
        verify=False
    )
    # On créé une liste de liste contenant les uuid et hostname de chaque équioement
    uuid_list = []
    for device in response.json()['response']:
        uuid_list.append([device['id'], device['hostname']])
        print(f"     Device Found: {device['hostname']} with the UUID {device['id']}")
    return uuid_list

#Pour une liste de device UUID fournit, colecte du hostname et du dernier device provisioning (lastUpdateTime)
# Si pas de provisioning, on renvoit 0 (epoch time) comme date du dernier provisioning
def get_all_cfs_device_info(dnac_url, dnac_token, list_of_device_uuids):
    print("[+] Searching the last provisioned date for each device")
    all_cfs_info = []
    with alive_bar(total=(len(list_of_device_uuids)), bar="filling", spinner="waves", dual_line="true", title="Getting devices UUID") as bar:
        for device_uuid in list_of_device_uuids:            
            #print(f"[--] Searching device UUID {device_uuid[0]}")            
            response = requests.get(
        f'https://{dnac_url}/api/v2/data/customer-facing-service/DeviceInfo?networkDeviceId={device_uuid[0]}',
        headers={
            'X-Auth-Token': '{}'.format(dnac_token),
            'Content-type': 'application/json',
        },
        verify=False
    )
            cfs_device_info = response.json()['response']
            if len(cfs_device_info) == 0:
                all_cfs_info.append([{'id': device_uuid[0], 'name': device_uuid[1], 'lastUpdateTime': 0}])
            else:
                all_cfs_info.append(cfs_device_info)
            bar()           
        return all_cfs_info
    
def make_epoch_time_human_readable(epoch_timestamp_in_ms: int) -> str:
    epoch_timestamp_divided = epoch_timestamp_in_ms / 1000.0
    human_readable_time = time.strftime('%d %b %Y %I:%M:%S %p', time.localtime(epoch_timestamp_divided))
    return human_readable_time

def print_last_provisioned(hostname, epoch_timestamp_in_ms):
    human_readable_time = make_epoch_time_human_readable(epoch_timestamp_in_ms)
    print(f'{hostname} was last provisioned: {human_readable_time}\n')

def last_provisioned(device_hostname, epoch_timestamp_in_ms):    
    if epoch_timestamp_in_ms == 0:
        print(f'[--] {device_hostname} has not been provisioned yet')
    else:
        seconds = epoch_timestamp_in_ms / 1000.0
        date_and_time = datetime.date.fromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S.%f')    
        print(f'[--] {device_hostname} last Time Provisioned:', date_and_time)

        # Get Current Time from epoch in ms
        the_time = time.time()
        the_time_in_ms = int(the_time * 1000)
        # Get Number of Seconds Difference between last_provisioned and now
        time_diff = the_time_in_ms - epoch_timestamp_in_ms
        # Do the Monster Math
        time_var = time_diff / 1000
        one_day = int(time_var // (24 * 3600))
        time_var = time_var % (24 * 3600)
        one_hour = int(time_var // 3600)
        time_var %= 3600
        one_minute = int(time_var // 60)
        time_var %= 60
        one_second = int(time_var)
        print(f"{one_day} days, {one_hour} hours, {one_minute} minutes, {one_second} seconds ago\n")

if __name__ == '__main__':

    # script arguments
    parser: ArgumentParser = ArgumentParser(description='Display the last provisioned date of all devices in Catalyst Center')
    parser.add_argument('--dnac', help='IP Address or FQDN of Catalyst Center Server', type=str, default=default_dnac_url, required=False)
    parser.add_argument('-u', '--user', help='username to authenticate on Catalyst Center', type=str, default=default_dnac_username, required=False)
    parser.add_argument('-p', '--password', help='password to authenticate on Catalyst Center', type=str, default=default_dnac_password, required=False)
    parser.add_argument('-v', '--verify', help='enable HTTPS certificate verification (Optional, Default=True)', default="True", choices=["True","False"], type=str, required=False)
    args = parser.parse_args()

    dnac_token = get_token(args.dnac, args.user, args.password)
    UUID_list = get_device_uuid(args.dnac, dnac_token)

    all_cfs_info = get_all_cfs_device_info(args.dnac, dnac_token, UUID_list)
    for result in all_cfs_info:
        try:
            hostname = result[0]['name']
            epoch_timestamp_in_ms = result[0]['lastUpdateTime']
            last_provisioned(hostname, epoch_timestamp_in_ms)
        except IndexError:
            continue
