import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from matplotlib import pyplot as plt
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
from popup import Inventory_popup, Pet_info_popup, service_popup, transaction_popups, Sales_popup, dashboard_popup, save_as_popup, service_popup
import copy
import calendar
import acc_creation

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
        '''
        datakey = database.fetch_data(f'SELECT {db.USERNAME} from {db.ACC_CRED} where {db.acc_cred.ENTRY_OTP} = ?', (entry_key, ))

        if not datakey or entry_key == None:
            messagebox.showwarning('Warning', 'Invalid entry method\ngo to log in instead')
            self.destroy()
            return
        else:
            global acc_info, date_logged, acc_cred, mainframes
            date_logged = _date_logged
            acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (datakey[0][0], ))
            acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (datakey[0][0], ))
            database.exec_nonquery([[f'UPDATE {db.ACC_CRED} SET {db.acc_cred.ENTRY_OTP} = NULL WHERE {db.USERNAME} = ?', (datakey[0][0], )]])
            del datakey 
        #for preventing security breach through python code; enable it to test it """
        '''

        global acc_info, acc_cred, date_logged, mainframes
        acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (entry_key, ))
        acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (entry_key, ))
        date_logged = _date_logged;
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
        global width, height, mainframes
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

        #self.main_frames = [dashboard_frame(self), transaction_frame(self), services_frame(self), sales_frame(self), inventory_frame(self), patient_info_frame(self), reports_frame(self), user_setting_frame(self), histlog_frame(self)]
        temp_labels = ['Dashboard', 'Transaction', 'Services', 'Sales', 'Inventory', 'Pet Info', 'Reports', 'User Settings', 'History']
        temp_icons = [self.dashboard_icon, self.transact_icon, self.services_icon, self.sales_icon, self.inventory_icon, self.patient_icon, self.report_icon, self.user_setting_icon, self.histlog_icon]
        temp_main_frames = [dashboard_frame, transaction_frame, services_frame, sales_frame, inventory_frame, patient_info_frame, reports_frame, user_setting_frame, histlog_frame]
        temp_user_lvl_access = list(database.fetch_data('Select * from account_access_level WHERE usn = ?', (acc_info[0][0], ))[0][1:])
        self.labels = []
        self.icons = []
        self.main_frames:list = []
        for i in range(len(temp_main_frames)):
            if temp_user_lvl_access[i]:
                self.icons.append(temp_icons[i])
                self.labels.append(temp_labels[i])
                self.main_frames.append(temp_main_frames[i](self))
        del temp_main_frames, temp_user_lvl_access, temp_labels, temp_icons

        self.active_win = None
        mainframes = self.main_frames
        self.active_main_frame = None

        '''setting the user level access'''
        '''user_level_access = database.fetch_data(sql_commands.get_level_acessess, (acc_info[0][2], ))[0]
        if(not user_level_access[1]):
            temp:inventory_frame = self.main_frames[4]
            temp.add_item_btn.destroy()
            del temp'''

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

        self.logo_label = ctk.CTkLabel(self.logo_frame, text=title_name, font=("DM Sans Medium", 16),
                                       text_color=Color.Grey_Bright, wraplength=150, justify='left')
        self.logo_label.pack(side="right",padx=(5,0))
        
        '''side buttons'''
        self.side_frame_btn: List[cctk.ctkButtonFrame] = []
        for i in range(len(self.main_frames)):
            self.side_frame_btn.append(cctk.ctkButtonFrame(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                                           fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                                           corner_radius=0, cursor="hand2",))
            
            #self.db_button.configure(command=partial(change_active_event, self.db_button, 0))
            self.side_frame_btn[i].configure(command=partial(load_main_frame, self.labels[i], i))
            self.side_frame_btn[i].pack()
            wbar = ctk.CTkLabel(self.side_frame_btn[i],text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
            wbar.pack(side="left")
            icon = ctk.CTkLabel(self.side_frame_btn[i],image=self.icons[i], text="")
            icon.pack(side="left", padx=(width * 0.016,width * 0.01))
            label = ctk.CTkLabel(self.side_frame_btn[i], text= self.labels[i], font=("DM Sans Medium", 16), text_color=Color.Grey_Bright,)
            label.pack(side="left")
            self.side_frame_btn[i].pack()
            self.side_frame_btn[i].update_children()

        self.sidebar_btn_mngr = cctku.button_manager(self.side_frame_btn, selected_btn_color, False, 0)
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

        self.title_label = ctk.CTkLabel(self.top_frame, text="", font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht)
        self.title_label.grid(row = 0, column=0,sticky='w', padx= width * 0.02)

        self.notif_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqheight()*0.5), text= "", image= self.notif_icon,
                                              fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight() *0.5), border_width=0, corner_radius=5,
                                              font=("Poppinds Medium", 16),hover_color=Color.White_Gray,)
        self.notif_btn.grid(row=0, column= 1, sticky='w')
        """self.settings_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqheight()* 0.5), text= "", image= self.settings_icon,
                                              fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight()* 0.5), border_width=0, corner_radius=5,
                                              font=("Poppinds Medium", 16),hover_color=Color.White_Gray,)
        self.settings_btn.grid(row=0, column= 2, sticky='w') """

        self.acc_btn = cctk.ctkButtonFrame(self.top_frame, round(self.top_frame.winfo_reqwidth() * .12),
                                           round(self.top_frame.winfo_reqheight()*.5), 5,
                                           fg_color=Color.White_Ghost,
                                           hover_color= Color.White_Gray,cursor="hand2")

        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.dp = ctk.CTkLabel(self.acc_btn, width * .03, width * .03, 0, 'transparent', 'transparent', text='', image=self.acc_icon,)
        self.dp.grid(row = 0, column = 0, rowspan = 3, sticky = 'nsew', pady = (round(height * .005), 0), padx = (round(height * .01), 0))
        self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][1]).upper(), font=("DM Sans Medium", 15))
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .005), 0), pady = (5,0))
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][2]).upper(), font=("DM Sans Medium", 12))
        self.position.grid(row = 1, column = 1, sticky = 'nw', padx = (round(height * .005), 0), pady = 0)

        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.acc_btn.update_children()
        self.update()

        '''menubars'''
        self.notif_menu_bar= cctk.menubar(self, width * default_menubar_width, height * default_menubar_height,
                                          corner_radius= 0, fg_color='black', border_width= 0,
                                          position=(self.notif_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                                    self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                                    'c'))
        """ self.settings_menu_bar = cctk.menubar(self, width * default_menubar_width, height * default_menubar_height,
                                              corner_radius= 5, fg_color=Color.White_Ghost, border_width= 0,
                                              position=(self.settings_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                                        self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2+0.005,
                                                        'c'))
        self.settings_menu_bar_dark_mode = ctk.CTkSwitch(self.settings_menu_bar,width=round(width * default_menubar_width/2), height=round(height * .12),text="Dark Mode",
                                                         font=("DM Sans Medium", 16), progress_color=Color.Blue_LapisLazuli_1, text_color=Color.Blue_Maastricht,
                                                         variable = switch_var_darkmode, onvalue="darkmode", offvalue="lightmode",
                                                         command=switch_darkmode,)
        self.settings_menu_bar_dark_mode.pack(anchor= 'c') """
        self.acc_menu_bar = cctk.menubar(self, width * acc_menubar_width, height * default_menubar_height, 0, fg_color=Color.White_Ghost,
                                         position= (1 - acc_menubar_width/2,
                                                    self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                                    'c'))

        self.top_frame_button_mngr = cctku.button_manager([self.notif_btn, self.acc_btn], Color.Platinum, True,
                                                          children=[self.notif_menu_bar, self.acc_menu_bar])

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
        self.canvas = None
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]

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
        ctk.CTkLabel(self.num_transactions, text="Transactions Today:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.transaction_today_count = ctk.CTkLabel(self.num_transactions, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.transaction_today_count.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.items_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.Light_Green, corner_radius=5)
        self.items_sales_frame.grid(row=3, column=0, sticky="nsew", padx=(self.income_frame_width*0.03), pady=(self.income_frame_height*0.015, self.income_frame_height*.015),)
        self.items_sales_frame.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.items_sales_frame, text="Items:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.items_sales_frame, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.items_sales_value.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.services_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.18, fg_color=Color.Red_Tulip, corner_radius=5)
        self.services_sales_frame.grid(row=4, column=0, sticky="nsew", padx=(self.income_frame_width*0.03),pady=( self.income_frame_height*.015))
        self.services_sales_frame.pack_propagate(0)
        ctk.CTkLabel(self.services_sales_frame, text="Services:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.services_sales_value = ctk.CTkLabel(self.services_sales_frame, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.services_sales_value.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        self.total_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=self.income_frame_height*0.15, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.total_sales_frame.grid(row=5, column=0, sticky="nsew", padx=(self.income_frame_width*0.03),pady=(self.income_frame_height*.015, self.income_frame_height*.05))
        self.total_sales_frame.pack_propagate(0)
        ctk.CTkLabel(self.total_sales_frame, text="Total:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(self.income_frame_width*.025,0))
        self.total_sales_value = ctk.CTkLabel(self.total_sales_frame, font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht)
        self.total_sales_value.pack(side="right", anchor="c", padx=(0,self.income_frame_width*.025))

        #Watermelon Pie
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
                                               column_format=f'/No:{int(width*.03)}-#c/Day:x-tl/Total:x-tl!30!30',
                                               header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent')
        self.sales_data_treeview.pack()

        self.current_total = ctk.CTkLabel(self.sales_history_frame, text="Total:   0,000.00", fg_color=Color.White_Chinese, corner_radius=5,height=height*0.05, width=width*0.125, anchor="e", font=("DM Sans Medium", 14))
        self.current_total.grid(row=2, column=1, sticky="e", padx=width*0.015, pady=(height*0.005,height*0.015))

        '''self.view_more_button = ctk.CTkButton(self.sales_history_frame, text='View More',width= self.income_frame_width*0.16, height=self.income_frame_height*0.06, font=('DM Sans Medium', 12), corner_radius=4, text_color=Color.Blue_Maastricht,
                                              fg_color=Color.White_AntiFlash,hover_color=Color.Platinum, command=lambda:print("Go To Report Section"))
        self.view_more_button.grid(row=2, column=0, sticky="w", padx=self.income_frame_width*0.035,pady=(0,self.income_frame_height*0.035))'''

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
                                               column_format=f'/No:{int(width*.03)}-#r/ClientName:x-tl/Service:x-tl/ContactNo:{int(width*.115)}-tr!30!30',)
        self.sched_data_treeview.pack()

        self.status_popup = Inventory_popup.show_status(self, (width, height, acc_cred, acc_info))
        self.generate_DISumarry()
        self.load_saled_data_treeview()
        self.load_scheduled_service()
        self.grid_forget()

    def load_scheduled_service(self):
        data = database.fetch_data("SELECT patient_name, service_name, 'TEST' FROM services_transaction_content WHERE scheduled_date = CURRENT_DATE")
        self.sched_data_treeview.update_table(data)

    def load_saled_data_treeview(self):
        date = datetime.datetime.now()
        data = database.fetch_data(sql_commands.get_monthly_sales_data, (date.month, date.year))
        total = sum([price_format_to_float(s[-1][1:]) for s in data])
        self.current_total.configure(text = 'Total:   ' + '₱' + format_price(total))
        self.sales_data_treeview.update_table(data)

    def show_status_popup(self, name: str, data):
            self.status_popup.status_label.configure(text = name)
            self.status_popup.update_treeview(data)
            self.status_popup.place(relx = .5, rely = .5, anchor = 'c')

    def show_pie(self, data: list = None):
        if(self.canvas is not None):
            self.canvas.get_tk_widget().destroy()
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                   float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]
        data = self.data if self.data[0] + self.data[1] > 0 else [1, 0]

        pie_figure= Figure(figsize=(self.income_frame_width*0.006,self.income_frame_height*0.013), dpi=100)
        pie_figure.set_facecolor(Color.White_Ghost)
        ax =pie_figure.add_subplot(111)
        ax.pie(data, autopct='%1.1f%%', startangle=0,counterclock=0, explode=(0.1,0), colors=[Color.Light_Green, Color.Red_Tulip],
                textprops={'fontsize':18, 'color': Color.White_Ghost, 'family':'monospace', 'weight':'bold' },)
        pie_figure.subplots_adjust(top=1,left=0,right=1, bottom=0)

        self.canvas = FigureCanvasTkAgg(pie_figure, self.income_summary_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row = 0, column=1, rowspan = 6)

    def generate_DISumarry(self):
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0),
                    int(database.fetch_data(sql_commands.get_todays_transaction_count)[0][0] or 0)]
        self.items_sales_value.configure(text = f'₱{format_price(self.data[0])}')
        self.services_sales_value.configure(text = f'₱{format_price(self.data[1])}')
        self.total_sales_value.configure(text = f'₱{format_price(self.data[0] + self.data[1])}')
        self.transaction_today_count.configure(text = self.data[2])
        self.show_pie()

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
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        global width, height, acc_cred, acc_info, mainframes
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.trash_icon = ctk.CTkImage(light_image=Image.open("image/trash.png"), size=(20,20))
        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
        self.service_icon = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(20,20))
        self.item_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"), size=(20,20))
        self.cal_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(20,20))
        self.proceed_icon = ctk.CTkImage(light_image=Image.open("image/rightarrow.png"), size=(15,15))
        self.invoice_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
        self.payment_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(22,16))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(18,18))
        
        """ self.grid_columnconfigure((1), weight=1)
        self.grid_rowconfigure((1), weight=1)

        self.or_num_label = ctk.CTkLabel(self, fg_color=Color.White_Ghost, corner_radius=5, width=width*0.125, height = height*0.05,
                                         text="OR#: 0001", font=("DM Sans Medium", 15))
        self.or_num_label.grid(row=0, column=0, padx=(width*0.005,0), pady=(height*0.01), sticky="w")

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Ghost, width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=2, padx=(width*0.005),  pady=(height*0.01))

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent", )
        self.top_frame.grid(row=1, column=0, columnspan=3, sticky="nsew")


        self.client_name_frame = ctk.CTkFrame(self, fg_color=Color.White_Ghost, width=width*0.4, height=height*0.05)
        self.client_name_frame.grid(row=0, column=1, sticky="w", padx=(width*0.005))
        self.client_name_frame.pack_propagate(0)

        self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
        self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

        self.client_name_entry = ctk.CTkOptionMenu(self.client_name_frame,font=("DM Sans Medium", 15), fg_color="white", text_color='black', command= change_customer_callback)
        self.client_name_entry.set('')
        self.client_names = [s[0] for s in database.fetch_data(sql_commands.get_owners)]
        self.client_name_entry.configure(values = self.client_names)
        self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005), pady=(height*0.005))

        self.transact_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3])
        self.transact_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))

        self.transact_treeview = cctk.cctkTreeView(self.transact_frame, data=[], width=width*0.8, height=height*0.675,
                                                   column_format=f'/No:{int(width*0.025)}-#r/Particulars:x-tl/UnitPrice:{int(width*0.085)}-tr/Quantity:{int(width*0.1)}-id/Total:{int(width*0.085)}-tr/Action:{int(width*.065)}-bD!30!30')
        self.transact_treeview.pack(pady=(height*0.01,0))
        self.transact_treeview.bd_commands = bd_commands

        self.bottom_frame = ctk.CTkFrame(self.transact_frame, fg_color="transparent", height=height*0.05)
        self.bottom_frame.pack(pady=(height*0.01), fill="x", padx=(width*0.005))
        #self.bottom_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))

        self.add_particulars = ctk.CTkButton(self.bottom_frame, width=width*0.125, height=height*0.05, text='Add Particulars',
                                             image=self.add_icon, command=lambda:self.show_particulars.place(relx=0.5, rely=0.5, anchor="c", client = self.client_name_entry.get()))
        self.add_particulars.pack(side="left",  padx=(width*0.005, 0))

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
                                             command=lambda:transaction_popups.show_transaction_proceed(self, (width, height, acc_cred), self.services_total_amount._text,
                                                            self.item_total_amount._text, self.price_total_amount._text, self.transact_treeview._data,
                                                            self.client_name_entry.get() or 'N/A', self.transact_treeview, self.service_dict).place(relx = .5, rely = .5, anchor = 'c'))
        self.proceeed_button.grid(row=3, column=2, pady=(0,height*0.025),padx=(0, width*0.005), sticky="e") 

        self.show_list_item: ctk.CTkFrame = transaction_popups.show_item_list(self, (width, height), self.transact_treeview, self.change_total_value_item)
        self.show_services_list: ctk.CTkFrame = transaction_popups.show_services_list(self, (width, height), self.transact_treeview, self.change_total_value_service)
        #self.show_proceed_transact: ctk.CTkFrame =
        self.show_customer_info:ctk.CTkFrame = transaction_popups.customer_info(self, (width, height))
        self.show_sched_service:ctk.CTkFrame = transaction_popups.scheduled_services(self,(width, height))
        self.show_particulars:ctk.CTkFrame = transaction_popups.add_particulars(self,(width, height), self.transact_treeview, self.change_total_value_item, self.change_total_value_service, self.service_dict)
        """
        
        selected_color = Color.Blue_Yale
        
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")
        
        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)
        
        self.invoice_frame = ctk.CTkFrame(self.base_frame, fg_color="transparent")
        self.payment_frame = ctk.CTkFrame(self.base_frame, fg_color="transparent")
        
        self.transact_frames=[self.invoice_frame, self.payment_frame]
        self.active_transact_frames = None
        
        def load_main_frame(cur_frame: int):
            if self.active_transact_frames is not None:
                self.active_transact_frames.pack_forget()
            self.active_transact_frames = self.transact_frames[cur_frame]
            self.active_transact_frames.pack(fill="both", expand=1)
        
        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")
        
        self.invoice_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.1,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.invoice_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.invoice_button.configure(command=partial(load_main_frame, 0))
        self.invoice_button_icon = ctk.CTkLabel(self.invoice_button, text="", image=self.invoice_icon)
        self.invoice_button_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.invoice_button_label = ctk.CTkLabel(self.invoice_button, text="RECEPTION", text_color="white", font=("DM Sans Medium",14))
        self.invoice_button_label.pack(side="left")
        self.invoice_button.grid()
        self.invoice_button.update_children()
        
        self.payment_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.1,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.payment_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.payment_button.configure(command=partial(load_main_frame, 1))
        self.payment_icon = ctk.CTkLabel(self.payment_button, text="",image=self.payment_icon)
        self.payment_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.payment_label = ctk.CTkLabel(self.payment_button, text="PAYMENT", text_color="white",  font=("DM Sans Medium",14))
        self.payment_label.pack(side="left")
        self.payment_button.grid()
        self.payment_button.update_children()
        
        self.button_manager = cctku.button_manager([self.invoice_button, self.payment_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)
        
        '''INVOICE FRAME: START'''
        
        self.invoice_frame.grid_rowconfigure(1, weight=1)
        self.invoice_frame.grid_columnconfigure(0, weight=1)
        
        '''TOP FRAME'''
        self.top_con_frame = ctk.CTkFrame(self.invoice_frame,fg_color="transparent")
        self.top_con_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        #invoice search button
        self.search_frame = ctk.CTkFrame(self.top_con_frame, width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.pack(side="left")
        self.search_frame.pack_propagate(0)
        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005,)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))
        
        self.add_item_btn = ctk.CTkButton(self.top_con_frame,width=width*0.1, height = height*0.05, text="Add Invoice",image=self.add_icon, font=("DM Sans Medium", 14))
        self.add_item_btn.configure(command=lambda:self.show_invoice.place(relx=0.5, rely=0.5, anchor="c"))
        self.add_item_btn.pack(side="left", padx=(width*0.005))

        self.refresh_btn = ctk.CTkButton(self.top_con_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command = self.update_invoice_treeview)
        self.refresh_btn.pack(side="left", padx=(0,width*0.005))
        
        #self.edit_btn = ctk.CTkButton(self.top_con_frame,text="Cancel Invoice", width=width*0.065, height = height*0.05, font=("DM Sans Medium", 14), fg_color= '#ff6464', command = self.cancel_invoice)
        #self.edit_btn.pack(side="right")
        
        self.cancel_invoice_btn = ctk.CTkButton(self.top_con_frame,text="Cancel Invoice", width=width*0.065, height = height*0.05, font=("DM Sans Medium", 14), fg_color= '#ff6464', command = self.cancel_invoice)
        self.cancel_invoice_btn.pack(side="right")
        
        '''INVOICE FRAME'''
        self.invoice_treeview_frame = ctk.CTkFrame(self.invoice_frame)
        self.invoice_treeview_frame.grid(row=1, column=0, sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))

        self.invoice_treeview = cctk.cctkTreeView(self.invoice_treeview_frame, width= width * .805, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/InvoiceId:{int(width*.075)}-tc/ClientName:x-tl/Services:{int(width*.125)}-tr/Items:{int(width*.125)}-tr/Total:{int(width*.1)}-tr/Date:{int(width*.1)}-tc!30!30')
        self.update_invoice_treeview()
        self.invoice_treeview.pack()

        self.proceeed_button = ctk.CTkButton(self.invoice_frame, text="Proceed to Payment", image=self.proceed_icon, height=height*0.05, width=width*0.135,font=("Arial", 14),
                                             compound="right", command = self.proceed_to_payment)
        self.proceeed_button.grid(row=2, column=0, pady=(0,height*0.01),padx=(0, width*0.005), sticky="e") 
        
        
        self.show_invoice:ctk.CTkFrame = transaction_popups.add_invoice(self,(width, height), self.update_invoice_treeview, acc_cred[0][0])
        
        '''INVOICE FRAME: END'''
        
        '''PAYMENT FRAME: START'''
        
        self.payment_frame.grid_rowconfigure(1, weight=1)
        self.payment_frame.grid_columnconfigure(2, weight=1)
        
        self.search_frame = ctk.CTkFrame(self.payment_frame,width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))
        
        """ self.view_btn = ctk.CTkButton(self.payment_frame,text="View Record", width=width*0.05, height = height*0.05, font=("DM Sans Medium",16))
        self.view_btn.grid(row=0, column=1, sticky="w", padx=(0, width*0.0025)) """
        
        self.refresh_btn = ctk.CTkButton(self.payment_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command = self.update_payment_treeview)
        self.refresh_btn.grid(row=0, column=2, sticky="w")
        
        self.payment_treeview_frame = ctk.CTkFrame(self.payment_frame)
        self.payment_treeview_frame.grid(row=1, column=0, columnspan=4, sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))

        self.payment_treeview = cctk.cctkTreeView(self.payment_treeview_frame, width= width * .805, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/InvoiceId:{int(width*.075)}-tc/ClientName:x-tl/Services:{int(width*.1)}-tr/Items:{int(width*.1)}-tr/Total:{int(width*.09)}-tr!30!30')
        self.update_payment_treeview()
        self.payment_treeview.pack()
        
        self.proceeed_button = ctk.CTkButton(self.payment_frame, text="Proceed", image=self.proceed_icon, height=height*0.05, width=width*0.135,font=("Arial", 14), compound="right")
        self.proceeed_button.configure(command= self.proceed_to_pay)
        self.proceeed_button.grid(row=2, column=3, pady=(0,height*0.01),padx=(0, width*0.005), sticky="e") 
        
        #self.show_proceed:ctk.CTkFrame =transaction_popups.show_transaction_proceed_demo(self,(width, height))
        self.show_payment_proceed = transaction_popups.show_payment_proceed(self,(width, height))
        load_main_frame(0)

    def cancel_invoice(self, bypass_confirmation: bool = False):
        if self.invoice_treeview.get_selected_data() is None:
            messagebox.showwarning("Fail to proceed", "Select an invoice \nto cancel")
            return
        if bypass_confirmation:
            database.exec_nonquery([[sql_commands.cancel_invoice, (self.invoice_treeview.get_selected_data()[0], )]])
        else:
            if(messagebox.askyesno("Cancel Invoice", "Are you really want\nto cancel this invoice")):
                database.exec_nonquery([[sql_commands.cancel_invoice, (self.invoice_treeview.get_selected_data()[0], )]])

        self.update_invoice_treeview()

    def proceed_to_pay(self):
        data = self.payment_treeview.get_selected_data()
        if(data):
            self.show_payment_proceed.place(invoice_data= data, cashier= acc_cred[0][0], treeview_callback= self.update_payment_treeview,
                                            update_callback= self.reset,
                                            relx = .5, rely = .5, anchor = 'c')
        else:
            messagebox.showwarning("Fail to proceed", "Select an invoice before\nheading into the payment")            

    def proceed_to_payment(self):
        data = self.invoice_treeview.get_selected_data()
        if(data):
            stock_quan = [s[0] for s in database.fetch_data(sql_commands.check_if_stock_can_accomodate, (data[0], ))]
            if 0 not in stock_quan: 
                database.exec_nonquery([[sql_commands.set_invoice_transaction_to_payment, (data[0], )]])
                self.update_payment_treeview()
                self.payment_treeview.data_frames[self.payment_treeview._data.index(data)].response()
                self.payment_button.response()
                self.update_invoice_treeview()
            else:
                messagebox.showwarning("Fail to proceed", "Current stock cannot accomodate the transaction")      
        else:
            messagebox.showwarning("Fail to proceed", "Select an invoice before\nheading into the payment")            
    
    def update_payment_treeview(self):
        self.payment_treeview.update_table(database.fetch_data(sql_commands.get_payment_invoice_info))

    def update_invoice_treeview(self):
        self.invoice_treeview.update_table(database.fetch_data(sql_commands.get_invoice_info))
        
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
        for i in mainframes:
            if isinstance(i, dashboard_frame):
                temp: dashboard_frame = i
                temp.show_pie()
                temp.generate_stat_tabs()
                temp.generate_DISumarry()
                temp.load_saled_data_treeview()
                temp.load_scheduled_service()
            if isinstance(i, reports_frame):
                temp: reports_frame = i
                temp.graphs_need_upgrade()
                temp.update_invetory_graph()
            if isinstance(i, sales_frame):
                temp: sales_frame = i
                temp.update_table()
            self.show_invoice.update_particular_pop_up()
        #check if there are certain mainframes there, then update all of those needed process and ui

        #self.client_name_entry.set('')
        #self.transact_treeview.delete_all_data()
        #self.price_total_amount.configure(text = '0.00')
        #self.services_total_amount.configure(text = '0.00')
        #self.item_total_amount.configure(text = '0.00')

class services_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_forget()

        def refresh(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            #self.services_raw_data = database.fetch_data(sql_commands.get_service_data, None)
            #self.services_data_for_treeview = [] if self.services_raw_data is None else [(s[0], format_price(float(s[1])), s[2]) for s in self.services_raw_data]
            self.update_table()           
            self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

    
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
        
        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=1, sticky="ns", padx=width*0.005,pady=height*0.01)

        self.top_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion, height = height*0.055, corner_radius=0)
        self.top_frame.grid(row=0, column=0 , sticky="nw",padx=width*0.005,pady=(height*0.01,0))

        self.search_frame = ctk.CTkFrame(self.top_frame, width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.pack(side="left", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))
        
        self.add_service = ctk.CTkButton(self.top_frame, text="Add Service", font=("DM Sans Medium", 14), width=width*0.1, height = height*0.05, image=self.plus,
                                         command=lambda: service_popup.add_service(self,(width, height), self.update_table).place(relx=0.5, rely=0.5, anchor="c"))
        self.add_service.pack(side="left", padx=(0,width*0.005), pady=(height*0.01))
        
        self.refresh_btn = ctk.CTkButton(self.top_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=refresh)
        self.refresh_btn.pack(side="left", padx=(0,width*0.005), pady=(height*0.01))

        self.sub_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,corner_radius=0)
        self.sub_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0, height*0.01))
        self.sub_frame.grid_rowconfigure(0, weight=1)
        self.sub_frame.grid_columnconfigure(0, weight=1)
        
        self.service_data_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Platinum, corner_radius=0)
        self.service_data_frame.grid(row=0, column=0, columnspan=6, sticky="nsew", padx=(width*0.005), pady=(height*0.0125, height*0.02))
        """ 
        self.services_raw_data = database.fetch_data(sql_commands.get_service_data, None)
        print(self.services_raw_data)
        self.services_data_for_treeview = [(s[0], format_price(float(s[1])), s[2]) for s in self.services_raw_data]
        
        self.services_treeview = cctk.cctkTreeView(self.service_data_frame, data = self.services_data_for_treeview, width=width*0.8, height=height*0.8,
                                               column_format=f'/No:{int(width*.025)}-#r/Name:x-tl/Price:{int(width*.07)}-tr/LastedEdited:{int(width*.1)}-tc/Actions:{int(width*.08)}-bD!30!30') """
        
        "TEST"
        self.services_raw_data = database.fetch_data(sql_commands.get_service_data_test, None)
        self.services_data_for_treeview = [(s[0], s[1], s[2], format_price(float(s[3]))) for s in self.services_raw_data]
        
        self.services_treeview = cctk.cctkTreeView(self.service_data_frame, data = self.services_data_for_treeview , width=width*0.8, height=height*0.8,
                                               column_format=f'/No:{int(width*.025)}-#r/ServiceCode:{int(width*.125)}-tc/ServiceName:x-tl/Category:{int(width*.175)}-tl/Price:{int(width*.115)}-tr!30!30')
        self.services_treeview.pack()
        
    def update_table(self):
        self.services_raw_data = database.fetch_data(sql_commands.get_service_data_test, None)
        self.services_data_for_treeview = [(s[0], s[1], s[2], format_price(float(s[3]))) for s in self.services_raw_data]
        self.services_treeview.update_table(self.services_data_for_treeview)

