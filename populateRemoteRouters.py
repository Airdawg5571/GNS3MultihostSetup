'''
Populate the Dynamips router database with remote routers.
For each remote server, duplicate each local router for use on the remote servers.

Good for GNS3 1.3.8 config file

@author: Flavius Graur (Airdawg)
'''

import json
import os
from copy import deepcopy


GNS3_CONFIG_FILE = '{0}\\GNS3\\gns3_gui.ini'.format(os.environ["APPDATA"])

config = None

with open(GNS3_CONFIG_FILE, 'r') as conf_file:
    config = json.load(conf_file)

servers = config['RemoteServers']
routers = config['Dynamips']['routers']

for router in routers:
    next_router = True
    for server in servers:

        if router['server'] == 'local':
            if next_router:
                print 'Found local router', router['name']
            next_router = False

            remote_exists = False
            for other_router in routers:
                if "{0}({1})".format(router['name'],server['host']) in other_router['name']:
                    remote_exists = True
                    break

            if remote_exists:
                break
            new_router = deepcopy(router)
            new_router['name'] = '{0}({1})'.format(new_router['name'], server['host'])
            new_router['server'] = "{0}:{1}".format(server['host'], server['port'])
            print 'Duplicating {0} for {1}'.format(router['name'], server['host'])
            routers.append(new_router)

with open(GNS3_CONFIG_FILE, "w") as conf_file:
    json.dump(config, conf_file, indent=4)
