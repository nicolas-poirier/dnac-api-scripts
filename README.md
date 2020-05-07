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
- System Args
  * Help section
```
$ python dnac_get-all-configs.py --help
usage: dnac_get-all-configs.py [-h] --dnac DNAC -u USER -p PASSWORD
                               [-v {True,False}]

Backup all configuration files from equipments in Cisco DNA Center inventory

optional arguments:
  -h, --help            show this help message and exit
  --dnac DNAC           IP Address or FQDN of DNA Center Server
  -u USER, --user USER  username to authenticate on DNA Center
  -p PASSWORD, --password PASSWORD
                        password to authenticate on DNA Center
  -v {True,False}, --verify {True,False}
                        enable HTTPS certificate verification (Optional,
                        Default=True)
```

## Authors & Maintainers

* Nicolas Poirier
  * Twitter: [@NicolasPoirie19](https://twitter.com/NicolasPoirie19)
  * LinkedIn: [Nicolas Poirier](https://www.linkedin.com/in/nicolas-poirier-fr)
  * Website: [wifiblog.fr](https://wifiblog.fr)

## License

This project is licensed to you under the [GNU General Public License v3.0](./LICENSE).
