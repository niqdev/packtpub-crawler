from drive import Drive
from scpUpload import ScpUpload
from logs import *

SERVICE_DRIVE = 'drive'
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
        if service_type == SERVICE_DRIVE:
            self.service = Drive(config)
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
