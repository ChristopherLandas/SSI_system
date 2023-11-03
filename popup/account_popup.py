import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
import tkcalendar
from Theme import Color
from util import database, generateId
from tkinter import messagebox
from constants import action
import datetime
from PIL import Image
import datetime
from functools import partial
from typing import *
import tkinter as tk
from util import encrypt

def change_password(master, info:tuple,):
    class change_password(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width=width*0.35, height=height*0.45, corner_radius= 0, fg_color='transparent')
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            def reset():
                self.place_forget()

            self.pass_icon = ctk.CTkImage(light_image= Image.open("image/create_acc.png"), size=(20,20))
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.pass_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='CHANGE PASSWORD', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.content_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.content_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.content_frame.grid_columnconfigure(0, weight=1)
            
            '''NAME FRAME'''
            self.acc_name_frame =ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.acc_name_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.02,height*0.0115))
            ctk.CTkLabel(self.acc_name_frame, text="Username: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.username_label = ctk.CTkLabel(self.acc_name_frame, text="Username", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.125, anchor="w", padx=(width*0.01))
            self.username_label.pack(side='left', fill="x", expand=1, padx=(0, width*0.005), pady=(height*0.0075))
           
            '''PASSWORD FRAME'''
            self.password_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.password_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.password_frame, text="New Password: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.password_entry = ctk.CTkEntry(self.password_frame,fg_color="white", placeholder_text="New Password", placeholder_text_color='light grey',font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, height=height*0.045 )
            self.password_entry.pack(side='left', fill="x", expand=1, padx=(0, width*0.005), pady=(height*0.0075))

            #'''AUTO GENERATE'''
            #self.auto_generate_btn = ctk.CTkButton(self.content_frame, text= 'Generate')
            #self.auto_generate_btn = 
           
            '''BOTTOM'''
            self.bottom_frame = ctk.CTkFrame(self, fg_color='transparent')
            self.bottom_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady = (0, height*0.01))
            
            self.cance__btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, text="Cancel", fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14))
            self.cance__btn.pack(side='left')
            
            self.update_password_btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, width=width*0.075, text="Update Password", font=("DM Sans Medium", 14), command= self.update_pass)
            self.update_password_btn.pack(side='right')

        def place(self, username: str, **kwargs):
            if(username is None):
                messagebox.showerror("Invalid", "Select an account to change", parent = self)
                return
            self.username_label.configure(text = username[0])
            return super().place(**kwargs)
        
        def update_pass(self):
            if len(self.password_entry.get() or []) < 5:
                messagebox.showerror("Invalid", "password must atleast\n5 characters long", parent = self)
                return
            new_pass = encrypt.pass_encrypt(self.password_entry.get())
            database.exec_nonquery([["UPDATE acc_cred SET pss = ?, slt = ? WHERE usn = ?", (new_pass['pass'], new_pass['salt'],
                                                                                            self.username_label._text)]])
            messagebox.showinfo("Success", f"{self.username_label._text}%s\nPassword is changed\nPassword: {self.password_entry.get()}" % "'" if self.username_label._text.endswith("s") else "s", parent = self)
            self.place_forget()
            self.pack_forget()
            self.grid_forget()
            #print(new_pass)

    return change_password(master, info)
#That place is not for  any man or particles of bread