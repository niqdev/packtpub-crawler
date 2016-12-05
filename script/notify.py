from gmail import Gmail
from ifttt import Ifttt
from join import Join
from logs import *

SERVICE_GMAIL = 'gmail'
SERVICE_IFTTT = 'ifttt'
SERVICE_JOIN = 'join'

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
            self.service = Ifttt(config, packpub_info, upload_info)
        elif service_type == SERVICE_JOIN:
            self.service = Join(config, packpub_info, upload_info)

    def run(self):
        """
        """
        self.service.send()
