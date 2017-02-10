from os.path import exists

import magic
import onedrivesdk
from onedrivesdk.helpers import GetAuthCodeServer

from logs import *
from utils import thread_loader


class OneDrive(object):
    """
    """

    def __init__(self, config):
        self.__config = config
        self.__onedrive_service = None
        self.__scopes = ['offline_access', 'onedrive.readwrite']
        self.info = {}

    def __guess_info(self, file_path):
        if not exists(file_path):
            raise IOError('file not found!')

        self.info = {
            'path': file_path,
            'name': file_path.split('/')[-1],
            'mime_type': magic.from_file(file_path, mime=True),
        }
        log_info('[+] new file upload on OneDrive:')
        log_info(self.info['name'])

    def __init_service(self):
        api_base_url = self.__config.get('onedrive', 'onedrive.api_base_url')
        client_id = self.__config.get('onedrive', 'onedrive.client_id')
        session_file = self.__config.get('onedrive', 'onedrive.session_file')

        if not exists(session_file):
            self.__save_credentials(session_file)

        http_provider = onedrivesdk.HttpProvider()
        auth_provider = onedrivesdk.AuthProvider(http_provider,
                                                client_id,
                                                self.__scopes)

        # Load the session
        auth_provider.load_session(path=session_file)
        auth_provider.refresh_token()
        self.__onedrive_service = onedrivesdk.OneDriveClient(api_base_url, auth_provider, http_provider)

    def __save_credentials(self, session_file):
        # api_base_url = self.__config.get('onedrive', 'onedrive.api_base_url')
        redirect_uri = 'http://localhost:8080/'
        client_id = self.__config.get('onedrive', 'onedrive.client_id')
        client_secret = self.__config.get('onedrive', 'onedrive.client_secret')

        client = onedrivesdk.get_default_client(client_id=client_id, scopes=self.__scopes)

        auth_url = client.auth_provider.get_auth_url(redirect_uri)

        # this will block until we have the code
        code = GetAuthCodeServer.get_auth_code(auth_url, redirect_uri)

        client.auth_provider.authenticate(code, redirect_uri, client_secret)

        # Save the session for later
        client.auth_provider.save_session(path=session_file)
        log_info('[+] new credentials saved')

    def __create_folder(self, item_id, folder_name): #Create folder with provided name
        f = onedrivesdk.Folder()
        i = onedrivesdk.Item()
        i.name = folder_name
        i.folder = f

        folder = self.__onedrive_service.item(drive='me', id=item_id).children.add(i)

        log_success('[+] creating new directory...')

        return folder.id #Return folder object ID

    def __get_folder(self): #Get folder name settings
        try: #Check folder name
            folder_name = self.__config.get('onedrive', 'onedrive.folder')
        except:
            folder_name = 'packtpub'

        item_id = 'root'
        directories = folder_name.split('/')
        for d in directories:
            if d == '.':
                continue
            try: # get folder if exists
                parent = self.__onedrive_service.item(drive='me', id=item_id)
                item = parent.children[d].get()
                item_id = item.id
            except:
                item_id = self.__create_folder(item_id, d)

        return item_id

    def __insert_file(self):
        print '[+] uploading file...'
        item = self.__onedrive_service.item(drive='me', id=self.__get_folder())
        file = item.children[self.info['name']].upload(self.info['path'])

        self.info['id'] = file.id
        self.info['download_url'] = file.web_url

    def upload(self, file_path):
        self.__guess_info(file_path)
        self.__init_service()
        thread_loader(self.__insert_file)
