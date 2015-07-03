from drive import Drive
from logs import *

SERVICE_DRIVE = 'drive'
SERVICE_DROPBOX = 'DROPBOX'

class Upload(object):
    """
    TODO interface or abstract class for upload services
    """

    def __init__(self, config, service_type):
        self.__config = config
        if service_type == SERVICE_DRIVE:
            self.service = Drive(config)
        elif service_type == SERVICE_DROPBOX:
            raise NotImplementedError('not implemented yet!')

    def run(self, paths):
        """
        """
        for path in paths:
            self.service.upload(path)
            log_dict(self.service.info)
