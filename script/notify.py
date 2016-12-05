from gmail import Gmail
from logs import *

SERVICE_GMAIL = 'gmail'
SERVICE_IFTTT = 'ifttt'

class Notify(object):
    """
    TODO interface or abstract class for notification services
    """

    def __init__(self, config, packpub_info, upload_info, service_type):
        self.__config = config
        self.info = {
            'details': []
        }
        if service_type == SERVICE_GMAIL:
            self.service = Gmail(config, packpub_info, upload_info)
        elif service_type == SERVICE_IFTTT:
            raise NotImplementedError('not implemented yet!')

    def run(self):
        """
        """
        self.service.send()
