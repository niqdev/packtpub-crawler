import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from time import sleep

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

def make_soup(response, debug=False):
    """
    Make soup from response
    """

    print '[*] fetching url... {0} | {1}'.format(response.status_code, response.url)
    soup = BeautifulSoup(response.text, from_encoding=response.encoding)
    if debug:
        print soup.prettify().encode('utf-8')
    return soup

def wait(delay):
    if delay > 0:
        print '[-] going to sleep {0} seconds'.format(delay)
        sleep(delay)
