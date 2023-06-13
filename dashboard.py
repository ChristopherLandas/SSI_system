import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
import datetime;
import _tkinter
import sql_commands
import numpy as np
from tkinter import messagebox
from util import *
from functools import partial
from tkextrafont import Font
from Theme import Color
from PIL import Image
from datetime import date
from customcustomtkinter import customcustomtkinter as cctk
from customcustomtkinter import customcustomtkinterutil as cctku
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from constants import db
from constants import action
from popup import Inventory_popup, Pet_info_popup, transaction_popups, Sales_popup, dashboard_popup
import copy

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')
width = 0
height = 0
acc_info = ()
acc_cred = ()
date_logged = None
mainframes = []

class dashboard(ctk.CTkToplevel):
    def __init__(self, master:ctk.CTk, entry_key: str, _date_logged: datetime):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self._master = master
        #makes the form full screen and removing the default tab bar
        """ datakey = database.fetch_data(f'SELECT {db.USERNAME} from {db.ACC_CRED} where {db.acc_cred.ENTRY_OTP} = ?', (entry_key, ))

        if not datakey or entry_key == None:
            messagebox.showwarning('Warning', 'Invalid entry method\ngo to log in instead')
            self.destroy()
            return
        else:
            global acc_info, date_logged, acc_cred
            date_logged = _date_logged;
            acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (datakey[0][0], ))
            acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (datakey[0][0], ))
            database.exec_nonquery([[f'UPDATE {db.ACC_CRED} SET {db.acc_cred.ENTRY_OTP} = NULL WHERE {db.USERNAME} = ?', (datakey[0][0], )]])
            del datakey
        #for preventing security breach through python code; enable it to test it """

        global acc_info, acc_cred, date_logged, mainframes
        date_logged = _date_logged;
        acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (entry_key, ))
        acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (entry_key, ))
        #temporary for free access; disable it when testing the security breach prevention or deleting it if deploying the system

        '''Fonts'''
        try:
            Font(file="Font/Poppins-Medium.ttf")
            Font(file="Font/Poppins-Regular.ttf")
            Font(file='Font/Poppins-Bold.ttf')
            #Transitioning to new font style
            Font(file="Font/DMSans-Bold.ttf")
            Font(file="Font/DMSans-Medium.ttf")
            Font(file='Font/DMSans-Regular.ttf')

            #Use DM Mono for numbers
            Font(file="Font/DMMono-Light.ttf")
            Font(file="Font/DMMono-Medium.ttf")
            Font(file="Font/DMMono-Regular.ttf")

        except _tkinter.TclError:
            pass

        #for testing purposes, might delete after the development
        '''Import Images'''
        self.inv_logo = ctk.CTkImage(light_image=Image.open("image/logo1.png"),size=(37,35))
        self.dashboard_icon = ctk.CTkImage(light_image=Image.open("image/dashboard.png"),size=(22,22))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(26,20))
        self.inventory_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"),size=(24,25))
        self.patient_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(22,25))
        self.report_icon = ctk.CTkImage(light_image=Image.open("image/report.png"),size=(22,22))
        self.notif_icon = ctk.CTkImage(light_image=Image.open("image/notif.png"),size=(22,25))
        self.settings_icon = ctk.CTkImage(light_image=Image.open("image/setting.png"),size=(25,25))
        self.acc_icon = ctk.CTkImage(light_image=Image.open("image/acc.png"),size=(40,40))
        self.transact_icon = ctk.CTkImage(light_image=Image.open("image/transact.png"),size=(22,20))
        self.services_icon = ctk.CTkImage(light_image=Image.open("image/services.png"),size=(24,26))
        self.user_setting_icon = ctk.CTkImage(light_image=Image.open("image/usersetting.png"),size=(24,27))
        self.histlog_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"),size=(22,25))

        '''Global Variables'''
        global width, height
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()

        '''Main Information'''
        side_frame_w = round(width * 0.175)
        default_menubar_width = .15
        default_menubar_height = .3
        acc_menubar_width = .2
        title_name = "J.Z. Angeles Veterinary Clinic"

        unselected_btn_color = Color.Blue_Yale
        selected_btn_color = Color.Blue_Steel

        self.active_win = None
        self.main_frames = [dashboard_frame(self), transaction_frame(self), services_frame(self), sales_frame(self), inventory_frame(self), patient_info_frame(self), reports_frame(self), user_setting_frame(self), histlog_frame(self)]
        mainframes = self.main_frames
        self.active_main_frame = None

        '''setting the user level access'''
        user_level_access = database.fetch_data(sql_commands.get_level_acessess, (acc_info[0][2], ))[0]
        if(not user_level_access[1]):
            temp:inventory_frame = self.main_frames[4]
            temp.add_item_btn.destroy()
            del temp
        '''events'''
        def load_main_frame(title: str, cur_frame: int):
            self.title_label.configure(text= title.upper())
            if self.active_main_frame is not None:
                self.active_main_frame.grid_forget()
            self.active_main_frame = self.main_frames[cur_frame]
            self.active_main_frame.grid(row =1, column =1, sticky = 'nsew')

        def log_out():
            b = messagebox.askyesno('Log out', 'Are you sure you want to log out?')
            if b:
                database.exec_nonquery([[f'UPDATE {db.LOG_HIST} SET {db.log_hist.TIME_OUT} = ? WHERE {db.log_hist.DATE_LOGGED} = ? AND {db.log_hist.TIME_IN} = ?',
                                        (datetime.datetime.now().time(), date_logged.date(), date_logged.time().strftime("%H:%M:%S"))]])
                self._master.deiconify()
                self.destroy()

        '''commands'''
        def switch_darkmode():
            print(switch_var_darkmode.get())

        '''Switch Value'''
        switch_var_darkmode = ctk.StringVar(value="lightmode")

        self.grid_rowconfigure(1,weight=1)
        self.side_frame = ctk.CTkFrame(self, height= height, width = side_frame_w,
                                       fg_color=Color.Blue_Yale, border_color=None, corner_radius=0)
        self.side_frame.grid(rowspan=2,row = 0, column=0)
        self.side_frame.pack_propagate(False)

        '''Company Logo'''
        self.logo_frame = ctk.CTkFrame(self.side_frame, height=round(height * 0.1), width=side_frame_w,
                                       fg_color="transparent",corner_radius=0)
        self.logo_frame.pack(pady=(round(height * 0.02),round(height * 0.03)))

        self.logo_icon = ctk.CTkLabel(self.logo_frame, text="", image=self.inv_logo)
        self.logo_icon.pack(side="left",padx=(0,10))

        self.logo_label = ctk.CTkLabel(self.logo_frame, text=title_name, font=("Poppins Medium", 16),
                                       text_color=Color.Grey_Bright, wraplength=180, justify='left')
        self.logo_label.pack(side="right",padx=(5,0))

        self.db_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.db_button.configure(command=partial(change_active_event, self.db_button, 0))
        self.db_button.configure(command=partial(load_main_frame, 'dashboard', 0))
        self.db_button.pack()
        self.db_wbar = ctk.CTkLabel(self.db_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.db_wbar.pack(side="left")
        self.db_icon = ctk.CTkLabel(self.db_button,image=self.dashboard_icon, text="")
        self.db_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.db_label = ctk.CTkLabel(self.db_button, text="Dashboard", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.db_label.pack(side="left")
        self.db_button.pack()
        self.db_button.update_children()


        self.transact_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.transact_button.configure(command=partial(change_active_event, self.transact_button, 1))
        self.transact_button.configure(command=partial(load_main_frame, 'Transactions', 1))
        self.transact_button.pack()
        self.transact_wbar = ctk.CTkLabel(self.transact_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.transact_wbar.pack(side="left")
        self.transact_icon = ctk.CTkLabel(self.transact_button,image=self.transact_icon, text="")
        self.transact_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.transact_label = ctk.CTkLabel(self.transact_button, text="Transactions", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.transact_label.pack(side="left")
        self.transact_button.pack()
        self.transact_button.update_children()


        self.services_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.services_button.configure(command=partial(change_active_event, self.services_button, 2))
        self.services_button.configure(command=partial(load_main_frame, 'Services', 2))
        self.services_button.pack()
        self.services_wbar = ctk.CTkLabel(self.services_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.services_wbar.pack(side="left")
        self.services_icon = ctk.CTkLabel(self.services_button,image=self.services_icon, text="")
        self.services_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.services_label = ctk.CTkLabel(self.services_button, text="Services", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.services_label.pack(side="left")
        self.services_button.pack()
        self.services_button.update_children()


        self.sales_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.sales_button.configure(command=partial(change_active_event, self.sales_button, 3))
        self.sales_button.configure(command=partial(load_main_frame, 'Sales', 3))
        self.sales_button.pack()
        self.sales_wbar = ctk.CTkLabel(self.sales_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.sales_wbar.pack(side="left")
        self.sales_icon = ctk.CTkLabel(self.sales_button,image=self.sales_icon, text="")
        self.sales_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.sales_label = ctk.CTkLabel(self.sales_button, text="Sales", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.sales_label.pack(side="left")
        self.sales_button.pack()
        self.sales_button.update_children()


        self.inventory_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.inventory_button.configure(command=partial(change_active_event, self.inventory_button, 4))
        self.inventory_button.configure(command=partial(load_main_frame, 'Inventory', 4))
        self.inventory_button.pack()
        self.inventory_wbar = ctk.CTkLabel(self.inventory_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.inventory_wbar.pack(side="left")
        self.inventory_icon = ctk.CTkLabel(self.inventory_button,image=self.inventory_icon, text="")
        self.inventory_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.inventory_label = ctk.CTkLabel(self.inventory_button, text="Inventory", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.inventory_label.pack(side="left")
        self.inventory_button.pack()
        self.inventory_button.update_children()


        self.patient_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.patient_button.configure(command=partial(change_active_event, self.patient_button, 5))
        self.patient_button.configure(command=partial(load_main_frame, 'Pet Information', 5))
        self.patient_button.pack()
        self.patient_wbar = ctk.CTkLabel(self.patient_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.patient_wbar.pack(side="left")
        self.patient_icon = ctk.CTkLabel(self.patient_button,image=self.patient_icon, text="")
        self.patient_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.patient_label = ctk.CTkLabel(self.patient_button, text="Pet Information", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.patient_label.pack(side="left")
        self.patient_button.pack()
        self.patient_button.update_children()


        self.report_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.report_button.configure(command=partial(change_active_event, self.report_button, 6))
        self.report_button.configure(command=partial(load_main_frame, 'Report', 6))
        self.report_button.pack()
        self.report_wbar = ctk.CTkLabel(self.report_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.report_wbar.pack(side="left")
        self.report_icon = ctk.CTkLabel(self.report_button,image=self.report_icon, text="")
        self.report_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.report_label = ctk.CTkLabel(self.report_button, text="Report", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.report_label.pack(side="left")
        self.report_button.pack()
        self.report_button.update_children()


        self.user_setting_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.user_setting_button.configure(command=partial(change_active_event, self.user_setting_button, 7))
        self.user_setting_button.configure(command=partial(load_main_frame, 'Users', 7))
        self.user_setting_button.pack()
        self.user_setting_wbar = ctk.CTkLabel(self.user_setting_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.user_setting_wbar.pack(side="left")
        self.user_setting_icon = ctk.CTkLabel(self.user_setting_button,image=self.user_setting_icon, text="")
        self.user_setting_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.user_setting_label = ctk.CTkLabel(self.user_setting_button, text="Users", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.user_setting_label = ctk.CTkLabel(self.user_setting_button, text="Users", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.user_setting_label.pack(side="left")
        self.user_setting_button.pack()
        self.user_setting_button.update_children()


        self.histlog_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.histlog_button.configure(command=partial(change_active_event, self.histlog_button, 8))
        self.histlog_button.configure(command=partial(load_main_frame, 'Action Log', 8))
        self.histlog_button.pack()
        self.histlog_wbar = ctk.CTkLabel(self.histlog_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.histlog_wbar.pack(side="left")
        self.histlog_icon = ctk.CTkLabel(self.histlog_button,image=self.histlog_icon, text="")
        self.histlog_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.histlog_label = ctk.CTkLabel(self.histlog_button, text="Action Log", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.histlog_label.pack(side="left")
        self.histlog_button.pack()
        self.histlog_button.update_children()

        self.sidebar_btn_mngr = cctku.button_manager([self.db_button, self.transact_button, self.services_button, self.sales_button,
                                                     self.inventory_button, self.patient_button, self.report_button, self.user_setting_button,
                                                     self.histlog_button], selected_btn_color, False, 0)
        self.sidebar_btn_mngr._state = (lambda: self.sidebar_btn_mngr.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.sidebar_btn_mngr.active.winfo_children()[0].configure(fg_color=Color.White_Ghost))
        self.sidebar_btn_mngr.click(self.sidebar_btn_mngr._default_active, None)


        '''Top Frame'''
        self.top_frame = ctk.CTkFrame(self, height=round(height * 0.1), width=round(width* 0.825),
                                      corner_radius=0,fg_color=Color.White_Ghost)
        self.top_frame.grid(row=0, column=1, sticky="nsew")
        self.top_frame.grid_propagate(False)

        self.top_frame.grid_columnconfigure(0, weight=1)
        self.top_frame.grid_rowconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(self.top_frame, text="", font=("Poppins Medium", 16), text_color=Color.Blue_Maastricht)
        self.title_label.grid(row = 0, column=0,sticky='w', padx= width * 0.02)

        self.notif_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqheight()*0.5), text= "", image= self.notif_icon,
                                              fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight() *0.5), border_width=0, corner_radius=5,
                                              font=("Poppinds Medium", 16),hover_color=Color.White_Gray,)
        self.notif_btn.grid(row=0, column= 1, sticky='w')
        self.settings_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqheight()* 0.5), text= "", image= self.settings_icon,
                                              fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight()* 0.5), border_width=0, corner_radius=5,
                                              font=("Poppinds Medium", 16),hover_color=Color.White_Gray,)
        self.settings_btn.grid(row=0, column= 2, sticky='w')

        self.acc_btn = cctk.ctkButtonFrame(self.top_frame, round(self.top_frame.winfo_reqwidth() * .12),
                                           round(self.top_frame.winfo_reqheight()*.5), 5,
                                           fg_color=Color.White_Ghost,
                                           hover_color= Color.White_Gray,cursor="hand2")

        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.dp = ctk.CTkLabel(self.acc_btn, width * .03, width * .03, 0, 'transparent', 'transparent', text='', image=self.acc_icon,)
        self.dp.grid(row = 0, column = 0, rowspan = 3, sticky = 'nsew', pady = (round(height * .005), 0), padx = (round(height * .01), 0))
        """ self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][1]).upper(), font=("Poppins Medium", 15))
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .005), 0), pady = (5,0))
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][2]).upper(), font=("Poppins Medium", 12))
        self.position.grid(row = 1, column = 1, sticky = 'nw', padx = (round(height * .005), 0), pady = 0) """

        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.acc_btn.update_children()
        self.update()

        '''menubars'''
        self.notif_menu_bar= cctk.menubar(self, width * default_menubar_width, height * default_menubar_height,
                                          corner_radius= 0, fg_color='black', border_width= 0,
                                          position=(self.notif_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                                    self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                                    'c'))
        self.settings_menu_bar = cctk.menubar(self, width * default_menubar_width, height * default_menubar_height,
                                              corner_radius= 5, fg_color=Color.White_Ghost, border_width= 0,
                                              position=(self.settings_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                                        self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2+0.005,
                                                        'c'))
        self.settings_menu_bar_dark_mode = ctk.CTkSwitch(self.settings_menu_bar,width=round(width * default_menubar_width/2), height=round(height * .12),text="Dark Mode",
                                                         font=("Poppins Medium", 16), progress_color=Color.Blue_LapisLazuli_1, text_color=Color.Blue_Maastricht,
                                                         variable = switch_var_darkmode, onvalue="darkmode", offvalue="lightmode",
                                                         command=switch_darkmode,)
        self.settings_menu_bar_dark_mode.pack(anchor= 'c')
        self.acc_menu_bar = cctk.menubar(self, width * acc_menubar_width, height * default_menubar_height, 0, fg_color=Color.White_Ghost,
                                         position= (1 - acc_menubar_width/2,
                                                    self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                                    'c'))

        self.top_frame_button_mngr = cctku.button_manager([self.notif_btn, self.settings_btn, self.acc_btn], Color.Platinum, True,
                                                          children=[self.notif_menu_bar, self.settings_menu_bar, self.acc_menu_bar])
        print (*self.main_frames, sep = '\n')
        tempdel = 0
        if not user_level_access[2]:
            self.db_button.destroy()
            self.main_frames[0 - tempdel].destroy()
            del self.main_frames[0]
            del self.db_button
            tempdel += 1
        if not user_level_access[3]:
            self.transact_button.destroy()
            self.main_frames[1 - tempdel].destroy()
            del self.transact_button
            tempdel += 1
        if not user_level_access[4]:
            self.services_button.destroy()
            self.main_frames[2 - tempdel].destroy()
            del self.services_button
            tempdel += 1
        if not user_level_access[5]:
            self.sales_button.destroy()
            self.main_frames[3 - tempdel].destroy()
            del self.sales_button
            tempdel += 1
        if not user_level_access[6]:
            self.inventory_button.destroy()
            self.main_frames[4 - tempdel].destroy()
            del self.inventory_button
            tempdel += 1
        if not user_level_access[7]:
            self.patient_button.destroy()
            self.main_frames[5 - tempdel].destroy()
            del self.patient_button
            tempdel += 1
        if not user_level_access[8]:
            self.report_button.destroy()
            self.main_frames[6 - tempdel].destroy()
            del self.report_button
            tempdel+= 1
        if not user_level_access[9]:
            self.user_setting_button.destroy()
            self.main_frames[7 - tempdel].destroy()
            del self.user_setting_button
            tempdel += 1
        if not user_level_access[10]:
            self.histlog_button.destroy()
            self.main_frames[8 - tempdel].destroy()
            del self.histlog_button
            tempdel += 1
        del user_level_access

        '''setting default events'''
        load_main_frame('Dashboard', 0)
        #change_active_event(self.db_button, 0)
        self.protocol("WM_DELETE_WINDOW", log_out)
        self.mainloop()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''main frames'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class dashboard_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Chinese)
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                   float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]


        def show_pie(master, data: list):
            labels = ["Items", "Service"]

            data = data if data[0] + data[1] > 0 else [1, 0]
            pie_figure= Figure(figsize=(self.income_frame_width*0.006,self.income_frame_height*0.013), dpi=100)
            pie_figure.set_facecolor(Color.White_Ghost)
            ax =pie_figure.add_subplot(111)
            ax.pie(data, autopct='%1.1f%%', startangle=0,counterclock=0, explode=(0.1,0), colors=[Color.Light_Green, Color.Red_Tulip],
                   textprops={'fontsize':18, 'color': Color.White_Ghost, 'family':'monospace', 'weight':'bold' },)
            pie_figure.subplots_adjust(top=1,left=0,right=1, bottom=0)

            canvas = FigureCanvasTkAgg(pie_figure, master)
            canvas.draw()
            canvas.get_tk_widget().grid(row = 0, column=1, rowspan = 6)

        self.date_frame = ctk.CTkFrame(self, fg_color=Color.White_Ghost, corner_radius= 5)
        self.date_frame.grid(row=0, column=7, padx = (width * .025, width * .01), pady= (height * .01), sticky='e')
        self.date_label = ctk.CTkLabel(self.date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14))
        self.date_label.pack(anchor='c', padx = width * .015, pady = height * .01)

        '''Income summary frame'''
        self.income_summary_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.income_summary_frame.grid(row=1, column=0, columnspan=4, padx= (width*.01 ,width*(.005)))
        self.income_summary_frame.grid_propagate(0)

        self.income_frame_width, self.income_frame_height = self.income_summary_frame.cget('width'), self.income_summary_frame.cget("height")

        '''Income summary frame contents'''
        self.income_summary_frame.grid_columnconfigure((0,1), weight=1)
        self.income_summary_frame.grid_rowconfigure((2,3,4), weight=1)
        self.income_summary_label = ctk.CTkLabel(self.income_summary_frame,text="Daily Income Summary",fg_color="transparent", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht,)
        self.income_summary_label.grid(row=0, column=0, sticky="ew", pady=(self.income_frame_height*0.04,0))
        self.income_summary_sub = ctk.CTkLabel(self.income_summary_frame,text=f"as of {date.today().strftime('%B %d, %Y')}", font=("DM Sans Medium", 14), text_color=Color.Grey_Davy)
        self.income_summary_sub.grid(row=1, column=0, sticky="ew")

        self.num_transactions = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.num_transactions.grid(row=2, column=0, sticky="nsew", padx=(self.income_frame_width*0.03), pady=(self.income_frame_height*0.05, self.income_frame_height*.015),)
        self.num_transactions.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.num_transactions, text="Transactions Today:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.num_transactions, text="0", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.items_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.Light_Green, corner_radius=5)
        self.items_sales_frame.grid(row=3, column=0, sticky="nsew", padx=(self.income_frame_width*0.03), pady=(self.income_frame_height*0.015, self.income_frame_height*.015),)
        self.items_sales_frame.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.items_sales_frame, text="Items:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.items_sales_frame, text=f"₱{format_price(self.data[0])}", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.services_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.Red_Tulip, corner_radius=5)
        self.services_sales_frame.grid(row=4, column=0, sticky="nsew", padx=(self.income_frame_width*0.03),pady=( self.income_frame_height*.015))
        self.services_sales_frame.pack_propagate(0)
        self.services_sales_label = ctk.CTkLabel(self.services_sales_frame, text="Services:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.services_sales_value = ctk.CTkLabel(self.services_sales_frame, text=f"₱{format_price(self.data[1])}", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.total_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.15, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.total_sales_frame.grid(row=5, column=0, sticky="nsew", padx=(self.income_frame_width*0.03),pady=(self.income_frame_height*.015, self.income_frame_height*.05))
        self.total_sales_frame.pack_propagate(0)
        self.total_sales_label = ctk.CTkLabel(self.total_sales_frame, text="Total:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.total_sales_value = ctk.CTkLabel(self.total_sales_frame, text=f"₱{format_price(self.data[1] + self.data[0])}", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))
        #Watermelon Pie
        show_pie(self.income_summary_frame, self.data)

        '''Inventory Stat Frame'''
        self.inventory_stat_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.inventory_stat_frame.grid_propagate(0)
        self.inventory_stat_frame.grid(row=1, column=4, columnspan=4, padx= (width*(.005) ,width * .01))
        self.inventory_stat_frame.grid_rowconfigure(1, weight=1)
        self.inventory_stat_frame.grid_columnconfigure(1, weight=1)

        self.inventory_frame_width, self.inventory_frame_height = self.inventory_stat_frame.cget('width'), self.inventory_stat_frame.cget('height')

        '''Inventory Stat Frame Contents'''
        self.inventory_stat_label = ctk.CTkLabel(self.inventory_stat_frame, text="Inventory Status", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht)
        self.inventory_stat_label.grid(row=0, column=1, sticky="w", padx=(self.inventory_frame_width*0.04,0),pady=(self.inventory_frame_height*0.04,self.inventory_frame_height*0.02))



        self.inventory_content_frame = ctk.CTkScrollableFrame(self.inventory_stat_frame, height=self.inventory_frame_height*0.16, fg_color=Color.White_Ghost)
        self.inventory_content_frame.grid_propagate()
        self.inventory_content_frame.grid_columnconfigure(1, weight=1)
        self.inventory_content_frame.grid(row=1, column=1, sticky="news", padx=self.inventory_frame_width*0.025, pady=(0,self.inventory_frame_height*0.04))
        self.stat_tabs: list = []
        self.generate_stat_tabs()

        stat_data = [('Reorder', '#cccc00', database.fetch_data(sql_commands.get_reorder_state) or None),
                     ('Critical', '#ff0000', database.fetch_data(sql_commands.get_critical_state) or None),
                     ('Out-Of-Stock', '#222222', database.fetch_data(sql_commands.get_out_of_stock_state) or None),
                     ('Near Expire', '#ff7900', database.fetch_data(sql_commands.get_near_expire_state) or None),
                     ('Expire', '#dd0000', database.fetch_data(sql_commands.get_expired_state) or None)]
        stat_data = [s for s in stat_data if s[-1] is not None]
        stat_tabs_info: dict = {s[0]: s[-1] for s in stat_data}

        for i in range(len(stat_data)):
            temp = dashboard_popup.status_bar(self.inventory_content_frame, (self.inventory_frame_width, self.income_frame_height),
                                                                             stat_data[i][0], stat_data[i][1],
                                                                             len(stat_data[i][-1]), self.show_status_popup, stat_tabs_info)
            self.stat_tabs.append(copy.copy(temp))
            self.stat_tabs[-1].grid(row = i, column = 1, sticky = 'nsew', padx=(self.inventory_frame_width*0.001 ),pady=(0,self.inventory_frame_height*0.02))
            del temp

        '''Sales History'''
        self.sales_history_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.sales_history_frame.grid(row=2, column=0, columnspan=4, padx= (width * .01, width*(.005)), pady=(height*0.017))
        self.sales_history_frame.grid_propagate(0)
        self.sales_history_frame.grid_columnconfigure(1,weight=1)
        self.sales_history_frame.grid_rowconfigure(1,weight=1)

        ctk.CTkLabel(self.sales_history_frame, text=f"Sales History", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht).grid(row=0, column=0, padx=(width*0.02,0), pady=(height*0.025, height*0.005))
        ctk.CTkLabel(self.sales_history_frame, text=f"as of {date.today().strftime('%B %Y')}", text_color="grey", font=("DM Sans Medium",14)).grid(row=0, column=1, sticky="sw", padx=(width*0.005,0), pady=(0,height*0.005))
        self.sales_data_frame = ctk.CTkFrame(self.sales_history_frame, fg_color="transparent")
        self.sales_data_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",pady=(0))

        self.sales_data_treeview = cctk.cctkTreeView(self.sales_data_frame, width=width*0.365, height=height*0.45,
                                               column_format=f'/No:{int(width*.03)}-#c/Day:x-tl/Total:x-tl/Action:{int(width*0.05)}-tc!30!30',
                                               header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent')
        self.sales_data_treeview.pack()

        self.current_total = ctk.CTkLabel(self.sales_history_frame, text="Total:   0,000.00", fg_color=Color.White_Chinese, corner_radius=5,height=height*0.05, width=width*0.125, anchor="e", font=("DM Sans Medium", 14))
        self.current_total.grid(row=2, column=1, sticky="e", padx=width*0.015, pady=(height*0.005,height*0.015))

        self.view_more_button = ctk.CTkButton(self.sales_history_frame, text='View More',width= self.income_frame_width*0.16, height=self.income_frame_height*0.06, font=('DM Sans Medium', 12), corner_radius=4, text_color=Color.Blue_Maastricht,
                                              fg_color=Color.White_AntiFlash,hover_color=Color.Platinum, command=lambda:print("Go To Report Section"))
        self.view_more_button.grid(row=2, column=0, sticky="w", padx=self.income_frame_width*0.035,pady=(0,self.income_frame_height*0.035))

        '''Schedule Appointments'''
        self.sched_client_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.sched_client_frame.grid(row=2, column=4, columnspan=4, padx= (width*(.005), width*.01 ), pady=(height*0.017))
        self.sched_client_frame.grid_propagate(0)
        self.sched_client_frame.grid_columnconfigure(1,weight=1)
        self.sched_client_frame.grid_rowconfigure(1,weight=1)

        ctk.CTkLabel(self.sched_client_frame, text="Scheduled Clients Today", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht).grid(row=0, column=0, padx=width*0.02, pady=(height*0.025, height*0.005))
        self.sched_data_frame = ctk.CTkFrame(self.sched_client_frame)
        self.sched_data_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=width*0.015, pady=(0,height*0.025))

        self.sched_data_treeview = cctk.cctkTreeView(self.sched_data_frame, width=width*0.365, height=height*0.45,
                                               column_format=f'/No:{int(width*.03)}-#r/ClientName:x-tl/Service:x-tr/Number:{int(width*.125)}-bD!30!30',
                                               header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent')
        self.sched_data_treeview.pack()

        self.status_popup = Inventory_popup.show_status(self, (width, height, acc_cred, acc_info))
        self.grid_forget()

    def show_status_popup(self, name: str, data):
            self.status_popup.status_label.configure(text = name)
            self.status_popup.update_treeview(data)
            self.status_popup.place(relx = .5, rely = .5, anchor = 'c')

    def show_pie(self, master, data: list):
        data = data if data[0] + data[1] > 0 else [1, 0]
        pie_figure= Figure(figsize=(self.income_frame_width*0.006,self.income_frame_height*0.013), dpi=100)
        pie_figure.set_facecolor(Color.White_Ghost)
        ax =pie_figure.add_subplot(111)
        ax.pie(data, autopct='%1.1f%%', startangle=0,counterclock=0, explode=(0.1,0), colors=[Color.Light_Green, Color.Red_Tulip],
                textprops={'fontsize':18, 'color': Color.White_Ghost, 'family':'monospace', 'weight':'bold' },)
        pie_figure.subplots_adjust(top=1,left=0,right=1, bottom=0)

        canvas = FigureCanvasTkAgg(pie_figure, master)
        canvas.draw()
        canvas.get_tk_widget().grid(row = 0, column=1, rowspan = 6)

    def generate_stat_tabs(self):
        for i in self.stat_tabs:
            i.destroy()
        self.stat_tabs.clear()
        stat_data = [('Reorder', '#cccc00', database.fetch_data(sql_commands.get_reorder_state) or None),
                     ('Critical', '#ff0000', database.fetch_data(sql_commands.get_critical_state) or None),
                     ('Out-Of-Stock', '#222222', database.fetch_data(sql_commands.get_out_of_stock_state) or None),
                     ('Near Expire', '#ff7900', database.fetch_data(sql_commands.get_near_expire_state) or None),
                     ('Expire', '#dd0000', database.fetch_data(sql_commands.get_expired_state) or None)]
        stat_data = [s for s in stat_data if s[-1] is not None]
        stat_tabs_info: dict = {s[0]: s[-1] for s in stat_data}

        for i in range(len(stat_data)):
            temp = dashboard_popup.status_bar(self.inventory_content_frame, (self.inventory_frame_width, self.income_frame_height),
                                                                             stat_data[i][0], stat_data[i][1],
                                                                             len(stat_data[i][-1]), self.show_status_popup, stat_tabs_info)
            self.stat_tabs.append(copy.copy(temp))
            self.stat_tabs[-1].grid(row = i, column = 1, sticky = 'nsew', padx=(self.inventory_frame_width*0.001 ),pady=(0,self.inventory_frame_height*0.02))
            del temp

    def grid(self, **kwargs):
        return super().grid(**kwargs)

class transaction_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, mainframes
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.customer_infos = []

        '''events'''
        def clear_without_verification():
            self.item_treeview.delete_all_data()
            self.final_total_value.configure(text = format_price(float(price_format_to_float(self.final_total_value._text)) - float(price_format_to_float(self.final_total_value._text))))
            self.item_total_value.configure(text = '0.00')

        def proceed():
            if not self.client_name_entry.get():
                messagebox.showerror('Unable to Proceed', 'Customer\'s Name must be filled')
                return
            if price_format_to_float(self.final_total_value._text) == 0:
                messagebox.showerror('Unable to Proceed', 'No Item Listed')
                return
            self.show_transaction_proceed = transaction_popups.show_transaction_proceed(self, (width, height, (self.item_treeview, self.service_treeview), acc_cred[0]),
                                                                                        self.item_treeview._data, self.service_treeview._data,
                                                                                        price_format_to_float(self.final_total_value._text),
                                                                                        self.client_name_entry.get(), self.customer_infos or None)
            self.show_transaction_proceed.place(relx = .5, rely =.5, anchor = 'c')


        self.trash_icon = ctk.CTkImage(light_image=Image.open("image/trash.png"), size=(20,20))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
        self.service_icon = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(20,20))
        self.item_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"), size=(20,20))
        self.cal_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(20,20))
        self.proceed_icon = ctk.CTkImage(light_image=Image.open("image/rightarrow.png"), size=(15,15))

        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((2), weight=1)

        self.or_num_label = ctk.CTkLabel(self, fg_color=Color.White_Ghost, corner_radius=5, width=width*0.125, height = height*0.05,
                                         text="OR#: 0001", font=("DM Sans Medium", 15))
        self.or_num_label.grid(row=0, column=0, padx=(width*0.005,0), pady=(height*0.01), sticky="w")

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Ghost, width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=2, padx=(width*0.005),  pady=(height*0.01))

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent", )
        self.top_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")


        self.client_name_frame = ctk.CTkFrame(self.top_frame, fg_color=Color.White_Ghost, width=width*0.4, height=height*0.05,)
        self.client_name_frame.pack(side="left",padx=(width*0.005))
        self.client_name_frame.pack_propagate(0)

        self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
        self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

        self.client_name_entry = ctk.CTkEntry(self.client_name_frame, placeholder_text="Client's Name",font=("DM Sans Medium", 15), border_width=0, fg_color="white")
        self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005), pady=(height*0.005))

        self.add_service = ctk.CTkButton(self.top_frame, image=self.service_icon, text="Add Service", height=height*0.05, width=width*0.1,font=("Arial", 14),
                                         command=lambda:self.show_services_list.place(relx=0.5, rely=0.5, anchor="c"))
        self.add_service.pack(side="left")

        self.add_item = ctk.CTkButton(self.top_frame, image=self.item_icon, text="Add item",height=height*0.05, width=width*0.1, font=("Arial", 14),
                                      command=lambda:self.show_list_item.place(relx=0.5, rely=0.5, anchor="c"))
        self.add_item.pack(side="left",padx=(width*0.005))
        self.sched_service = ctk.CTkButton(self.top_frame, image=self.cal_icon, text="Scheduled Service",height=height*0.05, width=width*0.1, font=("Arial", 14),
                                           command=lambda:self.show_sched_service.place(relx=0.5, rely=0.5, anchor="c"))
        self.sched_service.pack(side="right", padx=(0,width*0.005))

        self.transact_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3])
        self.transact_frame.grid(row=2, column=0, columnspan=3, sticky="new", padx=(width*0.005), pady=(height*0.01))

        '''self.transact_treeview = cctk.cctkTreeView(self.transact_frame, data=[], width=width*0.8, height=height*0.6,
                                                   column_format=f'/No:{int(width*0.025)}-#r/Particulars:x-tl/UnitPrice:{int(width*0.085)}-tr/Quantity:{int(width*0.1)}-tc/Total:{int(width*0.085)}-tr/Action:{int(width*.065)}-tl!30!30')
        self.transact_treeview.pack(pady=(height*0.01,0))

        self.bottom_frame = ctk.CTkFrame(self.transact_frame, fg_color="transparent", height=height*0.05)
        self.bottom_frame.pack(pady=(height*0.01), fill="x", padx=(width*0.005))
        #self.bottom_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
        """Testing ONLY REMOVE AFTER"""
        self.test = ctk.CTkButton(self.bottom_frame, text="TEST",  height=height*0.05, width=width*0.05,
                                  command=lambda: self.show_customer_info.place(relx=0.5, rely=0.5, anchor="c"))
        self.test.pack(side="left")

        self.price_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        self.price_total_frame.pack(side="right")
        self.price_total_frame.pack_propagate(0)

        ctk.CTkLabel(self.price_total_frame, text="Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
        self.price_total_amount = ctk.CTkLabel(self.price_total_frame, text="0,000.00", font=("Arial", 14))
        self.price_total_amount.pack(side="right",  padx=(0,width*0.0075))

        self.item_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        self.item_total_frame.pack(side="right", padx=(0,width*0.0075))
        self.item_total_frame.pack_propagate(0)

        ctk.CTkLabel(self.item_total_frame, text="Item:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
        self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text="0,000.00", font=("Arial", 14))
        self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))

        self.services_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        self.services_total_frame.pack(side="right", padx=(0,width*0.0075))
        self.services_total_frame.pack_propagate(0)

        ctk.CTkLabel(self.services_total_frame, text="Services:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
        self.services_total_amount = ctk.CTkLabel(self.services_total_frame, text="0,000.00", font=("Arial", 14))
        self.services_total_amount.pack(side="right",  padx=(0,width*0.0075))



        self.proceeed_button = ctk.CTkButton(self, text="Proceed", image=self.proceed_icon, height=height*0.05, width=width*0.1,font=("Arial", 14), compound="right",
                                             command=lambda:self.show_proceed_transact.place(relx=0.5, rely=0.5, anchor="center"))
        self.proceeed_button.grid(row=3, column=2, pady=(0,height*0.025))'''


        self.transact_treeview = cctk.cctkTreeView(self.transact_frame, data=[], width=width*0.8, height=height*0.6,
                                                   column_format=f'/No:{int(width*0.025)}-#r/Particulars:x-tl/UnitPrice:{int(width*0.085)}-tr/Quantity:{int(width*0.1)}-id/Total:{int(width*0.085)}-tr/Action:{int(width*.065)}-bD!30!30')
        self.transact_treeview.pack(pady=(height*0.01,0))

        self.bottom_frame = ctk.CTkFrame(self.transact_frame, fg_color="transparent", height=height*0.05)
        self.bottom_frame.pack(pady=(height*0.01), fill="x", padx=(width*0.005))
        #self.bottom_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))

        self.price_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        self.price_total_frame.pack(side="right")
        self.price_total_frame.pack_propagate(0)

        ctk.CTkLabel(self.price_total_frame, text="Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
        self.price_total_amount = ctk.CTkLabel(self.price_total_frame, text="0,000.00", font=("Arial", 14))
        self.price_total_amount.pack(side="right",  padx=(0,width*0.0075))

        self.item_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        self.item_total_frame.pack(side="right", padx=(0,width*0.0075))
        self.item_total_frame.pack_propagate(0)

        ctk.CTkLabel(self.item_total_frame, text="Item:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
        self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text="0,000.00", font=("Arial", 14))
        self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))

        self.services_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        self.services_total_frame.pack(side="right", padx=(0,width*0.0075))
        self.services_total_frame.pack_propagate(0)

        ctk.CTkLabel(self.services_total_frame, text="Services:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
        self.services_total_amount = ctk.CTkLabel(self.services_total_frame, text="0,000.00", font=("Arial", 14))
        self.services_total_amount.pack(side="right",  padx=(0,width*0.0075))

        self.proceeed_button = ctk.CTkButton(self, text="Proceed", image=self.proceed_icon, height=height*0.05, width=width*0.1,font=("Arial", 14), compound="right")
        self.proceeed_button.grid(row=3, column=2, pady=(0,height*0.025))

        """ self.service_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=Color.White_Ghost)
        self.service_frame.grid(row=1, column=0, columnspan=3, stick="nsew", padx=(width*0.005),pady=(0,height*0.005))
        self.service_frame.grid_columnconfigure(0, weight=1)
        self.service_frame.grid_rowconfigure(0, weight=1)

        self.service_treeview = cctk.cctkTreeView(self.service_frame, width=width*0.8, height=height*0.3, bd_pop_list= self.customer_infos,
                                                  column_format=f'/No:{int(width*.03)}-#c/ItemCode:{int(width*0.08)}-tc/ServiceName:x-tl/Pet:x-iT/Price:{int(width*.07)}-tr/Discount:{int(width*.08)}-tr/Total:{int(width*.08)}-tc/Action:{int(width*.05)}-bD!50!40',)
        self.service_treeview.grid(row=0, column=0, columnspan=4, padx=(width*0.005), pady=(height*0.01))

        self.service_clear_button = ctk.CTkButton(self.service_frame, text="", image=self.trash_icon, command=lambda:print("Clear All Service"),
                                                  fg_color="#EB455F", width=width*0.028, height=height*0.045, hover_color="#A6001A")
        self.service_clear_button.grid(row=1, column=1, pady=(0,height*0.01), padx=(0, width*0.005))
        self.service_add_button = ctk.CTkButton(self.service_frame, text="Add Service", image=self.add_icon, command= lambda: self.show_services_list.place(relx = .5, rely = .5, anchor = 'c'),
                                                 font=("DM Sans Medium", 14), width=width*0.1, height=height*0.045)
        self.service_add_button.grid(row=1, column=2, pady=(0,height*0.01), padx=(0, width*0.005))
        self.service_total_frame = ctk.CTkFrame(self.service_frame, height=height*0.045, width=width*0.2, corner_radius=5)
        self.service_total_frame.grid(row=1, column=3, pady=(0,height*0.01), padx=(0, width*0.05))
        self.service_total_frame.pack_propagate(0)
        self.service_total_label = ctk.CTkLabel(self.service_total_frame, text="Service Total:", font=("DM Sans Medium", 14))
        self.service_total_label.pack(side="left", padx=(width*0.01, 0))
        self.service_total_value = ctk.CTkLabel(self.service_total_frame, text="00,000.00", font=("DM Sans Medium", 14))
        self.service_total_value.pack(side="right", padx=(0, width*0.01))

        self.item_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=Color.White_Ghost)
        self.item_frame.grid(row=2, column=0, columnspan=3, stick="nsew", padx=(width*0.005),pady=(height*0.005,height*0.01))
        self.item_frame.grid_columnconfigure(0, weight=1)
        self.item_frame.grid_rowconfigure(0, weight=1)

        self.item_treeview = cctk.cctkTreeView(self.item_frame, width=width*0.8, height=height*0.3, row_hover_color="light grey",
                                               column_format=f'/No:{int(width*.03)}-#c/ItemCode:{int(width*0.08)}-tc/ItemName:x-tl/Price:{int(width*.07)}-tr/Quantity:{int(width*.15)}-id/Discount:{int(width*.08)}-tr/Total:{int(width*.08)}-tr/Action:{int(width*.05)}-bD!30!30')
        self.item_treeview.grid(row=0, column=0, columnspan=4, padx=(width*0.005), pady=(height*0.01))


        self.item_clear_button = ctk.CTkButton(self.item_frame, text="", image=self.trash_icon, command= self.clear_all_item,
                                                  fg_color="#EB455F", width=width*0.028, height=height*0.045, hover_color="#A6001A")
        self.item_clear_button.grid(row=1, column=1, pady=(0,height*0.01), padx=(0, width*0.005))
        self.item_add_button = ctk.CTkButton(self.item_frame, text="Add item", image=self.add_icon, command=lambda: self.show_list_item.place(relx = .5, rely= .5, anchor = 'c'),
                                                 font=("DM Sans Medium", 14), width=width*0.1, height=height*0.045)
        self.item_add_button.grid(row=1, column=2, pady=(0,height*0.01), padx=(0, width*0.005))
        self.item_total_frame = ctk.CTkFrame(self.item_frame, height=height*0.045, width=width*0.2, corner_radius=5)
        self.item_total_frame.grid(row=1, column=3, pady=(0,height*0.01), padx=(0, width*0.05))
        self.item_total_frame.pack_propagate(0)
        self.item_total_label = ctk.CTkLabel(self.item_total_frame, text="Item Total:", font=("DM Sans Medium", 14))
        self.item_total_label.pack(side="left", padx=(width*0.01, 0))
        self.item_total_value = ctk.CTkLabel(self.item_total_frame, text="0,000.00", font=("DM Sans Medium", 14))
        self.item_total_value.pack(side="right", padx=(0, width*0.01))


        self.bottom_frame = ctk.CTkFrame(self,height=height*0.05, fg_color="#E0E0E0")
        self.bottom_frame.grid(row=3, column=0, columnspan=3, pady=(0,height*0.01), padx=(width*0.005),sticky="nsew")
        self.bottom_frame.pack_propagate(0)


        self.proceed_button = ctk.CTkButton(self.bottom_frame, text="Proceed", cursor="hand2", hover_color="#2C74B3", command= proceed)
        self.proceed_button.pack(side="right", padx=10)

        self.draft_button = ctk.CTkButton(self.bottom_frame, text="Draft", cursor="hand2", hover_color="#2C74B3")
        self.draft_button.pack(side="right", padx=10)


        self.total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.2, fg_color="#F9F9F9")
        self.total_frame.pack(side="right", padx=10)
        self.total_frame.pack_propagate(0)

        self.final_total_label = ctk.CTkLabel(self.total_frame, text="Total:", font=("DM Sans Medium", 14))
        self.final_total_label.pack(side="left", padx=(width*0.01, 0))
        self.final_total_value = ctk.CTkLabel(self.total_frame, text="00,000,000.00", font=("DM Sans Medium", 14))
          self.final_total_value.pack(side="right", padx=(0, width*0.01))"""

        self.transact_treeview.bd_configs = [(4, [self.item_total_amount, self.price_total_amount])]
        self.transact_treeview.bd_configs = [(4, [self.services_total_amount, self.price_total_amount])]
        self.show_list_item: ctk.CTkFrame = transaction_popups.show_item_list(self, (width, height), self.transact_treeview, self.change_total_value_item)
        self.show_services_list: ctk.CTkFrame = transaction_popups.show_services_list(self, (width, height), self.transact_treeview, self.change_total_value_service)
        self.show_proceed_transact: ctk.CTkFrame = transaction_popups.show_transaction_proceed(self, (width, height))
        self.show_customer_info:ctk.CTkFrame = transaction_popups.customer_info(self, (width, height))
        self.show_sched_service:ctk.CTkFrame = transaction_popups.scheduled_services(self,(width, height))

    def change_total_value_item(self, value: float):
            value = float(value)
            self.item_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.item_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))

    def change_total_value_service(self, value: float):
            value = float(value)
            self.services_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.services_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))

    def clear_all_item(self):
           verification = messagebox.askyesno('Clear All', 'Are you sure you want to delete\nall trasaction record?')
           if verification:
                self.reset()

    def reset(self):
        temp: dashboard_frame = mainframes[0]
        temp.show_pie()
        self.item_treeview.delete_all_data()
        self.final_total_value.configure(text = format_price(float(price_format_to_float(self.final_total_value._text)) - float(price_format_to_float(self.final_total_value._text))))
        self.service_total_value.configure(text = '0.00')
        self.item_total_value.configure(text = '0.00')

class services_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='3').pack(anchor='w')

        '''events'''
        def update_tables(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.services_raw_data = database.fetch_data(sql_commands.get_service_data, None)
            self.services_data_for_treeview = [] if self.services_raw_data is None else [(s[0], format_price(float(s[1])), s[2]) for s in self.services_raw_data]
            self.services_treeview.update_table(self.services_data_for_treeview)
            self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        self.inventory = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(25,22))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

        self.grid_columnconfigure(4, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.search_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], width=width*0.35, height = height*0.05,)
        self.search_frame.grid(row=0, column=0,padx=(width*0.005))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="light grey")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="light grey", hover_color="grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))

        self.add_service = ctk.CTkButton(self,text="Add Service", width=width*0.1, height = height*0.05, image=self.plus)
        self.add_service.grid(row=0, column=1)

        """ self.service_inventory = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.inventory)
        self.service_inventory.grid(row=0, column=2,padx=(width*0.005,0)) """

        self.refresh_btn = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=update_tables)
        self.refresh_btn.grid(row=0, column=2,padx=(width*0.005))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Ghost, width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=5, padx=(0, width*0.005),  pady=(height*0.01))

        self.service_data_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3])
        self.service_data_frame.grid(row=1, column=0, columnspan=6, sticky="nsew", padx=(width*0.005), pady=(0,height*0.025))

        self.services_raw_data = database.fetch_data(sql_commands.get_service_data, None)
        self.services_data_for_treeview = [(s[0], format_price(float(s[1])), s[2]) for s in self.services_raw_data]
        self.services_treeview = cctk.cctkTreeView(self.service_data_frame, data = self.services_data_for_treeview, width=width*0.8, height=height*0.8,
                                               column_format=f'/No:{int(width*.025)}-#r/Name:x-tl/Price:{int(width*.07)}-tr/LastedEdited:{int(width*.1)}-tc/Actions:{int(width*.08)}-bD!30!30',
                                               header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent')
        self.services_treeview.pack(padx=(width*0.005), pady=(height*0.015))

class sales_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.grid_columnconfigure(2,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_forget()

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="nsew", padx=width*0.005,pady=height*0.01)

        self.search_frame = ctk.CTkFrame(self,width=width*0.3, height = height*0.05, fg_color="white")
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="light grey")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="light grey", hover_color="grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))


        self.refresh_btn = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1)

        self.treeview_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3])
        self.treeview_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))

        self.main_data = database.fetch_data(sql_commands.get_transaction_data, None)
        self.main_data = [(s[0], s[2], str(datetime.datetime.now().date()), format_price(float(s[3])), s[1]) for s in self.main_data]
        self.data_view = cctk.cctkTreeView(self.treeview_frame, width=width * .8, height=height * .8,
                                           column_format=f'/No:{int(width*0.025)}-#r/OR:{int(width*0.075)}-tc/Client:x-tl/Date:{int(width*0.15)}-tc/Total:{int(width*0.085)}-tr/Cashier:{int(width*.175)}-tl!30!30')
        #self.data_view.configure(double_click_command = lambda _: Sales_popup.show_sales_record_info(self, (width, height), ('a', 'b', 'c'), [None, None]).place(relx = .5, rely = .5, anchor = 'c') )
        self.data_view.pack(pady=(width*0.005))