class sales_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_forget()

        def set_date():
            self.data_view.update_table(database.fetch_data(f"SELECT transaction_uid, client_name, transaction_date, Total_amount, Attendant_usn FROM transaction_record WHERE transaction_date='{self.date_select_entry._text}'"))
            
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))

        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=1, sticky="ns", padx=width*0.005,pady=height*0.01)

        self.top_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion, height = height*0.055, corner_radius=0)
        self.top_frame.grid(row=0, column=0 , sticky="nw",padx=width*0.005,pady=(height*0.01,0))

        self.search_frame = ctk.CTkFrame(self.top_frame, width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))
        
        self.refresh_btn = ctk.CTkButton(self.top_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1,padx=(0, width*0.005))

        self.sub_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,corner_radius=0)
        self.sub_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0, height*0.01))
        self.sub_frame.grid_rowconfigure(1, weight=1)
        self.sub_frame.grid_columnconfigure(1, weight=1)
        
        '''DATE SELECTION'''
        self.date_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Platinum, height=height*0.05, width=width*0.175)
        self.date_frame.grid(row=0, column=0, padx=(width*0.005), pady=(height*0.01))
        self.date_frame.propagate(0)
        
        ctk.CTkLabel(self.date_frame, text="Date: ", font=("DM Sans Medium", 14),).pack(side="left", padx=(width*0.015,0), pady=(height*0.01))
        self.date_select_entry = ctk.CTkLabel(self.date_frame, text=date.today(), font=("DM Sans Medium", 14), fg_color=Color.White_Lotion, corner_radius=5)
        self.date_select_entry.pack(side="left", fill="both", expand=1,  padx=(0), pady=(height*0.005))
        
        self.show_calendar = ctk.CTkButton(self.date_frame, text="",image=self.cal_icon, height=height*0.05,width=width*0.025, fg_color=Color.Blue_Yale,
                                               command=lambda:cctk.tk_calendar(self.date_select_entry, "%s", date_format="raw", max_date=datetime.datetime.now(), set_date_callback=set_date))
        self.show_calendar.pack(side="left", padx=(width*0.0025), pady=(height*0.005))
        
        '''TREEVIEW'''
        self.treeview_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Platinum)
        self.treeview_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
        
        #self.main_data = database.fetch_data(sql_commands.get_transaction_data, None)
        #self.main_data = [(s[0], s[2], str(datetime.datetime.now().date()), format_price(float(s[3])), s[1]) for s in self.main_data]
        self.data_view = cctk.cctkTreeView(self.treeview_frame, width=width * .8, height=height * .8,
                                           column_format=f'/No:{int(width*0.025)}-#r/OR:{int(width*0.075)}-tc/Client:x-tl/Date:{int(width*0.15)}-tc/Total:{int(width*0.085)}-tr/Cashier:{int(width*.175)}-tl!30!30')
        #self.data_view.configure(double_click_command = lambda _: Sales_popup.show_sales_record_info(self, (width, height), ('a', 'b', 'c'), [None, None]).place(relx = .5, rely = .5, anchor = 'c') )
        self.data_view._double_click_command = lambda _: self.show_sale_info.place(relx=0.5, rely=0.5, anchor="c")
        self.data_view.pack()
        
        self.show_sale_info = Sales_popup.show_sales_record_info(self, (width, height)) 
        self.update_table()

    def grid(self, **kwargs):
        return super().grid(**kwargs)
    
    def update_table(self):
        self.data_view.update_table(database.fetch_data(f"SELECT transaction_uid, client_name, transaction_date, Total_amount, Attendant_usn FROM transaction_record WHERE transaction_date='{date.today()}'"))

