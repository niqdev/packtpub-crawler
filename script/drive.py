import os
import webbrowser
from oauth2client.client import flow_from_clientsecrets, OOB_CALLBACK_URN
from oauth2client.file import Storage
from logs import *

# TODO: remove
from utils import config_file

class Drive(object):
    """
    """

    def __init__(self, config):
        self.__config = config

    def __credentials(self):
        auth_token = self.__config.get('drive', 'drive.auth_token')

        if os.path.exists(auth_token):
            print '[+] file found: {0}'.format(auth_token)
            storage = Storage(auth_token)
            return storage.get()

        flow = flow_from_clientsecrets( \
            self.__config.get('drive', 'drive.client_secrets'), \
            self.__config.get('drive', 'drive.oauth2_scope'), \
            OOB_CALLBACK_URN)

        authorize_url = flow.step1_get_authorize_url()

        print '[-] open browser...'
        webbrowser.open(authorize_url)

        code = raw_input('[*] Please, enter verification code: ').strip()
        credentials = flow.step2_exchange(code)

        storage = Storage(auth_token)
        storage.put(credentials)
        return credentials

    def upload(self, filename):
        print filename
        self.__credentials()

if __name__ == '__main__':
    drive = Drive(config_file('../config/dev.cfg'))
    drive.upload('document.txt')

