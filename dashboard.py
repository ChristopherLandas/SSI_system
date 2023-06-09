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
from popup import Inventory_popup, transaction_popups, Sales_popup, dashboard_popup
import copy

ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')
width = 0
height = 0
acc_info = ()
acc_cred = ()
date_logged = None

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

        global acc_info, acc_cred, date_logged
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
        self.active_main_frame = None

        '''setting the user level access'''
        """  user_level_access = database.fetch_data(sql_commands.get_level_acessess, (acc_info[0][2], ))[0]
        if(not user_level_access[1]):
            temp:inventory_frame = self.main_frames[4]
            temp.add_item_btn.destroy()
            del temp
        del user_level_access
        """
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
        self.patient_button.configure(command=partial(load_main_frame, 'Pet Info', 5))
        self.patient_button.pack()
        self.patient_wbar = ctk.CTkLabel(self.patient_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.patient_wbar.pack(side="left")
        self.patient_icon = ctk.CTkLabel(self.patient_button,image=self.patient_icon, text="")
        self.patient_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.patient_label = ctk.CTkLabel(self.patient_button, text="Pet Info", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
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
        self.user_setting_button.configure(command=partial(load_main_frame, 'Settings', 7))
        self.user_setting_button.pack()
        self.user_setting_wbar = ctk.CTkLabel(self.user_setting_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.user_setting_wbar.pack(side="left")
        self.user_setting_icon = ctk.CTkLabel(self.user_setting_button,image=self.user_setting_icon, text="")
        self.user_setting_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
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
            pie_figure= Figure(figsize=(income_frame_width*0.006,income_frame_height*0.013), dpi=100)
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

        income_frame_width, income_frame_height = self.income_summary_frame.cget('width'), self.income_summary_frame.cget("height")

        '''Income summary frame contents'''
        self.income_summary_frame.grid_columnconfigure((0,1), weight=1)
        self.income_summary_frame.grid_rowconfigure((2,3,4), weight=1)
        self.income_summary_label = ctk.CTkLabel(self.income_summary_frame,text="Daily Income Summary",fg_color="transparent", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht,)
        self.income_summary_label.grid(row=0, column=0, sticky="ew", pady=(income_frame_height*0.04,0))
        self.income_summary_sub = ctk.CTkLabel(self.income_summary_frame,text=f"as of {date.today().strftime('%B %d, %Y')}", font=("DM Sans Medium", 14), text_color=Color.Grey_Davy)
        self.income_summary_sub.grid(row=1, column=0, sticky="ew")

        self.num_transactions = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.num_transactions.grid(row=2, column=0, sticky="nsew", padx=(income_frame_width*0.03), pady=(income_frame_height*0.05, income_frame_height*.015),)
        self.num_transactions.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.num_transactions, text="Transactions Today:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.num_transactions, text="0", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))

        self.items_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.18, fg_color=Color.Light_Green, corner_radius=5)
        self.items_sales_frame.grid(row=3, column=0, sticky="nsew", padx=(income_frame_width*0.03), pady=(income_frame_height*0.015, income_frame_height*.015),)
        self.items_sales_frame.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.items_sales_frame, text="Items:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.items_sales_frame, text=f"₱{format_price(self.data[0])}", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))

        self.services_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.18, fg_color=Color.Red_Tulip, corner_radius=5)
        self.services_sales_frame.grid(row=4, column=0, sticky="nsew", padx=(income_frame_width*0.03),pady=( income_frame_height*.015))
        self.services_sales_frame.pack_propagate(0)
        self.services_sales_label = ctk.CTkLabel(self.services_sales_frame, text="Services:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.services_sales_value = ctk.CTkLabel(self.services_sales_frame, text=f"₱{format_price(self.data[1])}", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))

        self.total_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.15, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.total_sales_frame.grid(row=5, column=0, sticky="nsew", padx=(income_frame_width*0.03),pady=(income_frame_height*.015, income_frame_height*.05))
        self.total_sales_frame.pack_propagate(0)
        self.total_sales_label = ctk.CTkLabel(self.total_sales_frame, text="Total:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.total_sales_value = ctk.CTkLabel(self.total_sales_frame, text=f"₱{format_price(self.data[1] + self.data[0])}", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))
        #Watermelon Pie
        show_pie(self.income_summary_frame, self.data)

        '''Inventory Stat Frame'''
        self.inventory_stat_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.inventory_stat_frame.grid_propagate(0)
        self.inventory_stat_frame.grid(row=1, column=4, columnspan=4, padx= (width*(.005) ,width * .01))
        self.inventory_stat_frame.grid_rowconfigure(1, weight=1)
        self.inventory_stat_frame.grid_columnconfigure(1, weight=1)

        inventory_frame_width, inventory_frame_height = self.inventory_stat_frame.cget('width'), self.inventory_stat_frame.cget('height')

        '''Inventory Stat Frame Contents'''
        self.inventory_stat_label = ctk.CTkLabel(self.inventory_stat_frame, text="Inventory Status", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht)
        self.inventory_stat_label.grid(row=0, column=1, sticky="w", padx=(inventory_frame_width*0.04,0),pady=(inventory_frame_height*0.04,inventory_frame_height*0.02))

        def show_status_popup(name: str, data):
            print(name)
            self.status_popup.status_label.configure(text = name)
            self.status_popup.update_treeview(data)
            self.status_popup.place(relx = .5, rely = .5, anchor = 'c')

        self.inventory_content_frame = ctk.CTkScrollableFrame(self.inventory_stat_frame, height=inventory_frame_height*0.16, fg_color=Color.White_Ghost)
        self.inventory_content_frame.grid_propagate()
        self.inventory_content_frame.grid_columnconfigure(1, weight=1)
        self.inventory_content_frame.grid(row=1, column=1, sticky="news", padx=inventory_frame_width*0.025, pady=(0,inventory_frame_height*0.04))
        self.stat_tabs: list = []

        stat_data = [('Reorder', '#cccc00', database.fetch_data(sql_commands.get_reorder_state) or None),
                     ('Critical', '#ff0000', database.fetch_data(sql_commands.get_critical_state) or None),
                     ('Out-Of-Stock', '#222222', database.fetch_data(sql_commands.get_out_of_stock_state) or None),
                     ('Near Expire', '#ff7900', database.fetch_data(sql_commands.get_near_expire_state) or None),
                     ('Expire', '#dd0000', database.fetch_data(sql_commands.get_expired_state) or None)]
        stat_data = [s for s in stat_data if s[-1] is not None]
        stat_tabs_info: dict = {s[0]: s[-1] for s in stat_data}

        for i in range(len(stat_data)):
            temp = dashboard_popup.status_bar(self.inventory_content_frame, (inventory_frame_width, income_frame_height),
                                                                             stat_data[i][0], stat_data[i][1],
                                                                             len(stat_data[i][-1]), show_status_popup, stat_tabs_info)
            self.stat_tabs.append(copy.copy(temp))
            self.stat_tabs[-1].grid(row = i, column = 1, sticky = 'nsew', padx=(inventory_frame_width*0.001 ),pady=(0,inventory_frame_height*0.02))
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

        self.view_more_button = ctk.CTkButton(self.sales_history_frame, text='View More',width= income_frame_width*0.16, height=income_frame_height*0.06, font=('DM Sans Medium', 12), corner_radius=4, text_color=Color.Blue_Maastricht,
                                              fg_color=Color.White_AntiFlash,hover_color=Color.Platinum, command=lambda:print("Go To Report Section"))
        self.view_more_button.grid(row=2, column=0, sticky="w", padx=income_frame_width*0.035,pady=(0,income_frame_height*0.035))

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

    def grid(self, **kwargs):
        return super().grid(**kwargs)

class transaction_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
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

        self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1,2), weight=1)

        self.or_num_label = ctk.CTkLabel(self, fg_color=Color.White_Ghost, corner_radius=5, width=width*0.125, height = height*0.05,
                                         text="OR#: 0001", font=("DM Sans Medium", 15))
        self.or_num_label.grid(row=0, column=0, padx=(width*0.005,0), pady=(height*0.01))

        self.client_name_frame = ctk.CTkFrame(self, fg_color=Color.White_Ghost, width=width*0.55, height=height*0.05,)
        self.client_name_frame.grid(row=0, column=1, columnspan=1)
        self.client_name_frame.pack_propagate(0)

        self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
        self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

        self.client_name_entry = ctk.CTkEntry(self.client_name_frame, placeholder_text="Client's Name",font=("DM Sans Medium", 15), border_width=0, fg_color="white")
        self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005,width*0.01), pady=(height*0.01))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Ghost, width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=2, padx=(0, width*0.005),  pady=(height*0.01))

        self.service_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=Color.White_Ghost)
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
        self.final_total_value.pack(side="right", padx=(0, width*0.01))

        self.show_list_item: ctk.CTkFrame = transaction_popups.show_item_list(self, (width, height, self.item_treeview))
        self.show_services_list: ctk.CTkFrame = transaction_popups.show_services_list(self, (width, height, self.service_treeview), self.customer_infos)
        self.item_treeview.bd_configs = [(6, [self.item_total_value, self.final_total_value])]
        self.service_treeview.bd_configs = [(6, [self.service_total_value, self.final_total_value])]

    def change_total_value_item(self, value: float):
            value = float(value)
            self.item_total_value.configure(text = format_price(float(price_format_to_float(self.item_total_value._text)) + value))
            self.final_total_value.configure(text = format_price(float(price_format_to_float(self.final_total_value._text)) + value))

    def change_total_value_service(self, value: float):
            value = float(value)
            self.service_total_value.configure(text = format_price(float(price_format_to_float(self.service_total_value._text)) + value))
            self.final_total_value.configure(text = format_price(float(price_format_to_float(self.final_total_value._text)) + value))

    def clear_all_item(self):
           verification = messagebox.askyesno('Clear All', 'Are you sure you want to delete\nall trasaction record?')
           if verification:
                self.reset()

    def reset(self):
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
            self.services_data_for_treeview = [(s[0], format_price(float(s[1])), s[2]) for s in self.services_raw_data]
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

        self.search_bar_frame = ctk.CTkFrame(self.search_frame, fg_color="light grey")
        self.search_bar_frame.pack(fill="both", padx=width*0.005, pady=height*0.0075)

        ctk.CTkLabel(self.search_bar_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_bar_frame, placeholder_text="Search", border_width=0, fg_color="light grey")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

        self.add_service = ctk.CTkButton(self,text="Add Service", width=width*0.1, height = height*0.05, image=self.plus)
        self.add_service.grid(row=0, column=1)

        self.service_inventory = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.inventory)
        self.service_inventory.grid(row=0, column=2,padx=(width*0.005,0))

        self.refresh_btn = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=update_tables)
        self.refresh_btn.grid(row=0, column=3,padx=(width*0.005))

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
        self.label = ctk.CTkLabel(self, text='4').pack(anchor='w')
        self.main_data = database.fetch_data(sql_commands.get_transaction_data, None)
        self.main_data = [(s[0], s[2], str(datetime.datetime.now().date()), format_price(float(s[3])), s[1]) for s in self.main_data]
        self.data_view = cctk.cctkTreeView(self, self.main_data, width * .8, height * .8,
                                           column_format='/No:75-#c/OR:75-tc/Client:x-tl/Date:175-tc/TotalPrice:125-tr/Cashier:125-tl/Actions:85-bD!50!30')
        self.data_view.configure(double_click_command = lambda _: Sales_popup.show_sales_record_info(self, (width, height), ('a', 'b', 'c'), [None, None]).place(relx = .5, rely = .5, anchor = 'c') )
        self.data_view.pack(pady = (15, 0))

        self.grid_forget()

