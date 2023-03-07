import customtkinter as ctk
import tkinter as tk

from functools import partial
from tkextrafont import Font
from Theme import Color
from PIL import Image



ctk.set_appearance_mode('light')
ctk.set_default_color_theme('blue')

class dashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.attributes("-fullscreen", True)
        #makes the form full screen and removing the default tab bar

        '''Import Font'''
        Font(file="Font/Poppins-Medium.ttf")
        Font(file="Font/Poppins-Regular.ttf")

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

        '''events'''
        def change_active_event(cur):
            if(self.active_win is not None):
                self.active_win.configure(fg_color = unselected_btn_color)
                self.active_win.configure(hover=True)
            self.active_win = cur
            self.title_label.configure(text=f"{self.active_win.cget('text').strip().upper()}")
            cur.configure(fg_color = selected_btn_color)
            cur.configure(hover=False)

        '''commands'''
        def switch_darkmode():
            print(switch_var_darkmode.get())

        '''menubars'''
        self.notif_menu_bar = None
        self.settings_menu_bar = None
        self.current_opened_menu_bar = None
        self.acc_menu_bar = None

        def show_notif_menubar():
            if(self.current_opened_menu_bar is not None):
                self.current_opened_menu_bar.destroy()
                if(str(self.current_opened_menu_bar) == str(self.notif_menu_bar)):
                    self.current_opened_menu_bar = None
                    self.notif_btn.configure(fg_color=Color.White_Ghost)
                    return
            self.notif_btn.configure(fg_color = Color.White_Platinum)
            self.notif_menu_bar= ctk.CTkFrame(self, width * default_menubar_width, height * default_menubar_height,
                                        corner_radius= 0, fg_color='black', border_width= 0)
            self.notif_menu_bar.place(relx = self.notif_btn.winfo_rootx() / self.winfo_width() + default_menubar_width/2,
                                rely= self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                anchor = 'c')
            self.current_opened_menu_bar = self.notif_menu_bar
            '''content code here'''

        '''Switch Value'''
        switch_var_darkmode = ctk.StringVar(value="lightmode")
        def show_settings_menubar():
            if(self.current_opened_menu_bar is not None):
                self.current_opened_menu_bar.destroy()
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

            self.settings_menu_bar_dark_mode = ctk.CTkSwitch(self.settings_menu_bar,width=round(width * default_menubar_width/2), height=round(height * .12),text="Dark Mode",
                                                             font=("Poppins Medium", 16), progress_color=Color.Blue_LapisLazuli_1, text_color=Color.Blue_Maastricht,
                                                             variable = switch_var_darkmode, onvalue="darkmode", offvalue="lightmode",
                                                             command=switch_darkmode,)
            self.settings_menu_bar_dark_mode.pack(anchor= 'c')
            '''content code here'''
            self.current_opened_menu_bar = self.settings_menu_bar

        def show_acc_menubar():
            if(self.current_opened_menu_bar is not None):
                self.current_opened_menu_bar.destroy()
                if(str(self.current_opened_menu_bar) == str(self.acc_menu_bar)):
                    self.current_opened_menu_bar = None
                    self.acc_btn.configure(fg_color=Color.White_Ghost)
                    return
            self.acc_btn.configure(fg_color=Color.White_Platinum)
            self.acc_menu_bar = ctk.CTkFrame(self, width * acc_menubar_width, height * default_menubar_height, 0, fg_color=Color.White_Ghost)
            self.acc_menu_bar.pack_propagate(0)
            self.acc_menu_bar.place(relx = 1 - acc_menubar_width/2,
                                    rely= self.top_frame.winfo_height()/ self.winfo_height() + default_menubar_height/2,
                                    anchor = 'c')
            ctk.CTkLabel(self.acc_menu_bar, text='test').pack(anchor = 'e')
            self.current_opened_menu_bar = self.acc_menu_bar

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


        self.dasbboard_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="    Dashboard",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.dashboard_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.dasbboard_button.configure(command=partial(change_active_event, self.dasbboard_button))
        self.dasbboard_button.pack()

        self.sales_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Sales",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.sales_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.sales_button.configure(command=partial(change_active_event, self.sales_button))
        self.sales_button.pack()

        self.inventory_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Inventory",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.inventory_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.inventory_button.configure(command=partial(change_active_event, self.inventory_button))
        self.inventory_button.pack()

        self.patient_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Patient Info",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.patient_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.patient_button.configure(command=partial(change_active_event, self.patient_button))
        self.patient_button.pack()

        self.report_button = ctk.CTkButton(self.side_frame, width=side_frame_w, height=round(height * 0.07),
                                              text="   Reports",font=("Poppins Medium", 16),text_color=Color.Grey_Bright,
                                              image=self.report_icon, anchor='w',border_spacing=round(width * 0.01), border_width=0,corner_radius=0,
                                              fg_color=unselected_btn_color,hover_color=Color.Blue_LapisLazuli_1,)
        self.report_button.configure(command=partial(change_active_event, self.report_button))
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
        self.acc_btn = ctk.CTkButton(master= self.top_frame, width= round(self.top_frame.winfo_reqwidth() * .12), text= "Juan dela Cruz",
                                              image= self.acc_icon, fg_color=Color.White_Ghost, height= round(self.top_frame.winfo_reqheight()*0.5), border_width=0,
                                              corner_radius=5, font=("Poppins Medium", 16), text_color=Color.Blue_Maastricht, hover_color=Color.White_Gray,
                                              command= show_acc_menubar)
        self.acc_btn.grid(row=0, column= 3, sticky='e', padx=(0,10))

        '''Main Frame'''
        self.main_frame = ctk.CTkFrame(self,corner_radius=0,fg_color=Color.White_Platinum)
        self.main_frame.grid(row=1, column=1, sticky="nsew")

        '''setting default events'''
        change_active_event(self.dasbboard_button)

        self.update()

        self.mainloop()

if __name__ == "__main__":
    print('test')
    dashboard()