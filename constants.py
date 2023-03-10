import mariadb

class db:
    DB = 'ssi'
    PORT = 3306
    HOST = '127.0.0.1'
    PASSWORD = 'test123'
    USERNAME = 'ROOT'

    class acc_cred:
        TABLE = 'acc_cred'
        USERNAME = 'usn'
        PASSWORD = 'pss'
        SALT = 'slt'