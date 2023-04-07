import uuid
import hashlib
import base64
import re
import mariadb
from constants import db
from functools import partial
from Theme import *
from typing import *


class encrypt:
    def pass_encrypt(pss, slt):
        salt = base64.urlsafe_b64encode(uuid.uuid4().bytes) if slt == None else slt.encode('utf-8')
        encryptor = hashlib.sha256()
        encryptor.update(str(pss).encode('utf-8') + salt)
        encrypted_password = encryptor.hexdigest()
        #encrypt the initial pass

        for _ in range(int(re.findall(r'\d{2}', encrypted_password)[0]) + len(pss)):
            encryptor.update(str(encrypted_password).encode('utf-8') + salt)
            encrypted_password = encryptor.hexdigest()
        #repeatedly encrypt the pass at the certain time

        return {"pass": encrypted_password, "salt": salt}

class database:
    def fetch_db_profile():
        try:
            mdb = mariadb.connect(user= db.USERNAME, password= db.PASSWORD, host= db.HOST, port= db.PORT, database= db.DB)
            return mdb
        except mariadb.Error:
            pass
        return None

    def fetch_data(cmd, tup, db_con):
        try:
            db_cur = db_con.cursor()
            db_cur.execute(cmd, tup)
            return db_cur.fetchall()
        except mariadb.Error as e:
            print(e)
        return None

    def exec_nonquery(cmds, db_con):
        try:
            db_cur = db_con.cursor()
            for i in range(len(cmds)):
                try:
                    db_cur.execute(cmds[i][0], cmds[i][1])
                except mariadb.IntegrityError:
                    print(f'command {i+1} error pushing')
        except mariadb.Error as e:
            print(e)
        else:
            db_con.commit()

def brighten_color(hexcode: str, i: int = 1):
    c = re.findall(r'[\d\w]{2}', hexcode)
    r = c[0]
    g = c[1]
    b = c[2]
    r = int(r, base=16)
    g = int(g, base=16)
    b = int(b, base=16)
    r = 00 if r * i < 0 else 255 if r * i > 255 else round(r * i)
    g = 00 if g * i < 0 else 255 if g * i > 255 else round(g * i)
    b = 00 if b * i < 0 else 255 if b * i > 255 else round(b * i)
    return "#%02x%02x%02x" % (r,g,b)

''' example of inserting data
usn = 'admin1'
pss = encrypt.pass_encrypt('admin', None)
database.exec_nonquery([[f'INSERT INTO {db.acc_cred.TABLE} VALUES (?, ?, ?)', (usn, pss["pass"], pss['salt'])]], database.fetch_db_profile())
#database.exec_nonquery([[f'DELETE FROM {db.acc_cred.TABLE} where {db.acc_cred.USERNAME} = ?', ('admin1',)]], database.fetch_db_profile())
'''