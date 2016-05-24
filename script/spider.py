import argparse
from utils import ip_address, config_file
from packtpub import Packpub
from upload import Upload, SERVICE_DRIVE, SERVICE_DROPBOX
from notify import Notify
from logs import *

def parse_types(args):
    if args.types is None:
        return [args.type]
    else:
        return args.types

def main():
    parser = argparse.ArgumentParser(
        description='Download FREE eBook every day from www.packtpub.com',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        version='1.0')

    parser.add_argument('-c', '--config', required=True, help='configuration file')
    parser.add_argument('-d', '--dev', action='store_true', help='only for development')
    parser.add_argument('-e', '--extras', action='store_true', help='download source code (if exists) and book cover')
    parser.add_argument('-u', '--upload', choices=[SERVICE_DRIVE, SERVICE_DROPBOX], help='upload to cloud')
    parser.add_argument('-a', '--archive', action='store_true', help='compress all file')
    parser.add_argument('-n', '--notify', action='store_true', help='notify via email')

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

        if args.notify:
            if upload is not None:
                Notify(config, packpub.info, upload.info).send_email()
            else:
                log_warn('[-] skip notification: missing upload info')

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
