from googledrive import GoogleDrive
from onedrive import OneDrive
from scpUpload import ScpUpload
from logs import *

SERVICE_GOOGLE_DRIVE = 'googledrive'
SERVICE_ONEDRIVE = 'onedrive'
SERVICE_DROPBOX = 'DROPBOX'
SERVICE_SCP = 'scp'

class Upload(object):
    """
    TODO interface or abstract class for upload services
    """

    def __init__(self, config, service_type):
        self.__config = config
        self.info = {
            'details': []
        }
        if service_type == SERVICE_GOOGLE_DRIVE:
            self.service = GoogleDrive(config)
        elif service_type == SERVICE_ONEDRIVE:
            self.service = OneDrive(config)
        elif service_type == SERVICE_DROPBOX:
            raise NotImplementedError('not implemented yet!')
        elif service_type == SERVICE_SCP:
            self.service = ScpUpload(config)

    def run(self, paths):
        """
        """
        for path in paths:
            self.service.upload(path)
            self.info['details'].append(self.service.info)
            log_dict(self.service.info)
