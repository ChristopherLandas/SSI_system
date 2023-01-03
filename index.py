import hashlib
import customtkinter
import tkinter.messagebox
import mariadb
import re

root_panel = customtkinter.CTk()
root_panel.geometry('500x500')
#GUI variables

def signIn():
    hash_encryptor = hashlib.new('sha256')
    #encryption variable

    try:
        db_con = mariadb.connect(user="root", password="test123", host="127.0.0.1", port=3306, database='test')
        db_cur = db_con.cursor()
        db_cur.execute('SELECT slt FROM login_credentials WHERE usn COLLATE LATIN1_GENERAL_CS = ?', (username_entry.get(),))
        salt = str(db_cur.fetchall()[0][0]).encode('utf-8')
    except IndexError:
        tkinter.messagebox.showinfo('error', 'incorrect username or password')
        return
    except mariadb.Error:
        tkinter.messagebox.showinfo('error', 'error connecting in database')
    else:
        db_cur.close()
        db_con.close()
    # get the salt from the db

    hash_encryptor.update(password_entry.get().encode('utf-8') + salt)
    encrypted_pass = hash_encryptor.hexdigest()
    #encode the text from the password entry, this is the initial encryption of the password

    for i in range(int(re.findall('\d{2}', encrypted_pass)[0]) + len(username_entry.get())):
        hash_encryptor.update(encrypted_pass.encode('utf-8') + salt)
        encrypted_pass = hash_encryptor.hexdigest()
    #repeteadly encrypt the the encrypted password where the length is based on the lenght of the username + the first 2 number of the initial passwordq

    try:
        db_con = mariadb.connect(user="root", password="test123", host="127.0.0.1", port=3306, database='test')
        db_cur = db_con.cursor()
        db_cur.execute('SELECT COUNT(*) AS len FROM login_credentials WHERE usn COLLATE LATIN1_GENERAL_CS = ? AND pss = ? AND slt = ?', (username_entry.get(), encrypted_pass, salt))
        does_have = db_cur.fetchall()[0][0] > 0
    except mariadb.Error:
        tkinter.messagebox.showinfo('error', mariadb.Error)
        return
    else:
        db_cur.close()
        db_con.close()
    #find the credentials based on the username, generated password and the salt. returns true if it finds any and false if there's none

    if(does_have):
        tkinter.messagebox.showinfo('Welcome', 'Welcome')
    else:
        tkinter.messagebox.showinfo('error', 'incorrect username or password')


#button function of sign in

username_entry = customtkinter.CTkEntry(root_panel, 280, 34, placeholder_text='Username', corner_radius=25)
username_entry.pack(pady=(130, 0))
#setup the username entry

password_entry = customtkinter.CTkEntry(root_panel, 280, 34, show='●', placeholder_text="Password", corner_radius=25)
password_entry.pack(pady=(20, 40))
#setup the password entry

signin_button = customtkinter.CTkButton(root_panel, 140, 28, 12, text='Sign in', command=signIn)
signin_button.pack()
root_panel.mainloop()