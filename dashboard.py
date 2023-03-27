import customtkinter as ctk
import tkinter as tk
import matplotlib.pyplot as plt
from tkinter import *
import _tkinter;
from functools import partial
from tkextrafont import Font
from Theme import Color
from PIL import Image
from datetime import date
from customcustomtkinter import customcustomtkinter as cctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


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
            #Transitioning to new font style
            Font(file="Font/DMSans-Bold.ttf")
            Font(file="Font/DMSans-Medium.ttf")
            Font(file='Font/DMSans-Regular.ttf')
        except _tkinter.TclError:
            pass
        #for testing purposes, might delete after the development

        '''Import Images'''
        self.inv_logo = ctk.CTkImage(light_image=Image.open("image/logo_1.png"),size=(37,35))
        self.dashboard_icon = ctk.CTkImage(light_image=Image.open("image/dashboard.png"),size=(22,22))
        self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales.png"),size=(26,20))
        self.inventory_icon = ctk.CTkImage(light_image=Image.open("image/inventory.png"),size=(24,25))
        self.patient_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(22,25))
        self.report_icon = ctk.CTkImage(light_image=Image.open("image/report.png"),size=(22,22))
        self.notif_icon = ctk.CTkImage(light_image=Image.open("image/notif.png"),size=(22,25))
        self.settings_icon = ctk.CTkImage(light_image=Image.open("image/setting.png"),size=(25,25))
        self.acc_icon = ctk.CTkImage(light_image=Image.open("image/acc.png"),size=(40,40))
        self.transact_icon = ctk.CTkImage(light_image=Image.open("image/transact.png"),size=(22,20))
        self.services_icon = ctk.CTkImage(light_image=Image.open("image/services.png"),size=(22,22))
        self.user_setting_icon = ctk.CTkImage(light_image=Image.open("image/usersetting.png"),size=(24,27))
        self.histlog_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"),size=(22,25))

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
        self.main_frames = [dashboard_frame(self), transaction_frame(self), services_frame(self), sales_frame(self), inventory_frame(self), patient_info_frame(self), reports_frame(self), user_setting_frame(self), histlog_frame(self)]
        self.active_main_frame = None

        '''events'''
        def change_active_event(cur, cur_frame, *args, **kwargs):
            if(self.active_win is not None):
                self.active_win.configure(fg_color = unselected_btn_color)
                self.active_win.winfo_children()[0].configure(fg_color="transparent")
                self.active_win.configure(hover=True)
            if(self.active_main_frame is not None):
                self.active_main_frame.grid_forget()
            self.active_main_frame = self.main_frames[cur_frame]
            self.main_frames[cur_frame].grid(row=1, column=1, sticky="nsew")
            self.active_win = cur
            #print(self.active_win.winfo_children()[0])
            self.active_win.winfo_children()[0].configure(fg_color=Color.White_Ghost)
            self.title_label.configure(text=f"{self.active_win.winfo_children()[2].cget('text').strip().upper()}")
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

        self.db_button = cctk.ctkButtonFrame(self.side_frame,  width=side_frame_w, height=round(height * 0.07),
                                             fg_color=unselected_btn_color, hover_color=Color.Blue_LapisLazuli_1,
                                             corner_radius=0, cursor="hand2",)
        self.db_button.configure(command=partial(change_active_event, self.db_button, 0))
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
        self.transact_button.configure(command=partial(change_active_event, self.transact_button, 1))
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
        self.services_button.configure(command=partial(change_active_event, self.services_button, 2))
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
        self.sales_button.configure(command=partial(change_active_event, self.sales_button, 3))
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
        self.inventory_button.configure(command=partial(change_active_event, self.inventory_button, 4))
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
        self.patient_button.configure(command=partial(change_active_event, self.patient_button, 5))
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
        self.report_button.configure(command=partial(change_active_event, self.report_button, 6))
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
        self.user_setting_button.configure(command=partial(change_active_event, self.user_setting_button, 7))
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
        self.histlog_button.configure(command=partial(change_active_event, self.histlog_button, 8))
        self.histlog_button.pack()
        self.histlog_wbar = ctk.CTkLabel(self.histlog_button,text="",fg_color="transparent", width=side_frame_w*0.02,height=round(height * 0.07))
        self.histlog_wbar.pack(side="left")
        self.histlog_icon = ctk.CTkLabel(self.histlog_button,image=self.histlog_icon, text="")
        self.histlog_icon.pack(side="left", padx=(width * 0.016,width * 0.01))
        self.histlog_label = ctk.CTkLabel(self.histlog_button, text="History Log", font=("Poppins Medium", 16), text_color=Color.Grey_Bright,)
        self.histlog_label.pack(side="left")
        self.histlog_button.pack()
        self.histlog_button.update_children()


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

        self.acc_btn = cctk.ctkButtonFrame(self.top_frame, round(self.top_frame.winfo_reqwidth() * .12),
                                           round(self.top_frame.winfo_reqheight()*.5), 5,
                                           fg_color=Color.White_Ghost, command= show_acc_menubar,
                                           hover_color= Color.White_Gray,cursor="hand2")

        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.dp = ctk.CTkLabel(self.acc_btn, width * .03, width * .03, 0, 'transparent', 'transparent', text='', image=self.acc_icon,)
        self.dp.grid(row = 0, column = 0, rowspan = 3, sticky = 'nsew', pady = (round(height * .005), 0), padx = (round(height * .01), 0))
        self.acc_name = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text='Juan dela Cruz', font=("Poppins Medium", 15))
        self.acc_name.grid(row = 0, column = 1, sticky = 'sw', padx = (round(height * .005), 0), pady = (5,0))
        self.position = ctk.CTkLabel(self.acc_btn, height = 0, fg_color='transparent', text='Owner', font=("Poppins Medium", 12))
        self.position.grid(row = 1, column = 1, sticky = 'nw', padx = (round(height * .005), 0), pady = 0)
        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))
        self.acc_btn.update_children()


        '''setting default events'''
        change_active_event(self.db_button, 0)
        self.mainloop()

