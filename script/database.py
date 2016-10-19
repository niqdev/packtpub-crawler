from logs import *
from firebase.firebase import FirebaseApplication, FirebaseAuthentication
import datetime

DB_FIREBASE = 'firebase'

class Database(object):
    """
    Store to database
    """

    def __init__(self, config, database_type, packpub_info, upload_info):
        self.__config = config
        self.__database_type = database_type

        data = packpub_info.copy()
        data['datetime'] = datetime.datetime.utcnow().isoformat()
        data.pop('paths', None)
        data.update(upload_info)
        self.__data = data

    def store(self):
        """
        """
        #log_json(self.__data)

        if self.__database_type == DB_FIREBASE:
            self.__store_firebase()

    def __store_firebase(self):
        """
        """

        authentication = FirebaseAuthentication(self.__config.get('firebase', 'firebase.database_secret'), None)
        #user = authentication.get_user()
        #print authentication.extra
        #print user.firebase_auth_token

        firebase = FirebaseApplication(self.__config.get('firebase', 'firebase.url'), authentication)
        result = firebase.post(self.__config.get('firebase', 'firebase.path'), self.__data)

        log_success('[+] Stored on firebase: {0}'.format(result['name']))
