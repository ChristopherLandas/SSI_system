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
import util
from datetime import date

def add_service(master, info:tuple, update_callback: callable):
    class add_service(ctk.CTkFrame):
        def __init__(self, master, info:tuple, update_callback: callable):
            width = info[0]
            height = info[1]
            super().__init__(master, width=width*0.4, height=height*0.55, corner_radius= 0, fg_color='transparent')
            
            self.update_callback = update_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            def reset():
                self.place_forget()
                self.service_name_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                self.category_option.set("Set Category")
                
                self.update_callback()
                
            def new_service():
                
                
                if self.service_name_entry.get() == "" and self.price_entry.get() == "" and self.category_option.get() == "Set Category":
                    messagebox.showerror("Missing Data", "Complete all the fields to continue")   
                    
                else:    
                    a = util.generateId(initial='S', length=6)
                    database.exec_nonquery([[sql_commands.insert_service_test, (a, self.service_name_entry.get(), 'test', self.price_entry.get(), 
                                                                                self.category_option.get(), self.radio_var.get(), 1, date.today())]])
                    messagebox.showinfo("Service Added", "New service is added")
                    reset()
                    
            def radio_callback():
                print(self.radio_var.get())

            
            self.service_icon = ctk.CTkImage(light_image= Image.open("image/services.png"), size=(20,20))
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.service_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='ADD SERVICE', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.content_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Platinum,)
            self.content_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.content_frame.grid_columnconfigure(0, weight=1)
            
            self.sub_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.sub_frame.pack(fill="both", expand=1, padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure((1), weight=1)
            
            '''NAME'''
            self.service_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.service_name_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(height*0.025,0))
            ctk.CTkLabel(self.service_name_frame, text="Service Name: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.service_name_entry = ctk.CTkEntry(self.service_name_frame, fg_color=Color.White_Lotion, placeholder_text="Service Name", placeholder_text_color='light grey',font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, height=height*0.045)
            self.service_name_entry.pack(side='left', fill="x", expand=1, padx=(0, width*0.005), pady=(height*0.0075))
            
            '''CATEGORY'''
            self.category_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.category_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(height*0.005,0))
            ctk.CTkLabel(self.category_frame, text="Category: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.category_option= ctk.CTkOptionMenu(self.category_frame, anchor="w", font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts)
            self.category_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            self.category_option.set("Set Category")
            
            '''PRICE'''
            self.price_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.price_frame.grid(row=2, column=0, sticky="nsew", pady=(height*0.005,0))
            ctk.CTkLabel(self.price_frame, text="Price: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.price_entry = ctk.CTkEntry(self.price_frame, fg_color=Color.White_Lotion, placeholder_text="Price", placeholder_text_color='light grey',font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, height=height*0.045)
            self.price_entry.pack(side='left', fill="x", expand=1, padx=(0, width*0.005), pady=(height*0.0075))
           
            '''DURATION TYPE'''
            self.duration_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.duration_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=(height*0.005,0))
            ctk.CTkLabel(self.duration_frame, text="Duration: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            
            self.radio_var = tk.IntVar(value=0) 
            self.one_rb_button = ctk.CTkRadioButton(self.duration_frame, text="one day", variable=self.radio_var, font=("DM Sans Medium", 14), value=0, command=radio_callback)
            self.one_rb_button.pack(side="left", padx=(width*0.005,0))
            self.more_rb_button = ctk.CTkRadioButton(self.duration_frame, text="multiple days", variable=self.radio_var, font=("DM Sans Medium", 14), value=1,  command=radio_callback)
            self.more_rb_button.pack(side="left")
            
            '''BOTTOM'''
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
            self.bottom_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005), pady = (0, height*0.01))
            
            self.cancel_btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, text="Cancel", fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14), command=reset)
            self.cancel_btn.pack(side='left')
            
            self.proceed_btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, width=width*0.115, text="Add Service", font=("DM Sans Medium", 14), command=new_service)
            self.proceed_btn.pack(side='right')
            
        def update_option(self):
            self.data=database.fetch_data(sql_commands.get_service_category_test)
            self.category_option.configure(values=[(s[0]) for s in self.data])
            
        def place(self, **kwargs):
            self.update_option()
            
            return super().place(**kwargs)
    return add_service(master, info, update_callback)

#That place is not for  any man or particles of bread