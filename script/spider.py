#!/bin/env python

import argparse
from utils import ip_address, config_file
from packtpub import Packpub
from upload import Upload, SERVICE_DRIVE, SERVICE_DROPBOX, SERVICE_SCP
from database import Database, DB_FIREBASE
from logs import *
from notify import Notify, SERVICE_GMAIL, SERVICE_IFTTT, SERVICE_JOIN

def parse_types(args):
    if args.types is None:
        return [args.type]
    else:
        return args.types

def main():
    parser = argparse.ArgumentParser(
        description='Download FREE eBook every day from www.packtpub.com',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        version='2.0.0')

    parser.add_argument('-c', '--config', required=True, help='configuration file')
    parser.add_argument('-d', '--dev', action='store_true', help='only for development')
    parser.add_argument('-e', '--extras', action='store_true', help='download source code (if exists) and book cover')
    parser.add_argument('-u', '--upload', choices=[SERVICE_DRIVE, SERVICE_DROPBOX, SERVICE_SCP], help='upload to cloud')
    parser.add_argument('-a', '--archive', action='store_true', help='compress all file')
    parser.add_argument('-n', '--notify', choices=[SERVICE_GMAIL, SERVICE_IFTTT, SERVICE_JOIN], help='notify after download')
    parser.add_argument('-s', '--store', choices=[DB_FIREBASE], help='store info')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-t', '--type', choices=['pdf', 'epub', 'mobi'],
        default='pdf', help='specify eBook type')
    group.add_argument('--all', dest='types', action='store_const',
        const=['pdf', 'epub', 'mobi'], help='all eBook types')

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

        if args.archive:
            raise NotImplementedError('not implemented yet!')

        upload = None
        if args.upload is not None:
            upload = Upload(config, args.upload)
            upload.run(packpub.info['paths'])

        if upload is not SERVICE_DRIVE:
            log_warn('[-] skip store info: missing upload info')
        elif args.store is not None:
            Database(config, args.store, packpub.info, upload.info).store()

        if args.notify:
            upload_info = None

            if upload is not None:
                upload_info = upload.info

            Notify(config, packpub.info, upload_info, args.notify).run()

    except KeyboardInterrupt:
        log_error('[-] interrupted manually')
    except Exception as e:
        log_debug(e)
        log_error('[-] something weird occurred, exiting...')

if __name__ == '__main__':
    print ("""
         __             __         __           __           __    __        __
        /\ \     __    /\ \       /\ \         /\ \         /\ \  /\ \    _ / /\\
       /  \ \   /\_\   \ \ \     /  \ \       /  \ \____   /  \ \ \ \ \  /_/ / /
      / /\ \ \_/ / /   /\ \_\   / /\ \ \     / /\ \_____\ / /\ \ \ \ \ \ \___\/
     / / /\ \___/ /   / /\/_/  / / /\ \ \   / / /\/___  // / /\ \_\/ / /  \ \ \\
    / / /  \/____/   / / /    / / /  \ \_\ / / /   / / // /_/_ \/_/\ \ \   \_\ \\
   / / /    / / /   / / /    / / / _ / / // / /   / / // /____/\    \ \ \  / / /
  / / /    / / /   / / /    / / / /\ \/ // / /   / / // /\____\/     \ \ \/ / /
 / / /    / / /___/ / /__  / / /__\ \ \/ \ \ \__/ / // / /______      \ \ \/ /
/ / /    / / //\__\/_/___\/ / /____\ \ \  \ \___\/ // / /_______\      \ \  /
\/_/     \/_/ \/_________/\/________\_\/   \/_____/ \/__________/       \_\/

Download FREE eBook every day from www.packtpub.com
@see github.com/niqdev/packtpub-crawler
        """)
    main()
