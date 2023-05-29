import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
import datetime;
import _tkinter
import sql_commands
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
from popup import Inventory_popup, transaction_popups

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

        '''
        #makes the form full screen and removing the default tab bar
        datakey = database.fetch_data(f'SELECT {db.USERNAME} from {db.ACC_CRED} where {db.acc_cred.ENTRY_OTP} = ?', (entry_key, ))
        if not datakey or entry_key == None:
            messagebox.showwarning('Warning', 'Invalid entry method\ngo to log in instead')
            self.destroy()
            return
        else:
            global acc_info, date_logged
            date_logged = _date_logged;
            acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (datakey[0][0], ))
            acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (datakey[0][0], ))
            print(acc_cred)
            database.exec_nonquery([[f'UPDATE {db.ACC_CRED} SET {db.acc_cred.ENTRY_OTP} = NULL WHERE {db.USERNAME} = ?', (datakey[0][0], )]])
            del datakey
        #for preventing security breach through python code; enable it to test it

        '''
        global acc_info, acc_cred, date_logged
        date_logged = _date_logged;
        acc_info = database.fetch_data(f'SELECT * FROM {db.ACC_INFO} where {db.USERNAME} = ?', (entry_key, ))
        acc_cred = database.fetch_data(f'SELECT * FROM {db.ACC_CRED} where {db.USERNAME} = ?', (entry_key, ))
        #temporary for free access; disable it when testing the security breach prevention or deleting it if deploying the system
        self._master = master
        '''Fonts'''
        '''
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
        '''
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
        self.patient_button.configure(command=partial(load_main_frame, 'Patient', 5))
        self.patient_button.pack()
        self.patient_wbar = ctk.CTkLabel(self.patient_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.patient_wbar.pack(side="left")
        self.patient_icon = ctk.CTkLabel(self.patient_button,image=self.patient_icon, text="")
        self.patient_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.patient_label = ctk.CTkLabel(self.patient_button, text="Patient", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
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
        self.user_setting_button.configure(command=partial(load_main_frame, 'User Settings', 7))
        self.user_setting_button.pack()
        self.user_setting_wbar = ctk.CTkLabel(self.user_setting_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.user_setting_wbar.pack(side="left")
        self.user_setting_icon = ctk.CTkLabel(self.user_setting_button,image=self.user_setting_icon, text="")
        self.user_setting_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.user_setting_label = ctk.CTkLabel(self.user_setting_button, text="User Setttings", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.user_setting_label.pack(side="left")
        self.user_setting_button.pack()
        self.user_setting_button.update_children()


        self.histlog_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        #self.histlog_button.configure(command=partial(change_active_event, self.histlog_button, 8))
        self.histlog_button.configure(command=partial(load_main_frame, 'History Log', 8))
        self.histlog_button.pack()
        self.histlog_wbar = ctk.CTkLabel(self.histlog_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.histlog_wbar.pack(side="left")
        self.histlog_icon = ctk.CTkLabel(self.histlog_button,image=self.histlog_icon, text="")
        self.histlog_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.histlog_label = ctk.CTkLabel(self.histlog_button, text="History Log", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
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
        self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][1]).upper(), font=("Poppins Medium", 15))
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .005), 0), pady = (5,0))
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text=str(acc_info[0][2]).upper(), font=("Poppins Medium", 12))
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
        load_main_frame('Dashboard', 4)
        #change_active_event(self.db_button, 0)
        self.protocol("WM_DELETE_WINDOW", log_out)
        self.mainloop()

