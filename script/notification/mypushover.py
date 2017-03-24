from logs import *
import requests
from pushover import Client

class Pushover(object):
    """
    """

    def __init__(self, config, packpub_info, upload_info):
        self.__config = config
        self.__packpub_info = packpub_info
        self.__client = Client(self.__config.get('pushover', 'pushover.user_key'), api_token=self.__config.get('pushover', 'pushover.api_key'))


    def send(self):
        self.__client.send_message(self.__packpub_info['description'].encode('utf-8'), title="New book downloaded from Packt: " + self.__packpub_info['title'].encode('utf-8'), url="https://www.packtpub.com/packt/offers/free-learning", url_title="See more")
        log_success('[+] notification sent to pushover')

    def sendError(self, exception, source):
        self.__client.send_message(repr(exception), title='packtpub-crawler {source}: Could not download ebook'.format(source=source))
        log_success('[+] error notification sent to pushover')
