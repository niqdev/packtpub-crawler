import ConfigParser
from utils import make_soup
from logs import *

class Packpub(object):
    """
    """

    def __init__(self, path):
        self.__config = self.__init_config(path)

    def __init_config(self, path):
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config

    def login(self):
        base_url = self.__config.get('url', 'url.base')
        login_url = self.__config.get('url', 'url.login')
        delay = float(self.__config.get('delay', 'delay.login'))

        soup = make_soup(base_url + login_url, delay, True)
