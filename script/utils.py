from termcolor import cprint
import json

import requests
from requests.exceptions import ConnectionError

def log_error(message):
    cprint(message, "red")
def log_warn(message):
    cprint(message, "yellow")
def log_info(message):
    cprint(message, "cyan")
def log_success(message):
    cprint(message, "green")
def log_json(list_dict):
    print json.dumps(list_dict, indent=2)

def current_ip_address():
    """
    Gets current IP address
    """

    try:
        response = requests.get('http://www.ip-addr.es')
        print "[*] fetching URL... {0} | {1}".format(response.status_code, response.url)
        log_success("[+] your current ip address is: {0}".format(response.text.strip()))
    except ConnectionError, e:
        print '[-] {0}'.format(e)
        log_error('[-] error internet connection, exiting...')
        exit(0)
