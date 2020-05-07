# dnac-api-scripts
Collection of standalone scripts I used with DNA Center APIs

## List of scripts

* dnac_get-all-configs.py
  * backup all configuration from the equipments on DNA Center Inventory

## dnac_get-all-configs

#### Prerequisites
* Cisco DNA Center
  * Release: 1.3.0.x - 1.3.3.x
* Python
  * Version 3.x

#### Usage

```
$ python dnac_get-all-configs.py --help
usage: dnac_get-all-configs.py [-h] --dnac DNAC -u USER -p PASSWORD

Backup all configuration files from equipments in Cisco DNA Center inventory

optional arguments:
  -h, --help            show this help message and exit
  --dnac DNAC           IP Address or FQDN of DNA Center Server
  -u USER, --user USER  username to authenticate on DNA Center
  -p PASSWORD, --password PASSWORD    
                        password to authenticate on DNA Center
```
