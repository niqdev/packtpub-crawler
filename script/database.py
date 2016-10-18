from logs import *
from firebase.firebase import FirebaseApplication, FirebaseAuthentication

DB_FIREBASE = 'firebase'

class Database(object):
    """
    Store to database
    """

    def __init__(self, config, database_type, packpub_info, upload_info):
        self.__config = config
        self.__database_type = database_type
        self.__packpub_info = packpub_info
        self.__upload_info = upload_info

    def store(self):
        """
        """

        #log_json(self.__packpub_info)
        #log_json(self.__upload_info)

        if self.__database_type == DB_FIREBASE:
            self.__store_firebase()

    def __store_firebase(self):
        """
        """

        # https://console.firebase.google.com/project/packtpub-crawler/settings/database

        authentication = FirebaseAuthentication(self.__config.get('firebase', 'firebase.database_secret'), None)
        print authentication.extra

        user = authentication.get_user()
        print user.firebase_auth_token

        firebase = FirebaseApplication(self.__config.get('firebase', 'firebase.url'), authentication)
        result = firebase.get(self.__config.get('firebase', 'firebase.path'), None)
        print result['a']
