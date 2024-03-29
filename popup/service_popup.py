import customtkinter as ctk
import json
import sql_commands
import tkinter as tk
from customcustomtkinter import customcustomtkinter as cctk, customcustomtkinterutil as cctku
from Theme import Color
from tkinter import messagebox
from constants import action
from PIL import Image
import datetime
from typing import *
from util import *
from datetime import date, datetime as dt
from Theme import Icons

SETTINGS_VAL : dict = json.load(open("Resources\\general_settings.json"))

def add_service(master, info:tuple, update_callback: callable):
    class add_service(ctk.CTkFrame):
        def __init__(self, master, info:tuple, update_callback: callable):
            width = info[0]
            height = info[1]
            acc = info[2]
            super().__init__(master, width=width*0.4, height=height*0.55, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.update_callback = update_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            def reset():
                self.place_forget()
                self.service_name_entry.delete(0, tk.END)
                self.price_entry.delete(0, tk.END)
                #self.category_option.set("Set Category")
                
            def new_service():
                if self.service_name_entry.get() == "" or self.price_entry.get() == "":
                    messagebox.showerror("Unable to proceed", "Fill all the fields", parent = self)
                    return
                if self.service_name_entry.get() == "" and self.price_entry.get() == "":
                    messagebox.showerror("Missing Data", "Complete all the fields to continue", parent = self)
                if database.fetch_data('SELECT COUNT(*) FROM service_info_test WHERE service_name = ?', (self.service_name_entry.get(), ))[0][0] > 0:
                    messagebox.showerror("Unable to proceed", "Service name already exist", parent = self)
                else:    
                    database.exec_nonquery([[sql_commands.insert_service, (self.id_label._text, self.service_name_entry.get(), self.price_entry.get(), self.radio_var.get(), 1, date.today())]])
                    messagebox.showinfo("Service Added", "New service is added", parent = self)
                    record_action(acc, action.ADD_SERVICE, action.ADD_SVC % (acc, self.id_label._text))
                    reset()
                    update_callback()
                    
            def radio_callback():
                if self.radio_var.get() == 0:
                    self.note_label.configure(text = "Price Indicate the overall price of the service")
                elif self.radio_var.get() == 1:
                    self.note_label.configure(text = "Price Indicate the price per day of the service")
                elif self.radio_var.get() == 2:
                    self.note_label.configure(text = "Price Indicate per total periods of the service")
            
            self.service_icon = ctk.CTkImage(light_image= Image.open("image/services.png"), size=(20,20))
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
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
            
            '''ID'''
            self.service_id_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.service_id_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(width*0.005,0))
            ctk.CTkLabel(self.service_id_frame, text="Service Code: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.id_label = ctk.CTkLabel(self.service_id_frame, fg_color=Color.White_Platinum, corner_radius=5,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, height=height*0.055, width=width*0.125, text="TETOMG")
            self.id_label.pack(side='left', padx=(0, width*0.005), pady=(width*0.005,0))
            
            
            '''NAME'''
            self.service_name_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.service_name_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(width*0.005,0))
            ctk.CTkLabel(self.service_name_frame, text="Service Name: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.service_name_entry = ctk.CTkEntry(self.service_name_frame, fg_color=Color.White_Lotion, placeholder_text="Service Name", placeholder_text_color='light grey',font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, height=height*0.055)
            self.service_name_entry.pack(side='left', fill="x", expand=1, padx=(0, width*0.005), pady=(height*0.0075))
            
            '''CATEGORY'''
            #self.category_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            #self.category_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(height*0.005,0))
            #ctk.CTkLabel(self.category_frame, text="Category: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            #self.category_option= ctk.CTkOptionMenu(self.category_frame, anchor="w", font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
            #                                     text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts)
            #self.category_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            #self.category_option.set("Set Category")
            
            '''PRICE'''
            self.price_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.price_frame.grid(row=3, column=0, sticky="nsew", pady=(height*0.005,0))
            ctk.CTkLabel(self.price_frame, text="Price: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            self.price_entry = ctk.CTkEntry(self.price_frame, fg_color=Color.White_Lotion, placeholder_text="Price", placeholder_text_color='light grey',font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, height=height*0.055)
            self.price_entry.pack(side='left', fill="x", expand=1, padx=(0, width*0.005), pady=(height*0.0075))
           
            '''DURATION TYPE'''
            self.duration_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent")
            self.duration_frame.grid(row=4, column=0, columnspan=2, sticky="nsew", pady=(height*0.005,0))
            ctk.CTkLabel(self.duration_frame, text="Duration: ", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, width=width*0.085, anchor="e").pack(side='left', padx=(width*0.0045,0))
            
            self.radio_var = tk.IntVar(value=0) 
            self.one_rb_button = ctk.CTkRadioButton(self.duration_frame, text="One Day", variable=self.radio_var, font=("DM Sans Medium", 14), value=0, command=radio_callback)
            self.one_rb_button.pack(side="left", padx=(width*0.005,0))
            self.more_rb_button = ctk.CTkRadioButton(self.duration_frame, text="Scheduled", variable=self.radio_var, font=("DM Sans Medium", 14), value=1,  command=radio_callback)
            self.more_rb_button.pack(side="left")
            self.multiple_per_rb_button = ctk.CTkRadioButton(self.duration_frame, text="Multiple Periods", variable=self.radio_var, font=("DM Sans Medium", 14), value=2, command=radio_callback)
            self.multiple_per_rb_button.pack(side="left", padx=(width*0.005,0))


            '''NOTE FRAME'''
            self.note_frame = ctk.CTkFrame(self.sub_frame, fg_color= 'transparent')
            self.note_frame.grid(row=5, column=0, columnspan=2, sticky="nsew", pady=(height*0.005,0))
            self.note_label = ctk.CTkLabel(self.note_frame, text= "Note here", text_color=Color.Blue_Yale, font=("DM Sans Medium", 14))
            self.note_label.pack(side = 'bottom', padx = (width*.01, 0))
            radio_callback()
            
            '''BOTTOM'''
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
            self.bottom_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005), pady = (0, height*0.01))
            
            self.cancel_btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, text="Cancel", fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14), command=reset)
            self.cancel_btn.pack(side='left')
            
            self.proceed_btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, width=width*0.115, text="Add Service", font=("DM Sans Medium", 14), command=new_service)
            self.proceed_btn.pack(side='right')
            
            def checkprice(a, b, c):
                if (re.search(r'[0-9\.]$', self.price_entry.get() or "") is None):
                    l = len(self.price_entry.get())
                    self.price_entry.delete(l-1, l)
            self.price_checker = ctk.StringVar()
            self.price_checker.trace_add("write", checkprice)
            self.price_entry.configure(textvariable = self.price_checker)

            self.name_limiter = cctku.entry_limiter(256, self.service_name_entry)
            self.service_name_entry.configure(textvariable = self.name_limiter)

        def place(self, **kwargs):
            self.id_label.configure(text=generateId('S',6).upper())
            return super().place(**kwargs)
    return add_service(master, info, update_callback)

