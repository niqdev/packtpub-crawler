import requests
import ConfigParser
from bs4 import BeautifulSoup
from time import sleep
from clint.textui import progress
import os, sys, itertools
from threading import Thread
from logs import *

def ip_address():
    """
    Gets current IP address
    """

    response = requests.get('http://www.ip-addr.es')
    print '[-] GET {0} | {1}'.format(response.status_code, response.url)
    log_info('[+] ip address is: {0}'.format(response.text.strip()))

def config_file(path):
    """
    Reads configuration file
    """
    if not os.path.exists(path):
        raise IOError('file not found!')

    log_info('[+] configuration file: {0}'.format(path))
    config = ConfigParser.ConfigParser()
    config.read(path)
    return config

def make_soup(response, debug=False):
    """
    Makes soup from response
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

def download_file(r, url, directory, filename):
    """
    Downloads file with progress bar
    """
    if not os.path.exists(directory):
        # creates directories recursively
        os.makedirs(directory)
        log_info('[+] created new directory: ' + directory)

    path = os.path.join(directory, filename)

    print '[-] downloading file from url: {0}'.format(url)
    response = r.get(url, stream=True)
    with open(path, 'wb') as f:
        total_length = int(response.headers.get('content-length'))
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    log_success('[+] new download: {0}'.format(path))
    return path

def thread_loader(function):
    """
    Starts a thread with loading bar
    """

    thread = Thread(target=function)
    thread.start()
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    while thread.is_alive():
        sys.stdout.write(spinner.next())
        sys.stdout.flush()
        # erase the last written char
        sys.stdout.write('\b')
