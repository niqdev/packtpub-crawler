import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
from time import sleep
import os
from clint.textui import progress

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

def download_file(r, url, directory,  filename):
    """
    Downloads file with progress bar
    """
    if not os.path.exists(directory):
        #creates directories recursively
        os.makedirs(directory)
        print '[+] created new directory: ' + directory

    filename = filename.encode('ascii', 'ignore').replace(' ', '_')
    path = os.path.join(directory, filename)

    print '[-] downloading file from url: {0}'.format(url)
    response = r.get(url, stream=True)
    with open(path, 'wb') as f:
        total_length = int(response.headers.get('content-length'))
        for chunk in progress.bar(response.iter_content(chunk_size=1024), expected_size=(total_length/1024) + 1):
            if chunk:
                f.write(chunk)
                f.flush()
    print '[+] new download: {0}'.format(path)