def calendar_with_scheduling(master, info:tuple, parent_ui: ctk.CTkLabel | ctk.CTkEntry = None, date_format = 'numerical', min_date = None, command: callable = None):
    class add_service(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent_ui: ctk.CTkLabel | ctk.CTkEntry = None, date_format = 'numerical', min_date = None, command: callable = None):
            width = info[0]
            height = info[1]
            global SETTINGS_VAL
            super().__init__(master, width=width * .65, height=height * .6, corner_radius= 0, fg_color=Color.White_Platinum)

            self.parent_ui = parent_ui
            self.date_format = date_format
            self._min_date = min_date or dt.today().date()
            self._command = command
            self.pack_propagate(0)
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(1, weight=1)
            self.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.055)
            self.top_frame.grid(row=0, column=0, sticky="ew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=Icons.schedule_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="Calendar", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.place_forget)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[0])
            self.main_frame.pack_propagate(0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid(row=1, column=0, sticky="nsew", padx=1, pady=(0,1))
            self.main_frame.grid_rowconfigure(0,weight=1)
            self.main_frame.grid_columnconfigure((0), weight=1)

            date = datetime.datetime.now()
            self.cal = cctk.tkc(self.main_frame, year=date.year, month=date.month, day=date.day, showweeknumbers=False, date_pattern="mm-dd-yyyy",
                                normalbackground="#EAEAEA", weekendbackground="#F3EFE0", state = ctk.NORMAL,
                                select_callback= self.get_data_schedule, mindate = self._min_date)
            self.cal.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(width*0.005))

            self.treeview_data = cctk.cctkTreeView(self.main_frame, width= width *.35, height= height * .4 * .8, column_format='/PetName:x-tl/Service:x-tl!33!35')
            self.treeview_data.grid(row=0, column=1, sticky="nse", padx=(width*0.005), pady=(width*0.005))

            self.btn = ctk.CTkButton(self.main_frame, text='Set Date', command= self.set_date_ui)
            self.btn.grid(row=1, column=0, columnspan=2, padx=(width*0.005), pady=(width*0.005))

            self.get_data_schedule()
            
        def get_data_schedule(self, m = None):
            selected_date = dt.now().strftime('%Y-%m-%d') if m is None else dt.strptime(m, '%m-%d-%Y').strftime('%Y-%m-%d')
            self.treeview_data.update_table(database.fetch_data(sql_commands.get_today_schedule_basic_info, (selected_date, selected_date)))

        def set_date_ui(self):

            if "numerical" in self.date_format:
                #label.configure(text= ( format % (self.cal.get_date())))
                date_text = str(self.cal.get_date())
            elif "raw" in self.date_format:
                date_text = self.cal.selection_get()
            elif "word" in self.date_format:
                #label.configure(text= f"{date_to_words(str(self.cal.get_date()))}")
                date_text = str(date_to_words(str(self.cal.get_date())))
            else:
                date_text = "Invalid Format"

            if len(self.treeview_data._data) >= SETTINGS_VAL['Daily_queue_max']:
                if not messagebox.askokcancel("Date over scheduled", "The date exceeds the schedule limit per day\nDo you want to proceed?", parent = self):
                    return
            #ask for over scheduling

            if isinstance(self.parent_ui, ctk.CTkLabel):
                self.parent_ui.configure(text = date_text)
            elif isinstance(self.parent_ui, ctk.CTkEntry):
                self.parent_ui.delete(0, ctk.END)
                self.parent_ui.insert(0, date_text)
            else:
                return date_text
            if self._command is not None:
                self._command()

            self.place_forget()
        
        def place(self, date = None, **kwargs):
            if date is not None:
                date = dt.strptime(date, '%m-%d-%Y').date()
                self.cal.configure(mindate = date)
            return super().place(**kwargs)

    return add_service(master, info, parent_ui, date_format, min_date)