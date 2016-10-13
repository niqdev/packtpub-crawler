from logs import *

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

        if self.__database_type == DB_FIREBASE:
            self.__store_firebase()

    def __store_firebase(self):
        """
        """
        log_json(self.__packpub_info)
        log_json(self.__upload_info)
