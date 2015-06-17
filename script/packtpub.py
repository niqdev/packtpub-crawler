import ConfigParser
import urllib
import requests
from utils import make_soup
from utils import wait
from logs import *

class Packpub(object):
    """
    """

    def __init__(self, path):
        self.__config = self.__init_config(path)
        self.__delay = float(self.__config.get('delay', 'delay.requests'))
        self.__url_base = self.__config.get('url', 'url.base')
        self.__headers = self.__init_headers()
        self.__session = requests.Session()

    def __init_config(self, path):
        config = ConfigParser.ConfigParser()
        config.read(path)
        return config

    def __init_headers(self):
        return {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
        }

    def __GET_login(self):
        url = self.__url_base + self.__config.get('url', 'url.loginGet')

        response = self.__session.get(url, headers=self.__headers)
        print '[-] GET {0} | {1}'.format(response.url, response.status_code)

        soup = make_soup(response)
        form = soup.find('form', {'id': 'packt-user-login-form'})
        payload = {
            'form_build_id': form.find('input', attrs={'name': 'form_build_id'})['value'],
            'form_id': form.find('input', attrs={'name': 'form_id'})['value'],
        }
        return payload

    def __POST_login(self, data):
        data['email'] = self.__config.get('credential', 'credential.email')
        data['password'] = self.__config.get('credential', 'credential.password')
        data['op'] = 'Login'
        print '[-] data: {0}'.format(urllib.urlencode(data))

        url = self.__url_base + self.__config.get('url', 'url.loginPost')

        # TODO in dev use GET instead of POST
        response = self.__session.post(url, headers=self.__headers, data=data)
        print '[-] POST {0} | {1}'.format(response.url, response.status_code)
        print '[-] cookies:'
        log_dict(requests.utils.dict_from_cookiejar(self.__session.cookies))
        print '[-] headers:'
        log_dict(response.headers)

        soup = make_soup(response)
        div_target = soup.find('div', {'id': 'deal-of-the-day'})

        payload = {
            'title': div_target.select('div.dotd-title > h2')[0].string,
            'description': div_target.select('div.dotd-main-book-summary > div')[2].string.strip(),
            'url_image': div_target.select('div.dotd-main-book-image img')[0]['src'].lstrip('//'),
            'url_claim': self.__url_base + div_target.select('a.twelve-days-claim')[0]['href']
        }
        log_json(payload)
        return payload

    def __GET_claim(self, data):
        response = self.__session.get(data['url_claim'], headers=self.__headers)
        print '[-] GET {0} | {1}'.format(response.url, response.status_code)
        print '[-] cookies:'
        log_dict(requests.utils.dict_from_cookiejar(self.__session.cookies))
        print '[-] headers:'
        log_dict(response.headers)

        soup = make_soup(response, True)
        
        #TODO
        payload = {}
        return payload

    def run(self):
        """
        https://www.packtpub.com/packt/offers/free-learning
        GET login
        POST login

        // find url
        GET https://www.packtpub.com/freelearning-claim/13539/21478
        // redirect to https://www.packtpub.com/account/my-ebooks

        DOWNLOAD info (title/description/image)
        DOWNLOAD pdf
        DOWNLOAD source (if exists)
        """

        GET_login_payload = self.__GET_login()
        wait(self.__delay)
        POST_login_payload = self.__POST_login(GET_login_payload)
        wait(self.__delay)
        self.__GET_claim(POST_payload)
