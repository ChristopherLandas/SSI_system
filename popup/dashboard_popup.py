import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from customcustomtkinter import customcustomtkinterutil as cctku

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
from util import *
import util
from datetime import date

def status_bar(master, info: tuple, height, width, text: str, icon_color: str, count: int, window: callable, data: dict, 
               fg_color:str = Color.White_AntiFlash, hover_color:str = Color.Platinum):
    class instance(cctk.ctkButtonFrame):
        def __init__(self, master, info:tuple,  height, width, text: str, icon_color: str, count: int, window: callable, data: list,
                     fg_color:str, hover_color:str):
            self.info =info
            self.width = width
            self.height = height
            self._window = window
            self._data = data

            super().__init__(master, height=self.height, width=self.width, fg_color=fg_color ,hover_color=hover_color,corner_radius=5,cursor="hand2")
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.status_label = ctk.CTkLabel(self, text=text, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.status_label.grid(row = 0, column = 0, padx=(self.height*0.15, 0), stick='w')
            self.status_light = ctk.CTkFrame(self, height=self.height*0.15, width=self.height*0.15, corner_radius=8, border_width=1,
                                             border_color=Color.White_Ghost,fg_color=icon_color)
            self.status_count = ctk.CTkLabel(self, text=count, font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht)
            
            
            self.status_light.grid(row = 0, column = 2, padx=(0,self.height*0.15))    
            self.status_count.grid(row = 0, column = 1, padx=(0, self.height*0.15))
            
            if self.status_count._text == 0 or self.status_label._text == 'Safe/Normal': 
                self.status_light.configure(fg_color='transparent',border_width=0)
                
            self.update_children()

        def response(self, _):
            self._window(self.status_label._text, self._data )
            return super().response(_)
        
        def update_data(self, count, data):
            self.status_count.configure(text=count)
            self._data = data


    return instance(master, info, height, width, text, icon_color, count, window, data, fg_color, hover_color)


def sales_history_popup(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color='transparent')

            self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_history.png"), size=(25,25))

            def reset():
                self.place_forget()
                
            def open_record(_):
                print(self.sales_treeview.get_selected_data()[0])
                pass
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.685, height=height*0.755, fg_color=Color.White_Color[3], corner_radius= 0)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.sales_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='SALES HISTORY', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            self.content_frame.grid_columnconfigure(0,weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            self.title_frame = ctk.CTkFrame(self.content_frame, height=height*0.065, width=width*0.3, fg_color=Color.White_Lotion)
            self.title_frame.grid(row=0, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsw")
            self.title_frame.grid_propagate(0)
            self.title_frame.grid_rowconfigure(0, weight=1)
            self.title_frame.grid_columnconfigure(1, weight=1)            
            
            ctk.CTkLabel(self.title_frame, text="Sales History of ", font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht).grid(row=0, column=0, padx=(width*0.01,0))
            self.date_label = ctk.CTkLabel(self.title_frame, text="MONTH DAY YEAR", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_AntiFlash, corner_radius=5)
            self.date_label.grid(row=0, column=1, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            self.button_frame = ctk.CTkFrame(self.title_frame)
            
            self.data_treeview_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum, corner_radius=0)
            self.data_treeview_frame.grid(row=1, column=0, columnspan=2, padx=(width*0.005), pady=(0, height*0.01), sticky="nsew")
            
            self.sales_treeview = cctk.cctkTreeView(self.data_treeview_frame,  width=width*0.665, height=height*0.65,
                                                    column_format=f'/No:{int(width*.035)}-#r/TransactionID:{int(width*0.1)}-tc/Client:x-tl/Cashier:{int(width*0.15)}-tl/Total:{int(width*0.125)}-tr!30!30',)
            self.sales_treeview._double_click_command = open_record
            self.sales_treeview.pack()
        
            self.total_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.175)
            self.total_frame.grid(row=2, column=1, sticky="nse", padx=width*0.005, pady=(0,height*0.01))
            self.total_frame.pack_propagate(0)
            ctk.CTkLabel(self.total_frame, text=f"Total: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht).pack(side=ctk.LEFT, padx=(width*0.01))
            self.current_total = ctk.CTkLabel(self.total_frame, text="0,000.00", font=("DM Sans Medium", 14))
            self.current_total.pack(side=ctk.RIGHT, padx=(width*0.01))
            
        def place(self, sales_info,**kwargs):
            
            self.date_label.configure(text=f"{sales_info[0].strftime('%B %d, %Y')}")
            self.current_total.configure(text = f"{sales_info[1]}")
            self.raw_data = database.fetch_data(sql_commands.get_daily_sales_data_by_day, (f"{sales_info[0]}",))
            self.sales_treeview.update_table(self.raw_data)
                       
            return super().place(**kwargs)
            
    return instance(master, info)

def sched_info_popup(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color='transparent')

            self.sched_icon = ctk.CTkImage(light_image=Image.open("image/schedule.png"), size=(25,25))
            self.height = height
            self.width = width
                
            def open_record(_):
                if self.scheduled_pet_treeview.get_selected_data():
                    temp = list(self.scheduled_pet_treeview.get_selected_data())
                    temp.extend(list(self.client_data))
                    sched_service_info_popup(master,(width, height)).place(relx=0.5, rely=0.525, anchor='c', sched_info=temp)
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.65, height=height*0.675, fg_color=Color.White_Color[3], corner_radius= 0)
            def reset():
                self.place_forget()

            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.sched_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='SCHEDULE INFO', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            self.content_frame.grid_columnconfigure(1, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            self.header_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            '''CLIENT FRAME'''
            self.client_frame = ctk.CTkFrame(self.header_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.175)
            self.client_frame.pack(side="left")
            self.client_frame.pack_propagate(0)
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14), fg_color='transparent',).pack(side='left', padx=(width*0.01,0))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14), fg_color='transparent',)
            self.client_name.pack(side="left", fill='x', expand=1)
            
            '''CONTACT FRAME'''
            self.contact_frame = ctk.CTkFrame(self.header_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.195)
            self.contact_frame.pack(side="left", padx=(width*0.005,0))
            self.contact_frame.pack_propagate(0)
            ctk.CTkLabel(self.contact_frame, text="Contact: ", font=("DM Sans Medium", 14), fg_color='transparent',).pack(side='left', padx=(width*0.01,0))
            self.contact_name = ctk.CTkLabel(self.contact_frame, text="00000000000", font=("DM Sans Medium", 14), fg_color='transparent',)
            self.contact_name.pack(side="left", fill='x', expand=1)
            
            '''PET SELECTION FRAME'''
            self.scheduled_pet_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.scheduled_pet_frame.grid(row=1, column=0, columnspan=2, padx=(width*0.005), pady=(0,height*0.01), sticky="nsew")
            self.scheduled_pet_frame.grid_columnconfigure(1, weight=1)
            self.scheduled_pet_frame.grid_rowconfigure(1, weight=1)
            
            ctk.CTkLabel(self.scheduled_pet_frame, text="Scheduled Pet/s", font=("DM Sans Medium", 16), fg_color='transparent',).grid(row=0, column=0, padx=(width*0.01), pady=(height*0.01), sticky="nsw")
            ctk.CTkLabel(self.scheduled_pet_frame, text="Services scheduled for today", font=("DM Sans Medium", 12), text_color="grey", fg_color='transparent',).grid(row=0, column=1, padx=(0,width*0.01), pady=(height*0.01), sticky="sw")
            
            self.scheduled_pet_treeview_frame = ctk.CTkFrame(self.scheduled_pet_frame, fg_color='transparent', corner_radius=0)
            self.scheduled_pet_treeview_frame.grid(row=1, column=0, columnspan=2, padx=(width*0.005), pady=(0,height*0.01), sticky="nsew")
            
            self.scheduled_pet_treeview = cctk.cctkTreeView(self.scheduled_pet_treeview_frame, width=width*0.6175, height=height*0.5,
                                                            column_format=f'/No:{int(width*.03)}-#r/ReceptionID:{int(width*.125)}-tc/PetName:x-tl/Service:{int(width*.125)}-tl/Price:{int(width*.125)}-tr!30!30')
            self.scheduled_pet_treeview._double_click_command = open_record
            self.scheduled_pet_treeview.pack()

            
        def reset(self):
            self.place_forget()
            
        def place(self, sched_info, **kwargs):
            
            self.client_data = sched_info
            self.client_name.configure(text=f"{sched_info[0]}") 
            self.contact_name.configure(text=f"{sched_info[1]}")
            
            self.scheduled_pet = database.fetch_data(sql_commands.get_pet_client_scheduled_today, (f'{self.client_data[0]}',))
            self.scheduled_pet_treeview.update_table(self.scheduled_pet)
            
            return super().place(**kwargs)
            
    return instance(master, info)

