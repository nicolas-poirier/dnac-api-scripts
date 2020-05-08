[![published](https://static.production.devnetcloud.com/codeexchange/assets/images/devnet-published.svg)](https://developer.cisco.com/codeexchange/github/repo/nicolas-poirier/dnac-api-scripts)

# dnac-api-scripts
Collection of standalone scripts I used with DNA Center APIs.  
You can follow the repository as new scripts will be added over time.  

## List of scripts

* [dnac_get-all-configs.py](https://github.com/nicolas-poirier/dnac-api-scripts/blob/master/README.md#dnac_get-all-configs)
  * backup all configuration from the equipments on DNA Center Inventory

## dnac_get-all-configs

#### Prerequisites
* Cisco DNA Center
  * Release: 1.3.0.x - 1.3.3.x
* Python
  * Version 3.x

#### Demo using Cisco DNA Center Sandbox
* https://sandboxdnac.cisco.com/
  * user: devnetuser
  * password: Cisco123!

While running the demo, there was 4 devices in DNA Center Inventory.  
After the execution of the script, the 4 configuration files for these equipements are saved along the script.

![](./demo-scripts/demo-dnac_get-all-configs.gif)
_(running with https://sandboxdnac.cisco.com/)_

#### Usage
- When using the script for the first time
  - First, download or clone this repository
    - ``` git clone https://github.com/nicolas-poirier/dnac-api-scripts.git ```
  - Go to the cloned repository directory
    - ``` cd dnac-api-scripts ```
  - Install Python required packages using the requirements file
    - ``` pip install -r requirements.txt ```

***You are now ready to use the script!***

- System Args
  * Help section:
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
