import ConfigParser
import urllib
import requests
from utils import make_soup
from utils import wait
from utils import download_file
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

    def __log_response(self, response, method='GET', detail=False):
        print '[-] {0} {1} | {2}'.format(method, response.url, response.status_code)
        if detail:
            print '[-] cookies:'
            log_dict(requests.utils.dict_from_cookiejar(self.__session.cookies))
            print '[-] headers:'
            log_dict(response.headers)

    def __GET_login(self):
        url = self.__url_base + self.__config.get('url', 'url.loginGet')

        response = self.__session.get(url, headers=self.__headers)
        self.__log_response(response)

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
        #print '[-] data: {0}'.format(urllib.urlencode(data))

        url = self.__url_base + self.__config.get('url', 'url.loginPost')

        # ONLY-DEV: use GET instead of POST
        #response = self.__session.get(url, headers=self.__headers, data=data)
        response = self.__session.post(url, headers=self.__headers, data=data)
        self.__log_response(response, 'POST', True)

        soup = make_soup(response)
        div_target = soup.find('div', {'id': 'deal-of-the-day'})

        payload = {
            'title': div_target.select('div.dotd-title > h2')[0].string.strip(),
            'description': div_target.select('div.dotd-main-book-summary > div')[2].string.strip(),
            'url_image': div_target.select('div.dotd-main-book-image img')[0]['src'].lstrip('//'),
            'url_claim': self.__url_base + div_target.select('a.twelve-days-claim')[0]['href']
        }
        log_json(payload)
        return payload

    def __GET_claim(self, data):
        # ONLY-DEV: use url.account
        #url_dev = self.__url_base + self.__config.get('url', 'url.account')
        #response = self.__session.get(url_dev, headers=self.__headers)
        response = self.__session.get(data['url_claim'], headers=self.__headers)
        self.__log_response(response)

        soup = make_soup(response)
        div_target = soup.find('div', {'id': 'product-account-list'})

        book_id = div_target.select('.product-line')[0]['nid']

        # only last one just claimed
        payload = {
            'book_id' : book_id,
            'author': div_target.find(class_='author').text.strip(),
            'url_pdf' : self.__url_base + '/ebook_download/{0}/pdf'.format(book_id),
            'url_epub' : self.__url_base + '/ebook_download/{0}/epub'.format(book_id),
            'url_mobi' : self.__url_base + '/ebook_download/{0}/mobi'.format(book_id),
        }
        log_json(payload)
        return payload


    def run(self):
        """
        """

        GET_login_payload = self.__GET_login()
        wait(self.__delay)
        POST_login_payload = self.__POST_login(GET_login_payload)
        wait(self.__delay)
        GET_claim_payload = self.__GET_claim(POST_login_payload)

        # TODO refactor
        directory = self.__config.get('path', 'path.ebooks')
        filename = POST_login_payload['title'] + '.pdf'
        download_file(self.__session, GET_claim_payload['url_pdf'], directory, filename)