class inventory_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
        self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
        self.disposal_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
        self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))
        self.history_icon = ctk.CTkImage(light_image= Image.open("image/histlogs.png"), size=(22,25))
        self.trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(22,25))
        
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

        selected_color = Color.Blue_Yale

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)
            
        def update_tables(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.data_view1.update_table(database.fetch_data(sql_commands.get_inventory_by_group, None))
            #self.data_view2.update_table(database.fetch_data(sql_commands.get_inventory_by_expiry, None))
            self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

        def sort_status_callback(option):
            if "Levels" in option:
                self.sort_status_option.configure(values=["Normal","Reorder","Critical"])
                self.sort_status_option.set("Normal")
            elif "Category" in option:
                self.sort_status_option.configure(values=["All Items","Medicine","Vaccination", "Accessories"])
                self.sort_status_option.set("All Items")
            else:
                self.sort_status_option.configure(values=["Safe","Nearly Expire", "Expired"])
                self.sort_status_option.set("Safe")
                #self.sort_type_var=["Safe","Nearly Expire", "Expired"]
        
        def reset(self):
            self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
            self.data2 = database.fetch_data(sql_commands.get_inventory_by_expiry, None)
            self.data_view1.update_table(self.data1)
            self.data_view2.update_table(self.data2)

        """  def change_view(_: any = None):
            if self.view_by_selection.get() == 'View by Item':
                self.data_view1.pack(pady=(height*0.005,0))
                self.data_view2.pack_forget()
            else:
                self.data_view2.pack(pady=(height*0.005,0))
                self.data_view1.pack_forget() """
        
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

        self.stock_disposal_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
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

        self.search_frame = ctk.CTkFrame(self.inventory_sub_frame,width=width*0.3, height = height*0.05)
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))

        self.search_frame.pack_propagate(0)
        ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0, fg_color="white")
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

        self.add_item_btn = ctk.CTkButton(self.inventory_sub_frame,width=width*0.08, height = height*0.05, text="Add Item",image=self.add_icon, font=("DM Sans Medium", 14),
                                          command= lambda : self.add_item_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_item_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.refresh_btn = ctk.CTkButton(self.inventory_sub_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=2, sticky="w")

        self.sort_type_option= ctk.CTkOptionMenu(self. inventory_sub_frame,  height = height*0.05, values=self.sort_status_var, anchor="center",
                                                 command=partial(sort_status_callback))
        self.sort_type_option.grid(row=0, column=4, padx=(width*0.005,0), sticky="e")

        self.sort_status_option= ctk.CTkOptionMenu(self. inventory_sub_frame,  height = height*0.05, values=self.sort_type_var, anchor="center")
        self.sort_status_option.grid(row=0, column=5, padx=(width*0.005), sticky="e")

        self.restock_btn = ctk.CTkButton(self.inventory_sub_frame, width=width*0.1, height = height*0.05, text="Stock Order", image=self.restock_icon, font=("DM Sans Medium", 14),
                                         command= lambda : self.restock_popup.place(default_data=self.data_view1.data_grid_btn_mng.active or None, relx = .5, rely = .5, anchor = 'c'))
        self.restock_btn.grid(row=3, column=5, pady=(height*0.01), sticky="e", padx=(0, width*0.005))
        self.tree_view_frame = ctk.CTkFrame(self.inventory_sub_frame, fg_color="transparent")
        self.tree_view_frame.grid(row=1, column=0,columnspan=6, sticky="nsew",padx=(width*0.005))

        self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.data_view1 = cctk.cctkTreeView(self.tree_view_frame, self.data1, width= width * .805, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Stock:{int(width*.07)}-tr/Price:{int(width*.07)}-tr/NearestExpire:{int(width*.1)}-tc/Status:{int(width*.08)}-tc!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 14),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,
                                           conditional_colors= {5: {'Reorder':'#ff7900', 'Critical':'red','Normal':'green', 'Out Of Stock': '#555555'}})
        self.data_view1.pack()
        
        self.refresh_btn.configure(command = update_tables)
        
        self.sort_type_option.set("View by Levels")
        
        '''INVENTORY FRAME: END'''

        '''RESTOCK: START'''
        #self.restock_frame.pack(fill="both", expand=1)
        self.restock_frame.grid_propagate(0)
        self.restock_frame.grid_rowconfigure(1, weight=1)
                     
        self.restock_frame.grid_columnconfigure(3, weight=1)

        self.rs_search_frame = ctk.CTkFrame(self.restock_frame,width=width*0.3, height = height*0.05)
        self.rs_search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))

        self.rs_search_frame.pack_propagate(0)
        ctk.CTkLabel(self.rs_search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.rs_search_entry = ctk.CTkEntry(self.rs_search_frame, placeholder_text="Search", border_width=0, fg_color="white")
        self.rs_search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

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
        self.rs_data_view1 = cctk.cctkTreeView(self.rs_treeview_frame, data=[],width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Quantity:{int(width*.08)}-tr/SupplierName:x-tr/Action:{int(width*.075)}-tc!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
        self.rs_data_view1.pack()
        '''RESTOCK FRAME: END'''
        
        '''ITEM DISPOSAL: START'''
        self.disposal_frame.grid_propagate(0)
        self.disposal_frame.grid_rowconfigure(1, weight=1)
        self.disposal_frame.grid_columnconfigure(3, weight=1) 
        
        self.ds_treeview_frame = ctk.CTkFrame(self.disposal_frame,fg_color="transparent")
        self.ds_treeview_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=width*0.005)
        
        #self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.ds_data_view1 = cctk.cctkTreeView(self.ds_treeview_frame, data=[],width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Quantity:{int(width*.15)}-tr/ExpiryDate:{int(width*.185)}-tr/Action:{int(width*.075)}-tc!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
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
        self.restock_popup = Inventory_popup.restock(self, (width, height, acc_cred, acc_info))
        self.add_item_popup = Inventory_popup.add_item(self, (width, height, acc_cred, acc_info))
        self.supplier_list_popup = Inventory_popup.supplier_list(self,(width, height, acc_cred, acc_info))
        
        sort_status_callback("View by Levels")
        load_main_frame(0)
        
class patient_info_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='6').pack(anchor='w')
        self.grid_forget()