class inventory_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info, mainframes
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(18,18))
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
        self.edit_icon = ctk.CTkImage(light_image= Image.open("image/edit_icon.png"), size=(16,16))

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

        self.sort_type_option_var = ctk.StringVar(value="Sort by Levels")
        self.sort_status_option_var = ctk.StringVar(value="Normal")

        self.sort_status_var=["Sort by Levels","Sort by Category", "Sort by Expiry"]
        self.sort_type_var=["Normal","Reorder","Critical"]

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        '''data'''
        selected_color = Color.Blue_Yale
        self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
        self.sell_rate = {s[0]: s[1] for s in database.fetch_data(sql_commands.get_selling_rate)}

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)

        def refresh(_ :any = None):
            self.sort_type_option.set('Sort by Levels')
            sort_status_callback('Sort by Levels')

        def update_tables(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.refresh_btn.after(1000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
            self.data_view1.pack_forget()
            temp = [(self.sell_rate[s[0]], ) + s for s in self.list_show]
            #self.data_view1.update_table(self.list_show)
            self.data_view1.update_table(temp)
            self.data_view1.pack()

        def get_categories():
            
            data = database.fetch_data("SELECT categ_name FROM categories")
            category_data = ["All Items"]
            for i in range(len(data)):
                category_data.append(data[i][0])
            
            return category_data

        def sort_status_callback(option):
            if "Levels" in option:
                self.sort_status_option.configure(values=["All", "Normal","Reorder","Critical", "Out of Stock"])
                self.sort_status_option.set("All")
                sort_status_configuration_callback()
            elif "Category" in option:
                self.sort_status_option.configure(values=get_categories())
                self.sort_status_option.set("All Items")
                #sort_status_configuration_callback()
            else:
                self.sort_status_option.configure(values=["All","Safe","Nearly Expire", "Expired", "No Expiration"])
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
            elif 'Category' in self.sort_type_option.get():
                if "All" in self.sort_status_option.get():
                    self.list_show = database.fetch_data(sql_commands.get_inventory_by_group)
                else:
                    self.list_show = database.fetch_data(sql_commands.get_category_specific_inventory, (self.sort_status_option.get(), ))
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
            self.data_view1.update_table(self.data1)

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")


        self.inventory_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.inventory_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.inventory_button.configure(command=partial(load_main_frame, 0))
        self.inventory_icon = ctk.CTkLabel(self.inventory_button, text="",image=self.inventory_icon)
        self.inventory_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.inventory_label = ctk.CTkLabel(self.inventory_button, text="INVENTORY", text_color="white", font=("DM Sans Medium", 14))
        self.inventory_label.pack(side="left")
        self.inventory_button.grid()
        self.inventory_button.update_children()

        self.stock_in_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.stock_in_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.stock_in_button.configure(command=partial(load_main_frame, 1))
        self.stock_in_icon = ctk.CTkLabel(self.stock_in_button, text="",image=self.restock_icon)
        self.stock_in_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_in_label = ctk.CTkLabel(self.stock_in_button, text="RECEIVING", text_color="white", font=("DM Sans Medium", 14))
        self.stock_in_label.pack(side="left")
        self.stock_in_button.grid()
        self.stock_in_button.update_children()

        self.stock_disposal_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.stock_disposal_button.grid(row=0, column=2, sticky="sw", padx=(0,width*0.0025), pady=0)
        self.stock_disposal_button.configure(command=partial(load_main_frame, 2))
        self.stock_disposal_icon = ctk.CTkLabel(self.stock_disposal_button, text="",image=self.trash_icon)
        self.stock_disposal_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.stock_disposal_label = ctk.CTkLabel(self.stock_disposal_button, text="ITEM DISPOSAL", text_color="white", font=("DM Sans Medium", 14))
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

        '''Search Reference'''
        self.search_frame = ctk.CTkFrame(self.inventory_sub_frame,width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))

        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005, command=search)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))
        '''End'''
        
        """ self.refresh_btn = ctk.CTkButton(self.inventory_sub_frame,text="", width=width*0.0275, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1, sticky="w",padx=(0, width*0.005)) """
        
        self.add_item_btn = ctk.CTkButton(self.inventory_sub_frame,width=width*0.08, height = height*0.05, text="Add Item",image=self.add_icon, font=("DM Sans Medium", 14),
                                          command= lambda : self.add_item_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_item_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))
        
        self.view_category = ctk.CTkButton(self.inventory_sub_frame, height=height*0.05,width=width*0.07, text="Category",  font=("DM Sans Medium", 14),
                                           command = lambda: self.category_popup.place(relx=0.5, rely=0.5, anchor="c"))
        self.view_category.grid(row=0, column=2, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.refresh_btn = ctk.CTkButton(self.inventory_sub_frame,text="", width=width*0.0275, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=3, sticky="w")

        self.sort_frame = ctk.CTkFrame(self.inventory_sub_frame,  height = height*0.05, fg_color=Color.Platinum)
        self.sort_frame.grid(row=0, column=5, padx=(width*0.005), pady=(height*0.007), sticky="e")

        self.sort_type_option= ctk.CTkOptionMenu(self.sort_frame, values=self.sort_status_var, anchor="center", font=("DM Sans Medium", 12), width=width*0.115, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=partial(sort_status_callback))
        self.sort_type_option.grid(row=0, column=0, padx=(width*0.0045,0), pady=(height*0.0065), sticky="e")

        self.sort_status_option= ctk.CTkOptionMenu(self.sort_frame, values=self.sort_type_var, anchor="center", font=("DM Sans Medium", 12), width=width*0.1, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Color[3],
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=sort_status_configuration_callback)
        self.sort_status_option.grid(row=0, column=1, padx=(width*0.005), pady=(height*0.0065), sticky="e")

        self.restock_btn = ctk.CTkButton(self.inventory_sub_frame, width=width*0.1, height = height*0.05, text="Stock Order", image=self.restock_icon, font=("DM Sans Medium", 14),
                                        command= lambda : self.restock_popup.place(default_data=self.data_view1.data_grid_btn_mng.active or None, update_cmds=self.update_tables, relx = .5, rely = .5, anchor = 'c'))
        self.restock_btn.grid(row=3, column=5, pady=(height*0.01), sticky="e", padx=(0, width*0.005))
        self.tree_view_frame = ctk.CTkFrame(self.inventory_sub_frame, fg_color="transparent")
        self.tree_view_frame.grid(row=1, column=0,columnspan=6, sticky="nsew",padx=(width*0.005))

        #self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.data_view1 = cctk.cctkTreeView(self.tree_view_frame, None, width= width * .805, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/Rate:{int(width*.045)}-tc/ItemName:x-tl/Stock:{int(width*.07)}-tr/Price:{int(width*.07)}-tr/NearestExpire:{int(width*.1)}-tc/Status:{int(width*.08)}-tc!30!30',
                                           conditional_colors= {6: {'Reorder':'#ff7900', 'Critical':'red','Normal':'green', 'Out Of Stock': '#555555', 'Safe':'green', 'Nearly Expire':'#FFA500','Expired':'red'},
                                                                1: {'🠉': 'green', '🠋': 'red', '-' : '#AAAAAA'}})
        self.data_view1.pack()

        self.refresh_btn.configure(command = refresh)

        self.sort_type_option.set("Sort by Levels")

        '''INVENTORY FRAME: END'''

        '''RESTOCK: START'''
        def refresh_rs_data_view1():
            self.rs_data_view1.update_table(database.fetch_data(sql_commands.get_recieving_items))

        def restocking_callback():
            refresh_rs_data_view1()
            update_tables()
            self.inventory_button.response()


        def _restock(_: any = None):
            if self.rs_data_view1.get_selected_data():
                self.restock_confirm.place(relx= 0.5, rely=0.5, anchor="c", restocking_info= self.rs_data_view1.get_selected_data(),
                                           after_callback = restocking_callback)
            """ self.restock_popup.stock(self.rs_data_view1)
            temp:dashboard_popup = mainframes[0]
            temp.generate_stat_tabs() """
        #self.restock_frame.pack(fill="both", expand=1)
        self.restock_frame.grid_propagate(0)
        self.restock_frame.grid_rowconfigure(1, weight=1)

        self.restock_frame.grid_columnconfigure(3, weight=1)

        self.rs_search_frame = ctk.CTkFrame(self.restock_frame,width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.rs_search_frame.grid(row=0, column=0,sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.rs_search_frame.pack_propagate(0)

        ctk.CTkLabel(self.rs_search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))
        self.rs_search_entry = ctk.CTkEntry(self.rs_search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.rs_search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.rs_search_btn = ctk.CTkButton(self.rs_search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005, command=search)
        self.rs_search_btn.pack(side="left", padx=(0, width*0.0025))

        self.rs_add_item_btn = ctk.CTkButton(self.restock_frame,width=width*0.1, height = height*0.05, text="Add Order",image=self.add_icon, font=("DM Sans Medium", 14),
                                           command= lambda : self.restock_popup.place(default_data=self.data_view1.data_grid_btn_mng.active or None, relx = .5, rely = .5, anchor = 'c'))
        self.rs_add_item_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_refresh_btn = ctk.CTkButton(self.restock_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command= refresh_rs_data_view1)

        self.rs_refresh_btn.grid(row=0, column=2, sticky="w", padx=(0,width*0.005))

        self.receive_history = ctk.CTkButton(self.restock_frame, width=width*0.025, height = height*0.05, text="Received Items", image=self.history_icon, font=("DM Sans Medium", 14),
                                             command=lambda: self.history_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.receive_history.grid(row=0, column=3, sticky="e", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_supplier_btn = ctk.CTkButton(self.restock_frame,width=width*0.08, height = height*0.05, text="Supplier",image=self.person_icon, font=("DM Sans Medium", 14),
                                          command= lambda : self.supplier_list_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.rs_supplier_btn.grid(row=0, column=4,sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.rs_treeview_frame = ctk.CTkFrame(self.restock_frame,fg_color="transparent")
        self.rs_treeview_frame.grid(row=1, column=0, columnspan=5, sticky="nsew", padx=width*0.005)

        #self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.rs_data = database.fetch_data(sql_commands.get_recieving_items)
        self.rs_data_view1 = cctk.cctkTreeView(self.rs_treeview_frame, data= self.rs_data,width= width * .805, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ReceivingID:{int(width *.08)}-tc/ItemName:x-tl/Quantity:{int(width*.08)}-tr/Remaining:{int(width*.08)}-tl/SupplierName:{int(width*.15)}-tl/Action:{int(width*.075)}-bD!30!30',
                                            double_click_command= _restock)
        self.rs_data_view1.configure(double_click_command = _restock)
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
        self.category_popup = Inventory_popup.show_category(self, (width, height, acc_cred, acc_info))
        self.restock_confirm = Inventory_popup.restock_confirmation(self, (width, height, acc_cred, acc_info))
        
        sort_status_callback("View by Levels")
        load_main_frame(0)

    def update_tables(self):
        for i in mainframes:
            if isinstance(i, dashboard_frame):
                temp: dashboard_frame = i
                temp.show_pie()
                temp.generate_stat_tabs()
                temp.generate_DISumarry()
                temp.load_saled_data_treeview()
                temp.load_scheduled_service()
            if isinstance(i, reports_frame):
                temp: reports_frame = i
                temp.graphs_need_upgrade()
                temp.update_invetory_graph()
            if isinstance(i, sales_frame):
                temp: sales_frame = i
                temp.update_table()

class patient_info_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        #self.label = ctk.CTkLabel(self, text='6').pack(anchor='w')

        def update_table():
            self.refresh_btn.configure(state = "disabled")
            self.data = database.fetch_data('SELECT id, p_name, o_name, contact from pet_info')
            self.pet_data_view.update_table(self.data)
            self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
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
        self.date_label.grid(row=0, column=1, padx=(width*0.005), pady=(height*0.01))

        self.top_frame =ctk.CTkFrame(self, fg_color=Color.White_Lotion, height = height*0.055, corner_radius=0)
        self.top_frame.grid(row=0, column=0, sticky="nsw", padx=(width*0.005,0), pady=(height*0.01,0))
        
        
        self.search_frame = ctk.CTkFrame(self.top_frame,width=width*0.3, height = height*0.05, fg_color=Color.Platinum)
        self.search_frame.pack(side="left", padx=(width*0.005), pady=(height*0.01))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.005))
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white",placeholder_text_color="light grey", font=("DM Sans Medium", 14))
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
        self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="light grey",
                                        width=width*0.005)
        self.search_btn.pack(side="left", padx=(0, width*0.0025))

        self.refresh_btn = ctk.CTkButton(self.top_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=update_table)
        self.refresh_btn.pack(side="left")
        
        self.add_record_btn = ctk.CTkButton(self.top_frame, width=width*0.08, height = height*0.05, text="Add Record",image=self.add_icon, font=("DM Sans Medium", 14),
                                            command=lambda:self.new_record.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_record_btn.pack(side="left",padx=(width*0.005), pady=(height*0.01))

        self.view_record_btn = ctk.CTkButton(self.top_frame, text="View Record", image=self.gen_icon, font=("DM Sans Medium", 14), width=width*0.1,height = height*0.05,
                                              command=self.view_record)
        self.view_record_btn.pack(side="left",padx=(0,width*0.005), pady=(height*0.01))

        self.treeview_frame =ctk.CTkFrame(self,fg_color=Color.White_Color[3],corner_radius=0)
        self.treeview_frame.grid(row=1, column=0, columnspan=5,sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))
        self.treeview_frame.grid_columnconfigure(0, weight=1)

        self.data = database.fetch_data('SELECT id, p_name, o_name, contact from pet_info')
        #print(self.data)
        self.pet_data_view = cctk.cctkTreeView(self.treeview_frame, data=self.data,width= width * .805, height= height * .775, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/PetID:{int(width*.075)}-tc/PetName:x-tl/OwnerName:{int(width*.225)}-tl/ContactNo:{int(width*.165)}-tr/Action:{int(width*.075)}-bD!30!30',)
        self.pet_data_view.grid(row=0, column=0, columnspan=3, pady=(height*0.01))

        self.new_record = Pet_info_popup.new_record(self, (width, height, acc_cred, acc_info), self.update)
        self.record_view = Pet_info_popup.view_record(self, (width, height, acc_cred, acc_info), self.update)

    def update(self) -> None:
        self.data = database.fetch_data('SELECT id, p_name, o_name, contact from pet_info')
        self.pet_data_view.update_table(self.data)
        return super().update()
    
    def view_record(self):
        pet_data = self.pet_data_view.get_selected_data()
        if(pet_data):
            self.record_view.place(relx = .5, rely = .5, anchor = 'c', pet_data=pet_data)
        else:
            messagebox.showwarning('Warning','No Record is selected')

class reports_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        '''constants'''
        self.months = ["January", "February", "March","April","May", "June", "July", "August","September","October", "November", "December"]
        self.days = [*range(1, 13, 1)]
        

        '''variables'''
        self.data_loading_manager: List[bool] = [False for _ in range(3)]
        self.previous_date = '0';
        self.previous_month = '0';
        self.previous_year = '0';

        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
        self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
        self.generate_report_icon = ctk.CTkImage(light_image=Image.open("image/gen_report.png"),size=(26,26))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.sales_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])
        self.inventory_report_frame = ctk.CTkFrame(self.base_frame,fg_color=Color.White_Color[3])

        self.sales_report_frame.grid_columnconfigure(0, weight=1)
        self.sales_report_frame.grid_rowconfigure((1,2), weight=1)

        self.inventory_report_frame.grid_columnconfigure(1, weight=1)
        self.inventory_report_frame.grid_rowconfigure(1, weight=1)

        self.report_frames=[self.sales_report_frame, self.inventory_report_frame]
        self.active_report = None

        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.daily_pie_canvas = None
        self.daily_hbar_canvas = None
        self.monthly_vbar_canvas = None
        self.yearly_vbar_canvas = None

        selected_color = Color.Blue_Yale

        '''events'''
        self.label=["Items", "Services"]
        self.info = [width*0.0055,height*0.005,Color.White_Platinum]

        monthly_label = [*range(1, calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[-1]+1, 1)]
        monthly_data_items = [database.fetch_data(sql_commands.get_items_daily_sales_sp, (f'2023-07-{s}',))[0][0] or 0 for s in monthly_label]
        monthly_data_service = [database.fetch_data(sql_commands.get_services_daily_sales_sp, (f'2023-07-{s}',))[0][0] or 0 for s in monthly_label]

        yearly_data_items = [database.fetch_data(sql_commands.get_items_monthly_sales_sp, (s, datetime.datetime.year))[0][0] or 0 for s in self.months]
        yearly_data_service = [database.fetch_data(sql_commands.get_services_monthly_sales_sp, (s, datetime.datetime.year))[0][0] or 0 for s in self.months]

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row =1, column =0, sticky = 'nsew',padx=width*0.005, pady=height*0.005)

        def report_menu_callback(report_type):
            if "Daily" in report_type:
                self.monthly_graph.grid_forget()
                self.month_option.pack_forget()
                self.year_option.pack_forget()
                self.yearly_graph.grid_forget()
                self.daily_data_view.pack()
                self.monthly_data_view.pack_forget()
                self.yearly_data_view.pack_forget()
                self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.date_selected_label.pack(side="left", padx=(0, width*0.005))
                self.show_calendar.pack(side="left",  padx=(0, width*0.005))

            elif "Monthly" in report_type:
                self.date_selected_label.pack_forget()
                self.show_calendar.pack_forget()
                self.daily_graph.pack_forget()
                self.daily_data_view.pack_forget()
                self.yearly_graph.grid_forget()
                self.yearly_data_view.pack_forget()
                self.monthly_data_view.pack()
                self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.month_option.pack(side="left", padx=(0, width*0.005))
                self.year_option.pack(side="left", padx=(0, width*0.005))

            elif "Yearly" in report_type:
                self.date_selected_label.pack_forget()
                self.show_calendar.pack_forget()
                self.month_option.pack_forget()
                self.daily_graph.pack_forget()
                self.daily_data_view.pack_forget()
                self.monthly_data_view.pack_forget()
                self.yearly_data_view.pack()
                self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
                self.year_option.pack(side="left", padx=(0, width*0.005))
            self.update_graphs()

        def set_date():
            cctk.tk_calendar(self.date_selected_label,"%s", date_format="word", max_date = datetime.date.today(),
                             set_date_callback= self.update_graphs,
                             date_select_default= datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y'))

        operational_year = [str(s[0]) for s in database.fetch_data(sql_commands.get_active_year_transaction)] or [str(datetime.datetime.now().year)]
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)]


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
        self.sales_report_label = ctk.CTkLabel(self.sales_report_button, text="SALES REPORT", text_color="white", font=("DM Sans Medium", 14))
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
        self.inventory_report_label = ctk.CTkLabel(self.inventory_report_button, text="INVENTORY REPORT", text_color="white", font=("DM Sans Medium", 14))
        self.inventory_report_label.pack(side="left")
        self.inventory_report_button.grid()
        self.inventory_report_button.update_children()

        self.button_manager = cctku.button_manager([self.sales_report_button, self.inventory_report_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        
        
        '''SALES REPORT'''
        self.report_option_var = ctk.StringVar(value="Daily Report")
        
        self.top_con_frame = ctk.CTkFrame(self.sales_report_frame, fg_color="transparent")
        self.top_con_frame.grid(row=0, column=0, sticky="nsew", pady=(height*0.005,0) )

        self.sales_report_top = ctk.CTkFrame(self.top_con_frame, fg_color=Color.White_Platinum, height=height*0.0575)
        self.sales_report_top.pack(side="left", fill="y")
        
        self.report_type_menu = ctk.CTkOptionMenu(self.sales_report_top, values=["Daily Report", "Monthly Report", "Yearly Report"], variable=self.report_option_var,anchor="center",
                                                  font=("DM Sans Medium",14), height=height*0.045, width=width*0.135,
                                                  command= report_menu_callback)
        self.report_type_menu.pack(side="left", padx=(width*0.003, width*0.005))

        self.date_selected_label = ctk.CTkLabel(self.sales_report_top, text=f"{date.today().strftime('%B %d, %Y')}", fg_color=Color.White_Color[3], corner_radius=5, height=height*0.045, font=("DM Sans Medium",14),
                                                width=width*0.125)
        self.date_selected_label.pack(side="left", padx=(0, width*0.005))

        self.show_calendar = ctk.CTkButton(self.sales_report_top, text="", image=self.calendar_icon, height=height*0.045, width=width*0.025, command=set_date)
        self.show_calendar.pack(side="left",  padx=(0, width*0.0025))

        """ self.refresh_btn = ctk.CTkButton(self.sales_report_frame, text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command= lambda: self.update_graphs(True))
        self.refresh_btn.grid(row=0, column=1, sticky="w",  padx=(width*0.0025), pady=(height*0.005,0)) """
        
        self.show_gen_report = ctk.CTkButton(self.top_con_frame, image=self.generate_report_icon, width=width*0.125,  text="Generate Report", height=height*0.0575, font=("DM Sans Medium", 14),
                                             command = lambda: self.save_as_popup.place(relx = .5, rely = .5, anchor = 'c', default_config = self.report_type_menu.get()))
        self.show_gen_report.pack(side="right")
        #generating reports end

        self.month_option = ctk.CTkOptionMenu(self.sales_report_top, values= self.months, anchor="center", width=width*0.1, font=("DM Sans Medium",14), height=height*0.045, command= self.update_graphs)
        self.month_option.set(f"{date.today().strftime('%B')}")
        self.year_option = ctk.CTkOptionMenu(self.sales_report_top, values=operational_year, width=width*0.075, font=("DM Sans Medium",14), height=height*0.045, anchor="center", command= self.update_graphs)
        self.year_option.set(f"{date.today().strftime('%Y')}")

        self.daily_graph = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum)
        self.daily_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)
        self.daily_graph.grid_columnconfigure((3), weight=2)
        self.daily_graph.grid_rowconfigure((0), weight=1)

        self.sales_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color=Color.White_Platinum)
        self.sales_daily_graph.grid(row=0, column= 0,columnspan=3, sticky="nsew",  padx=(width*0.005,0), pady=(height*0.01))

        self.items_total = ctk.CTkLabel(self.daily_graph,  text=f"Item:        {format_price(self.data[0])}", corner_radius=5, fg_color=Color.White_Lotion,  font=("DM Sans Medium",14), height=height*0.05)
        self.items_total.grid(row=1, column=0, sticky="nsew", padx=(width*0.005,0), pady=(0,height*0.007))
        self.service_total = ctk.CTkLabel(self.daily_graph,text=f"Services     {format_price(self.data[1])}", corner_radius=5, fg_color=Color.White_Lotion,  font=("DM Sans Medium",14), height=height*0.05)
        self.service_total.grid(row=1, column=1, sticky="nsew",padx=(width*0.005), pady=(0,height*0.007))
        self.income_total = ctk.CTkLabel(self.daily_graph,text=f"Total    {format_price(self.data[0] + self.data[1])}", corner_radius=5, fg_color=Color.White_Lotion,  font=("DM Sans Medium",14), height=height*0.05)
        self.income_total.grid(row=1, column=2, sticky="nsew", pady=(0,height*0.007))

        self.bars_daily_graph = ctk.CTkFrame(self.daily_graph, fg_color=Color.White_Platinum, height=height*0.35)
        self.bars_daily_graph.grid(row=0, column= 3, sticky="nsew", padx=(width*0.005), pady=(height*0.01,0))
        self.bars_daily_graph.pack_propagate(0)

        self.data_frame = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum, corner_radius=0, height=height*0.35)
        self.data_frame.grid(row=2, column=0, sticky="nsew", columnspan = 2,pady=(0, height*0.0075))

        self.daily_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.8, height=height *0.4,
                                           column_format=f'/No:{int(width*0.025)}-#c/OR:{int(width*0.095)}-tc/Client:x-tl/Service:{int(width*0.185)}-tc/Item:{int(width*0.185)}-tr/Total:{int(width*0.125)}-tl!30!30')
        self.daily_data_view.pack()


        self.monthly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum)
        self.monthly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.monthly_data_view = cctk.cctkTreeView(self.data_frame, width=width*0.8, height=height *0.5,
                                           column_format=f"/No:{int(width*.025)}-#c/Date:x-tl/Item:{int(width*.2)}-tr/Service:{int(width*.2)}-tr/Total:{int(width*.1)}-tc!30!30")
        self.monthly_data_view.pack()

        self.monthly_vbar_canvas = self.show_bar(self.monthly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,Color.White_Platinum], label=monthly_label)
        self.monthly_vbar_canvas.get_tk_widget().pack(pady=(10))

        self.yearly_graph = ctk.CTkFrame(self.sales_report_frame, fg_color=Color.White_Platinum)
        self.yearly_graph.grid(row=1, column=0, sticky="nsew", columnspan=2, pady=height*0.0075)

        self.yearly_data_view = cctk.cctkTreeView(self.data_frame,  width=width*0.8, height=height *0.5,
                                           column_format=f"/No:{int(width*.025)}-#c/Month:x-tl/Item:{int(width*.2)}-tr/Service:{int(width*.2)}-tr/Total:{int(width*.1)}-tc!30!30")
        self.yearly_data_view.pack()

        self.yearly_vbar_canvas = self.show_bar(self.yearly_graph, data_item=yearly_data_items, data_service=yearly_data_service, info=[width*0.01,height*0.005,Color.White_Platinum], label=self.months)
        self.yearly_vbar_canvas.get_tk_widget().pack(pady=(10))
        report_menu_callback("Daily")

        #region: inv rep
        '''INVENTORY REPORT'''
        """  self.search_frame = ctk.CTkFrame(self.inventory_report_frame,width=width*0.3, height = height*0.05, fg_color=Color.White_Platinum)
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.0025), pady=(height*0.005,0))
        self.search_frame.pack_propagate(0)

        ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
        self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0,font=("Arial", 14), text_color="black", fg_color=Color.White_Color[3])
        self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1) """

        self.rep_refresh_btn = ctk.CTkButton(self.inventory_report_frame, text="", width=width*0.03, height = height*0.0575, image=self.refresh_icon, fg_color="#83BD75")
        self.rep_refresh_btn.grid(row=0, column=1, sticky="w", pady=(height*0.005), padx=(width*0.005))
        
        self.generate_rep_btn = ctk.CTkButton(self.inventory_report_frame,  image=self.generate_report_icon, width=width*0.175,  text="Generate Inventory Report", height=height*0.0575, font=("DM Sans Medium", 14),
                                              command = lambda: self.save_as_inventory_rep_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.generate_rep_btn.grid(row=0, column=0, sticky="w", pady=(height*0.005))

        self.bought_item_con_col = None

        self.rep_treeview_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="transparent")
        self.rep_treeview_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=(width*0.0025), pady=(height*0.005,0))

        self.inventory_rep_treeview = cctk.cctkTreeView(self.rep_treeview_frame, width=width*0.8, height=height *0.8,
                                           column_format=f"/No:{int(width*.025)}-#c/ItemName:x-tl/InitialStock:{int(width*.2)}-tr/CurrentStock:{int(width*.2)}-tr!30!30",
                                           conditional_colors= self.bought_item_con_col)
        self.inventory_rep_treeview.pack()
        
        self.update_invetory_graph()
        self.update_invetory_graph()
        #endregion

        self.save_as_popup = save_as_popup.show_popup(self, (width , height))
        self.save_as_inventory_rep_popup = save_as_popup.show_popup_inventory(self, (width, height))
        load_main_frame(0)

    def update_invetory_graph(self):
        current_stock = database.fetch_data(sql_commands.get_current_stock_group_by_name)
        bought_item = database.fetch_data(sql_commands.get_all_bought_items_group_by_name)
        bought_item_dict = {s[0]: s[1] for s in bought_item}
        bought_item_con_col = {1: {s[0]: 'blue' for s in bought_item}}

        inventory_report_data = [(s[0], s[1] + (0 if s[0] not in bought_item_dict else bought_item_dict[s[0]]), s[1]) for s in current_stock]
        self.inventory_rep_treeview._conditional_colors = bought_item_con_col
        self.inventory_rep_treeview.update_table(inventory_report_data)


    def show_pie(self, data = None):
        if(self.daily_pie_canvas is not None):
            self.daily_pie_canvas.get_tk_widget().destroy()
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                    float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)] if data is None else data
        height = self.info[1]
        width =self.info[0]
        fg_color = self.info[2]

        data = self.data if self.data[0] + self.data[1] > 0 else [0,1]

        label = self.label
        pie_figure= Figure(figsize=(width, height), dpi=100)
        pie_figure.set_facecolor(fg_color)
        ax =pie_figure.add_subplot(111)
        ax.pie(data, labels=label, autopct='%1.1f%%', startangle=90,counterclock=0,
                textprops={'fontsize':12, 'color':"black", 'family':'monospace'}, colors=[Color.Light_Green,Color.Red_Tulip])

        self.daily_pie_canvas = FigureCanvasTkAgg(pie_figure, self.sales_daily_graph,)
        self.daily_pie_canvas.draw()
        self.daily_pie_canvas.get_tk_widget().pack()

    def show_hbar(self, data = None):
        if self.daily_hbar_canvas is not None:
            self.daily_hbar_canvas.get_tk_widget().destroy()
        self.data =[float(database.fetch_data(sql_commands.get_items_daily_sales)[0][0] or 0),
                float(database.fetch_data(sql_commands.get_services_daily_sales)[0][0] or 0)] if data is None else data

        height = self.info[1]
        width =self.info[0]
        fg_color = self.info[2]

        #data = self.data if self.data[0] + self.data[1] > 0 else [0,1]
        label = self.label

        bar_figure= Figure(figsize=(width, height), dpi=100)
        bar_figure.set_facecolor(fg_color)
        ax =bar_figure.add_subplot(111)
        ax.barh(label, self.data, align='center',  color=[Color.Light_Green,Color.Red_Tulip])
        #ax.set_xlabel("Income")
        self.daily_hbar_canvas = FigureCanvasTkAgg(bar_figure, self.bars_daily_graph)
        self.daily_hbar_canvas.draw()
        self.daily_hbar_canvas.get_tk_widget().pack()

    def show_bar(self, master, data_service, data_item, info=[], label=[]):
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
        #canvas.draw()
        canvas.get_tk_widget().pack(pady=(10))
        return canvas
    
    def update_graphs(self, force_reload: bool = False):
        force_reload = str(force_reload) == 'True'
        #as some of the caller of the function return their value, this will recheck the bool of the argument

        if 'Daily' in self.report_option_var.get():
            if not self.data_loading_manager[0] or self.date_selected_label._text != self.previous_date or force_reload:
                date = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%Y-%m-%d')
                self.data = [float(database.fetch_data(sql_commands.get_items_daily_sales_sp, (date,))[0][0] or 0),
                            float(database.fetch_data(sql_commands.get_services_daily_sales_sp, (date,))[0][0] or 0)]
                self.show_pie(self.data)
                self.show_hbar(self.data)
                self.items_total.configure(text=f"Item:        {format_price(self.data[0])}")
                self.service_total.configure(text=f"Services:        {format_price(self.data[1])}")
                self.income_total.configure(text=f"Total:        {format_price(self.data[0]+self.data[1])}")
                #self.daily_data_view.update_table(self.data) for adding data in the bottom treeview

                self.previous_date = self.date_selected_label._text
                self.data_loading_manager[0] = True
                self.daily_data_view.update_table(database.fetch_data(sql_commands.daily_report_treeview_data, (date, )))

        if 'Monthly' in self.report_option_var.get():
            if not self.data_loading_manager[1] or (self.year_option.get()+self.month_option.get()) != self.previous_year+self.previous_month or force_reload:
                m = datetime.datetime.strptime(self.month_option.get(), '%B').strftime('%m')
                y = self.year_option.get()
                monthly_label = [*range(1, calendar.monthrange(datetime.datetime.now().year, int(m))[-1]+1, 1)]
                monthly_data_items = [database.fetch_data(sql_commands.get_items_daily_sales_sp, (f'{y}-{m}-{s}',))[0][0] or 0 for s in monthly_label]
                monthly_data_service = [database.fetch_data(sql_commands.get_services_daily_sales_sp, (f'{y}-{m}-{s}',))[0][0] or 0 for s in monthly_label]

                self.monthly_vbar_canvas.get_tk_widget().destroy()
                self.monthly_vbar_canvas = self.show_bar(self.monthly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,Color.White_Platinum], label=monthly_label)
                self.monthly_vbar_canvas.get_tk_widget().pack()

                self.data_loading_manager[1] = True
                self.previous_month = self.month_option.get()
                self.previous_year = self.year_option.get()
                self.monthly_data_view.update_table(database.fetch_data(sql_commands.monthly_report_treeview_data, (m, y)))

        if 'Yearly' in self.report_option_var.get():
            if not self.data_loading_manager[2] or self.year_option.get() != self.previous_year or force_reload:
                y = self.year_option.get()

                monthly_data_items = [database.fetch_data(sql_commands.get_items_monthly_sales_sp, (self.months.index(s)+1, y))[0][0] or 0 for s in self.months]
                monthly_data_service = [database.fetch_data(sql_commands.get_services_monthly_sales_sp, (self.months.index(s)+1, y))[0][0] or 0 for s in self.months]

                self.yearly_vbar_canvas.get_tk_widget().destroy()
                self.yearly_vbar_canvas = self.show_bar(self.yearly_graph, data_item=monthly_data_items, data_service=monthly_data_service, info=[width*0.0175,height*0.005,Color.White_Platinum], label=self.months)
                self.yearly_vbar_canvas.get_tk_widget().pack()

                self.data_loading_manager[2] = True
                self.previous_year = self.year_option.get()
                self.yearly_data_view.update_table(database.fetch_data(sql_commands.yearly_report_treeview_data, (y, )))
        #set the previous selection to avoid repeating load

    def graphs_need_upgrade(self):
        self.data_loading_manager = [False for _ in range(3)]
        self.update_graphs(True)

