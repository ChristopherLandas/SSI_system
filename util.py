import uuid
import hashlib
import base64
import re
import mariadb
from constants import db
from functools import partial
from Theme import *

test = {"name" : "chris"}

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

class sequence:
    def bind_command(tup, cmd):
        for o in tup:
            o.bind('<Button-1>', lambda _: cmd(None))


    def bind_event(tup, master, color_hover, color_hover_exit):
        for o in tup:
            o.bind('<Enter>', lambda _: master.configure(fg_color = color_hover))
            o.bind('<Leave>', lambda _: master.configure(fg_color = color_hover_exit))

    def unbind_event(tup):
        for o in tup:
            o.unbind('<Enter>', None)
            o.unbind('<Leave>', None)


''' example of inserting data
usn = 'admin'
pss = encrypt.pass_encrypt('admin', None)
database.exec_nonquery([[f'INSERT INTO {db.acc_cred.TABLE} VALUES (?, ?, ?)', (usn, pss["pass"], pss['salt'])]], database.fetch_db_profile())
'''