class inventory_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, mainframes
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
        self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(20,21))
        self.disposal_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
        self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))
        self.history_icon = ctk.CTkImage(light_image= Image.open("image/histlogs.png"), size=(22,25))
        self.trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(16,18))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.inventory_sub_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.restock_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.disposal_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])

        self.report_frames=[self.inventory_sub_frame, self.restock_frame,self.disposal_frame]
        self.active_report = None

        self.sort_type_option_var = ctk.StringVar(value="View by Levels")
        self.sort_status_option_var = ctk.StringVar(value="Normal")

        self.sort_status_var=["View by Levels","View by Category", "View by Expiry"]
        self.sort_type_var=["Normal","Reorder","Critical"]

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        '''data'''
        selected_color = Color.Blue_Yale
        self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)

        def refresh(_ :any = None):
            self.sort_type_option.set('View by Levels')
            sort_status_callback('View by Levels')

        def update_tables(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.refresh_btn.after(1000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
            self.data_view1.pack_forget()
            self.data_view1.update_table(self.list_show)
            self.data_view1.pack()

        def sort_status_callback(option):
            if "Levels" in option:
                self.sort_status_option.configure(values=["All", "Normal","Reorder","Critical"])
                self.sort_status_option.set("All")
                sort_status_configuration_callback()
            elif "Category" in option:
                self.sort_status_option.configure(values=["All Items","Medicine", "Accessories", "Food"])
                self.sort_status_option.set("All Items")
                #sort_status_configuration_callback()
            else:
                self.sort_status_option.configure(values=["Safe","Nearly Expire", "Expired", "No Expiration"])
                self.sort_status_option.set("Safe")
                sort_status_configuration_callback()
                #self.sort_type_var=["Safe","Nearly Expire", "Expired"]

        def sort_status_configuration_callback(_: any = None):
            self.search_entry.delete(0, ctk.END)
            if "Levels" in self.sort_type_option.get():
                if "All" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
                elif "Normal" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_normal_inventory)
                elif "Reorder" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_reorder_inventory)
                elif "Critical" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_critical_inventory)
            elif 'Expiry' in self.sort_type_option.get():
                if 'Safe' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_safe_expire_inventory)
                elif 'Nearly' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_near_expire_inventory)
                elif 'Expired' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_expired_inventory)
                elif 'No Exp' in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_non_expiry_inventory)
            update_tables()

        def search(_: any = None):
            if self.search_entry.get():
                temp = [s for s in self.list_show if self.search_entry.get().lower() in s[0].lower()]
                self.data_view1.update_table(temp)
                del temp
            else:
                update_tables()

        def reset(self):
            self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
            self.data2 = database.fetch_data(sql_commands.get_inventory_by_expiry, None)
            self.data_view1.update_table(self.data1)
            self.data_view2.update_table(self.data2)

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")


        self.inventory_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.1,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.inventory_button.configure(command=partial(load_main_frame, 0))
        self.inventory_icon = ctk.CTkLabel(self.inventory_button, text="",image=self.inventory_icon)
        self.inventory_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_label = ctk.CTkLabel(self.inventory_button, text="INVENTORY", text_color="white",)
        self.inventory_label.pack(side="left")
        self.inventory_button.grid()
        self.inventory_button.update_children()

        self.stock_in_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.1,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.stock_in_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.stock_in_button.configure(command=partial(load_main_frame, 1))
        self.stock_in_icon = ctk.CTkLabel(self.stock_in_button, text="",image=self.restock_icon)
        self.stock_in_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_in_label = ctk.CTkLabel(self.stock_in_button, text="RECEIVING", text_color="white")
        self.stock_in_label.pack(side="left")
        self.stock_in_button.grid()
        self.stock_in_button.update_children()

        self.stock_disposal_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.stock_disposal_button.grid(row=0, column=2, sticky="sw", padx=(0,width*0.0025), pady=0)
        self.stock_disposal_button.configure(command=partial(load_main_frame, 2))
        self.stock_disposal_icon = ctk.CTkLabel(self.stock_disposal_button, text="",image=self.trash_icon)
        self.stock_disposal_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_disposal_label = ctk.CTkLabel(self.stock_disposal_button, text="ITEM DISPOSAL", text_color="white")
        self.stock_disposal_label.pack(side="left")
        self.stock_disposal_button.grid()
        self.stock_disposal_button.update_children()

        self.button_manager = cctku.button_manager([self.inventory_button, self.stock_in_button, self.stock_disposal_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        '''INVENTORY FRAME: START'''
        self.inventory_sub_frame.pack(fill="both", expand=1)
        self.inventory_sub_frame.grid_propagate(0)
        self.inventory_sub_frame.grid_rowconfigure(1, weight=1)
        self.inventory_sub_frame.grid_columnconfigure(3, weight=1)

        """ self.search_frame = ctk.CTkFrame(self.inventory_sub_frame,width=width*0.3, height = height*0.05)
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0, fg_color="white")
        self.search_entry.bind('<Return>', search)
        self.search_entry.bind('<Button-1>', lambda _: self.search_entry.configure(state = ctk.NORMAL))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1) """

        self.search_frame = ctk.CTkFrame(self.inventory_sub_frame,width=width*0.3, height = height*0.05, fg_color="light grey")
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="grey",
                                        width=width*0.005, command=search)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))

        '''self.search_frame = ctk.CTkFrame(self.inventory_sub_frame,width=width*0.3, height = height*0.05, fg_color="light grey")
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0, fg_color="white")
        self.search_entry.bind('<Return>', search)
        self.search_entry.bind('<Button-1>', lambda _: self.search_entry.configure(state = ctk.NORMAL))
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="grey",
                                        width=width*0.005, command=search)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))'''

        self.add_item_btn = ctk.CTkButton(self.inventory_sub_frame,width=width*0.08, height = height*0.05, text="Add Item",image=self.add_icon, font=("DM Sans Medium", 14),
                                          command= lambda : self.add_item_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_item_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.refresh_btn = ctk.CTkButton(self.inventory_sub_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=2, sticky="w")

        self.sort_type_option= ctk.CTkOptionMenu(self. inventory_sub_frame,  height = height*0.05, values=self.sort_status_var, anchor="center",
                                                 command=partial(sort_status_callback))
        self.sort_type_option.grid(row=0, column=4, padx=(width*0.005,0), sticky="e")

        self.sort_status_option= ctk.CTkOptionMenu(self. inventory_sub_frame,  height = height*0.05, values=self.sort_type_var, anchor="center",
                                                   command=sort_status_configuration_callback)
        self.sort_status_option.grid(row=0, column=5, padx=(width*0.005), sticky="e")

        self.restock_btn = ctk.CTkButton(self.inventory_sub_frame, width=width*0.1, height = height*0.05, text="Stock Order", image=self.restock_icon, font=("DM Sans Medium", 14),
                                         command= lambda : self.restock_popup.place(default_data=self.data_view1.data_grid_btn_mng.active or None, update_cmds=[mainframes[0].generate_stat_tabs, ], relx = .5, rely = .5, anchor = 'c'))
        self.restock_btn.grid(row=3, column=5, pady=(height*0.01), sticky="e", padx=(0, width*0.005))
        self.tree_view_frame = ctk.CTkFrame(self.inventory_sub_frame, fg_color="transparent")
        self.tree_view_frame.grid(row=1, column=0,columnspan=6, sticky="nsew",padx=(width*0.005))

        self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.data_view1 = cctk.cctkTreeView(self.tree_view_frame, self.data1, width= width * .805, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Stock:{int(width*.07)}-tr/Price:{int(width*.07)}-tr/NearestExpire:{int(width*.1)}-tc/Status:{int(width*.08)}-tc!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 14),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,
                                           conditional_colors= {5: {'Reorder':'#ff7900', 'Critical':'red','Normal':'green', 'Out Of Stock': '#555555', 'Safe':'green', 'Nearly Expire':'#FFA500','Expired':'red'}})
        self.data_view1.pack()

        self.refresh_btn.configure(command = refresh)

        self.sort_type_option.set("View by Levels")

        '''INVENTORY FRAME: END'''

        '''RESTOCK: START'''
        #self.restock_frame.pack(fill="both", expand=1)
        self.restock_frame.grid_propagate(0)
        self.restock_frame.grid_rowconfigure(1, weight=1)

        self.restock_frame.grid_columnconfigure(3, weight=1)

        """ self.rs_search_frame = ctk.CTkFrame(self.restock_frame,width=width*0.3, height = height*0.05)
        self.rs_search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))

        self.rs_search_frame.pack_propagate(0)
        ctk.CTkLabel(self.rs_search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.rs_search_entry = ctk.CTkEntry(self.rs_search_frame, placeholder_text="Search", border_width=0, fg_color="white")
        self.rs_search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1) """

        self.rs_search_frame = ctk.CTkFrame(self.restock_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
        self.rs_search_frame.grid(row=0, column=0,padx=(width*0.005))
        self.rs_search_frame.pack_propagate(0)

        ctk.CTkLabel(self.rs_search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
        self.rs_search_entry = ctk.CTkEntry(self.rs_search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
        self.rs_search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.rs_search_btn = ctk.CTkButton(self.rs_search_frame, text="", image=self.search, fg_color="white", hover_color="grey",
                                        width=width*0.005)
        self.rs_search_btn.pack(side="left", padx=(0, width*0.0025))

        self.rs_add_item_btn = ctk.CTkButton(self.restock_frame,width=width*0.1, height = height*0.05, text="Add Order",image=self.add_icon, font=("DM Sans Medium", 14),
                                           command= lambda : self.restock_popup.place(default_data=self.data_view1.data_grid_btn_mng.active or None, relx = .5, rely = .5, anchor = 'c'))
        self.rs_add_item_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_refresh_btn = ctk.CTkButton(self.restock_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")

        self.rs_refresh_btn.grid(row=0, column=2, sticky="w", padx=(0,width*0.005))

        self.receive_history = ctk.CTkButton(self.restock_frame, width=width*0.025, height = height*0.05, text="Received Items", image=self.history_icon, font=("DM Sans Medium", 14),
                                             command=lambda: self.history_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.receive_history.grid(row=0, column=3, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_supplier_btn = ctk.CTkButton(self.restock_frame,width=width*0.08, height = height*0.05, text="Supplier",image=self.person_icon, font=("DM Sans Medium", 14),
                                          command= lambda : self.supplier_list_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.rs_supplier_btn.grid(row=0, column=4,sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_treeview_frame = ctk.CTkFrame(self.restock_frame,fg_color="transparent")
        self.rs_treeview_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=width*0.005)

        #self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.rs_data = database.fetch_data(sql_commands.get_recieving_items)
        self.rs_data_view1 = cctk.cctkTreeView(self.rs_treeview_frame, data= self.rs_data,width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ReceivingID:{int(width * .07)}-tc/ItemName:x-tl/Quantity:{int(width*.08)}-tr/SupplierName:x-tr/Action:{int(width*.075)}-bD!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel)
        self.rs_data_view1.configure(double_click_command = lambda _: self.restock_popup.stock(self.rs_data_view1))
        self.rs_data_view1.pack()
        '''RESTOCK FRAME: END'''

        '''ITEM DISPOSAL: START'''
        def dispose_item(_: any = None):
            data = (self.ds_data_view1._data[self.ds_data_view1.data_frames.index(self.ds_data_view1.data_grid_btn_mng.active)])
            uid = database.fetch_data(sql_commands.get_uid, (data[0], ))[0][0]
            if messagebox.askyesno('Dispose item', 'Are you sure you wan\'t to\nDispose the item?'):
                database.exec_nonquery([[sql_commands.delete_disposing_items, (uid, data[1])]])
                database.exec_nonquery([[sql_commands.record_disposal_process, data + ('klyde', )]])
                self.ds_data_view1.update_table(database.fetch_data(sql_commands.get_for_disposal_items))

        self.disposal_frame.grid_propagate(0)
        self.disposal_frame.grid_rowconfigure(1, weight=1)
        self.disposal_frame.grid_columnconfigure(3, weight=1)

        self.ds_treeview_frame = ctk.CTkFrame(self.disposal_frame,fg_color="transparent")
        self.ds_treeview_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=width*0.005)

        self.ds_data = database.fetch_data(sql_commands.get_for_disposal_items)
        self.ds_data_view1 = cctk.cctkTreeView(self.ds_treeview_frame, data= self.ds_data,width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Quantity:{int(width*.15)}-tr/Action:{int(width*.075)}-bD!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel, double_click_command=dispose_item)
        self.ds_data_view1.pack()

        self.ds_disposal_history = ctk.CTkButton(self.disposal_frame, width=width*0.025, height = height*0.05, text="Disposal Record", image=self.history_icon, font=("DM Sans Medium", 14),
                                             command=lambda: self.disposal_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.ds_disposal_history.grid(row=0, column=0, sticky="w", padx=(width*0.005), pady=(height*0.01))

        self.ds_refresh_btn = ctk.CTkButton(self.disposal_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.ds_refresh_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005))

        self.ds_dispose_all = ctk.CTkButton(self.disposal_frame, width=width*0.025, height = height*0.05, text="Dispose All", image=self.disposal_icon, font=("DM Sans Medium", 14))
        self.ds_dispose_all.grid(row=0, column=4, sticky="w", padx=(0,width*0.005), pady=(height*0.01))


        '''ITEM DISPOSAL: END'''

        self.disposal_popup = Inventory_popup.disposal_history(self, (width, height, acc_cred, acc_info))
        self.history_popup = Inventory_popup.receive_history(self, (width, height, acc_cred, acc_info))
        self.restock_popup = Inventory_popup.restock(self, (width, height, acc_cred, acc_info), self.rs_data_view1)
        self.add_item_popup = Inventory_popup.add_item(self, (width, height, acc_cred, acc_info))
        self.supplier_list_popup = Inventory_popup.supplier_list(self,(width, height, acc_cred, acc_info))

        sort_status_callback("View by Levels")
        load_main_frame(0)

class patient_info_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='6').pack(anchor='w')

        self.grid_forget()
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
        self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))
        self.trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(22,25))
        self.gen_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(18,20))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=4, sticky="n", padx=(width*0.005), pady=(height*0.01))

        self.search_frame = ctk.CTkFrame(self,width=width*0.3, height = height*0.05, fg_color="white")
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="light grey")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="light grey", hover_color="grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))

        """ self.search_frame = ctk.CTkFrame(self,width=width*0.3, height = height*0.05, fg_color=Color.White_Color[3])
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0,font=("Arial", 14), text_color="black", fg_color=Color.White_Platinum)
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1) """

        self.add_record_btn = ctk.CTkButton(self, width=width*0.08, height = height*0.05, text="Add Record",image=self.add_icon, font=("DM Sans Medium", 14),
                                            command=lambda:self.new_record.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_record_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.refresh_btn = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=2, sticky="w")

        self.treeview_frame =ctk.CTkFrame(self,fg_color=Color.White_Color[3])
        self.treeview_frame.grid(row=1, column=0, columnspan=5,sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))
        self.treeview_frame.grid_columnconfigure(0, weight=1)

        self.data = database.fetch_data('SELECT p_name, o_name, contact from pet_info')
        self.pet_data_view = cctk.cctkTreeView(self.treeview_frame, data=self.data,width= width * .805, height= height * .75, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/PetName:x-tl/OwnerName:{int(width*.25)}-tr/LastUpdate:{int(width*.185)}-tr/Action:{int(width*.075)}-bD!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
        self.pet_data_view.grid(row=0, column=0, columnspan=3, pady=(height*0.01))


        self.view_record = ctk.CTkButton(self.treeview_frame, text="View Record", image=self.gen_icon, font=("Arial", 14), width=width*0.1,height=height*0.0425,
                                              command=lambda:self.view_record.place(relx = .5, rely = .5, anchor = 'c'), state="enable")
        self.view_record.grid(row=1,column=2, pady=(0,height*0.05),padx=(0,width*0.005))
        #if no item is selected the button remains disabled

        self.new_record = Pet_info_popup.new_record(self, (width, height, acc_cred, acc_info))
        self.view_record = Pet_info_popup.view_record(self, (width, height, acc_cred, acc_info))

    def update(self) -> None:
        self.data = database.fetch_data('SELECT p_name, o_name, contact from pet_info')
        self.pet_data_view.update_table(self.data)
        return super().update()

class reports_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='7').pack(anchor='w')
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))

        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))


        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.sales_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])
        self.inventory_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])

        self.sales_report_frame.grid_columnconfigure(1, weight=1)
        self.sales_report_frame.grid_rowconfigure(2, weight=1)

        self.inventory_report_frame.grid_columnconfigure(1, weight=1)
        self.inventory_report_frame.grid_rowconfigure(1, weight=1)

        self.report_frames=[self.sales_report_frame, self.inventory_report_frame]
        self.active_report = None

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        selected_color = Color.Blue_Yale
        '''Test DATA'''

        data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
               float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]

        label=["Items", "Services"]

        monthly_data_items=[4427, 4573, 765, 777, 1513, 528, 4132, 4975, 4826, 4998, 568, 3184, 4586, 3587, 59, 966, 3644, 1298, 823, 2134, 1786, 3505, 4735, 3221, 4746, 4394, 3719, 2040, 574, 21, 627]
        monthly_data_service=[1235, 4541, 615, 767, 1455, 528, 4132, 4975, 4826, 4998, 568, 3184, 4586, 3587, 59, 966, 3644, 1298, 823, 2134, 1786, 3505, 4735, 3221, 4746, 4394, 3719, 2040, 574, 21, 627]
        monthly_label=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31']

        yearly_data_service=[63186, 42850, 42820, 55140, 58043, 99675, 86688, 81409, 5547, 3301, 2170, 44858]
        yearly_data_items=[63186, 42850, 42820, 55140, 58043, 99675, 86688, 81409, 5547, 3301, 2170, 44858]
        yearly_label=["January", "Febuary", "March","April","May", "June", "July", "August","September","October", "November", "December"]

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row =1, column =0, sticky = 'nsew',padx=width*0.005, pady=height*0.005)

        def report_menu_callback(report_type):

            if "Daily" in report_type:
                self.monthly_graph.grid_forget()
                self.month_option.grid_forget()
                self.year_option.grid_forget()
                self.year_option.grid_forget()
                self.yearly_graph.grid_forget()
                self.daily_data_view.pack(pady=height*0.01, padx=width*0.005)
                self.monthly_data_view.pack_forget()
                self.yearly_data_view.pack_forget()
                self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.date_selected_label.grid(row=0, column=1, padx=(0, width*0.005))
                self.show_calendar.grid(row=0, column=2,  padx=(0, width*0.005))

            elif "Monthly" in report_type:
                self.date_selected_label.grid_forget()
                self.show_calendar.grid_forget()
                self.daily_graph.grid_forget()
                self.daily_data_view.pack_forget()
                self.yearly_graph.grid_forget()
                self.yearly_data_view.pack_forget()
                self.monthly_data_view.pack(pady=height*0.01, padx=width*0.005)
                self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.month_option.grid(row=0, column=1)
                self.year_option.grid(row=0, column=2, padx=(width*0.005, width*0.01))
            elif "Yearly" in report_type:
                self.date_selected_label.grid_forget()
                self.show_calendar.grid_forget()
                self.month_option.grid_forget()
                self.daily_graph.grid_forget()
                self.monthly_data_view.pack_forget()
                self.yearly_data_view.pack(pady=height*0.01, padx=width*0.005)
                self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.year_option.grid(row=0, column=2, padx=(width*0.005, width*0.01))

        def set_date():
            cctk.tk_calendar(self.date_selected_label,"%s", date_format="word")

        def show_pie(master, data, info=[], label=[]):

            height = info[1]
            width =info[0]
            fg_color = info[2]

            label = label
            data = data
            pie_figure= Figure(figsize=(width, height), dpi=100)
            pie_figure.set_facecolor(fg_color)
            ax =pie_figure.add_subplot(111)
            ax.pie(data, labels=label, autopct='%1.1f%%', startangle=90,counterclock=0,
                   textprops={'fontsize':12, 'color':"black", 'family':'monospace'}, colors=[Color.Light_Green,Color.Red_Tulip])

            canvas = FigureCanvasTkAgg(pie_figure, master)
            canvas.draw()
            canvas.get_tk_widget().pack()

        def show_hbar(master, data, info=[], label=[]):

            height = info[1]
            width =info[0]
            fg_color = info[2]

            label = label
            data = data

            bar_figure= Figure(figsize=(width, height), dpi=100)
            bar_figure.set_facecolor(fg_color)
            ax =bar_figure.add_subplot(111)
            ax.barh(label, data, align='center',  color=[Color.Light_Green,Color.Red_Tulip])
            #ax.set_xlabel("Income")
            canvas = FigureCanvasTkAgg(bar_figure, master)
            canvas.draw()
            canvas.get_tk_widget().pack()

        def show_bar(master, data_service, data_item, info=[], label=[]):

            height = info[1]
            width =info[0]
            fg_color = info[2]

            _label = label
            _data_service = data_service
            _data_item = data_item

            x_axis = np.arange(len(_label))

            bar_figure= Figure(figsize=(width, height), dpi=100)
            bar_figure.set_facecolor(fg_color)
            ax = bar_figure.add_subplot(111)

            ax.bar(x_axis-0.2, _data_item, width=0.4, label=_label[0], color=Color.Light_Green)
            ax.bar(x_axis+0.2, _data_service, width=0.4, label = _label[1], color= Color.Red_Tulip)
            ax.legend(["Income", "Services"])
            ax.set_xticks(x_axis,_label)
            #ax.set_xlabel("Income")

            canvas = FigureCanvasTkAgg(bar_figure, master)
            canvas.draw()
            canvas.get_tk_widget().pack()

        operational_year = ["2021","2022","2023"]
        """ starting_year = 2014
        for i in range((int(date.today().strftime('%Y'))+1)-starting_year):
           operational_year.append(str(starting_year+i)) """

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")


        self.sales_report_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.sales_report_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.sales_report_button.configure(command=partial(load_main_frame, 0))
        self.sales_report_icon = ctk.CTkLabel(self.sales_report_button, text="",image=self.sales_icon)
        self.sales_report_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.sales_report_label = ctk.CTkLabel(self.sales_report_button, text="SALES REPORT", text_color="white",)
        self.sales_report_label.pack(side="left")
        self.sales_report_button.grid()
        self.sales_report_button.update_children()

        self.inventory_report_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_report_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_report_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.inventory_report_button.configure(command=partial(load_main_frame, 1))
        self.inventory_report_icon = ctk.CTkLabel(self.inventory_report_button, text="",image=self.inventory_icon)
        self.inventory_report_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_report_label = ctk.CTkLabel(self.inventory_report_button, text="INVENTORY REPORT", text_color="white")
        self.inventory_report_label.pack(side="left")
        self.inventory_report_button.grid()
        self.inventory_report_button.update_children()

        self.button_manager = cctku.button_manager([self.sales_report_button, self.inventory_report_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        self.report_option_var = ctk.StringVar(value="Daily Report")

        self.sales_report_top = ctk.CTkFrame(self.sales_report_frame)
        self.sales_report_top.grid(row=0, column=0, sticky="w", pady=(height*0.0025,0))

        self.report_type_menu = ctk.CTkOptionMenu(self.sales_report_top, values=["Daily Report", "Monthly Report", "Yearly Report"], variable=self.report_option_var,anchor="center",
                                                  command=partial(report_menu_callback))
        self.report_type_menu.grid(row=0, column=0, padx=(width*0.005), pady=height*0.005)

        self.date_selected_label = ctk.CTkLabel(self.sales_report_top, text=f"{date.today().strftime('%B %d, %Y')}", fg_color=Color.White_Color[3], corner_radius=5,
                                                width=width*0.1)
        self.date_selected_label.grid(row=0, column=1, padx=(0, width*0.005))

        self.show_calendar = ctk.CTkButton(self.sales_report_top, text="", image=self.calendar_icon, width=width*0.025,
                                           command=set_date)
        self.show_calendar.grid(row=0, column=2,  padx=(0, width*0.005))

        self.refresh_btn = ctk.CTkButton(self.sales_report_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1, sticky="w",  padx=(width*0.0025), pady=(height*0.005,0))

        self.refresh_btn = ctk.CTkButton(self.sales_report_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1, sticky="w",  padx=(width*0.0025), pady=(height*0.005,0))

        self.month_option = ctk.CTkOptionMenu(self.sales_report_top, values=["April","May", "June"], anchor="center", width=width*0.1 )
        self.month_option.set(f"{date.today().strftime('%B')}")
        self.year_option = ctk.CTkOptionMenu(self.sales_report_top, values=operational_year, width=width*0.075, anchor="center")
        self.year_option.set(f"{date.today().strftime('%Y')}")

        self.daily_graph = ctk.CTkFrame(self.sales_report_frame, fg_color="#DBDBDB")
        self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
        self.daily_graph.grid_columnconfigure((3), weight=2)
        self.daily_graph.grid_rowconfigure((0), weight=1)

        self.sales_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color="#DBDBDB")
        self.sales_daily_graph.grid(row=0, column= 0,columnspan=3, sticky="nsew",  padx=(width*0.005,0), pady=(height*0.01))

        self.items_total = ctk.CTkLabel(self.daily_graph,  text=f"Item:        {format_price(data[0])}", corner_radius=5, fg_color="white")
        self.items_total.grid(row=1, column=0,padx=(width*0.005,0), pady=(0,height*0.007))
        self.service_total = ctk.CTkLabel(self.daily_graph,text=f"Services     {format_price(data[1])}", corner_radius=5, fg_color="white")
        self.service_total.grid(row=1, column=1, padx=(width*0.005), pady=(0,height*0.007))
        self.income_total = ctk.CTkLabel(self.daily_graph,text=f"Total    {format_price(data[0] + data[1])}", corner_radius=5, fg_color="white")
        self.income_total.grid(row=1, column=2, sticky="nsew", pady=(0,height*0.007))

        self.bars_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color="#DBDBDB", height=height*0.35)
        self.bars_daily_graph.grid(row=0, column= 3, sticky="nsew", padx=(width*0.005), pady=(height*0.01,0))
        self.bars_daily_graph.pack_propagate(0)

        show_pie(self.sales_daily_graph, data=data if data[0] + data[1] > 0 else [1,0], info=[width*0.004,height*0.005,"#DBDBDB"], label=label)
        show_hbar(self.bars_daily_graph, data=data, info=[width*0.05,height*0.005,"#DBDBDB"], label=label)

        self.data_frame = ctk.CTkFrame(self.sales_report_frame, height=height*0.35)
        self.data_frame.grid(row=2, column=0, sticky="nsew", columnspan = 2,pady=height*0.0075)

        self.daily_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.785, height=height *0.35,
                                           column_format=f'/No:{int(width*0.025)}-#c/OR:{int(width*0.075)}-tc/Client:x-tl/Service:{int(width*0.2)}-tc/Item:{int(width*0.2)}-tr/Total:{int(width*0.1)}-tl!30!30')
        self.daily_data_view.pack(pady=height*0.01, padx=width*0.005)

        self.monthly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color="#DBDBDB")
        self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.monthly_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.795, height=height *0.5,
                                           column_format=f"/No:{int(width*.025)}-#c/Date:x-tl/Item:{int(width*.2)}-tr/Service:{int(width*.2)}-tr/Total:{int(width*.1)}-tc!30!30")
        self.monthly_data_view.pack()

        show_bar(self.monthly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.0045,"#DBDBDB"], label=monthly_label)

        self.yearly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color="#DBDBDB")
        self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.yearly_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.795, height=height *0.5,
                                           column_format=f"/No:{int(width*.025)}-#c/Month:x-tl/Item:{int(width*.2)}-tr/Service:{int(width*.2)}-tr/Total:{int(width*.1)}-tc!30!30")
        self.yearly_data_view.pack()

        show_bar(self.yearly_graph, data_item=yearly_data_items, data_service=yearly_data_service, info=[width*0.01,height*0.005,"#DBDBDB"], label=yearly_label)
        report_menu_callback("Daily")

        '''INVENTORY REPORT'''
        self.search_frame = ctk.CTkFrame(self.inventory_report_frame,width=width*0.3, height = height*0.05, fg_color=Color.White_Platinum)
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.0025), pady=(height*0.005,0))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0,font=("Arial", 14), text_color="black", fg_color=Color.White_Color[3])
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

        self.rep_refresh_btn = ctk.CTkButton(self.inventory_report_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.rep_refresh_btn.grid(row=0, column=1, sticky="w", pady=(height*0.005,0))

        self.rep_treeview_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="transparent")
        self.rep_treeview_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.0025), pady=(height*0.005,0))

        self.inventory_rep_treeview = cctk.cctkTreeView(self.rep_treeview_frame, width=width*0.8, height=height *0.8,
                                           column_format=f"/No:{int(width*.025)}-#c/ItemName:x-tl/InitialStock:{int(width*.2)}-tr/CurrentStock:{int(width*.2)}-tr!30!30")
        self.inventory_rep_treeview.pack()
        load_main_frame(0)

