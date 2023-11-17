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
from util import *
from popup import audit_popup

def new_customer(master, info:tuple, command_callback: callable = None):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback: callable):

            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            
            super().__init__(master,corner_radius= 0, fg_color="transparent")

            self._callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.acc_cred = acc_cred
            self.acc_info = acc_info


            def reset():
                self.customer_name_entry.delete(0, ctk.END)
                self.customer_num_entry.delete(0, ctk.END)
                self.customer_address_entry.delete(0, ctk.END)
                #self.birthday_entry.configure(text = 'Set Birthday')
                self.place_forget()
                
            def validate_contact(var, mode, index):
                if not validate_contact_num(self.number_var.get()):
                    self.customer_num_entry.delete(0, "end")
                if len(self.customer_num_entry.get()) > 20:
                    messagebox.showwarning("Entry Exceeding", "Number exceeds the accepted length", parent = self)
                    self.customer_num_entry.delete(20)

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
            self.number_var = ctk.StringVar()
            
            '''customer NAME ID'''
            self.customer_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_name_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.customer_name_frame, text="Customer ID: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_id_entry = ctk.CTkLabel(self.customer_name_frame,font=("DM Sans Medium", 14), fg_color=Color.White_Platinum, text="CUSTOMER ID",width=width*0.1, corner_radius=5)
            self.customer_id_entry.pack(side='left',fill="y", expand=0, padx=(0, width*0.0025), pady=(height*0.005,0))
           
            
            '''customer NAME ENTRY'''
            self.customer_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_name_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.customer_name_frame, text="Customer's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_name_entry = ctk.CTkEntry(self.customer_name_frame, placeholder_text="Customer Name",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion)
            self.customer_name_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
           
            '''customer CONTACT ENTRY'''
            self.customer_num_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_num_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            ctk.CTkLabel(self.customer_num_frame, text="Contact Number: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_num_entry = ctk.CTkEntry(self.customer_num_frame, placeholder_text="",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion,textvariable=self.number_var)
            self.customer_num_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
            self.number_var.trace_add('write', validate_contact)
            
            '''customer ADDRESS ENTRY'''
            self.customer_address_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_address_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.customer_address_frame, text="Address: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_address_entry = ctk.CTkEntry(self.customer_address_frame, placeholder_text="",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion)
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
            
            def check_for_names():
                txt = self.customer_name_entry.get()
                char_format = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-' "
                #contains all the valid characters

                if str.islower(txt[0]):
                    temp = txt[0].upper()
                    self.customer_name_entry.delete(0, 1)
                    self.customer_name_entry.insert(0, temp)
                #if the first letter is lowercase, copy the text, make it capital, delete the first word then replace the other

                for i in range(len(txt)):
                    if txt[i] not in char_format:
                        self.customer_name_entry.delete(i, i+1)
                #if it's not in the char format, delete letter based on which index it was located

            def check_for_number():
                num = self.customer_num_entry.get()
                char_format = "1234567890"

                if num[0] != '+' or num[0] not in char_format:
                    temp = num[0].upper()
                    self.customer_num_entry.delete(0, 1)
                    self.customer_num_entry.insert(0, temp)

                for i in range(1, len(num), 1):
                    if num[i] not in char_format:
                        self.customer_num_entry.delete(i, i+1)

            self.customer_address_limiter = cctku.entry_limiter(128, self.customer_address_entry)
            self.customer_name_limiter = cctku.entry_limiter(128, self.customer_name_entry, check_for_names)
            self.customer_num_limiter = cctku.entry_limiter(20, self.customer_num_entry, check_for_number)

            self.customer_address_entry.configure(textvariable = self.customer_address_entry)
            self.customer_name_entry.configure(textvariable = self.customer_name_limiter)
            self.customer_num_entry.configure(textvariable = self.customer_num_limiter)

        def add_record(self):
            if not self.customer_name_entry.get() and not self.customer_num_entry.get() and not self.customer_address_entry.get():
                messagebox.showerror("Fail to Proceed", "Fill the all of the entries", parent = self)
                return
            elif database.fetch_data(sql_commands.check_owner_if_exist, (self.customer_name_entry.get(),))[0][0] > 0:
                messagebox.showerror("Fail to Proceed", "Name already exist\nAdd prefix to make it unique", parent = self)
                return
            
            if database.exec_nonquery([[sql_commands.insert_new_pet_owner, (self.customer_id_entry._text, self.customer_name_entry.get(), self.customer_address_entry.get(), self.customer_num_entry.get(), self.acc_cred[0][0])]]):
                messagebox.showinfo("Success", f"{self.customer_name_entry.get()} is successfully added in the records", parent = self)
            else:
                messagebox.showerror("Fail to Proceed", "An error Occured", parent = self)
            
            if callable(self._callback):
                self._callback()
            self.place_forget()
            
        def place(self, **kwargs):
            self.customer_id_entry.configure(text = generateId('CU',7).upper())
            return super().place(**kwargs)
            
    return instance(master, info, command_callback)

def view_record(master, info:tuple, command_callback: callable = None):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback: callable):

            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            
            super().__init__(master,corner_radius= 0, fg_color="transparent")

            self._callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.acc_cred = acc_cred
            self.acc_info = acc_info

            def validate_contact(var, mode, index):
                if not validate_contact_num(self.number_var.get()):
                    self.customer_num_entry.delete(0, "end")
                if len(self.customer_num_entry.get()) > 20:
                    messagebox.showwarning("Entry Exceeding", "Number exceeds the accepted length", parent = self)
                    self.customer_num_entry.delete(20)

            def reset():
                [entry.configure(state = ctk.NORMAL) for entry in self.entries]
                self.customer_name_entry.delete(0, ctk.END)
                self.customer_num_entry.delete(0, ctk.END)
                self.customer_address_entry.delete(0, ctk.END)
                self.total_number_entry.delete(0, ctk.END)
                cancel_edit()
                self.place_forget()
                
            def open_histoy_log():
                temp = database.fetch_data("SELECT added_by, CAST(date_added AS DATE), updated_by, CAST(updated_date AS DATE) FROM pet_owner_info WHERE owner_id = ?", (self.customer_id_entry._text,))
                self.history_log.place(relx=0.5, rely=0.5, anchor = 'c', info=temp)
            
            def edit_record():
                self.customer_name_entry.configure(state = ctk.NORMAL, border_width=1, fg_color = Color.White_Lotion)
                self.customer_num_entry.configure(state = ctk.NORMAL, border_width=1, fg_color = Color.White_Lotion)
                self.customer_address_entry.configure(state = ctk.NORMAL, border_width=1, fg_color = Color.White_Lotion)
                
                self.edit_info_button.pack_forget()
                self.save_info_button.pack(side='right',fill="y", expand=0, padx=(height*0.005), pady=(height*0.005,0))
                self.cancel_edit.pack(side='right',fill="y", expand=0, padx=(height*0.005), pady=(height*0.005,0))
            
            def cancel_edit():
                self.customer_name_entry.delete(0, ctk.END)
                self.customer_num_entry.delete(0, ctk.END)
                self.customer_address_entry.delete(0, ctk.END)
                
                self.customer_name_entry.insert(0, self.record_info[1])
                self.customer_num_entry.insert(0, self.record_info[2])
                self.customer_address_entry.insert(0, self.record_info[3])
                
                self.customer_name_entry.configure(state = ctk.DISABLED, border_width=0, fg_color = Color.White_Platinum)
                self.customer_num_entry.configure(state = ctk.DISABLED, border_width=0, fg_color = Color.White_Platinum)
                self.customer_address_entry.configure(state = ctk.DISABLED, border_width=0, fg_color = Color.White_Platinum)
                
                self.edit_info_button.pack(side='right',fill="y", expand=0, padx=(height*0.005), pady=(height*0.005,0))
                self.save_info_button.pack_forget()
                self.cancel_edit.pack_forget()
                
                
            def update_record():
                if self.customer_name_entry.get()=="" or self.customer_num_entry.get()=="" or self.customer_address_entry.get()=="":
                    messagebox.showerror("Fail to Proceed", "Cannot accept blank values", parent = self)
                    return
                elif database.fetch_data(sql_commands.check_owner_if_exist, (self.customer_name_entry.get(),))[0][0] > 0 and self.customer_name_entry.get() != self.record_info[1]:
                    messagebox.showerror("Fail to Proceed", "Name already exist", parent = self)
                    return
                
                
                if self.customer_name_entry.get()==self.record_info[1] and self.customer_num_entry.get()==self.record_info[2] and self.customer_address_entry.get()==self.record_info[3]:
                    messagebox.showwarning('Update Confirmation','There are no changes in the record.', parent = self)
                else:
                    database.exec_nonquery([[sql_commands.update_customer_record_info, (self.customer_name_entry.get(), self.customer_address_entry.get(), self.customer_num_entry.get(), self.acc_cred[0][0], self.customer_id_entry._text,)]])
                    messagebox.showinfo("Success", f"{self.customer_id_entry._text} updated successfully", parent = self)
                    self._callback()
                    reset()
            self.number_var = ctk.StringVar()  
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.45, height=height*0.5, border_width=1, border_color=Color.Platinum)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,columnspan=3, sticky="ew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image='').pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="CUSTOMER RECORD", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            self.sub_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.sub_frame.pack(fill="both", expand=1, padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure((0, 1), weight=1)
            
            '''customer NAME ID'''
            self.customer_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_name_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.customer_name_frame, text="Customer ID: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_id_entry = ctk.CTkLabel(self.customer_name_frame,font=("DM Sans Medium", 14), fg_color=Color.White_Platinum, text="CUSTOMER ID",width=width*0.1, corner_radius=5)
            self.customer_id_entry.pack(side='left',fill="y", expand=0, padx=(0, width*0.0025), pady=(height*0.005,0))
            #self.add_icon
            
            self.info_log = ctk.CTkButton(self.customer_name_frame, text='', image=Icons.get_image('info_icon', (30,30)),height=height*0.045, width=height*0.045, command=open_histoy_log)
            self.info_log.pack(side='right',fill="y", expand=0, padx=(0), pady=(height*0.005,0))
            
            self.edit_info_button = ctk.CTkButton(self.customer_name_frame, image=Icons.get_image("add_icon", (18,18)), text='Edit', font=("DM Sans Medium", 14), width=width*0.01, fg_color="#3b8dd0", command=edit_record)
            self.edit_info_button.pack(side='right',fill="y", expand=0, padx=(height*0.005), pady=(height*0.005,0))

            self.save_info_button = ctk.CTkButton(self.customer_name_frame, image=Icons.get_image("save_icon", (18,18)), text='Update Record',font=("DM Sans Medium", 14), width=width*0.01, fg_color="#83bd75", hover_color=Color.Green_Button_Hover_Color, command=update_record)
            self.cancel_edit = ctk.CTkButton(self.customer_name_frame, text="Cancel", hover_color=Color.Red_Pastel, fg_color=Color.Red_Tulip, font=("DM Sans Medium", 14), width=width*0.015, command=cancel_edit)
            

            '''customer NAME ENTRY'''
            self.customer_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_name_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.customer_name_frame, text="Customer's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_name_entry = ctk.CTkEntry(self.customer_name_frame, placeholder_text="Customer Name",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum,)
            self.customer_name_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
           
            '''customer CONTACT ENTRY'''
            self.customer_num_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_num_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            ctk.CTkLabel(self.customer_num_frame, text="Contact Number: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01),)
            self.customer_num_entry = ctk.CTkEntry(self.customer_num_frame, placeholder_text="",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum,  textvariable=self.number_var)
            self.customer_num_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
            self.number_var.trace_add('write', validate_contact)
            
            '''customer ADDRESS ENTRY'''
            self.customer_address_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_address_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.customer_address_frame, text="Address: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.customer_address_entry = ctk.CTkEntry(self.customer_address_frame, placeholder_text="",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum,)
            self.customer_address_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))
            
            '''customer NUMBER OF TRANSACTIONS'''
            self.customer_number_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.customer_number_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.customer_number_frame, text="Transaction Count: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.1, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.total_number_entry = ctk.CTkEntry(self.customer_number_frame, placeholder_text="",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum,)
            self.total_number_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005,0))

            self.entries = [self.customer_name_entry, self.customer_num_entry, self.customer_address_entry, self.total_number_entry]
            self.history_log = audit_popup.audit_info(self, (width, height))
            
            def check_for_names():
                txt = self.customer_name_entry.get()
                char_format = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-' "

                if str.islower(txt[0]):
                    temp = txt[0].upper()
                    self.customer_name_entry.delete(0, 1)
                    self.customer_name_entry.insert(0, temp)

                for i in range(len(txt)):
                    if txt[i] not in char_format:
                        self.customer_name_entry.delete(i, i+1)

            def check_for_number():
                num = self.customer_num_entry.get()
                char_format = "1234567890"

                if num[0] != '+' or num[0] not in char_format:
                    temp = num[0].upper()
                    self.customer_num_entry.delete(0, 1)
                    self.customer_num_entry.insert(0, temp)

                for i in range(1, len(num), 1):
                    if num[i] not in char_format:
                        self.customer_num_entry.delete(i, i+1)

            self.name_limiter = cctku.entry_limiter(128, self.customer_name_entry, check_for_names)
            self.number_limiter = cctku.entry_limiter(20, self.customer_num_entry, check_for_number)
            self.address_limiter = cctku.entry_limiter(128, self.customer_address_entry )

            self.customer_name_entry.configure(textvariable = self.name_limiter)
            self.customer_num_entry.configure(textvariable = self.number_limiter)
            self.customer_address_entry.configure(textvariable = self.address_limiter)

        def set_entries(self):
            self.record_info = database.fetch_data(sql_commands.get_customer_view_record, (self.info[0],))[0]
            [entry.configure(state = ctk.NORMAL) for entry in self.entries]
            [entry.delete(0, ctk.END) for entry in self.entries]
            self.customer_id_entry.configure(text = self.record_info[0])
            self.customer_name_entry.insert(0, self.record_info[1])
            self.customer_num_entry.insert(0, self.record_info[2])
            self.customer_address_entry.insert(0, self.record_info[3])
            self.total_number_entry.insert(0, self.record_info[4])
            [entry.configure(state = ctk.DISABLED) for entry in self.entries]
            
            
        def place(self, info, **kwargs):
            self.info = info
            self.set_entries()
            return super().place(**kwargs)
            
    return instance(master, info, command_callback)