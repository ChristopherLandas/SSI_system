from typing import *
import customtkinter as ctk
import sys
import os
from util import database
from util import encrypt
from tkinter import messagebox

def popup_name_here(master, obj, info:tuple) -> ctk.CTkFrame:
    class add_item(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="red")
            self.pack_propagate(0)
            self.grid_propagate(0)
            #basic inforamtion needed; measurement
            '''events'''
            def reset():
                self.pss_entry.delete(0, ctk.END)
                self.name_entry.delete(0, ctk.END)
                self.usn_entry.delete(0, ctk.END)
                self.place_forget()
                self.pack_forget()
                self.grid_forget()

            def record_acc():
                if database.fetch_data('SELECT * FROM acc_cred where usn = ?',( self.usn_entry.get(), )):
                    messagebox.showinfo('Can\'t Create record', 'Username already exist')
                    return
                password = encrypt.pass_encrypt(self.pss_entry.get())
                database.exec_nonquery([['INSERT INTO acc_cred VALUES(?, ?, ?, NULL)', (self.usn_entry.get(), password['pass'], password['salt'])],
                                        ['INSERT INTO acc_info VALUES(?, ?, ?)', (self.usn_entry.get(), self.name_entry.get(), self.job_pos.get())]])
                messagebox.showinfo('SUCCESS', f'Acc {self.usn_entry.get()}\nhas been successfully registered')


            self.usn_entry = ctk.CTkEntry(self, width=140, placeholder_text="usn")
            self.usn_entry.pack()
            self.name_entry = ctk.CTkEntry(self, width=140, placeholder_text="name")
            self.name_entry.pack()
            self.pss_entry = ctk.CTkEntry(self, width=140, show = "*", placeholder_text='password')
            self.pss_entry.pack()
            self.job_pos = ctk.CTkOptionMenu(self, values=["Owner", "Assisstant"])
            self.job_pos.pack()
            self.login_btn = ctk.CTkButton(self, text='create acc', command=record_acc)
            self.login_btn.pack()
            self.back_btn = ctk.CTkButton(self, text='back', command= lambda: master.destroy())
            self.back_btn.pack()
            #the actual frame, modification on the frame itself goes here

    return add_item(master, obj, info)
    #return the class as the frame

x,y = 1920,1080
ctk1 = ctk.CTk()
ctk1.state("zoomed")
ctk1.update()
ctk1.attributes("-fullscreen", True)
frame = popup_name_here(ctk1, None, (x * .8, y * .8))
frame.place(relx = .5, rely = .5, anchor = 'c')
ctk1.mainloop()
#for running and testing