class reports_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='7').pack(anchor='w')
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))

        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)
        
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

        self.month_option = ctk.CTkOptionMenu(self.sales_report_top, values=["April","May", "June"], anchor="center", width=width*0.1 )
        self.month_option.set(f"{date.today().strftime('%B')}")
        self.year_option = ctk.CTkOptionMenu(self.sales_report_top, values=operational_year, width=width*0.075, anchor="center")
        self.year_option.set(f"{date.today().strftime('%Y')}")
        
        self.daily_graph = ctk.CTkFrame(self.sales_report_frame, fg_color="transparent", height=height*0.35)
        self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
        self.daily_graph.grid_columnconfigure((3), weight=2)
        self.daily_graph.grid_rowconfigure((0), weight=1)

        self.sales_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color="#DBDBDB")
        self.sales_daily_graph.grid(row=0, column= 0,columnspan=3, sticky="nsew",  padx=(width*0.005,0), pady=(height*0.01))

        self.bottom_frame = ctk.CTkFrame(self.daily_graph, fg_color="transparent")
        self.bottom_frame.grid(row=1, column=0, columnspan=3, pady=(0,height*0.01))
        
        self.items_total = ctk.CTkLabel(self.bottom_frame,  text=f"Item:        {format_price(data[0])}", corner_radius=5, fg_color="white")
        self.items_total.pack(side="left", padx=width*0.005,)
        self.service_total = ctk.CTkLabel(self.bottom_frame,text=f"Services     {format_price(data[1])}", corner_radius=5, fg_color="white")
        self.service_total.pack(side="left")
        self.income_total = ctk.CTkLabel(self.bottom_frame,text=f"Total    {format_price(data[0] + data[1])}", corner_radius=5, fg_color="white")
        self.income_total.pack(side="left", padx=width*0.005)
        
        self.bars_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color="#DBDBDB", height=height*0.35)
        self.bars_daily_graph.grid(row=0, column= 3, sticky="nsew", padx=(width*0.005), pady=(height*0.01,0))
        self.bars_daily_graph.pack_propagate(0)

        show_pie(self.sales_daily_graph, data=data if data[0] + data[1] > 0 else [1,0], info=[width*0.005,height*0.005,"#DBDBDB"], label=label)
        show_hbar(self.bars_daily_graph, data=data, info=[width*0.05,height*0.005,"#DBDBDB"], label=label)

        self.data_frame = ctk.CTkFrame(self.sales_report_frame, height=height*0.3, fg_color="#DBDBDB")
        self.data_frame.grid(row=2, column=0, sticky="nsew", columnspan = 2, pady=(0,height*0.005))
    
        self.daily_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.795, height=height *0.5, header_color=Color.Blue_Yale, content_color="transparent",
                                           column_format=f"/No:{int(width*.025)}-#c/OR:{int(width*.085)}-tc/Client:x-tl/Item:{int(width*.15)}-tr/Service:{int(width*.15)}-tr/Total:{int(width*.085)}-tc!30!30")
        self.daily_data_view.pack()

        self.monthly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color="#DBDBDB")
        self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.monthly_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.795, height=height *0.5, header_color=Color.Blue_Yale, content_color="transparent",
                                           column_format=f"/No:{int(width*.025)}-#c/Date:x-tl/Item:{int(width*.2)}-tr/Service:{int(width*.2)}-tr/Total:{int(width*.1)}-tc!30!30")
        self.monthly_data_view.pack()

        show_bar(self.monthly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,"#DBDBDB"], label=monthly_label)

        self.yearly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color="#DBDBDB")
        self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.yearly_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.795, height=height *0.5, header_color=Color.Blue_Yale, content_color="transparent",
                                           column_format=f"/No:{int(width*.025)}-#c/Month:x-tl/Item:{int(width*.2)}-tr/Service:{int(width*.2)}-tr/Total:{int(width*.1)}-tc!30!30")
        self.yearly_data_view.pack()

        show_bar(self.yearly_graph, data_item=yearly_data_items, data_service=yearly_data_service, info=[width*0.01,height*0.005,"#DBDBDB"], label=yearly_label)

        report_menu_callback("Daily")
        load_main_frame(0)

class user_setting_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='8').pack(anchor='w')
        self.grid_forget()
        
        

class histlog_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='9').pack(anchor='w')
        self.grid_forget();

dashboard(None, 'admin', datetime.datetime.now)