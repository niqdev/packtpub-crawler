from logs import *
import requests

class Join(object):
    """
    """

    def __init__(self, config, packpub_info, upload_info):
        self.__config = config
        self.__packpub_info = packpub_info

    def send(self):
        url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?apikey={apiKey}&deviceId={deviceIds}&title={title}&text={description}".format(
            apiKey=self.__config.get('join', 'join.api_key'),
            deviceIds=self.__config.get('join', 'join.device_ids'),
            title="New book downloaded from Packt: " + self.__packpub_info['title'].encode('utf-8'),
            description=self.__packpub_info['description'].encode('utf-8')
        )

        r = requests.post(url)

        log_success('[+] Notification sent to Join')

    def sendError(self, exception):
        url = "https://joinjoaomgcd.appspot.com/_ah/api/messaging/v1/sendPush?apikey={apiKey}&deviceId={deviceIds}&title={title}&text={description}".format(
            apiKey=self.__config.get('join', 'join.api_key'),
            deviceIds=self.__config.get('join', 'join.device_ids'),
            title='packtpub-crawler: Could not download ebook',
            description=repr(exception)
        )

        r = requests.post(url)

        log_success('[+] Notification sent to Join')
