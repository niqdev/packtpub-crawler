from termcolor import cprint
import json
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from time import sleep

def log_error(message):
    cprint(message, 'red')
def log_warn(message):
    cprint(message, 'yellow')
def log_info(message):
    cprint(message, 'cyan')
def log_success(message):
    cprint(message, 'green')
def log_json(list_dict):
    print json.dumps(list_dict, indent=2)

def current_ip_address():
    """
    Gets current IP address
    """

    try:
        response = requests.get('http://www.ip-addr.es')
        print '[*] fetching URL... {0} | {1}'.format(response.status_code, response.url)
        log_success('[+] your current ip address is: {0}'.format(response.text.strip()))
    except ConnectionError, e:
        print '[-] {0}'.format(e)
        log_error('[-] error internet connection, exiting...')
        exit(0)

def make_soup(url, delay):
    """
    Makes soup from url
    """

    soup = None
    try:
        headers = {
            #latest version of chrome
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)

        print '[*] fetching url... {0} | {1}'.format(response.status_code, response.url)
        soup = BeautifulSoup(response.text, from_encoding=response.encoding)
        #print soup.prettify().encode('utf-8')
        sleep(delay)

    except ConnectionError, e:
        log_warn('[-] {0}'.format(e))

    if soup is None:
        log_error('[-] error while making soup, exiting...')
        exit(0)
    else:
        return soup
