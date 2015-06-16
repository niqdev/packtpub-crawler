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

    def __url_login(self):
        base_url = self.__config.get('url', 'url.base')
        login_url = self.__config.get('url', 'url.login')
        return base_url + login_url

    def __data_POST_login(self, soup):
        form = soup.find('form', {'id': 'packt-user-login-form'})
        #print form.find_all('input', attrs={'name': 'form_build_id'}, limit=1)[0]['value']
        #print form.find('input', attrs={'name': 'form_build_id'})['value']
        #print form.find('input', attrs={'name': 'form_id'})['value']

        data = {
            'email': self.__config.get('credential', 'credential.email'),
            'password': self.__config.get('credential', 'credential.password'),
            'op': 'Login',
            'form_build_id': form.find('input', attrs={'name': 'form_build_id'})['value'],
            'form_id': form.find('input', attrs={'name': 'form_id'})['value'],
        }
        print '[-] data: {0}'.format(urllib.urlencode(data))
        return data

    def __login(self):
        """
        GET request to home page, parse response and return data
        """
        url = self.__url_login()

        GET_login_res = self.__session.get(url, headers=self.__headers)
        print 'GET {0} | {1}'.format(GET_login_res.url, GET_login_res.status_code)
        GET_soup = make_soup(GET_login_res, True)
        POST_data = self.__data_POST_login(GET_soup)

        wait(self.__delay)
        POST_login_res = self.__session.post(url, headers=self.__headers, data=POST_data)
        print 'POST {0} | {1}'.format(POST_login_res.url, POST_login_res.status_code)
        POST_soup = make_soup(POST_login_res, True)

        print 'cookies {0}'.format(self.__session.cookies)
        print 'cookies', requests.utils.dict_from_cookiejar(self.__session.cookies)
        print 'headers {0}'.format(POST_login_res.headers)
        print 'content {0}'.format(POST_login_res.content)
        print 'soup {0}'.format(POST_soup)

    def download_pdf(self):
        """
        https://www.packtpub.com/packt/offers/free-learning
        GET login
        POST login

        https://www.packtpub.com/account/my-ebooks
        GET account
        DOWNLOAD info (title/description/image)
        DOWNLOAD pdf
        DOWNLOAD source (if exists)
        """

        log_success("TODO downloading PDF")
        self.__login()
