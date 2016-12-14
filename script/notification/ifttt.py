from logs import *
import requests

class Ifttt(object):
    """
    """

    def __init__(self, config, packpub_info, upload_info):
        self.__packpub_info = packpub_info
        self.__url = "https://maker.ifttt.com/trigger/{eventName}/with/key/{apiKey}".format(
            eventName=config.get('ifttt', 'ifttt.event_name'),
            apiKey=config.get('ifttt', 'ifttt.key')
        )

    def send(self):
        r = requests.post(self.__url, data = {'value1':self.__packpub_info['title'].encode('utf-8'), 'value2':self.__packpub_info['description'].encode('utf-8')})
        log_success('[+] notification sent to IFTTT')

    def sendError(self, exception, source):
        title = "packtpub-crawler [{source}]: Could not download ebook".format(source=source)
        r = requests.post(self.__url, data = {'value1':title, 'value2':repr(exception)})

        log_success('[+] error notification sent to IFTTT')
