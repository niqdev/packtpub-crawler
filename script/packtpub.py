import ConfigParser
import urllib
import requests
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

        #soup = make_soup(base_url + login_url, delay, True)
        soup = make_soup(base_url + login_url)

        form = soup.find('form', {'id': 'packt-user-login-form'})
        #print form.find_all('input', attrs={'name': 'form_build_id'}, limit=1)[0]['value']
        #print form.find('input', attrs={'name': 'form_build_id'})['value']
        #print form.find('input', attrs={'name': 'form_id'})['value']

        payload = {
            'email': self.__config.get('credential', 'credential.email'),
            'password': self.__config.get('credential', 'credential.password'),
            'op': 'Login',
            'form_build_id': form.find('input', attrs={'name': 'form_build_id'})['value'],
            'form_id': form.find('input', attrs={'name': 'form_id'})['value'],
        }

        print urllib.urlencode(payload)
