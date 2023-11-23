import customtkinter as ctk
from typing import Optional
from Theme import Color
from util import database
from util import *
from tkinter import messagebox
from PIL import Image
from typing import *

def authorization(master, info:tuple, command_callback :Optional[callable] = None, roles: str = "('Assisstant', 'Owner')"):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback :Optional[callable]):
            width = info[0] * .4
            height = info[1] * .4
            super().__init__(master, width, height, corner_radius= 0, fg_color="white")
            self.command_callback = command_callback
            self.user_name_authorized_by = None
            self.pack_propagate(0)
            self._border_color = Color.White_Platinum
            self.authorized_roles = roles

            self.user_icon = ctk.CTkImage(light_image=Image.open("image/user_icon.png"),size=(30,30))
            self.pass_icon = ctk.CTkImage(light_image=Image.open("image/pass_icon.png"),size=(30,30))
            self.show_icon = ctk.CTkImage(light_image=Image.open("image/view.png"),size=(28,28))
            self.hide_icon = ctk.CTkImage(light_image=Image.open("image/hide.png"),size=(28,28))

            self.upper_frame = ctk.CTkFrame(self, height= height * .15, fg_color= Color.Blue_Yale, corner_radius= 0)
            self.upper_frame.pack(fill = 'x', padx=(1),pady=(1,0))
            self.upper_frame.pack_propagate(0)

            ctk.CTkLabel(self.upper_frame, text = 'Authorization', font=("DM Sans Medium", 16), text_color= 'white').pack(side = 'left', padx = (width * .01, 0))
            self.close_btn = ctk.CTkButton(self.upper_frame,  height * .12, height * .12, text= 'x', command=self.reset)

            self.close_btn.pack(side = ctk.RIGHT, padx = (0, width * .005))
            
            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,height= height *.87, corner_radius= 0)
            self.main_frame.pack(fill = ctk.BOTH, padx=(1),pady=(0,1))
            self.main_frame.grid_propagate(0)

            self.user_label = ctk.CTkLabel(self.main_frame, text='Administrator Username', font=('DM Sans Medium',17),
                                       text_color=Color.Grey_Davy)
            self.user_label.grid(row=2, column=0,sticky='sw',pady = (width * .025, 0), padx = 44)

            self.user_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                        fg_color=Color.White_Milk, width = width * .75)
            self.user_frame.grid(row=3, column=0,sticky='ew', padx=(35))

            self.user_icon_label = ctk.CTkLabel(self.user_frame, text='', image=self.user_icon)
            self.user_icon_label.pack(side='left', padx=(5,0),pady=(5))
            self.user_entry = ctk.CTkEntry(self.user_frame, width = width * .75, height=round(height * 0.03),font=('DM Sans Medium',16),border_width=0,
                                        fg_color=Color.White_Milk, text_color=Color.Blue_Maastricht)
            self.user_entry.pack(side='right', fill='x', expand=True,padx=(5,10),pady=(5))

            self.password_label = ctk.CTkLabel(self.main_frame, text='Password', font=('DM Sans Medium',17),
                                        text_color=Color.Grey_Davy)
            self.password_label.grid(row=4, column=0,sticky='sw',padx=(44,44),pady=(10,0))

            '''Frame for the password entry'''
            self.pass_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                        fg_color=Color.White_Milk, width = width * .75)
            self.pass_frame.grid(row=5, column=0,sticky='ew',padx=(35))

            self.pass_icon_label = ctk.CTkLabel(self.pass_frame, text='',image=self.pass_icon)
            self.pass_icon_label.pack(side='left', padx=(5,0),pady=(5))

            self.password_entry = ctk.CTkEntry(self.pass_frame,height=round(height * 0.03),font=('DM Sans Medium',16),border_width=0,
                                        fg_color=Color.White_Milk, show='●', width = width * .75, text_color= 'black')
            self.password_entry.pack(side='left', fill='x', expand=True,padx=(3),pady=(5))
            
            self.login_button = ctk.CTkButton(self.main_frame, text="Authorize", height=45,
                                          font=('DM Sans Medium',16),text_color='#FFFFFF',
                                          fg_color=Color.Blue_Cobalt,corner_radius=5,
                                          command= self.authorize)
            self.login_button.grid(row=7, column=0, sticky='nse', padx=(42,35),pady=(20,35))


        def authorize(self, _: any = None):
            try:
                salt = database.fetch_data(f'SELECT {db.acc_cred.SALT} FROM {db.ACC_CRED} WHERE {db.USERNAME} COLLATE LATIN1_GENERAL_CS = ?',
                                        (self.user_entry.get(), ))[0][0]
            except IndexError:
                self.password_entry.delete(0, ctk.END)
                messagebox.showinfo('Error', 'Username Or Password Incorrect', parent = self)
                return
            _db = f"SELECT COUNT(*)\
                  FROM acc_cred\
                  JOIN acc_info\
                      ON acc_cred.usn = acc_info.usn\
                  WHERE acc_cred.usn COLLATE LATIN1_GENERAL_CS = ?\
                          AND acc_cred.pss = ?\
                          AND acc_info.job_position IN {self.authorized_roles}"
            print(_db)
            count = database.fetch_data(_db ,(self.user_entry.get(), encrypt.pass_encrypt(self.password_entry.get(), salt)['pass']))
            if count[0][0] == 0:
                self.password_entry.delete(0, ctk.END)
                messagebox.showinfo('Error', 'Username Or Password Incorrect', parent = self)
            else:
                if database.fetch_data('SELECT state FROM acc_info WHERE usn = ?', (self.user_entry.get(), ))[0][0] == 0:
                    messagebox.showerror("Failed to Login", "The Account you're been\nlogged has been deactivated.\nInquire to the Owner", parent = self)
                    return

                self.user_name_authorized_by = self.user_entry.get()

                if callable(self.command_callback):
                    self.command_callback()
                self.reset()

        def reset(self):
            self.password_entry.delete(0, ctk.END)
            self.user_entry.delete(0, ctk.END)
            self.place_forget()
            pass

    return instance(master, info, command_callback)