class user_setting_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='8').pack(anchor='w')
        #self.grid_forget()
        #self.label = ctk.CTkLabel(self, text='7').pack(anchor='w')
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
        #call roles icon
        self.roles_icon = ctk.CTkImage(light_image=Image.open("image/patient.png"), size=(16,16))
        #call account creation tab icon
        self.account_creation_icon = ctk.CTkImage(light_image = Image.open("image/person_icon.png"), size=(24,25))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        #frame for roles tab

        self.roles_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])
        #frame for account creation tab
        self.account_creation_frame = ctk.CTkFrame(self.base_frame,fg_color="green")

        self.sales_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])
        self.inventory_report_frame = ctk.CTkFrame(self.base_frame,fg_color="green")

        self.sales_report_frame.grid_columnconfigure(1, weight=1)
        self.sales_report_frame.grid_rowconfigure(2, weight=1)

        self.inventory_report_frame.grid_columnconfigure(1, weight=1)

        self.report_frames=[self.sales_report_frame, self.inventory_report_frame]
        self.active_report = None

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        selected_color = Color.Blue_Yale

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row =1, column =0, sticky = 'nsew',padx=width*0.005, pady=height*0.005)

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)
        #date on top right
        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")

        #first tab on top frame
        self.roles_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.roles_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.roles_button.configure(command=partial(load_main_frame, 0))
        self.roles_tab_icon = ctk.CTkLabel(self.roles_button, text="",image=self.roles_icon)
        self.roles_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.sales_report_label = ctk.CTkLabel(self.roles_button, text="ROLES", text_color="white",font=('Poppins', 15))
        self.sales_report_label.pack(side="left")
        self.roles_button.grid()
        self.roles_button.update_children()
        #second tab on top frame
        self.account_creation_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.account_creation_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.account_creation_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.account_creation_button.configure(command=partial(load_main_frame, 1))
        self.account_creation_tab_icon = ctk.CTkLabel(self.account_creation_button, text="",image=self.account_creation_icon)
        self.account_creation_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_report_label = ctk.CTkLabel(self.account_creation_button, text="ACCOUNT CREATION", text_color="white",font=('Poppins', 15))
        self.inventory_report_label.pack(side="left")
        self.account_creation_button.grid()
        self.account_creation_button.update_children()

        self.button_manager = cctku.button_manager([self.roles_button, self.account_creation_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        self.report_option_var = ctk.StringVar(value="Daily Report")
        #data for accounts
        #StringVars
        self.staff_name_svar = ctk.StringVar(value='Choose staff here...')

        #staff name list
        staff_names = []
        staff_names2 = [['Andrew Tate', 'Owner', 1, 1, 1, 1, 1, 1, 1, 1, 1], ['MLD', 'Assistant', 1, 0, 0, 0, 0, 1, 1, 0, 0], ['Sneako', 'Assistant', 0, 1, 1, 1, 1, 0, 0, 0, 0], ['Fresh And Fit', 'Admin', 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        #roles list
        roles_list = database.fetch_data('SELECT title FROM user_level_access')
        roles_list = [s[0] for s in roles_list]
        print(roles_list)

        #functions
        #disable all checkboxes
        def disable_privilege_checkboxes():
            self.dashboard_chk_box.configure(state='disabled')
            self.transaction_chk_box.configure(state='disabled')
            self.service_chk_box.configure(state='disabled')
            self.sales_chk_box.configure(state='disabled')
            self.inventory_chk_box.configure(state='disabled')
            self.pet_info_chk_box.configure(state='disabled')
            self.reports_chk_box.configure(state='disabled')
            self.users_chk_box.configure(state='disabled')
            self.action_log_chk_box.configure(state='disabled')
            self.role_cbox.configure(state='disabled')
            self.update_acc_btn.configure(state='disabled')
            self.clear_fields_btn.configure(state='disabled')
            self.edit_acc_btn.configure(state='disabled')
            self.role_cbox.set('')
            self.staff_name_cbox.set('Choose staff here...')
            clear_all_role_fields()
        #enable all checkboxes
        def enable_privilege_checkboxes():
            self.dashboard_chk_box.configure(state='normal')
            self.transaction_chk_box.configure(state='normal')
            self.service_chk_box.configure(state='normal')
            self.sales_chk_box.configure(state='normal')
            self.inventory_chk_box.configure(state='normal')
            self.pet_info_chk_box.configure(state='normal')
            self.reports_chk_box.configure(state='normal')
            self.users_chk_box.configure(state='normal')
            self.action_log_chk_box.configure(state='normal')
            self.role_cbox.configure(state='normal')
            self.update_acc_btn.configure(state='normal')
            self.clear_fields_btn.configure(state='normal')
            self.edit_acc_btn.configure(state='normal')
        #get all names in list
        def get_staff_name():
            for i in range(0, len(staff_names2)):
                if(not staff_names2[i][0] in staff_names):
                    staff_names.append(staff_names2[i][0])
        #check acc stat
        def check_acc(choice):
            enable_privilege_checkboxes()
            for l in checkbox_privilege_list:
                l.deselect()
            for i in range(0, len(staff_names2)):
                if(staff_names2[i][0] == choice):
                    self.role_cbox.set(staff_names2[i][1])
                    for j in range(2, len(staff_names2[i])):
                        if(staff_names2[i][j]):
                            checkbox_privilege_list[j-2].select()
        #cbox event
        def refresh_staff_names():
            #name combo box
            self.staff_name_cbox.grid_forget()
            self.staff_name_cbox = ctk.CTkComboBox(self.roles_inner_frame, values=staff_names, state='readonly', variable=self.staff_name_svar, font=('Poppins', (height*0.030)), dropdown_text_color='white', dropdown_fg_color='#3B8ED0', dropdown_font=('Poppins', (height*0.028)), width=(width*0.3), button_color='#3B8ED0', button_hover_color='#2C74B3', command=check_acc)
            self.staff_name_cbox.grid(row=0, column=1, sticky='ew', padx=((width*0.005)), pady=height*0.005)

        #clear all role fields
        def clear_all_role_fields():
            for i in checkbox_privilege_list:
                i.deselect()
        #update account
        def update_staff_account():
            for i in range(0, len(staff_names2)):
                if (self.staff_name_cbox.get()==staff_names2[i][0]):
                    staff_names2[i] = [staff_names2[i][0],
                                        self.role_cbox.get(),
                                        self.dashboard_chk_box.get(),
                                        self.transaction_chk_box.get(),
                                        self.service_chk_box.get(),
                                        self.sales_chk_box.get(),
                                        self.inventory_chk_box.get(),
                                        self.pet_info_chk_box.get(),
                                        self.reports_chk_box.get(),
                                        self.users_chk_box.get(),
                                        self.action_log_chk_box.get()]
            disable_privilege_checkboxes()

        #pre watched
        get_staff_name()

        #frame for roles tab
        self.roles_inner_frame = ctk.CTkFrame(self.sales_report_frame)
        self.roles_inner_frame.pack(fill=tk.BOTH, expand=True)
        self.roles_inner_frame.grid_rowconfigure(4, weight=1)

        #name label
        ctk.CTkLabel(self.roles_inner_frame, text="Name:", font=('Poppins', (height*0.032), 'bold'), text_color='#06283D').grid(row=0, column=0, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #name combo box
        self.staff_name_cbox = ctk.CTkComboBox(self.roles_inner_frame, values=staff_names, state='readonly', variable=self.staff_name_svar, font=('Poppins', (height*0.030)), dropdown_text_color='white', dropdown_fg_color='#3B8ED0', dropdown_font=('Poppins', (height*0.028)), width=(width*0.3), button_color='#3B8ED0', button_hover_color='#2C74B3', command=check_acc)
        self.staff_name_cbox.grid(row=0, column=1, sticky='ew', padx=((width*0.005)), pady=height*0.005)
        #roles label
        ctk.CTkLabel(self.roles_inner_frame, text="Roles:", font=('Poppins', (height*0.032), 'bold'), text_color='#06283D').grid(row=1, column=0, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #roles combo box
        self.role_cbox = ctk.CTkComboBox(self.roles_inner_frame, values=roles_list, state='readonly', font=('Poppins', (height*0.030)), dropdown_font=('Poppins', (height*0.028)), width=(width*0.3), button_color='#3B8ED0', button_hover_color='#2C74B3')
        self.role_cbox.grid(row=1, column=1, sticky="we", pady = (height*0.005), padx = (width*0.005))
        #edit account button
        self.edit_acc_btn = ctk.CTkButton(self.roles_inner_frame, text='EDIT ACCOUNT', command=exit, font=('Poppins', (height*0.022)))
        self.edit_acc_btn.grid(row=2, column=1, sticky='we', pady = (height*0.005), padx = (width*0.005))

        #privileges frame
        self.privileges_frame = ctk.CTkFrame(self.roles_inner_frame)
        self.privileges_frame.grid(row=3, column=0, sticky='nesw', columnspan=3)
        #privileges lbl
        ctk.CTkLabel(self.privileges_frame, text='Privileges:', font=('Poppins', (height*0.032), 'bold'), text_color='#06283D').grid(row=0, column=0, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #dashboard privilege title
        ctk.CTkLabel(self.privileges_frame, text='Dashboard', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=1, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #dashboard privilege checkbox
        self.dashboard_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.dashboard_chk_box.grid(row=1, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #transactions privilege title
        ctk.CTkLabel(self.privileges_frame, text='Transactions', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=2, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #transactions privilege checkbox
        self.transaction_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.transaction_chk_box.grid(row=2, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #service privilege title
        ctk.CTkLabel(self.privileges_frame, text='Services', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=3, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #service privilege checkbox
        self.service_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.service_chk_box.grid(row=3, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #sales privilege title
        ctk.CTkLabel(self.privileges_frame, text='Sales', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=4, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #sales privilege checkbox
        self.sales_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.sales_chk_box.grid(row=4, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #inventory privilege title
        ctk.CTkLabel(self.privileges_frame, text='Inventory', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=5, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #inventory privilege checkbox
        self.inventory_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.inventory_chk_box.grid(row=5, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #pet info privilege title
        ctk.CTkLabel(self.privileges_frame, text='Pet Info', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=6, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #pet info privilege checkbox
        self.pet_info_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.pet_info_chk_box.grid(row=6, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #report privilege title
        ctk.CTkLabel(self.privileges_frame, text='Report', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=7, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #report privilege checkbox
        self.reports_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.reports_chk_box.grid(row=7, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #users privilege title
        ctk.CTkLabel(self.privileges_frame, text='Users', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=8, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #users privilege checkbox
        self.users_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.users_chk_box.grid(row=8, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #action log privilege title
        ctk.CTkLabel(self.privileges_frame, text='Action Log', font=('Poppins', (height*0.022)), text_color='#06283D').grid(row=9, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #action log privilege checkbox
        self.action_log_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=('Poppins', (height*0.022)), text_color='#06283D')
        self.action_log_chk_box.grid(row=9, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))

        #frame for buttons
        self.buttons_frame = ctk.CTkFrame(self.roles_inner_frame)
        self.buttons_frame.grid(row=4, column=0, sticky='nesw', columnspan=3)
        #to center children
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=1)

        #update account button
        self.update_acc_btn = ctk.CTkButton(self.buttons_frame, text='UPDATE', command=update_staff_account, font=('Poppins', (height*0.022)))
        self.update_acc_btn.grid(row=0, column=0, pady = (height*0.005), padx = (width*0.005), sticky='e')
        #clear role fields button
        self.clear_fields_btn = ctk.CTkButton(self.buttons_frame, text='CLEAR', command=disable_privilege_checkboxes, font=('Poppins', (height*0.022)))
        self.clear_fields_btn.grid(row=0, column=1, pady = (height*0.005), padx = (width*0.005), sticky='w')
        #list of all checkboxes
        checkbox_privilege_list = [self.dashboard_chk_box,
                            self.transaction_chk_box,
                            self.service_chk_box,
                            self.sales_chk_box,
                            self.inventory_chk_box,
                            self.pet_info_chk_box,
                            self.reports_chk_box,
                            self.users_chk_box,
                            self.action_log_chk_box]
        #default
        #disable everything
        disable_privilege_checkboxes()

        #account creation tab
        #account creation frame
        self.box_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="white")
        self.box_frame.pack(fill=tk.BOTH, expand=True)

        #String Values
        password_svar = tk.StringVar()
        repass_svar = tk.StringVar()
        c_v1=tk.IntVar(value=0)
        #show password function
        def my_show():
            if(c_v1.get()==1):
                self.password_entry.configure(show='')
                self.reenter_password_entry.configure(show = '')
            else:
                self.password_entry.configure(show='*')
                self.reenter_password_entry.configure(show = '*')
        #subject for removal
        def open_pin_toplvl():
            pin_top = tk.Toplevel()
            pin_top_offsetx, pin_top_offsety = self.winfo_x() + self.winfo_width(), self.winfo_y()
            padx = 0 # the padding you need.
            pady = 0
            pin_top.geometry(f"+{pin_top_offsetx + padx}+{pin_top_offsety + pady}")
            pin_top.title('Enter PIN to continue')

            def check_pin():
                if pin_entry.get() == "1234":
                    add_new_acc()
                    clear_acc_creation_fields()
                    get_staff_name()
                    self.staff_name_cbox.set(staff_names)
                    quit()
                else:
                    messagebox.showerror("Error", "Wrong Pin", icon='error')
            enter_pin_lbl = ctk.CTkLabel(pin_top, text="Enter PIN:",font=("Poppins", 25))
            enter_pin_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
            pin_entry = ctk.CTkEntry(pin_top, placeholder_text='****', height=height*0.065, width=width*0.12,font=("Poppins", 25), show="*")
            pin_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
            confirm_btn = ctk.CTkButton(pin_top, text='CONFIRM', command=check_pin,font=("Poppins", 25))
            confirm_btn.grid(row=1, column=0, padx=10, pady=10, sticky="sew")
            cancel2_btn = ctk.CTkButton(pin_top, text='CANCEL', command=lambda: [pin_top.destroy()] ,font=("Poppins", 25))
            cancel2_btn.grid(row=1, column=1, padx=10, pady=10, sticky="sew")
            #end of removal
        #clears all account creation fields
        def clear_acc_creation_fields():
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.reenter_password_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            #self.address_entry.delete(0, tk.END)
            #self.contact_no_entry.delete(0, tk.END)
        #checks if all entry has value and if password are the same
        def check_entry():
            if len(self.username_entry.get()) == 0 or len(self.password_entry.get()) == 0 or len(self.first_name_entry.get()) == 0 or len(self.last_name_entry.get()) == 0:
                    messagebox.showerror("Error", "Enter all fields", icon='error')
            else:
                if self.password_entry.get() == self.reenter_password_entry.get():
                    create_new_acc()
                    messagebox.showinfo("Account Created", "Account Created Successfully!")
                    #open_pin_toplvl()
                else:
                    messagebox.showerror("Error", "Passwords do not match", icon='error')

        #ship the values
        def add_new_acc():
            if database.fetch_data('SELECT * FROM acc_cred where usn = ?',( self.username_entry.get(), )):
                    messagebox.showinfo('Can\'t Create record', 'Username already exist')
                    return
            fullname = f'{self.first_name_entry.get()} {self.last_name_entry.get()}'
            password = encrypt.pass_encrypt(self.password_entry.get())
            database.exec_nonquery([['INSERT INTO acc_cred VALUES(?, ?, ?, NULL)', (self.username_entry.get(), password['pass'], password['salt'])],
                                    ['INSERT INTO acc_info VALUES(?, ?, ?)', (self.username_entry.get(), fullname, self.position_cbox.get())]])
            clear_acc_creation_fields()

        def create_new_acc():
            add_new_acc()
            #clear_acc_creation_fields()
            #get_staff_name()
            #refresh_staff_names()
        '''ACCOUNT CREATION: START'''
        #user info label
        self.user_info_title_lbl = ctk.CTkLabel(self.box_frame, text='Create New Account',font=("Poppins", 35), text_color="#06283D")
        self.user_info_title_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw", columnspan=2)

        #account details frame
        self.account_details_frame = ctk.CTkFrame(self.box_frame)
        self.account_details_frame.grid(row=1, column=0, sticky='nesw', padx = (0, width*0.024))

        #username label
        self.username_lbl = ctk.CTkLabel(self.account_details_frame, text='Username:',font=("Poppins", 25, "bold"), text_color="#06283D")
        self.username_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        #username entry
        self.username_entry = ctk.CTkEntry(self.account_details_frame, placeholder_text='assistant1', height=height*0.08, width=width*0.25,font=("Poppins", 25))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        #password label
        self.password_lbl = ctk.CTkLabel(self.account_details_frame, text='Password:',font=("Poppins", 25, "bold"), text_color="#06283D")
        self.password_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        #password entry
        self.password_entry = ctk.CTkEntry(self.account_details_frame, textvariable=password_svar, height=height*0.08, width=width*0.25,font=("Poppins", 25), show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        #Re-enter Password label
        self.reenter_password_lbl = ctk.CTkLabel(self.account_details_frame, text='Re-enter Password:',font=("Poppins", 25, "bold"), text_color="#06283D")
        self.reenter_password_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        #Re-enter Password entry
        self.reenter_password_entry = ctk.CTkEntry(self.account_details_frame, textvariable=repass_svar, height=height*0.08, width=width*0.25,font=("Poppins", 25), show='*')
        self.reenter_password_entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsw")

        c1 = ctk.CTkSwitch(self.account_details_frame,text='Show Password',variable=c_v1,onvalue=1,offvalue=0,command=my_show)
        c1.grid(row=3,column=1)

        #position label
        self.position_title_lbl = ctk.CTkLabel(self.account_details_frame, text='Position:',font=("Poppins", 25, "bold"), text_color="#06283D")
        self.position_title_lbl.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        #position cbox
        self.position_cbox = ctk.CTkOptionMenu(self.account_details_frame, values=roles_list, font=("Poppins", 25), height=height*0.08,width=width*0.25, dropdown_font=('Poppins', 25), button_color='#3B8ED0', button_hover_color='#2C74B3')
        self.position_cbox.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

        #personal info frame
        self.personal_info_frame = ctk.CTkFrame(self.box_frame)
        self.personal_info_frame.grid(row=1, column=1, sticky='nesw')

        #first name label
        self.first_name_lbl = ctk.CTkLabel(self.personal_info_frame, text='First Name:',font=("Poppins", 25, "bold"), text_color="#06283D")
        self.first_name_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        #first name entry
        self.first_name_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="John", height=height*0.08, width=width*0.25,font=("Poppins", 25))
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsw")
        #last name name label
        self.last_name_lbl = ctk.CTkLabel(self.personal_info_frame, text='Last Name:',font=("Poppins", 25, "bold"), text_color="#06283D")
        self.last_name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        #last name entry
        self.last_name_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="Doe", height=height*0.08, width=width*0.25,font=("Poppins", 25))
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsw")
        #contact no label
        #self.contact_no_lbl = ctk.CTkLabel(self.personal_info_frame, text='Contact No.:',font=("Poppins", 25, "bold"), text_color="#06283D")
        #self.contact_no_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        #contact no entry
        #self.contact_no_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="0922 123 1234", height=height*0.08, width=width*0.25,font=("Poppins", 25))
        #self.contact_no_entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsw")
        #address label
        #self.address_lbl = ctk.CTkLabel(self.personal_info_frame, text='Address:',font=("Poppins", 25, "bold"), text_color="#06283D")
        #self.address_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        #address entry
        #self.address_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="123 Otentukumpo St.", height=height*0.08, width=width*0.25,font=("Poppins", 25))
        #self.address_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsw")
        #frame for bottom windows
        self.bottom_frame= ctk.CTkFrame(self.box_frame, fg_color='white')
        self.bottom_frame.grid(row=10, column=0, padx=10, pady=10, sticky="s", columnspan=4)
        #create button
        self.update_btn = ctk.CTkButton(self.bottom_frame, text='CREATE', command=check_entry,font=("Poppins", 25), fg_color='#2678F3', text_color='white')
        self.update_btn.grid(row=0, column=0, padx=10, pady=10, sticky="sew")
        #clear account creation fields button
        self.update_btn = ctk.CTkButton(self.bottom_frame, text='CLEAR', command=clear_acc_creation_fields, font=("Poppins", 25), fg_color='white', text_color='#2678F3', border_color="#2678F3", border_width=2.5)
        self.update_btn.grid(row=0, column=1, padx=10, pady=10, sticky="sew")
        '''ACCOUNT CREATION: START'''
        load_main_frame(0)

        self.account_creation_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.155,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.account_creation_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.account_creation_button.configure(command=partial(load_main_frame, 1))
        self.account_creation_tab_icon = ctk.CTkLabel(self.account_creation_button, text="",image=self.account_creation_icon)
        self.account_creation_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_report_label = ctk.CTkLabel(self.account_creation_button, text="ACCOUNT CREATION", text_color="white",font=('Poppins', 15))
        self.inventory_report_label.pack(side="left")
        self.account_creation_button.grid()
        self.account_creation_button.update_children()

        self.button_manager = cctku.button_manager([self.roles_button, self.account_creation_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        self.report_option_var = ctk.StringVar(value="Daily Report")
        #data for accounts
        #StringVars
        self.staff_name_svar = ctk.StringVar(value='Choose staff here...')

        #staff name list
        staff_names = []
        staff_names2 = [['Andrew Tate', 'Owner', 1, 1, 1, 1, 1, 1, 1, 1, 1], ['MLD', 'Assistant', 1, 0, 0, 0, 0, 1, 1, 0, 0], ['Sneako', 'Assistant', 0, 1, 1, 1, 1, 0, 0, 0, 0], ['Fresh And Fit', 'Admin', 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        #roles list
        roles_list = ['Admin', 'Assistant']

        #functions
        #disable all checkboxes
        def disable_privilege_checkboxes():
            self.dashboard_chk_box.configure(state='disabled')
            self.transaction_chk_box.configure(state='disabled')
            self.service_chk_box.configure(state='disabled')
            self.sales_chk_box.configure(state='disabled')
            self.inventory_chk_box.configure(state='disabled')
            self.pet_info_chk_box.configure(state='disabled')
            self.reports_chk_box.configure(state='disabled')
            self.users_chk_box.configure(state='disabled')
            self.action_log_chk_box.configure(state='disabled')
            #self.role_cbox.configure(state='disabled')
            self.update_acc_btn.configure(state='disabled')
            self.clear_fields_btn.configure(state='disabled')
            #self.edit_acc_btn.configure(state='disabled')
            #self.role_cbox.set('')
            #self.staff_name_cbox.set('Choose staff here...')
            clear_all_role_fields()
        #enable all checkboxes
        def enable_privilege_checkboxes():
            self.dashboard_chk_box.configure(state='normal')
            self.transaction_chk_box.configure(state='normal')
            self.service_chk_box.configure(state='normal')
            self.sales_chk_box.configure(state='normal')
            self.inventory_chk_box.configure(state='normal')
            self.pet_info_chk_box.configure(state='normal')
            self.reports_chk_box.configure(state='normal')
            self.users_chk_box.configure(state='normal')
            self.action_log_chk_box.configure(state='normal')
            self.role_cbox.configure(state='normal')
            self.update_acc_btn.configure(state='normal')
            self.clear_fields_btn.configure(state='normal')
            self.edit_acc_btn.configure(state='normal')
        #get all names in list
        def get_staff_name():
            for i in range(0, len(staff_names2)):
                if(not staff_names2[i][0] in staff_names):
                    staff_names.append(staff_names2[i][0])
        #check acc stat
        def check_acc(choice):
            enable_privilege_checkboxes()
            for l in checkbox_privilege_list:
                l.deselect()
            for i in range(0, len(staff_names2)):
                if(staff_names2[i][0] == choice):
                    self.role_cbox.set(staff_names2[i][1])
                    for j in range(2, len(staff_names2[i])):
                        if(staff_names2[i][j]):
                            checkbox_privilege_list[j-2].select()
        #cbox event
        def refresh_staff_names():
            #name combo box
            self.staff_name_cbox.grid_forget()
            self.staff_name_cbox = ctk.CTkComboBox(self.roles_inner_frame, values=staff_names, state='readonly', variable=self.staff_name_svar, font=('Poppins', (height*0.030)), dropdown_text_color='white', dropdown_fg_color='#3B8ED0', dropdown_font=('Poppins', (height*0.028)), width=(width*0.3), button_color='#3B8ED0', button_hover_color='#2C74B3', command=check_acc)
            self.staff_name_cbox.grid(row=0, column=1, sticky='ew', padx=((width*0.005)), pady=height*0.005)

        #clear all role fields
        def clear_all_role_fields():
            for i in checkbox_privilege_list:
                i.deselect()
        #update account
        def update_staff_account():
            for i in range(0, len(staff_names2)):
                if (self.staff_name_cbox.get()==staff_names2[i][0]):
                    staff_names2[i] = [staff_names2[i][0],
                                        self.role_cbox.get(),
                                        self.dashboard_chk_box.get(),
                                        self.transaction_chk_box.get(),
                                        self.service_chk_box.get(),
                                        self.sales_chk_box.get(),
                                        self.inventory_chk_box.get(),
                                        self.pet_info_chk_box.get(),
                                        self.reports_chk_box.get(),
                                        self.users_chk_box.get(),
                                        self.action_log_chk_box.get()]
            disable_privilege_checkboxes()

        #pre watched
        get_staff_name()

        #frame for roles tab
        self.roles_inner_frame = ctk.CTkFrame(self.roles_frame, fg_color="transparent")
        self.roles_inner_frame.grid(row=0,column=0, sticky="ns")
        self.roles_inner_frame.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(self.roles_inner_frame, text="Role:", font=("Arial",16)).grid(row=0, column=0, sticky='w', pady = (height*0.005), padx = (width*0.01))
        self.role_cbox = ctk.CTkOptionMenu(self.roles_inner_frame, values=roles_list,  font=("Arial",16), dropdown_font=("Arial",16), width=(width*0.3), button_color='#3B8ED0', button_hover_color='#2C74B3')
        self.role_cbox.grid(row=0, column=1, sticky="we", pady = (height*0.005), padx = (width*0.005))

        #privileges frame
        self.privileges_frame = ctk.CTkFrame(self.roles_inner_frame)
        self.privileges_frame.grid(row=1, column=0, sticky='nesw', columnspan=3)
        #privileges lbl
        ctk.CTkLabel(self.privileges_frame, text='Privileges:', font=("Arial",16), text_color='#06283D').grid(row=0, column=0, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #dashboard privilege title
        ctk.CTkLabel(self.privileges_frame, text='Dashboard', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=1, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #dashboard privilege checkbox
        self.dashboard_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.dashboard_chk_box.grid(row=1, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #transactions privilege title
        ctk.CTkLabel(self.privileges_frame, text='Transactions', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=2, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #transactions privilege checkbox
        self.transaction_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.transaction_chk_box.grid(row=2, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #service privilege title
        ctk.CTkLabel(self.privileges_frame, text='Services', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=3, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #service privilege checkbox
        self.service_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.service_chk_box.grid(row=3, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #sales privilege title
        ctk.CTkLabel(self.privileges_frame, text='Sales', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=4, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #sales privilege checkbox
        self.sales_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.sales_chk_box.grid(row=4, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #inventory privilege title
        ctk.CTkLabel(self.privileges_frame, text='Inventory', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=5, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #inventory privilege checkbox
        self.inventory_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.inventory_chk_box.grid(row=5, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #pet info privilege title
        ctk.CTkLabel(self.privileges_frame, text='Pet Info', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=6, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #pet info privilege checkbox
        self.pet_info_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.pet_info_chk_box.grid(row=6, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #report privilege title
        ctk.CTkLabel(self.privileges_frame, text='Report', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=7, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #report privilege checkbox
        self.reports_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.reports_chk_box.grid(row=7, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #users privilege title
        ctk.CTkLabel(self.privileges_frame, text='Users', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=8, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #users privilege checkbox
        self.users_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.users_chk_box.grid(row=8, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))
        #action log privilege title
        ctk.CTkLabel(self.privileges_frame, text='Action Log', font=("Arial", (height*0.022)), text_color='#06283D').grid(row=9, column=0, sticky='w', pady = (height*0.005), padx = ((width*0.08), (width*0.01)))
        #action log privilege checkbox
        self.action_log_chk_box = ctk.CTkCheckBox(self.privileges_frame, text='', font=("Arial", (height*0.022)), text_color='#06283D')
        self.action_log_chk_box.grid(row=9, column=1, sticky='w', pady = (height*0.005), padx = (width*0.01))

        #frame for buttons
        self.buttons_frame = ctk.CTkFrame(self.roles_inner_frame)
        self.buttons_frame.grid(row=4, column=0,sticky="nsew", columnspan=3)

        self.clear_fields_btn = ctk.CTkButton(self.buttons_frame, text='Clear', command=disable_privilege_checkboxes, font=("Arial", (height*0.022)))
        self.clear_fields_btn.pack(side="left", padx=(width*0.05,0), pady=(height*0.025))

        self.update_acc_btn = ctk.CTkButton(self.buttons_frame, text='Update', command=update_staff_account, font=("Arial", (height*0.022)))
        self.update_acc_btn.pack(side="right", padx=(0,width*0.05), pady=(height*0.025))

        #clear role fields button
        #list of all checkboxes
        checkbox_privilege_list = [self.dashboard_chk_box,
                            self.transaction_chk_box,
                            self.service_chk_box,
                            self.sales_chk_box,
                            self.inventory_chk_box,
                            self.pet_info_chk_box,
                            self.reports_chk_box,
                            self.users_chk_box,
                            self.action_log_chk_box]
        #default
        #disable everything
        #disable_privilege_checkboxes()

        #account creation tab
        #account creation frame
        self.box_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="white")
        self.box_frame.pack(fill=tk.BOTH, expand=True)

        #String Values
        password_svar = tk.StringVar()
        repass_svar = tk.StringVar()
        c_v1=tk.IntVar(value=0)
        #show password function
        def my_show():
            if(c_v1.get()==1):
                self.password_entry.configure(show='')
            else:
                self.password_entry.configure(show='*')
        #subject for removal
        def open_pin_toplvl():
            pin_top = tk.Toplevel()
            pin_top_offsetx, pin_top_offsety = self.winfo_x() + self.winfo_width(), self.winfo_y()
            padx = 0 # the padding you need.
            pady = 0
            pin_top.geometry(f"+{pin_top_offsetx + padx}+{pin_top_offsety + pady}")
            pin_top.title('Enter PIN to continue')

            def check_pin():
                if pin_entry.get() == "1234":
                    add_new_acc()
                    clear_acc_creation_fields()
                    get_staff_name()
                    self.staff_name_cbox.set(staff_names)
                    quit()
                else:
                    messagebox.showerror("Error", "Wrong Pin", icon='error')
            enter_pin_lbl = ctk.CTkLabel(pin_top, text="Enter PIN:",font=("Poppins", 25))
            enter_pin_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="ns")
            pin_entry = ctk.CTkEntry(pin_top, placeholder_text='****', height=height*0.065, width=width*0.12,font=("Poppins", 25), show="*")
            pin_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ns")
            confirm_btn = ctk.CTkButton(pin_top, text='CONFIRM', command=check_pin,font=("Poppins", 25))
            confirm_btn.grid(row=1, column=0, padx=10, pady=10, sticky="sew")
            cancel2_btn = ctk.CTkButton(pin_top, text='CANCEL', command=lambda: [pin_top.destroy()] ,font=("Poppins", 25))
            cancel2_btn.grid(row=1, column=1, padx=10, pady=10, sticky="sew")
            #end of removal
        #clears all account creation fields
        def clear_acc_creation_fields():
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.reenter_password_entry.delete(0, tk.END)
            self.first_name_entry.delete(0, tk.END)
            self.last_name_entry.delete(0, tk.END)
            self.address_entry.delete(0, tk.END)
            self.contact_no_entry.delete(0, tk.END)
        #checks if all entry has value and if password are the same
        def check_entry():
            if len(self.username_entry.get()) == 0 or len(self.password_entry.get()) == 0 or len(self.address_entry.get()) == 0 or len(self.contact_no_entry.get()) == 0 or len(self.first_name_entry.get()) == 0 or len(self.last_name_entry.get()) == 0:
                    messagebox.showerror("Error", "Enter all fields", icon='error')
            else:
                if self.password_entry.get() == self.reenter_password_entry.get():
                    create_new_acc()
                    messagebox.showinfo("Account Created", "Account Created Successfully!")
                    #open_pin_toplvl()
                else:
                    messagebox.showerror("Error", "Passwords do not match", icon='error')

        #ship the values
        def add_new_acc():
            fullname = f'{self.first_name_entry.get()} {self.last_name_entry.get()}'
            pos = self.position_cbox.get()

            single_acc_data = [fullname, pos]
            if(pos=='Assistant'):
                single_acc_data = [fullname, pos, 0, 1, 1, 1, 1, 1, 0, 1, 0]
            else:
                single_acc_data = [fullname, pos, 1, 1, 1, 1, 1, 1, 1, 1, 1]
            staff_names2.append(single_acc_data)

        #create new acc
        def create_new_acc():
            add_new_acc()
            clear_acc_creation_fields()
            get_staff_name()
            refresh_staff_names()
        '''ACCOUNT CREATION: START'''
        #user info label
        self.user_info_title_lbl = ctk.CTkLabel(self.box_frame, text='Create New Account',font=("Arial", 20), text_color="#06283D")
        self.user_info_title_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw", columnspan=2)

        #account details frame
        self.account_details_frame = ctk.CTkFrame(self.box_frame)
        self.account_details_frame.grid(row=1, column=0, sticky='nesw', padx = (0, width*0.024))

        #username label
        self.username_lbl = ctk.CTkLabel(self.account_details_frame, text='Username:',font=("Arial", 16), text_color="#06283D")
        self.username_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        #username entry
        self.username_entry = ctk.CTkEntry(self.account_details_frame, placeholder_text='assistant1', height=height*0.08, width=width*0.25,font=("Arial", 25))
        self.username_entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")
        #password label
        self.password_lbl = ctk.CTkLabel(self.account_details_frame, text='Password:',font=("Arial", 16), text_color="#06283D")
        self.password_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        #password entry
        self.password_entry = ctk.CTkEntry(self.account_details_frame, textvariable=password_svar, height=height*0.08, width=width*0.25,font=("Arial", 25), show='*')
        self.password_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        #show password checkbutton
        c1 = ctk.CTkSwitch(self.account_details_frame,text='Show Password',variable=c_v1,onvalue=1,offvalue=0,command=my_show)
        c1.grid(row=2,column=1)
        #Re-enter Password label
        self.reenter_password_lbl = ctk.CTkLabel(self.account_details_frame, text='Re-enter Password:',font=("Arial", 16), text_color="#06283D")
        self.reenter_password_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        #Re-enter Password entry
        self.reenter_password_entry = ctk.CTkEntry(self.account_details_frame, textvariable=repass_svar, height=height*0.08, width=width*0.25,font=("Arial", 25), show='*')
        self.reenter_password_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsw")
        #position label
        self.position_title_lbl = ctk.CTkLabel(self.account_details_frame, text='Position:',font=("Arial", 16), text_color="#06283D")
        self.position_title_lbl.grid(row=4, column=0, padx=10, pady=10, sticky="w")
        #position cbox
        self.position_cbox = ctk.CTkComboBox(self.account_details_frame, values=roles_list, font=("Arial", 25), height=height*0.08,width=width*0.25, dropdown_font=("Arial", 25), button_color='#3B8ED0', button_hover_color='#2C74B3')
        self.position_cbox.grid(row=4, column=1, padx=10, pady=(0, 10), sticky="ew")

        #personal info frame
        self.personal_info_frame = ctk.CTkFrame(self.box_frame)
        self.personal_info_frame.grid(row=1, column=1, sticky='nesw')

        #first name label
        self.first_name_lbl = ctk.CTkLabel(self.personal_info_frame, text='First Name:',font=("Arial", 16), text_color="#06283D")
        self.first_name_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="w")
        #first name entry
        self.first_name_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="John", height=height*0.08, width=width*0.25,font=("Arial", 25))
        self.first_name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="nsw")
        #last name name label
        self.last_name_lbl = ctk.CTkLabel(self.personal_info_frame, text='Last Name:',font=("Arial", 16), text_color="#06283D")
        self.last_name_lbl.grid(row=1, column=0, padx=10, pady=10, sticky="w")
        #last name entry
        self.last_name_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="Doe", height=height*0.08, width=width*0.25,font=("Arial", 25))
        self.last_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="nsw")
        #contact no label
        self.contact_no_lbl = ctk.CTkLabel(self.personal_info_frame, text='Contact No.:',font=("Arial", 16), text_color="#06283D")
        self.contact_no_lbl.grid(row=2, column=0, padx=10, pady=10, sticky="w")
        #contact no entry
        self.contact_no_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="0922 123 1234", height=height*0.08, width=width*0.25,font=("Arial", 25))
        self.contact_no_entry.grid(row=2, column=1, padx=10, pady=10, sticky="nsw")
        #address label
        self.address_lbl = ctk.CTkLabel(self.personal_info_frame, text='Address:',font=("Arial", 16), text_color="#06283D")
        self.address_lbl.grid(row=3, column=0, padx=10, pady=10, sticky="w")
        #address entry
        self.address_entry = ctk.CTkEntry(self.personal_info_frame, placeholder_text="123 Otentukumpo St.", height=height*0.08, width=width*0.25,font=("Arial", 25))
        self.address_entry.grid(row=3, column=1, padx=10, pady=10, sticky="nsw")
        #frame for bottom windows
        self.bottom_frame= ctk.CTkFrame(self.box_frame, fg_color='white')
        self.bottom_frame.grid(row=10, column=0, padx=10, pady=10, sticky="s", columnspan=4)
        #create button
        self.create_btn = ctk.CTkButton(self.bottom_frame, text='CREATE', command=check_entry,font=("Arial", 25), fg_color='#2678F3', text_color='white')
        self.create_btn.grid(row=0, column=1, padx=10, pady=10, sticky="sew")
        #clear account creation fields button
        self.clear_btn = ctk.CTkButton(self.bottom_frame, text='CLEAR', command=clear_acc_creation_fields, font=("Arial", 25), fg_color='white', text_color='#2678F3', border_color="#2678F3", border_width=2.5)
        self.clear_btn.grid(row=0, column=0, padx=10, pady=10, sticky="sew")
        '''ACCOUNT CREATION: START'''


        load_main_frame(0)

class histlog_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='9').pack(anchor='w')
        self.grid_forget()
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))


        # Searchbar
        self.search_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], width=width*0.35, height = height*0.05,)
        self.search_frame.grid(row=0, column=0,padx=(width*0.005), pady=(width * 0.005))
        self.search_frame.pack_propagate(0)

        self.search_bar_frame = ctk.CTkFrame(self.search_frame, fg_color="light grey")
        self.search_bar_frame.pack(fill="both", padx=width*0.005, pady=height*0.0075)

        ctk.CTkLabel(self.search_bar_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_bar_frame, placeholder_text="Search", border_width=0, fg_color="light grey")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

        self.actionlog_refresh_btn = ctk.CTkButton(self, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.actionlog_refresh_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3,padx=(width*0.005), pady=(width * 0.005))

        self.log_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3])
        self.log_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=(width*0.005), pady=(0,width * 0.005))

        self.data = database.fetch_data(sql_commands.get_hist_log)
        self.actionlog_treeview = cctk.cctkTreeView(self.log_frame, data= self.data, width=width*0.8, height=height*0.8,
                                               column_format=f'/No:{int(width*.025)}-#r/User:x-tl/DateLogged:{int(width*0.2)}-tc/TimeIn:{int(width*.15)}-tl/TimeOut:{int(width*.15)}-tl!30!30')
        self.actionlog_treeview.pack(pady=(height*0.015))

    def place(self, **kwargs):
        self.actionlog_treeview.pack_forget()
        self.actionlog_treeview.update_table(database.fetch_data(sql_commands.get_hist_log))
        self.after(1000, self.actionlog_treeview.pack(pady=(height*0.015)))
        return super().place(**kwargs)
dashboard(None, 'admin', datetime.datetime.now)