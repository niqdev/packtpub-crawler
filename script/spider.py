"""
// setup environment
sudo easy_install pip

// lists installed modules and version
pip freeze

sudo pip install termcolor
sudo pip install beautifulsoup4
sudo pip install requests
"""

import argparse
from utils import *

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Download FREE eBook every day from www.packtpub.com", version='0.1')
    args = parser.parse_args()

    try:
        current_ip_address()

    except KeyboardInterrupt:
        log_error("[-] interrupted manually")
    except Exception as e:
        log_warn('[-] {0}'.format(e))
        log_error("[-] something weird occurred, exiting...")
