import customtkinter as ctk
import tkinter as tk
from tk import *
import _tkinter;
from functools import partial
from tkextrafont import Font
from Theme import Color
from PIL import Image
from datetime import date
from util import sequence
from customcustomtkinter import customcustomtkinter as cctk


ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')
width = 0
height = 0

class dashboard(ctk.CTkToplevel):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.attributes("-fullscreen", True)
        #makes the form full screen and removing the default tab bar

        try:
            Font(file="Font/Poppins-Medium.ttf")
            Font(file="Font/Poppins-Regular.ttf")
            Font(file='Font/Poppins-Bold.ttf')
        except _tkinter.TclError:
            pass
        #for testing purposes, might delete after the development

        '''Import Images'''
        self.inv_logo = ctk.CTkImage(light_image=Image.open("image/logo_1.png"),size=(37,35))
        self.dashboard_icon = ctk.CTkImage(light_image=Image.open("image/dashboard.png"),size=(22,22))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(26,20))
        self.inventory_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"),size=(24,25))
        self.patient_icon = ctk.CTkImage(light_image=Image.open("image/patient.png"),size=(22,25))
        self.report_icon = ctk.CTkImage(light_image=Image.open("image/report.png"),size=(22,22))
        self.notif_icon = ctk.CTkImage(light_image=Image.open("image/notif.png"),size=(22,25))
        self.settings_icon = ctk.CTkImage(light_image=Image.open("image/setting.png"),size=(25,25))
        self.acc_icon = ctk.CTkImage(light_image=Image.open("image/acc.png"),size=(40,40))

        global width, height
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        side_frame_w = round(width * 0.175)
        default_menubar_width = .15
        default_menubar_height = .3
        acc_menubar_width = .2
        title_name = "J.Z. Angeles Veterinary Clinic"

        unselected_btn_color = Color.Blue_Yale
        selected_btn_color = Color.Blue_Steel

        self.active_win = None
        self.main_frames = [dashboard_frame(self), sales_frame(self), inventory_frame(self), patient_info_frame(self), reports_frame(self)]
        self.active_main_frame = None

        '''events'''
        def change_active_event(cur, cur_frame):
            if(self.active_win is not None):
                self.active_win.configure(fg_color = unselected_btn_color)
                self.active_win.configure(hover=True)
            if(self.active_main_frame is not None):
                self.active_main_frame.grid_forget()
            self.active_main_frame = self.main_frames[cur_frame]
            self.main_frames[cur_frame].grid(row=1, column=1, sticky="nsew")
            self.active_win = cur
            self.title_label.configure(text=f"{self.active_win.cget('text').strip().upper()}")
            cur.configure(fg_color = selected_btn_color)
            cur.configure(hover=False)

        '''commands'''
        def switch_darkmode():
            print(switch_var_darkmode.get())

        '''menubars'''
        self.current_opened_menu_bar = None
        self.notif_menu_bar = None
        self.settings_menu_bar = None
        self.acc_menu_bar = None
        self.active_btn_menu_bar = None

        def show_notif_menubar():
            if(self.current_opened_menu_bar is not None):
                self.current_opened_menu_bar.destroy()
                self.active_btn_menu_bar.configure(fg_color=Color.White_Ghost)
                self.active_btn_menu_bar = None
                if(str(self.current_opened_menu_bar) == str(self.notif_menu_bar)):
                    self.current_opened_menu_bar = None
                    return
            self.notif_btn.configure(fg_color = Color.White_Platinum)
            self.notif_menu_bar= ctk.CTkFrame(self, width * default_menubar_width, height * default_menubar_height,
                                        corner_radius= 0, fg_color='black', border_width= 0)
            self.notif_menu_bar.place(relx = self.notif_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                rely= self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                anchor = 'c')
            self.active_btn_menu_bar = self.notif_btn

            self.current_opened_menu_bar = self.notif_menu_bar
            '''content code here'''

        '''Switch Value'''
        switch_var_darkmode = ctk.StringVar(value="lightmode")
        def show_settings_menubar():
            if(self.current_opened_menu_bar is not None):
                self.current_opened_menu_bar.destroy()
                self.active_btn_menu_bar.configure(fg_color=Color.White_Ghost)
                self.active_btn_menu_bar = None
                if(str(self.current_opened_menu_bar) == str(self.settings_menu_bar)):
                    self.current_opened_menu_bar = None
                    self.settings_btn.configure(fg_color=Color.White_Ghost)
                    return
            self.settings_btn.configure(fg_color=Color.White_Platinum)
            self.settings_menu_bar = ctk.CTkFrame(self, width * default_menubar_width, height * default_menubar_height,
                                                    corner_radius= 5, fg_color=Color.White_Ghost, border_width= 0)
            self.settings_menu_bar.pack_propagate(0)
            self.settings_menu_bar.place(relx= self.settings_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                        rely = self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2+0.005,
                                        anchor = 'c')
            self.active_btn_menu_bar = self.settings_btn


            self.settings_menu_bar_dark_mode = ctk.CTkSwitch(self.settings_menu_bar,width=round(width * default_menubar_width/2), height=round(height * .12),text="Dark Mode",
                                                             font=("Poppins Medium", 16), progress_color=Color.Blue_LapisLazuli_1, text_color=Color.Blue_Maastricht,
                                                             variable = switch_var_darkmode, onvalue="darkmode", offvalue="lightmode",
                                                             command=switch_darkmode,)
            self.settings_menu_bar_dark_mode.pack(anchor= 'c')
            '''content code here'''
            self.current_opened_menu_bar = self.settings_menu_bar

        def show_acc_menubar(_):
            if(self.current_opened_menu_bar is not None):
                self.current_opened_menu_bar.destroy()
                self.active_btn_menu_bar.configure(fg_color=Color.White_Ghost)
                self.active_btn_menu_bar = None
                self.acc_btn.configure(hover= True)
                if(str(self.current_opened_menu_bar) == str(self.acc_menu_bar)):
                    self.current_opened_menu_bar = None
                    self.acc_btn.configure(fg_color=Color.White_Gray)
                    return
            self.acc_btn.configure(hover= False, fg_color=Color.White_Platinum)
            self.acc_menu_bar = ctk.CTkFrame(self, width * acc_menubar_width, height * default_menubar_height, 0, fg_color=Color.White_Ghost)
            self.acc_menu_bar.pack_propagate(0)
            self.acc_menu_bar.place(relx = 1 - acc_menubar_width/2,
                                    rely= self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                    anchor = 'c')

            self.active_btn_menu_bar = self.acc_btn
            self.current_opened_menu_bar = self.acc_menu_bar
            return

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


        self.dashboard_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="    Dashboard",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.dashboard_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.dashboard_button.configure(command=partial(change_active_event, self.dashboard_button, 0))
        self.dashboard_button.pack()

        self.sales_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Sales",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.sales_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.sales_button.configure(command=partial(change_active_event, self.sales_button, 1))
        self.sales_button.pack()

        self.inventory_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Inventory",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.inventory_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.inventory_button.configure(command=partial(change_active_event, self.inventory_button, 2))
        self.inventory_button.pack()

        self.patient_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Patient Info",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.patient_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.patient_button.configure(command=partial(change_active_event, self.patient_button, 3))
        self.patient_button.pack()

        self.report_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Reports",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.report_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.report_button.configure(command=partial(change_active_event, self.report_button, 4))
        self.report_button.pack()

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
                                              font=("Poppinds Medium", 16),hover_color=Color.White_Gray,
                                              command= show_notif_menubar,)
        self.notif_btn.grid(row=0, column= 1, sticky='w')
        self.settings_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqheight()* 0.5), text= "", image= self.settings_icon,
                                              fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight()* 0.5), border_width=0, corner_radius=5,
                                              font=("Poppinds Medium", 16),hover_color=Color.White_Gray,
                                              command= show_settings_menubar)
        self.settings_btn.grid(row=0, column= 2, sticky='w')

        '''
        old acc_btn
        self.acc_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqwidth() * .12), text= "Juan dela Cruz",
                                              image= self.acc_icon, fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight()*0.5), border_width=0,
                                              corner_radius=5, font=("Poppins Medium", 16), text_color=Color.Blue_Maastricht, hover_color=Color.White_Gray,
                                              command= show_acc_menubar)
        '''

        '''old acc button na ginawa ko nung tue
        self.acc_btn = ctk.CTkFrame(self.top_frame, round(self.top_frame.winfo_reqwidth() * .12), round(self.top_frame.winfo_reqheight()*.5),
                                    5, fg_color=Color.White_Ghost)
        self.acc_btn.grid_propagate(0)
        self.dp = ctk.CTkLabel(self.acc_btn, width * .03, width * .03, 0, 'transparent', 'transparent', text='', image=self.acc_icon,)
        self.dp.grid(row = 0, column = 0, rowspan = 3, sticky = 'nsew', pady = (round(height * .005), 0), padx = (round(height * .01), 0))
        self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text='Juan dela Cruz', font=("Poppins Medium", 16))
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .005), 0), pady = 0)
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text='Owner', font=("Poppins Medium", 12))
        self.position.grid(row = 1, column = 1, sticky = 'nw', padx = (round(height * .005), 0), pady = 0)
        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))

        sequence.bind_command((self.acc_btn, self.dp, self.acc_name, self.position), show_acc_menubar)
        sequence.bind_event((self.acc_btn, self.dp, self.acc_name, self.position), self.acc_btn,  Color.White_Gray, Color.White_Ghost)
        '''

        self.acc_btn = cctk.ctkButtonFrame(self.top_frame, round(self.top_frame.winfo_reqwidth() * .12),
                                           round(self.top_frame.winfo_reqheight()*.5), 5,
                                           fg_color=Color.White_Ghost, command= show_acc_menubar,
                                           hover_color= Color.White_Gray,)
        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.dp = ctk.CTkLabel(self.acc_btn, width * .03, width * .03, 0, 'transparent', 'transparent', text='', image=self.acc_icon,)
        self.dp.grid(row = 0, column = 0, rowspan = 3, sticky = 'nsew', pady = (round(height * .005), 0), padx = (round(height * .01), 0))
        self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text='Juan dela Cruz', font=("Poppins Medium", 16))
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .005), 0), pady = 0)
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text='Owner', font=("Poppins Medium", 12))
        self.position.grid(row = 1, column = 1, sticky = 'nw', padx = (round(height * .005), 0), pady = 0)
        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.acc_btn.update_children()


        '''setting default events'''
        change_active_event(self.dashboard_button, 0)
        self.mainloop()

