from logs import *
import requests

class Ifttt(object):
    """
    """

    def __init__(self, config, packpub_info, upload_info):
        self.__config = config
        self.__packpub_info = packpub_info

    def send(self):
        url = "https://maker.ifttt.com/trigger/" + self.__config.get('ifttt', 'ifttt.event_name') + "/with/key/" + self.__config.get('ifttt', 'ifttt.key')
        r = requests.post(url, data = {'value1':self.__packpub_info['title'].encode('utf-8'), 'value2':self.__packpub_info['description'].encode('utf-8')})

        log_success('[+] Notification sent to IFTTT')