def sched_service_info_popup(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color='transparent')

            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            self.sched_icon = ctk.CTkImage(light_image=Image.open("image/schedule.png"), size=(25,25))
            self.close = ctk.CTkImage(light_image=Image.open("image/close.png"), size=(18,18))
            self.done = ctk.CTkImage(light_image=Image.open("image/done.png"), size=(22,22))
            
            self.height = height
            self.width = width

            def cancel_resched():
                self.sched_date.configure(text=f"{date.today()}")
                self.queston_frame.grid_forget()
                
            def proceed_resched():
                print(self.sched_date.cget('text'))
            
            def check_date():
                
                if str(self.sched_date._text) == str(date.today()):
                    self.queston_frame.grid_forget()
                else:
                    self.queston_frame.grid(row=4, column=0, columnspan=2, sticky="ns", padx=(width*0.005), pady=(0,height*0.01))
                    
            self.main_frame = ctk.CTkFrame(self, width=width*0.45, height=height*0.575, fg_color=Color.White_Color[3], corner_radius= 0)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.sched_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='SERVICE SCHEDULE', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)

            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            self.content_frame.grid_columnconfigure((0,1), weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            '''RECEPTION FRAME'''
            self.reception_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.reception_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01,0))
            ctk.CTkLabel(self.reception_frame, text="ReceptionID: ", font=("DM Sans Medium", 14), fg_color='transparent',width=width*0.075, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.reception_name = ctk.CTkLabel(self.reception_frame, text="Grooming", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', padx=(width*0.005), width=width*0.125)
            self.reception_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''DATE ADDED FRAME'''
            self.date_added_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.date_added_frame.grid(row=0, column=1, sticky="nsew",  padx=(0,width*0.005), pady=(height*0.01,0))
            ctk.CTkLabel(self.date_added_frame, text="Date Added: ", font=("DM Sans Medium", 14), fg_color='transparent',width=width*0.075, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.date_added_name = ctk.CTkLabel(self.date_added_frame, text="Grooming", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', padx=(width*0.005), width=width*0.125)
            self.date_added_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''INFO FRAME'''
            self.info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.info_frame.grid(row=1, column=0, columnspan=2, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            self.info_frame.grid_columnconfigure((0,1), weight=1)
            
            '''CLIENT FRAME'''
            self.client_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_AntiFlash)
            self.client_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.client_frame, text="Client Name: ", font=("DM Sans Medium", 14), fg_color='transparent', width=width*0.065, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', width=width*0.125)
            self.client_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''CONTACT FRAME'''
            self.contact_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_AntiFlash)
            self.contact_frame.grid(row=0, column=1, sticky="nsew", padx=(0,width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.contact_frame, text="Contact: ", font=("DM Sans Medium", 14), fg_color='transparent', width=width*0.065, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.contact_name = ctk.CTkLabel(self.contact_frame, text="00000000000", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', width=width*0.125)
            self.contact_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''PET FRAME'''
            self.pet_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_AntiFlash)
            self.pet_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.pet_frame, text="Pet Name: ", font=("DM Sans Medium", 14), fg_color='transparent', width=width*0.065, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.pet_name = ctk.CTkLabel(self.pet_frame, text="Grooming", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', padx=(width*0.005), width=width*0.125)
            self.pet_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''SERVICE FRAME'''
            self.service_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_AntiFlash)
            self.service_frame.grid(row=2, column=0, sticky="nsew",padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.service_frame, text="Service: ", font=("DM Sans Medium", 14), fg_color='transparent', width=width*0.065, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.service_name = ctk.CTkLabel(self.service_frame, text="Grooming", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', padx=(width*0.005), width=width*0.125)
            self.service_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''PRICE FRAME'''
            self.price_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_AntiFlash)
            self.price_frame.grid(row=2, column=1, sticky="nsew", padx=(0,width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.price_frame, text="Price: ", font=("DM Sans Medium", 14), fg_color='transparent',width=width*0.05, anchor="e").pack(side='left', padx=(width*0.005,0), pady=(height*0.0085))
            self.price_name = ctk.CTkLabel(self.price_frame, text="Grooming", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', padx=(width*0.005), width=width*0.125)
            self.price_name.pack(side="left", fill='x', expand=1, padx=(0,width*0.005), pady=(height*0.0085))
            
            '''SCHDULE FRAME'''
            self.sched_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Platinum)
            self.sched_frame.grid(row=3, column=0, columnspan=2, sticky="ns", padx=(width*0.005), pady=(height*0.025,height*0.01))
            ctk.CTkLabel(self.sched_frame, text="Schedule Date: ", font=("DM Sans Medium", 14), fg_color='transparent',width=width*0.065, anchor="e").pack(side='left', padx=(width*0.01,0), pady=(height*0.0085))
            
            self.sched_date = ctk.CTkLabel(self.sched_frame, text="Grooming", font=("DM Sans Medium", 14), fg_color=Color.White_Lotion, corner_radius=5, padx=(width*0.005), width=width*0.15)
            self.sched_date.pack(side="left", fill='both', expand=1, padx=(0), pady=(height*0.0085))
            
            self.show_calendar = ctk.CTkButton(self.sched_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.sched_date, "%s", date_format="raw", min_date=datetime.datetime.now(), set_date_callback=check_date), corner_radius=5)
            self.show_calendar.pack(side="left", fill='x', expand=1, padx=(width*0.0025,width*0.005), pady=(height*0.0085))
            
            '''QUESTION FRAME'''
            self.queston_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Platinum)
            ctk.CTkLabel(self.queston_frame, text="Change Schedule?", font=("DM Sans Medium", 14), fg_color='transparent',width=width*0.065, anchor="e").pack(side='left', padx=(width*0.01,0), pady=(height*0.0085))
            
            self.no_button = ctk.CTkButton(self.queston_frame, text="No", width=width*0.075, height=height*0.055, font=("DM Sans Medium", 16), image=self.close,
                                           fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip, command=cancel_resched)
            self.no_button.pack(side='left', padx=(width*0.01,0), pady=(height*0.0085))
            
            self.yes_button = ctk.CTkButton(self.queston_frame, text="Yes", width=width*0.075, height=height*0.055, font=("DM Sans Medium", 16), image=self.done,
                                            command=proceed_resched)
            self.yes_button.pack(side='left', padx=(width*0.005), pady=(height*0.0085))
            
            self.data_labels = (self.reception_name, self.pet_name, self.service_name, self.price_name,
                                self.client_name, self.contact_name, self.date_added_name, self.sched_date)
            
        def reset(self):
            self.unload_data()
            self.place_forget()
            
            
        def load_data(self, data):
            for i in range(len(data)):
                self.data_labels[i].configure(text=data[i])
            
        def unload_data(self):
            for i in range(len(self.data_labels)):
                self.data_labels[i].configure(text="")
        
        def place(self, sched_info, **kwargs):
            
            temp =list(database.fetch_data(sql_commands.get_pet_service_date_sched, (f"{sched_info[4]}", f"{sched_info[1]}",f"{sched_info[0]}",f"{sched_info[2]}"))[0])
            data = sched_info + temp
            
            self.load_data(data)
            return super().place(**kwargs)
            
    return instance(master, info)