class dashboard_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.date_frame = ctk.CTkFrame(self, fg_color=Color.White_Ghost, corner_radius= 12)
        self.date_frame.grid(row=0, column=0, padx = (width * .025, 0), pady= (height * .025, 0), sticky='nsew')
        ctk.CTkLabel(self.date_frame, text=date.today().strftime('%B %d, %Y'), font=("Poppins Medium", 16)).pack(anchor='c', padx = width * .015, pady = height * .01)

        self.inventory_stat_frame = ctk.CTkFrame(self, width * .37, height * .35,  fg_color=Color.White_Ghost, corner_radius= 12)
        self.inventory_stat_frame.pack_propagate(0)
        self.inventory_stat_frame.grid(row=1, column=0, padx = (width * .025, 0), pady= (height * .03, 0), sticky='nsew')
        ctk.CTkLabel(self.inventory_stat_frame, text= 'Inventory Status', font=('Poppins Bold', 16)).pack(padx=(width * .01), pady=(height * .01), anchor = 'w')

        self.daily_income_frame = ctk.CTkFrame(self, width * .37, height * .35,  fg_color=Color.White_Ghost, corner_radius= 12)
        self.daily_income_frame.pack_propagate(0)
        self.daily_income_frame.grid(row=1, column=1, padx = (width * .025, 0), pady= (height * .03, 0), sticky='nsew')
        ctk.CTkLabel(self.daily_income_frame, text= 'Daily Income', font=('Poppins Bold', 16)).pack(padx=(width * .01), pady=(height * .01), anchor = 'w')

        self.recent_client_frame = ctk.CTkFrame(self, width * .37, height * .3,  fg_color=Color.White_Ghost, corner_radius= 12)
        self.recent_client_frame.pack_propagate(0)
        self.recent_client_frame.grid(row=2, column=0, padx = (width * .025, 0), pady= (height * .03, 0), sticky='nsew')
        ctk.CTkLabel(self.recent_client_frame, text= 'Recent Client', font=('Poppins Bold', 16)).pack(padx=(width * .01), pady=(height * .01), anchor = 'w')

        self.scheduled_client_frame = ctk.CTkFrame(self, width * .37, height * .3,  fg_color=Color.White_Ghost, corner_radius= 12)
        self.scheduled_client_frame.pack_propagate(0)
        self.scheduled_client_frame.grid(row=2, column=1, padx = (width * .025, 0), pady= (height * .03, 0), sticky='nsew')
        ctk.CTkLabel(self.scheduled_client_frame, text= 'Scheduled Client', font=('Poppins Bold', 16)).pack(padx=(width * .01), pady=(height * .01), anchor = 'w')
        self.grid_forget()

class sales_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='2').pack(anchor='w')
        self.grid_forget()

class inventory_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='3').pack(anchor='w')
        self.grid_forget()

class patient_info_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='4').pack(anchor='w')
        self.grid_forget()

class reports_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='5').pack(anchor='w')
        self.grid_forget()

dashboard()