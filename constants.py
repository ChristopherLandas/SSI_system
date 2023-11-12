class db:
    DB = 'ssi_merged'
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
    RESTOCK_TYPE = 'Restock'
    RECIEVING_STOCk_TYPE = 'Recieving stock'
    ADD_ITEM_TYPE = 'Item Encoding'
    INVOICE_TYPE = 'invoice'
    TRANSACTION_TYPE = 'Transaction Record'
    DISPOSAL_TYPE = 'Disposal'
    ADD_SERVICE = 'Service Encoding'


    RESTOCKED_ITEM = f'RST/%s/%s/%s' #item stocked, stocked_change, success?
    CONFIRM_RECIEVE_ITEM = f'CRI/%s/%s/%s' #item recieve and move to inventory, user, item_uid, stock
    ADD_ITEM = f'ADD/%s/%s' #UID of the item, success?
    ADD_SVC = f'ADDS/%s/%s' #UID of the service, success?
    MAKE_INVOICE = f'INVM/%s/%s' # Invoice maked, user, uid
    MAKE_TRANSACTION = 'TRNM/%s/%s' # Transaction made, user, uid
    MOVE_TO_DISPOSAL = 'DPSM/%s/%s' #Move item to disposal, user, item_uid
    OFFICIALLY_DISPOSE = 'DPSO/%s/%s' #Completely disposal of item, user, item_uid
