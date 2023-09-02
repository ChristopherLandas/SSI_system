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

def status_bar(master, info:tuple, text: str, icon_color: str, count: int, window: callable, data: dict):
    class instance(cctk.ctkButtonFrame):
        def __init__(self, master, info:tuple, text: str, icon_color: str, count: int, window: callable, data: dict):
            self.width = info[0]
            self.height = info[1]
            self._window = window
            self._data = data

            super().__init__(master, height=self.height * .2, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum,corner_radius=5,cursor="hand2")

            self.status_label = ctk.CTkLabel(self, text=text, font=("DM Sans Medium", 14))
            self.status_label.pack(side="left", padx=(self.width*0.04,0))
            self.status_light = ctk.CTkLabel(self, text="", height=self.height*0.04, width=self.width*0.03, corner_radius=8, fg_color=icon_color)
            self.status_light.pack(side="right", padx=(self.width*0.025,self.width*0.05))
            self.status_count = ctk.CTkLabel(self, text=count, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.status_count.pack(side="right")
            self.update_children()

        def response(self, _):
            self._window(self.status_label._text, self._data[self.status_label._text])
            print(self._data[self.status_label._text])
            return super().response(_)


    return instance(master, info, text, icon_color, count, window, data)


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

            def reset():
                self.place_forget()
                
            def open_record(_):
                print(self.sales_treeview.get_selected_data()[0])
                pass
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.5, height=height*0.6, fg_color=Color.White_Color[3], corner_radius= 0)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.sched_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='SCHEDULE INFO', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")
            
            
        def place(self, sched_info, **kwargs):
            
            print(sched_info)        
            
            return super().place(**kwargs)
            
    return instance(master, info)