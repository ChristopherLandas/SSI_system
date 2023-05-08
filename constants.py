class db:
    DB = 'ssi'
    PORT = 3306
    HOST = '127.0.0.1'
    PASSWORD = 'hello123'
    #USERNAME = 'root'

    ACC_CRED = 'acc_cred'
    USERNAME = 'usn'
    class acc_cred:
        PASSWORD = 'pss'
        SALT = 'slt'
        ENTRY_OTP = 'entry_OTP'

    ACC_INFO = 'acc_info'
    class acc_info:
        NAME = 'full_name'
        POSITION = 'job_position'

    LOG_HIST = 'log_history'
    class log_hist:
        DATE_LOGGED = 'date_logged'
        TIME_IN = 'time_in'
        TIME_OUT = 'time_out'
        EMINEM = 'without me'

class action:
    RESTOCKED_ITEM = f'RST/%s/%s/%s' #item stocked, stocked_change, success?
    ADD_ITEM = f'ADD/%s' #UID of the item
