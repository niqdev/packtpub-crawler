from logs import *

class Notify(object):
    """
    """

    def __init__(self, config):
        self.__config = config

    def __prepare_message(self, packpub_info, upload_info):
        """
        """
        log_json(packpub_info)
        log_json(upload_info)

    def send_email(self, packpub_info, upload_info):
        """
        http://naelshiab.com/tutorial-send-email-python/
        """
        self.__prepare_message(packpub_info, upload_info)