class user_setting_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        selected_color = Color.Blue_Yale
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
        self.accounts_icon = ctk.CTkImage(light_image=Image.open("image/accounts.png"), size=(24,24))
        self.account_creation_icon = ctk.CTkImage(light_image = Image.open("image/create_acc.png"), size=(24,24))
        self.roles_icon = ctk.CTkImage(light_image = Image.open("image/role.png"), size=(24,24))
        self.deactivated_icon = ctk.CTkImage(light_image = Image.open("image/deact.png"), size=(24,24))

        '''TAB SETUP'''
        self.base_frame = ctk.CTkFrame(self, corner_radius=0,fg_color=Color.White_Lotion)
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(0, weight=1)

        self.account_base_frame = acc_creation.accounts_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)
        self.acc_creation_frame = acc_creation.creation_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)
        self.role_account_frame = acc_creation.roles_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)
        self.deactivated_frame = acc_creation.deactivated_frame(self.base_frame, width=width, height=height, fg_color=Color.White_Lotion, corner_radius=0)

        self.report_frames=[self.account_base_frame, self.acc_creation_frame, self.role_account_frame, self.deactivated_frame]
        self.active_report = None

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.grid_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.grid(row=0, column=0, sticky="nsew")

        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(4, weight=1)
        
        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=6, sticky="nsew")
        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15), fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=5, sticky="n")

        '''ACCOUNTS BUTTON TAB'''
        self.accounts_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.accounts_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.accounts_button.configure(command=partial(load_main_frame, 0))
        self.account_tab_icon = ctk.CTkLabel(self.accounts_button, text="",image=self.accounts_icon)
        self.account_tab_icon.pack(side="left", padx=(width*0.01,width*0.0025))
        self.accounts_label = ctk.CTkLabel(self.accounts_button, text="ACCOUNTS", text_color="white",font=('DM Sans Medium', 14))
        self.accounts_label.pack(side="left")
        self.accounts_button.grid()
        self.accounts_button.update_children()
        
        '''ACCOUNT CREATION TAB'''
        self.account_creation_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125, fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.account_creation_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.account_creation_button.configure(command=partial(load_main_frame, 1))
        self.account_creation_tab_icon = ctk.CTkLabel(self.account_creation_button, text="",image=self.account_creation_icon)
        self.account_creation_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.account_creation_label = ctk.CTkLabel(self.account_creation_button, text="CREATION", text_color="white",font=('DM Sans Medium', 14))
        self.account_creation_label.pack(side="left")
        self.account_creation_button.grid()
        self.account_creation_button.update_children()

        '''ROLES CREATION TAB'''
        self.roles_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.roles_button.grid(row=0, column=2, sticky="s", padx=(0,width*0.0025), pady=0)
        self.roles_button.configure(command=partial(load_main_frame, 2))
        self.roles_tab_icon = ctk.CTkLabel(self.roles_button, text="",image=self.roles_icon)
        self.roles_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.roles_label = ctk.CTkLabel(self.roles_button, text="ROLES", text_color="white",font=('DM Sans Medium', 14))
        self.roles_label.pack(side="left")
        self.roles_button.grid()
        self.roles_button.update_children()

        '''DEACTIVATED TAB'''
        self.deactivated_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.135, fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)
        self.deactivated_button.grid(row=0, column=3, sticky="s", padx=(0,width*0.0025), pady=0)
        self.deactivated_button.configure(command=partial(load_main_frame, 3))
        self.deactivated_tab_icon = ctk.CTkLabel(self.deactivated_button, text="",image=self.deactivated_icon)
        self.deactivated_tab_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.deactivated_label = ctk.CTkLabel(self.deactivated_button, text="DEACTIVATED", text_color="white",font=('DM Sans Medium', 14))
        self.deactivated_label.pack(side="left")
        self.deactivated_button.grid()
        self.deactivated_button.update_children()

        self.button_manager = cctku.button_manager([self.accounts_button, self.account_creation_button, self.roles_button, self.deactivated_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        def update_staff_acc():
            role_values = []
            for i in range(len(self.changeFrame.access_lvls)):
                role_values.append(self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].get())
            role_values = tuple(role_values) + (self.changeFrame.usn_option.get(),)
            database.exec_nonquery([['UPDATE account_access_level SET Dashboard = ?, Transaction = ?,\
                                      Services = ?, Sales = ?, Inventory = ?, Pet_Info = ?, Report = ?,\
                                      User = ?, Action = ? Where usn = ?', role_values]])
            #implement the job pos change here

        '''def set_checkBox_accessess(data:list, e:any = None):
            for i in range(len(self.changeFrame.access_lvls)):
                if data[i+2] == 1:
                    self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].configure(state = ctk.NORMAL)
                    if(active_access[i+1] == 1):
                        self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].select(False)
                    else:
                        self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].deselect(False)
                else:
                    self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].deselect(False)
                    self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].configure(state = ctk.DISABLED)'''
        #TBA: proceed command config needed

        def set_checkBox(e:any = None):
            self.changeFrame.accept_button.configure(state = ctk.NORMAL)
            self.changeFrame.selected_role_option.configure(state = ctk.NORMAL, values = [s[0] for s in database.fetch_data(sql_commands.get_all_position_titles)])
            job_pos = database.fetch_data('SELECT job_position FROM acc_info WHERE usn = ?', (self.changeFrame.usn_option.get(),))[0][0]
            data = database.fetch_data('SELECT * FROM user_level_access WHERE title = ?', (job_pos,))[0]
            active_access = database.fetch_data('Select * FROM account_access_level WHERE usn = ?', (self.changeFrame.usn_option.get(),))[0]
            self.changeFrame.selected_role_option.set(job_pos)
            for i in range(len(self.changeFrame.access_lvls)):
                if data[i+2] == 1:
                    self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].configure(state = ctk.NORMAL)
                    if(active_access[i+1] == 1):
                        self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].select(False)
                    else:
                        self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].deselect(False)
                else:
                    self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].deselect(False)
                    self.changeFrame.check_boxes[self.changeFrame.access_lvls[i]].configure(state = ctk.DISABLED)

        """

        self.creationFrame = acc_creation.creation_frame(self.acc_creation_frame, width * .85, height * .82, fg_color= 'white', corner_radius=5)
        self.creationFrame.grid(row=1, column=1, sticky="w")

        self.rolesFrame = acc_creation.roles_frame(self.roles_frame, width * .85, height * .82, fg_color= 'white', corner_radius=5)
        self.rolesFrame.grid(row=1, column=1, sticky="w")

        self.deactivatedFrame = acc_creation.deactivated_frame(self.deactivated_frame, width * .85, height * .82, fg_color= 'white', corner_radius=5)
        self.deactivatedFrame.grid(row=1, column=1, sticky="w")
        #self.changeFrame.usn_option.configure(values = [s [0] for s in database.fetch_data('SELECT usn from acc_cred')], command = set_checkBox)
        #self.changeFrame.accept_button.configure(state = ctk.DISABLED, command = update_staff_acc);

        #account creation tab
        #account creation frame
        self.box_frame = ctk.CTkFrame(self.inventory_report_frame,fg_color="white")
        self.box_frame.pack(fill=tk.BOTH, expand=True)

        def create_new_acc():
            password1 = encrypt.pass_encrypt(self.acc_create.name_entry.get())
            aula = (self.acc_create.name_entry.get(),)
            temp = []
            for i in range(len(self.acc_create.access_lvls)):
                temp.append(self.acc_create.check_boxes[self.acc_create.access_lvls[i]].get())
            aula = aula + tuple(temp);
            database.exec_nonquery([['INSERT INTO acc_cred VALUES(?, ?, ?, NULL)',(self.acc_create.name_entry.get(), password1['pass'], password1['salt'])],
                                    ['INSERT INTO acc_info VALUES(?, ?, ?)', (self.acc_create.name_entry.get(), self.acc_create.name_entry.get(), self.acc_create.position_option.get())],
                                    ['INSERT INTO account_access_level VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', aula]])
            #add_new_acc()
            #clear_acc_creation_fields()
            #get_staff_name()
            #refresh_staff_names()

        '''ACCOUNT CREATION: START'''
        
        '''temporary implementation'''
        
        def enable_checkboxes(e:any = None):
            data = database.fetch_data('SELECT * FROM user_level_access WHERE Title = ?', (self.acc_create.position_option.get(),))[0]

            self.acc_create.access_lvls
            self.acc_create.check_boxes
            for i in range(len(self.acc_create.access_lvls)):
                if data[i+2] == 1:
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].configure(state = ctk.NORMAL) 
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].select(False)
                else:
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].deselect(False)
                    self.acc_create.check_boxes[self.acc_create.access_lvls[i]].configure(state = ctk.DISABLED)
                #self.acc_create.check_boxes[self.acc_create.access_lvls[i]].configure(value = data[i + 2])

        self.acc_create = acc_creation.creation_frame(self.box_frame, width * .85, height * .82, 5, fg_color= 'light grey')
        self.acc_create.grid(row=1, column=1, sticky="w")
        '''
        roles_list = database.fetch_data('SELECT title FROM user_level_access')
        roles_list = [s[0] for s in roles_list]
        #roles = roles_list = [s[0] for s in roles_list]
        self.acc_create.position_option.set('Select Position');
        self.acc_create.position_option.configure(values = roles_list, command = enable_checkboxes)

        self.acc_create.accept_button.configure(command = create_new_acc)
        ''' """
        load_main_frame(0)

