class db:
    DB = 'ssi1'
    PORT = 3306
    HOST = '127.0.0.1'
    PASSWORD = 'test123'
    USERNAME = 'ROOT'

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