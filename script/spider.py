'''
// setup environment
sudo easy_install pip

// lists installed modules and version
pip freeze

sudo pip install termcolor
sudo pip install beautifulsoup4
sudo pip install requests

// run
python spider.py
python spider.py -h
'''

import argparse
import ConfigParser
from utils import *

def do_login():
    login_soup = make_soup(BASE_DEV_URL + LOGIN_DEV_URL, DELAY_REQUEST)

def parse_environment(param):
    """
    Parse environment: default is development
    """
    environment = 'config/dev.cfg'

    if param and param.strip() == 'prod':
        environment = 'config/prod.cfg'

    log_info('[*] init environment: ' + environment)
    
    config = ConfigParser.ConfigParser()
    return config.read(environment)

def main():
    parser = argparse.ArgumentParser(description='Download FREE eBook every day from www.packtpub.com', version='0.1')
    parser.add_argument('-e', '--environment', dest='environment', default='dev', help='configuration environment')
    args = parser.parse_args()

    try:
        config = parse_environment(args.environment)
        #current_ip_address()
        #do_login()

    except KeyboardInterrupt:
        log_error('[-] interrupted manually')
    except Exception as e:
        log_warn('[-] {0}'.format(e))
        log_error('[-] something weird occurred, exiting...')

if __name__ == '__main__':
    main()