class histlog_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        
        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
        self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
        self.histlog = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
        self.action = ctk.CTkImage(light_image=Image.open("image/patient.png"), size=(18,21))
        self.calendar = ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(17,18))

        self.base_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Color[3])
        self.base_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
        self.base_frame.grid_propagate(0)
        self.base_frame.grid_columnconfigure(0, weight=1)
        self.base_frame.grid_rowconfigure(1, weight=1)

        self.action_log_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])
        self.log_history_frame = ctk.CTkFrame(self.base_frame, fg_color=Color.White_Color[3])

        self.action_log_frame.grid_columnconfigure(2, weight=1)
        self.action_log_frame.grid_rowconfigure(1, weight=1)
        
        self.log_history_frame.grid_columnconfigure(2, weight=1)
        self.log_history_frame.grid_rowconfigure(1, weight=1)
        
        self.report_frames=[self.action_log_frame, self.log_history_frame]
        self.active_report = None
        
        self.grid_forget()
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        selected_color = Color.Blue_Yale

        def load_main_frame(cur_frame: int):
            if self.active_report is not None:
                self.active_report.pack_forget()
            self.active_report = self.report_frames[cur_frame]
            self.active_report.pack(fill="both", expand=1)
            
        self.top_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew" ,padx=(width*0.005),  pady=(height*0.01,0))
        self.top_frame.grid_columnconfigure(2, weight=1)

        ctk.CTkFrame(self.top_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

        self.date_label = ctk.CTkLabel(self.top_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 16),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=3, sticky="n")


        self.action_log_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.13,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.action_log_button.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
        self.action_log_button.configure(command=partial(load_main_frame, 0))
        self.action_log_icon = ctk.CTkLabel(self.action_log_button, text="",image=self.action)
        self.action_log_icon.pack(side="left", padx=(width*0.01,width*0.005)) 
        self.action_log_label = ctk.CTkLabel(self.action_log_button, text="ACTION HISTORY", text_color="white", font=("DM Sans Medium", 14))
        self.action_log_label.pack(side="left")
        self.action_log_button.grid()
        self.action_log_button.update_children()

        self.log_in_button = cctk.ctkButtonFrame(self.top_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                           fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

        self.log_in_button.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
        self.log_in_button.configure(command=partial(load_main_frame, 1))
        self.log_in_icon = ctk.CTkLabel(self.log_in_button, text="",image=self.histlog)
        self.log_in_icon.pack(side="left", padx=(width*0.01,width*0.005))
        self.log_in_label = ctk.CTkLabel(self.log_in_button, text="LOGIN HISTORY", text_color="white", font=("DM Sans Medium", 14))
        self.log_in_label.pack(side="left")
        self.log_in_button.grid()
        self.log_in_button.update_children()

        self.button_manager = cctku.button_manager([self.action_log_button, self.log_in_button], selected_color, False, 0)
        self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
        self.button_manager.click(self.button_manager._default_active, None)

        '''ACTION HISTORY - START'''
        
        self.sort_date_frame = ctk.CTkFrame(self.action_log_frame,width=width*0.25, height = height*0.055,fg_color=Color.Platinum)
        self.sort_date_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.sort_date_frame.pack_propagate(0)
        
        ctk.CTkLabel(self.sort_date_frame, text="Sort by Date:", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht).pack(side="left", padx=(width*0.01, width*0.001),pady=(height*0.01))
        self.date_sort_label = ctk.CTkLabel(self.sort_date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, corner_radius=5, fg_color=Color.White_Lotion)
        self.date_sort_label.pack(side="left", fill="both", expand=1,pady=(height*0.0065),padx=(width*0.001) )
        
        self.date_button = ctk.CTkButton(self.sort_date_frame, text="", height=height*0.045, width=width*0.025, image=self.calendar,
                                         command=lambda: cctk.tk_calendar(self.date_sort_label, "%s", date_format="word", max_date=datetime.datetime.now(), set_date_callback= self.update_action_content))
        self.date_button.pack(side="left",padx=(0,width*0.005),pady=(height*0.0065))
        
        self.sort_role_frame = ctk.CTkFrame(self.action_log_frame, width=width*0.1,  height = height*0.055,fg_color=Color.Platinum)
        self.sort_role_frame.grid(row=0, column=1, sticky="nsew", padx=(0,width*0.005), pady=(height*0.01))
        
        roles = database.fetch_data('SELECT DISTINCT TITLE FROM user_level_access')
        roles = [s[0] for s in roles]

        self.sort_role_option = ctk.CTkOptionMenu(self.sort_role_frame, values= roles, anchor="center", font=("DM Sans Medium", 12), width=width*0.1, dropdown_fg_color=Color.White_AntiFlash,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts,
                                                 command= self.update_action_content)
        self.sort_role_option.pack(fill="both", expand=1,pady=(height*0.0065),padx=(width*0.0045))
        
        self.refresh_btn = ctk.CTkButton(self.action_log_frame,text="", width=width*0.03, height = height*0.055, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=2, sticky="w",padx=(0,width*0.005), pady=(height*0.01))
        
        '''Table'''
        self.action_table_frame = ctk.CTkFrame(self.action_log_frame, fg_color=Color.Platinum)
        self.action_table_frame.grid(row=1, column=0,padx=(width*0.005), pady=(0,height*0.01), sticky="nsew", columnspan=3)
        self.action_table_frame.grid_columnconfigure(0, weight=1)
        self.action_table_frame.grid_rowconfigure(0, weight=1)
        
        self.action_table_style = ttk.Style()
        self.action_table_style.theme_use("clam")
        self.action_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
        self.action_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
        self.action_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
        self.action_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
        self.columns = ("rec_no", "username","role","action","time")
        self.column_names = ("No", "Username","Type", "Description", "Time")
        
            
        self.action_tree = ttk.Treeview(self.action_table_frame, columns=self.columns, show="headings",)
        
        for i in range(len(self.columns)):
            self.action_tree.heading(f"{self.columns[i]}", text=f"{self.column_names[i]}")

        self.action_tree.column("rec_no", width=int(width*0.001),anchor="w")
        self.action_tree.column("username", width=int(width*0.15), anchor="w")
        self.action_tree.column("role", width=int(width*0.1), anchor="w")
        self.action_tree.column("action", width=int(width*0.45), anchor="w")
        self.action_tree.column("time", width=int(width*0.15), anchor="c")
            
        self.action_tree.tag_configure("odd",background=Color.White_AntiFlash)
        self.action_tree.tag_configure("even",background=Color.White_Ghost)
            
        self.action_tree.grid(row=0, column=0, sticky="nsew")
            
        self.y_scrollbar = ttk.Scrollbar(self.action_table_frame, orient=tk.VERTICAL, command=self.action_tree.yview)
        self.action_tree.configure(yscroll=self.y_scrollbar.set)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")

        """Table End"""
        
        '''ACTION HISTORY - END'''
        
        '''LOGIN HISTORY - START'''
        
        self.sort_date_frame = ctk.CTkFrame(self.log_history_frame,width=width*0.25, height = height*0.055,fg_color=Color.Platinum)
        self.sort_date_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
        self.sort_date_frame.pack_propagate(0)
        
        ctk.CTkLabel(self.sort_date_frame, text="Sort by Date:", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht).pack(side="left", padx=(width*0.01, width*0.001),pady=(height*0.01))
        self.login_date_sort_label = ctk.CTkLabel(self.sort_date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, corner_radius=5, fg_color=Color.White_Lotion)
        self.login_date_sort_label.pack(side="left", fill="both", expand=1,pady=(height*0.0065),padx=(width*0.001) )
        
        self.date_button_log = ctk.CTkButton(self.sort_date_frame, text="", height=height*0.045, width=width*0.025, image=self.calendar,
                                         command=lambda: cctk.tk_calendar(self.login_date_sort_label, "%s", date_format="word", max_date=datetime.datetime.now(),
                                                                          set_date_callback= self.update_login_audit))
        self.date_button_log.pack(side="left",padx=(0,width*0.005),pady=(height*0.0065))
        
        self.refresh_btn = ctk.CTkButton(self.log_history_frame,text="", width=width*0.03, height = height*0.055, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=1, sticky="w",padx=(0,width*0.005), pady=(height*0.01))
        
        '''Table'''
        
        self.login_table_frame = ctk.CTkFrame(self.log_history_frame, fg_color=Color.Platinum)
        self.login_table_frame.grid(row=1, column=0,padx=(width*0.005), pady=(0,height*0.01), sticky="nsew", columnspan=3)
        self.login_table_frame.grid_columnconfigure(0, weight=1)
        self.login_table_frame.grid_rowconfigure(0, weight=1)
        
        self.login_table_style = ttk.Style()
        self.login_table_style.theme_use("clam")
        self.login_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
        self.login_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
        self.login_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
        self.login_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
        self.columns = ("rec_no", "username","role","date","time_in","time_out")
        self.column_names = ("No", "Username","Role", "Date", "TimeIn", "TimeOut")
        
            
        self.log_audit_tree = ttk.Treeview(self.login_table_frame, columns=self.columns, show="headings",)
           
        for i in range(len(self.columns)):
            self.log_audit_tree.heading(f"{self.columns[i]}", text=f"{self.column_names[i]}")

        self.log_audit_tree.column("rec_no", width=int(width*0.01),anchor="w")
        self.log_audit_tree.column("username", width=int(width*0.35), anchor="w")
        self.log_audit_tree.column("role", width=int(width*0.15), anchor="w")
        self.log_audit_tree.column("date", width=int(width*0.15), anchor="c")
        self.log_audit_tree.column("time_in", width=int(width*0.15), anchor="c")
        self.log_audit_tree.column("time_out", width=int(width*0.15), anchor="c")
            
        self.log_audit_tree.tag_configure("odd",background=Color.White_AntiFlash)
        self.log_audit_tree.tag_configure("even",background=Color.White_Ghost)
            
        self.log_audit_tree.grid(row=0, column=0, sticky="nsew")
            
        self.y_scrollbar = ttk.Scrollbar(self.login_table_frame, orient=tk.VERTICAL, command=self.log_audit_tree.yview)
        self.log_audit_tree.configure(yscroll=self.y_scrollbar.set)
        self.y_scrollbar.grid(row=0, column=1, sticky="ns")
        """Table End"""
        
        '''LOGIN HISTORY - END'''        
        
        self.update_login_audit()
        self.update_action_content()
        load_main_frame(0)
    
    def update_action_content(self, e: any = None):
        for i in self.action_tree.get_children():
            self.action_tree.delete(i)
        temp = database.fetch_data(sql_commands.get_raw_action_history, (datetime.datetime.strptime(self.date_sort_label._text, '%B %d, %Y').strftime('%Y-%m-%d'), self.sort_role_option.get()))
        modified_data = [(temp.index(s) + 1, s[0], s[1].capitalize(), decode_action(s[2]), s[3].strftime("%m/%d/%Y at %I:%M %p")) for s in temp]
        for i in range(len(modified_data)):
            if (i % 2) == 0:
                tag = "even"
            else:
                tag ="odd"
            self.action_tree.insert(parent='', index='end', iid=i, text="", values= modified_data[i], tags=tag )
    

    def update_login_audit(self, e: any = None):
        for i in self.log_audit_tree.get_children():
            self.log_audit_tree.delete(i)
        temp = database.fetch_data(sql_commands.get_log_history, (datetime.datetime.strptime(self.login_date_sort_label._text, '%B %d, %Y'), ))
        temp = [(s[0], s[1], s[2].strftime('%m/%d/%y'), s[3], s[4]) for s in temp]
        for i in range(len(temp)):
            if (i % 2) == 0:
                tag = "even"
            else:
                tag ="odd"
            self.log_audit_tree.insert(parent='', index='end', iid=i, text="", values= (i + 1, )+ temp[i], tags=tag )

dashboard(None, 'admin', datetime.datetime.now)
