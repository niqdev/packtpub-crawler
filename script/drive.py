from os.path import exists
import webbrowser
from oauth2client.client import flow_from_clientsecrets, OOB_CALLBACK_URN
from oauth2client.file import Storage
import httplib2
import magic
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from utils import thread_loader
from logs import *

class Drive(object):
    """
    """

    def __init__(self, config):
        self.__config = config
        self.__drive_service = None
        self.info = {}

    def __guess_info(self, file_path):
        if not exists(file_path):
            raise IOError('file not found!')

        self.info = {
            'path': file_path,
            'name': file_path.split('/')[-1],
            'mime_type': magic.from_file(file_path, mime=True),
        }
        log_info('[+] new file upload:')
        # log_dict(self.file_info)

    def __init_service(self):
        auth_token = self.__config.get('drive', 'drive.auth_token')

        if not exists(auth_token):
            self.__save_credentials(auth_token)

        storage = Storage(auth_token)
        credentials = storage.get()

        http = httplib2.Http()
        http = credentials.authorize(http)
        self.__drive_service = build('drive', 'v2', http=http)

    def __save_credentials(self, auth_token):
        flow = flow_from_clientsecrets(
            self.__config.get('drive', 'drive.client_secrets'),
            self.__config.get('drive', 'drive.oauth2_scope'),
            OOB_CALLBACK_URN)

        authorize_url = flow.step1_get_authorize_url()

        print '[-] open browser...'
        webbrowser.open(authorize_url)

        code = raw_input('[*] Please, enter verification code: ').strip()
        credentials = flow.step2_exchange(code)

        storage = Storage(auth_token)
        storage.put(credentials)
        log_info('[+] new credentials saved')

    def __insert_file(self):
        print '[+] uploading file...'
        media_body = MediaFileUpload(
            self.info['path'], mimetype=self.info['mime_type'], resumable=True)
        body = {
            'title': self.info['name'],
            'description': 'uploaded with packtpub-crawler',
            'mimeType': self.info['mime_type']
        }
        file = self.__drive_service.files().insert(body=body, media_body=media_body).execute()
        # log_dict(file)

        print '\b[+] updating file permissions...'
        permissions = {
            'role': 'reader',
            'type': 'anyone',
            'value': self.__config.get('drive', 'drive.gmail')
        }
        self.__drive_service.permissions().insert(fileId=file['id'], body=permissions).execute()

        # self.__drive_service.files().get(fileId=file['id']).execute()

        self.info['id'] = file['id']
        self.info['download_url'] = file['webContentLink']

    def upload(self, file_path):
        self.__guess_info(file_path)
        self.__init_service()
        thread_loader(self.__insert_file)
