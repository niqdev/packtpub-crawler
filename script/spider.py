"""
// setup environment
sudo easy_install pip

// lists installed modules and version
pip freeze

sudo pip install termcolor
sudo pip install beautifulsoup4
sudo pip install requests
sudo pip install requests[security]
sudo pip install clint

// run
python spider.py
python spider.py -e prod
python spider.py -h
"""

import argparse
from utils import ip_address, config_file
from packtpub import Packpub
from logs import *

def parse_types(args):
    if args.types is None:
        return [args.type]
    else:
        return args.types

def main():
    parser = argparse.ArgumentParser(\
        description='Download FREE eBook every day from www.packtpub.com', \
        formatter_class=argparse.ArgumentDefaultsHelpFormatter, \
        version='0.2')

    parser.add_argument('-c', '--config', required=True, help='configuration file')
    parser.add_argument('-d', '--dev', action='store_true')
    parser.add_argument('-e', '--extras', action='store_true')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--type', choices=['pdf', 'epub', 'mobi'], \
        default='pdf', help='ebook type')
    group.add_argument('-a', '--all', dest='types', action='store_const', \
        const=['pdf', 'epub', 'mobi'])

    args = parser.parse_args()

    try:
        #ip_address()
        config = config_file(args.config)
        types = parse_types(args)

        packpub = Packpub(config, args.dev)
        packpub.run()
        log_json(packpub.info)

        packpub.download_ebooks(types)
        if args.extras:
            packpub.download_extras()

    except KeyboardInterrupt:
        log_error('[-] interrupted manually')
    except Exception as e:
        log_debug(e)
        log_error('[-] something weird occurred, exiting...')

if __name__ == '__main__':
    main()
