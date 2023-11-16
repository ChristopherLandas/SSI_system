import tkinter as tk
import re
import customtkinter as ctk
import sql_commands
import tkcalendar
import util
from typing import Optional, Tuple, Union
from customcustomtkinter import customcustomtkinter as cctk
from Theme import Color
from util import database, generateId
from util import *
from tkinter import messagebox
from datetime import date, datetime
from constants import action
from PIL import Image
from functools import partial
from typing import *



def audit_info(master, info:tuple, title: Optional[str] = "Record Information"):
    class audit_info(ctk.CTkFrame):
        def __init__(self, master, info:tuple, title: Optional[str]):
            width = info[0]
            height = info[1]
            super().__init__(master, width=width*0.3, height=height*0.4, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.title = title
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=Icons.get_image('info_icon', (25,25)), anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text=self.title, anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.confirm_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.confirm_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.confirm_frame.grid_columnconfigure(0, weight=1)
            
            '''Added By'''
            self.added_by_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.added_by_frame.grid(row=0, column=0, sticky='nsew', pady = (height*0.025,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.added_by_frame, text="Added By:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e').pack(side='left',pady = (height*0.01), padx = (0))
            self.added_by_name = ctk.CTkLabel(self.added_by_frame, text="N/A", font=("DM Sans Medium", 14))
            self.added_by_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            '''Added Date'''
            self.added_date_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.added_date_frame.grid(row=1, column=0, sticky='nsew', pady = (0,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.added_date_frame, text="Added Date:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e').pack(side='left',pady = (height*0.01), padx = (0))
            self.added_date_entry = ctk.CTkLabel(self.added_date_frame, text="N/A", font=("DM Sans Medium", 14))
            self.added_date_entry.pack(side='left',pady = (height*0.01), padx = (0))
            
            '''Added By'''
            self.updated_by_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.updated_by_frame.grid(row=2, column=0, sticky='nsew', pady = (0,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.updated_by_frame, text="Updated By:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e').pack(side='left',pady = (height*0.01), padx = (0))
            self.updated_by_name = ctk.CTkLabel(self.updated_by_frame, text="N/A", font=("DM Sans Medium", 14))
            self.updated_by_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            '''Added Date'''
            self.updated_date_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.updated_date_frame.grid(row=3, column=0, sticky='nsew', pady = (0,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.updated_date_frame, text="Updated Date:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e' ).pack(side='left',pady = (height*0.01), padx = (0))
            self.updated_date_entry = ctk.CTkLabel(self.updated_date_frame, text="N/A", font=("DM Sans Medium", 14))
            self.updated_date_entry.pack(side='left',pady = (height*0.01), padx = (0))
            
            self.entries = [self.added_by_name, self.added_date_entry, self.updated_by_name, self.updated_date_entry]
        def reset(self):
            [entry.configure(text= 'N/A')  for entry in self.entries]
            self.place_forget()
        
        def set_entries(self):
            for entry in range(len(self.entries)):
                self.entries[entry].configure(text=self.info[entry])
        
        def place(self, info,**kwargs):
            self.info = info[0]
            self.set_entries()
            return super().place(**kwargs)
            
    return audit_info(master, info, title)