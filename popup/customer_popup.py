import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import tkcalendar
from Theme import Color
from util import database, generateId
from tkinter import messagebox
from constants import action
from PIL import Image
from Theme import Color, Icons
from customcustomtkinter import customcustomtkinterutil as cctku
from functools import partial
import sql_commands
import tkinter as tk
from tkinter import ttk
import datetime

def new_customer(master, info:tuple, command_callback: callable = None):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback: callable):

            width = info[0]
            height = info[1]
            #acc_cred = info[2]
            #acc_info = info[3]
            super().__init__(master,corner_radius= 0, fg_color="transparent")

            self._callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            def reset():
                self.customer_name_entry.delete(0, ctk.END)
                self.customer_num_entry.delete(0, ctk.END)
                self.customer_address_entry.delete(0, ctk.END)
                #self.birthday_entry.configure(text = 'Set Birthday')
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.4, height=height*0.5, border_width=1, border_color=Color.Platinum)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,columnspan=3, sticky="ew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image='').pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="NEW CUSTOMER RECORD", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            self.sub_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.sub_frame.pack(fill="both", expand=1, padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure((0, 1), weight=1)
            
            '''customer NAME ENTRY'''
            self.customer_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            ctk.CTkLabel(self.customer_frame, text="Customer's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_name_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="Customer Name",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion)
            self.customer_name_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
            
            '''BDAY'''
            '''self.bday_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.bday_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.bday_frame, text="Birthday: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.birthday_entry = ctk.CTkLabel(self.bday_frame, text="Set Birthday", fg_color=Color.White_Platinum, corner_radius=5,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.birthday_entry.pack(side="left", fill="both", expand=1, padx=(0), pady=(height*0.005))

            self.show_calendar = ctk.CTkButton(self.bday_frame, text="",image=Icons.get_image("calendar_icon", (25,25)), height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.birthday_entry, "%s", date_format="raw", max_date=datetime.datetime.now()))
            self.show_calendar.pack(side="left", padx=(width*0.0025), pady=(height*0.005))'''
            #unnecessary
            
            '''customer CONTACT ENTRY'''
            self.customer_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            ctk.CTkLabel(self.customer_frame, text="Contact Number: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_num_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="Optional",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion)
            self.customer_num_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
            
            '''customer ADDRESS ENTRY'''
            self.customer_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.customer_frame, text="Address: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_address_entry = ctk.CTkEntry(self.customer_frame, placeholder_text="Optional",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion)
            self.customer_address_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))

            '''BOT FRAME'''
            self.bot_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.bot_frame.grid(row=2,column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
           
            self.cancel_btn = ctk.CTkButton(self.bot_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left",padx=(width*0.005), pady=(width*0.005)) 
            
            self.add_btn = ctk.CTkButton(self.bot_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Add Record',
                                         command=self.add_record)
            self.add_btn.pack(side="right",padx=(width*0.005),pady=(width*0.005))

            def num_entry_checker():
                if self.customer_num_entry.get()[-1].isdecimal():
                    return
                elif self.customer_num_entry.get()[-1] == "+":
                    return
                self.customer_num_entry.delete(len(self.customer_address_entry.get()) - 2, ctk.END)

            self.customer_address_limiter = cctku.entry_limiter(256, self.customer_address_entry)
            self.customer_name_limiter = cctku.entry_limiter(128, self.customer_name_entry)
            self.customer_num_limiter = cctku.entry_limiter(20, self.customer_num_entry, num_entry_checker)

            self.customer_address_entry.configure(textvariable = self.customer_address_entry)
            self.customer_name_entry.configure(textvariable = self.customer_name_limiter)
            self.customer_num_entry.configure(textvariable = self.customer_num_limiter)

        def add_record(self):
            if not self.customer_name_entry.get():
                messagebox.showerror("Fail to Proceed", "Fill the Name entry", parent = self)
                return
            elif database.fetch_data(sql_commands.check_owner_if_exist, (self.customer_name_entry.get(),))[0][0] > 0:
                messagebox.showerror("Fail to Proceed", "Name already exist\nAdd prefix to make it unique", parent = self)
                return
            
            if database.exec_nonquery([[sql_commands.insert_new_pet_owner, (self.customer_name_entry.get(), self.customer_num_entry.get() or None, self.customer_address_entry.get() or None)]]):
                messagebox.showinfo("Success", f"{self.customer_name_entry.get()} Added")
            else:
                messagebox.showerror("Fail to Proceed", "An error Occured", parent = self)

            if callable(self._callback):
                self._callback()
            self.place_forget()
            
    return instance(master, info, command_callback)