class dashboard_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Chinese)
        self.data =[1457,2688]

        def show_pie(master):
            labels = ["Items", "Service"]


            data = self.data
            pie_figure= Figure(figsize=(frame_width*0.006,frame_height*0.013), dpi=100)
            pie_figure.set_facecolor(Color.White_Ghost)
            ax =pie_figure.add_subplot(111)
            ax.pie(data, autopct='%1.1f%%', startangle=0,counterclock=0, explode=(0.1,0), colors=[Color.Red_Tulip, Color.Light_Green],
                   textprops={'fontsize':18, 'color': Color.White_Ghost, 'family':'monospace', 'weight':'bold' },)
            ax.legend(labels, loc=8, ncol=2, bbox_to_anchor=(0.5,-0.12),prop={'family':"monospace", "size": 13}, labelcolor=Color.Blue_Maastricht, frameon=0)
            pie_figure.subplots_adjust(top=1,left=0,right=1, bottom=0)

            canvas = FigureCanvasTkAgg(pie_figure, master)
            canvas.draw()
            canvas.get_tk_widget().grid(row = 0, column=1, rowspan = 5)



        self.date_frame = ctk.CTkFrame(self, fg_color=Color.White_Ghost, corner_radius= 5)
        self.date_frame.grid(row=0, column=7, padx = (width * .025, width * .01), pady= (height * .01), sticky='e')
        self.date_label = ctk.CTkLabel(self.date_frame, text=date.today().strftime('%B %d, %Y'), font=("DM Sans Medium", 14))
        self.date_label.pack(anchor='c', padx = width * .015, pady = height * .01)

        self.income_summary_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.income_summary_frame.grid(row=1, column=0, columnspan=4, padx= (width*.01 ,width*(.005)))
        self.income_summary_frame.grid_propagate(0)

        frame_width, frame_height = self.income_summary_frame.cget('width'), self.income_summary_frame.cget("height")

        self.income_summary_frame.grid_columnconfigure((0,1), weight=1)
        self.income_summary_frame.grid_rowconfigure((2,3,4), weight=1)
        self.income_summary_label = ctk.CTkLabel(self.income_summary_frame,text="Daily Income Summary",fg_color="transparent", font=("DM Sans Medium", 17), text_color=Color.Blue_Maastricht,)
        self.income_summary_label.grid(row=0, column=0, sticky="ew", pady=(frame_height*0.04,0))
        self.income_summary_sub = ctk.CTkLabel(self.income_summary_frame,text=f"as of {date.today().strftime('%B %d, %Y')}", font=("DM Sans Medium", 14), text_color=Color.Grey_Davy)
        self.income_summary_sub.grid(row=1, column=0, sticky="ew")

        self.items_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.items_sales_frame.grid(row=2, column=0, sticky="nsew", padx=(frame_width*0.03), pady=(frame_height*0.05, frame_height*.015),)
        self.items_sales_frame.pack_propagate(0)
        self.items_sales_label = ctk.CTkLabel(self.items_sales_frame, text="Items:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(frame_width*.025,0))
        self.items_sales_value = ctk.CTkLabel(self.items_sales_frame, text="₱000,000.00", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,frame_width*.025))

        self.services_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.services_sales_frame.grid(row=3, column=0, sticky="nsew", padx=(frame_width*0.03),pady=( frame_height*.015))
        self.services_sales_frame.pack_propagate(0)
        self.services_sales_label = ctk.CTkLabel(self.services_sales_frame, text="Services:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(frame_width*.025,0))
        self.services_sales_value = ctk.CTkLabel(self.services_sales_frame, text="₱000,000.00", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,frame_width*.025))

        self.total_sales_frame = ctk.CTkFrame(self.income_summary_frame,height=frame_height*0.18, fg_color=Color.White_AntiFlash, corner_radius=5)
        self.total_sales_frame.grid(row=4, column=0, sticky="nsew", padx=(frame_width*0.03),pady=(frame_height*.015,0))
        self.total_sales_frame.pack_propagate(0)
        self.total_sales_label = ctk.CTkLabel(self.total_sales_frame, text="Total:", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="left", anchor="c", padx=(frame_width*.025,0))
        self.total_sales_value = ctk.CTkLabel(self.total_sales_frame, text="₱000,000.00", font=("DM Sans Medium", 15),text_color=Color.Blue_Maastricht).pack(side="right", anchor="c", padx=(0,frame_width*.025))
        #Watermelon Pie
        show_pie(self.income_summary_frame)

        self.view_more_button = ctk.CTkButton(self.income_summary_frame, text='View More',width= frame_width*0.2, height=frame_height*0.07, font=('DM Sans Medium', 12), corner_radius=4, text_color=Color.White_Ghost,
                                              fg_color=Color.Blue_Steel, command=lambda:print("Go To Report Section"))
        self.view_more_button.grid(row=5, column=1, sticky="e", padx=frame_width*0.02,pady=(0,frame_height*0.035))


        self.inventory_stat_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.inventory_stat_frame.grid(row=1, column=4, columnspan=4, padx= (width*(.005) ,width * .01))

        self.sched_client_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.sched_client_frame.grid(row=2, column=0, columnspan=4, padx= (width*.01 ,width*(.005)), pady=(height*0.017))

        self.log_history_frame = ctk.CTkFrame(self, width=width*.395, height=height*0.395, fg_color=Color.White_Ghost, corner_radius=5)
        self.log_history_frame.grid(row=2, column=4, columnspan=4, padx= (width*(.005) ,width * .01), pady=(height*0.017))

class transaction_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='2').pack(anchor='w')
        self.grid_forget()

class services_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='3').pack(anchor='w')
        self.grid_forget()

class sales_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='4').pack(anchor='w')
        self.grid_forget()

class inventory_frame(ctk.CTkFrame):
    global width, height
    def __init__(self, master):
        super().__init__(master,corner_radius=0,fg_color=Color.White_Platinum)
        self.label = ctk.CTkLabel(self, text='5').pack(anchor='w')
        self.grid_forget()

class patient_info_frame(ctk.CTkFrame):
    global width, height
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
        self.grid_forget()

dashboard()