'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''main frames'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
class dashboard_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Chinese)
        self.data =[1457.75,4011.25]

        def show_pie(master, data):
            labels = ["Items", "Service"]


            data = data
            pie_figure= Figure(figsize=(income_frame_width*0.006,income_frame_height*0.013), dpi=100)
            pie_figure.set_facecolor(Color.White_Ghost)
            ax =pie_figure.add_subplot(111)
            ax.pie(data, autopct='%1.1f%%', startangle=0,counterclock=0, explode=(0.1,0), colors=[Color.Red_Tulip, Color.Light_Green],
                   textprops={'fontsize':18, 'color': Color.White_Ghost, 'family':'monospace', 'weight':'bold' },)
            ax.legend(labels, loc=8, ncol=2,prop={'family':"monospace", "size": 13}, labelcolor=Color.Blue_Maastricht, frameon=0)
            pie_figure.subplots_adjust(top=1,left=0,right=1, bottom=0)

            canvas = FigureCanvasTkAgg(pie_figure, master)
            canvas.draw()
            canvas.get_tk_widget().grid(row = 0, column=1, rowspan = 5)

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

        self.items_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.items_sales_frame.grid(row=2, column=0, sticky="nsew", padx=(income_frame_width*0.03), pady=(income_frame_height*0.05, income_frame_height*.015),)
        self.items_sales_frame.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.items_sales_frame, text="Items:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.items_sales_frame, text="₱000,000.00", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))

        self.services_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.services_sales_frame.grid(row=3, column=0, sticky="nsew", padx=(income_frame_width*0.03),pady=( income_frame_height*.015))
        self.services_sales_frame.pack_propagate(0)
        self.services_sales_label = ctk.CTkLabel(self.services_sales_frame, text="Services:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.services_sales_value = ctk.CTkLabel(self.services_sales_frame, text="₱000,000.00", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))

        self.total_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=income_frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.total_sales_frame.grid(row=4, column=0, sticky="nsew", padx=(income_frame_width*0.03),pady=(income_frame_height*.015,0))
        self.total_sales_frame.pack_propagate(0)
        self.total_sales_label = ctk.CTkLabel(self.total_sales_frame, text="Total:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(income_frame_width*.025,0))
        self.total_sales_value = ctk.CTkLabel(self.total_sales_frame, text="₱000,000.00", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,income_frame_width*.025))
        #Watermelon Pie
        show_pie(self.income_summary_frame, self.data)

        self.view_more_button = ctk.CTkButton(self.income_summary_frame, text='View More',width= income_frame_width*0.16, height=income_frame_height*0.06, font=('DM Sans Medium', 12), corner_radius=4, text_color=Color.Blue_Maastricht,
                                              fg_color=Color.White_AntiFlash,hover_color=Color.Platinum, command=lambda:print("Go To Report Section"))
        self.view_more_button.grid(row=5, column=1, sticky="e", padx=income_frame_width*0.02,pady=(0,income_frame_height*0.035))

        '''Inventory Stat Frame'''
        self.inventory_stat_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.inventory_stat_frame.grid_propagate(0)
        self.inventory_stat_frame.grid(row=1, column=4, columnspan=4, padx= (width*(.005) ,width * .01))
        self.inventory_stat_frame.grid_rowconfigure((1,2,3,4), weight=1)
        self.inventory_stat_frame.grid_columnconfigure(1, weight=1)

        inventory_frame_width, inventory_frame_height = self.inventory_stat_frame.cget('width'), self.inventory_stat_frame.cget('height')
        '''Inventory Stat Frame Contents'''
        self.inventory_stat_label = ctk.CTkLabel(self.inventory_stat_frame, text="Inventory Status", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht)
        self.inventory_stat_label.grid(row=0, column=1, sticky="w", padx=(inventory_frame_width*0.04,0),pady=(inventory_frame_height*0.04,inventory_frame_height*0.02))

        self.reorder_level_button  = cctk.ctkButtonFrame(self.inventory_stat_frame, height=inventory_frame_height*0.04, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum,corner_radius=5,cursor="hand2")
        self.reorder_level_button.configure(command=lambda: print("Show Items need reordering"))
        self.reorder_level_button.grid(row=1, column=1, sticky="nsew", padx=(inventory_frame_width*0.025 ),pady=(0,inventory_frame_height*0.02))
        self.reorder_label = ctk.CTkLabel(self.reorder_level_button, text="Reorder Items", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.reorder_label.pack(side="left", padx=(inventory_frame_width*0.04,0))
        self.reorder_light = ctk.CTkLabel(self.reorder_level_button, text="", height=inventory_frame_height*0.04, width=inventory_frame_width*0.03, corner_radius=8, fg_color=Color.Orange_Dandelion)
        self.reorder_light.pack(side="right", padx=(inventory_frame_width*0.025,inventory_frame_width*0.05))
        self.reorder_count = ctk.CTkLabel(self.reorder_level_button, text="8", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.reorder_count.pack(side="right")
        self.reorder_level_button.update_children()

        self.critical_level_button  = cctk.ctkButtonFrame(self.inventory_stat_frame, height=inventory_frame_height*0.04, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum,corner_radius=5,cursor="hand2")
        self.critical_level_button.configure(command=lambda: print("Show Items critical level"))
        self.critical_level_button.grid(row=2, column=1, sticky="nsew", padx=(inventory_frame_width*0.025 ),pady=(0,inventory_frame_height*0.02))
        self.critical_label = ctk.CTkLabel(self.critical_level_button, text="Critical Items", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.critical_label.pack(side="left", padx=(inventory_frame_width*0.04,0))
        self.critical_light = ctk.CTkLabel(self.critical_level_button, text="", height=inventory_frame_height*0.04, width=inventory_frame_width*0.03, corner_radius=8, fg_color=Color.Red_Pastel)
        self.critical_light.pack(side="right", padx=(inventory_frame_width*0.025,inventory_frame_width*0.05))
        self.critical_count = ctk.CTkLabel(self.critical_level_button, text="10", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.critical_count.pack(side="right")
        self.critical_level_button.update_children()

        self.nearly_expired_level_button  = cctk.ctkButtonFrame(self.inventory_stat_frame, height=inventory_frame_height*0.04, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum,corner_radius=5,cursor="hand2")
        self.nearly_expired_level_button.configure(command=lambda: print("Show nearly expired items"))
        self.nearly_expired_level_button.grid(row=3, column=1, sticky="nsew", padx=(inventory_frame_width*0.025 ),pady=(0, inventory_frame_height*0.02))
        self.nearly_expired_label = ctk.CTkLabel(self.nearly_expired_level_button, text="Nearly Expired Items", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.nearly_expired_label.pack(side="left", padx=(inventory_frame_width*0.04,0))
        self.nearly_expired_light = ctk.CTkLabel(self.nearly_expired_level_button, text="", height=inventory_frame_height*0.04, width=inventory_frame_width*0.03, corner_radius=8, fg_color=Color.Orange_Dandelion)
        self.nearly_expired_light.pack(side="right", padx=(inventory_frame_width*0.025,inventory_frame_width*0.05))
        self.nearly_expired_count = ctk.CTkLabel(self.nearly_expired_level_button, text="5", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.nearly_expired_count.pack(side="right")
        self.nearly_expired_level_button.update_children()

        self.expired_level_button  = cctk.ctkButtonFrame(self.inventory_stat_frame, height=inventory_frame_height*0.04, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum, corner_radius=5,cursor="hand2")
        self.expired_level_button.configure(command=lambda: print("Show expired items"))
        self.expired_level_button.grid(row=4, column=1, sticky="nsew", padx=(inventory_frame_width*0.025 ),pady=(0, inventory_frame_height*0.05))
        self.expired_label = ctk.CTkLabel(self.expired_level_button, text="Expired Items", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.expired_label.pack(side="left", padx=(inventory_frame_width*0.04,0))
        self.expired_light = ctk.CTkLabel(self.expired_level_button, text="", height=inventory_frame_height*0.04, width=inventory_frame_width*0.03, corner_radius=8, fg_color=Color.Red_Pastel)
        self.expired_light.pack(side="right", padx=(inventory_frame_width*0.025,inventory_frame_width*0.05))
        self.expired_count = ctk.CTkLabel(self.expired_level_button, text="3", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
        self.expired_count.pack(side="right")
        self.expired_level_button.update_children()

        self.sched_client_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.sched_client_frame.grid(row=2, column=0, columnspan=4, padx= (width*.01 ,width*(.005)), pady=(height*0.017))

        self.log_history_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.log_history_frame.grid(row=2, column=4, columnspan=4, padx= (width*(.005) ,width * .01), pady=(height*0.017))

class transaction_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        '''events'''

        def clear_without_verification():
            self.item_treeview.delete_all_data()
            self.final_total_value.configure(text = format_price(float(price_format_to_float(self.final_total_value._text)) - float(price_format_to_float(self.final_total_value._text))))
            self.item_total_value.configure(text = '0.00')

        def proceed():
            if price_format_to_float(self.final_total_value._text) == 0:
                messagebox.showerror('Unable to Proceed', 'No Item Listed')
                return
            self.show_transaction_proceed = transaction_popups.show_transaction_proceed(self, (width, height, (self.item_treeview, self.service_treeview), acc_cred[0]),
                                                                                        self.item_treeview._data, self.service_treeview._data,
                                                                                        price_format_to_float(self.final_total_value._text))
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

        self.service_treeview = cctk.cctkTreeView(self.service_frame, width=width*0.8, height=height*0.3,
                                                  column_format=f'/No:{int(width*.03)}-#c/ItemCode:{int(width*0.08)}-tc/ServiceName:x-tl/Patient:x-#l/Price:{int(width*.07)}-tr/Discount:{int(width*.08)}-tr/Total:{int(width*.08)}-tc/Action:{int(width*.05)}-bD!50!40',
                                                  double_click_command= lambda _: print('hello'))
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
        self.service_total_value = ctk.CTkLabel(self.service_total_frame, text="00,000,000.00", font=("DM Sans Medium", 14))
        self.service_total_value.pack(side="right", padx=(0, width*0.01))

        self.item_frame = ctk.CTkFrame(self, corner_radius=5, fg_color=Color.White_Ghost)
        self.item_frame.grid(row=2, column=0, columnspan=3, stick="nsew", padx=(width*0.005),pady=(height*0.005,height*0.01))
        self.item_frame.grid_columnconfigure(0, weight=1)
        self.item_frame.grid_rowconfigure(0, weight=1)

        self.item_treeview = cctk.cctkTreeView(self.item_frame, width=width*0.8, height=height*0.3,
                                               column_format=f'/No:{int(width*.03)}-#c/ItemCode:{int(width*0.08)}-tc/ItemName:x-tl/Price:{int(width*.07)}-tr/Quantity:{int(width*.1)}-id/Discount:{int(width*.08)}-tr/Total:{int(width*.08)}-tr/Action:{int(width*.05)}-bD!50!40')
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
        self.item_total_value = ctk.CTkLabel(self.item_total_frame, text="00,000,000.00", font=("DM Sans Medium", 14))
        self.item_total_value.pack(side="right", padx=(0, width*0.01))


        self.bottom_frame = ctk.CTkFrame(self,height=height*0.05, fg_color="#E0E0E0")
        self.bottom_frame.grid(row=3, column=0, columnspan=3, pady=(0,height*0.01), padx=(width*0.005),sticky="nsew")
        self.bottom_frame.pack_propagate(0)

        '''self.clear_all_button = ctk.CTkButton(self.bottom_frame, text="Clear All", fg_color="#EB455F", hover_color="#A6001A",
                                              cursor="hand2")
        self.clear_all_button.pack(side="left")'''

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
        self.show_services_list: ctk.CTkFrame = transaction_popups.show_services_list(self, (width, height, self.service_treeview))
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
        self.main_data = [(s[0], 'Alfredo', str(datetime.datetime.now().date()), format_price(float(s[2])), s[1]) for s in self.main_data]
        self.data_view = cctk.cctkTreeView(self, self.main_data, width * .8, height * .8,
                                           column_format='/No:75-#c/OR:75-tc/Client:x-tl/Date:175-tc/TotalPrice:125-tr/Cashier:125-tl/Actions:85-bD!50!30')
        self.data_view.pack(pady = (15, 0))

        self.grid_forget()

class inventory_frame(ctk.CTkFrame):
    global width, height, acc_cred, acc_info
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)

        self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

        '''events'''
        def update_tables(_ :any = None):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.data_view1.update_table(database.fetch_data(sql_commands.get_inventory_by_group, None))
            self.data_view2.update_table(database.fetch_data(sql_commands.get_inventory_by_expiry, None))
            self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

        def change_view(_: any = None):
            if self.view_by_selection.get() == 'View by Item':
                self.data_view1.pack(pady=(height*0.005,0))
                self.data_view2.pack_forget()
            else:
                self.data_view2.pack(pady=(height*0.005,0))
                self.data_view1.pack_forget()

        self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
        self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))

        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.search_frame = ctk.CTkFrame(self,width=width*0.3, height = height*0.05, fg_color=Color.White_Color[3])
        self.search_frame.grid(row=0, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))

        self.add_item_btn = ctk.CTkButton(self,width=width*0.08, height = height*0.05, text="Add Item",image=self.add_icon, font=("DM Sans Medium", 14),
                                          command= lambda : self.add_item_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.add_item_btn.grid(row=0, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

        self.refresh_btn = ctk.CTkButton(self,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
        self.refresh_btn.grid(row=0, column=2, sticky="w")

        self.view_by_selection = ctk.CTkOptionMenu(self, width=width*0.18, height = height*0.05, values=["View by Item", "View by Expiry"],
                                                   command=change_view )
        self.view_by_selection.set("View by Item")
        self.view_by_selection.grid(row=0, column=4, padx=(0,width*0.005))


        self.date_label = ctk.CTkLabel(self, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 15),
                                       fg_color=Color.White_Color[3], width=width*0.125, height = height*0.05, corner_radius=5)
        self.date_label.grid(row=0, column=5, padx=(0, width*0.005),  pady=(height*0.01), sticky="e")

        self.restock_btn = ctk.CTkButton(self, width=width*0.1, height = height*0.05, text="Record Stock", image=self.restock_icon, font=("DM Sans Medium", 14),
                                         command= lambda : self.restock_popup.place(relx = .5, rely = .5, anchor = 'c'))
        self.restock_btn.grid(row=2, column=5, pady=(height*0.01), sticky="e", padx=(0, width*0.005))
        self.grid_propagate(0)

        self.data_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3])
        self.data_frame.grid(row=1, column=0, columnspan=6,  padx=(width*0.005), sticky="nsew")

        self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.data_view1 = cctk.cctkTreeView(self.data_frame, self.data1, width= width * .8, height= height * .75,
                                           column_format=f'/No:{int(width*.025)}-#r/Name:x-tl/Stock:{int(width*.07)}-tr/Price:{int(width*.07)}-tr/NearestExpire:{int(width*.1)}-tc/Status:{int(width*.08)}-tl!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                           conditional_colors= {5: {'Reorder':'#ff7900', 'Critical':'red','Normal':'green', 'Out Of Stock': '#555555'}})
        self.data_view1.pack(pady=(height*0.005,0))

        self.data2 = database.fetch_data(sql_commands.get_inventory_by_expiry, None)
        self.data_view2 = cctk.cctkTreeView(self.data_frame, self.data2, width= width * .8, height= height * .75,
                                           column_format=f'/No:{int(width*.025)}-#r/Name:x-tl/Stock:{int(width*.07)}-tr/Price:{int(width*.07)}-tr/ExpirationDate:{int(width*.1)}-tc/Status:{int(width*.08)}-tl!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                           conditional_colors= {5: {'Nearly Expire':'#ff7900', 'Expired':'red','Safe':'green'}})


        #self.refresh_btn.configure(command = lambda: self.data_view.update_table(database.fetch_data(sql_commands.get_inventory_by_group, None)))
        self.refresh_btn.configure(command = update_tables)

        self.restock_popup = Inventory_popup.restock(self, (width, height, acc_cred, acc_info))
        self.add_item_popup = Inventory_popup.add_item(self, (width, height, acc_cred, acc_info))
        self.grid_forget()

    def reset(self):
        self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
        self.data2 = database.fetch_data(sql_commands.get_inventory_by_expiry, None)
        self.data_view1.update_table(self.data1)
        self.data_view2.update_table(self.data2)

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
        self.label = ctk.CTkLabel(self, text='7').pack(anchor='w')
        self.grid_forget()

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