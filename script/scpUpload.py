from os.path import exists
import webbrowser
import httplib2
import magic
from utils import thread_loader
from logs import *
import paramiko
from scp import SCPClient

class ScpUpload(object):
    """
    """

    def __init__(self, config):
        self.__config = config
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

    def __insert_file(self):
        print '[+] uploading file...'
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # get config settings
        host = self.__config.get('drive', 'scp.host')
        user = self.__config.get('drive', 'scp.user')
        password = self.__config.get('drive', 'scp.password')
        timeout = self.__config.get('drive', 'scp.timeout')
        remotePath = self.__config.get('drive', 'scp.path')

        ssh.connect(host, username=user, password=password)
        scpclient = SCPClient(ssh.get_transport(), socket_timeout=float(timeout))
        scpclient.put(self.info['path'], remotePath+self.info['name'])

    def upload(self, file_path):
        self.__guess_info(file_path)
        thread_loader(self.__insert_file)
