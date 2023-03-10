import customtkinter as ctk
import tkinter as tk
from tkextrafont import Font
from PIL import Image
from Theme import Color
import dashboard


class loginUI(ctk.CTk):

    __is_PasswordVisible = True

    def __init__(self):
        super().__init__()

        '''Import Font'''
        Font(file="Font/Poppins-Medium.ttf")
        Font(file="Font/Poppins-Regular.ttf")

        '''functions and processes'''
        def login():
            dashboard.dashboard()

        '''Import Icons and Images'''
        self.bg_img = ctk.CTkImage(light_image=Image.open("image/bg.png"),size=(1920,1080))
        self.logo_img = ctk.CTkImage(light_image=Image.open("image/logo.png"),size=(80,80))
        self.user_icon = ctk.CTkImage(light_image=Image.open("image/user_icon.png"),size=(30,30))
        self.pass_icon = ctk.CTkImage(light_image=Image.open("image/pass_icon.png"),size=(30,30))
        self.show_icon = ctk.CTkImage(light_image=Image.open("image/view.png"),size=(28,28))
        self.hide_icon = ctk.CTkImage(light_image=Image.open("image/hide.png"),size=(28,28))

        '''Setting values of the root window'''
        title_name = "J.Z. Angeles Veterinary Clinic"
        width = self.winfo_screenwidth()
        heigth = self.winfo_screenheight()

        root_w = round(width * 0.4)
        root_h = round(heigth * 0.85)
        pos_x = width/2
        pos_y = heigth/2 - root_h/2

        self.title(title_name)
        self.geometry('%dx%d+%d+%d' % (root_w,root_h,pos_x,pos_y))
        self.minsize(root_w,root_h)
        print(self.state())
        self.configure(fg_color=Color.Blue_Oxford)

        '''Background Image'''
        self.main_bg = ctk.CTkLabel(self, text='', image=self.bg_img)
        self.main_bg.place(x=0, y=0, relwidth=1, relheight=1)

        '''Main frame'''
        self.main_frame =  ctk.CTkFrame(self, width=360, height=550,corner_radius=5,
                                        fg_color=Color.White_Lotion, bg_color=Color.Blue_LapisLazuli)
        self.main_frame.place(relx=0.5, rely=0.5, anchor='c')
        self.main_frame.grid_propagate(False)

        self.main_frame.grid_columnconfigure(0,weight=1)
        self.main_frame.grid_rowconfigure(6, weight=1)

        '''container for company logo and name'''
        self.title_cont = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.title_cont.grid(row=0,column=0, padx=10, pady=(40,10))

        self.logo_label = ctk.CTkLabel(self.title_cont, text="", image=self.logo_img)
        self.logo_label.pack(side='left',padx=(10,5), pady=10)

        self.name_label = ctk.CTkLabel(self.title_cont, text=title_name, font=('Poppins Medium',23),
                                       wraplength=200, justify='left', text_color=Color.Blue_Maastricht)
        self.name_label.pack(side='right',padx=(5,10), pady=10)

        self.login_label = ctk.CTkLabel(self.main_frame, text='Login', font=('Poppins Medium',22),
                                        text_color=Color.Blue_Maastricht)
        self.login_label.grid(row=1,column=0,sticky="w",padx=(42,10),pady=(10,5))

        self.user_label = ctk.CTkLabel(self.main_frame, text='Username', font=('Poppins',17),
                                       text_color=Color.Grey_Davy)
        self.user_label.grid(row=2, column=0,sticky='sw',padx=(42,10),pady=(0,0))

        '''Frame for the username entry'''
        self.user_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                       fg_color=Color.White_Milk)
        self.user_frame.grid(row=3, column=0,sticky='ew',padx=(44,35))

        self.user_icon_label = ctk.CTkLabel(self.user_frame, text='', image=self.user_icon)
        self.user_icon_label.pack(side='left', padx=(5,0),pady=(5))
        self.user_entry = ctk.CTkEntry(self.user_frame, height=round(heigth * 0.03),font=('Poppins',16),border_width=0,
                                       fg_color=Color.White_Milk, text_color=Color.Blue_Maastricht)
        self.user_entry.pack(side='right', fill='x', expand=True,padx=(5,10),pady=(5))

        self.password_label = ctk.CTkLabel(self.main_frame, text='Password', font=('Poppins',17),
                                       text_color=Color.Grey_Davy)
        self.password_label.grid(row=4, column=0,sticky='sw',padx=(42,10),pady=(20,0))

        '''Frame for the password entry'''
        self.pass_frame = ctk.CTkFrame(self.main_frame, border_color=Color.Grey_Davy, border_width=2,
                                       fg_color=Color.White_Milk)
        self.pass_frame.grid(row=5, column=0,sticky='ew',padx=(44,35))

        self.pass_icon_label = ctk.CTkLabel(self.pass_frame, text='',image=self.pass_icon)
        self.pass_icon_label.pack(side='left', padx=(5,0),pady=(5))

        self.password_entry = ctk.CTkEntry(self.pass_frame,height=round(heigth * 0.03),font=('Poppins',16),border_width=0,
                                       fg_color=Color.White_Milk, show='*')
        self.password_entry.pack(side='left', fill='x', expand=True,padx=(3),pady=(5))
        self.show_pass_btn =ctk.CTkButton(self.pass_frame,width=28,height=28,
                                          image=self.hide_icon, text="",
                                          fg_color='transparent', hover=False,
                                          command=self.show_pass)
        self.show_pass_btn.pack(side='right', padx=(0,5))
        '''Error message'''
        self.error_label = ctk.CTkLabel(self.main_frame, text='', text_color='red',
                                        font=('Poppins',17))
        self.error_label.grid(row=6, column=0,sticky='nsew')
        '''login button'''
        self.login_button = ctk.CTkButton(self.main_frame, text="LOGIN", height=50,
                                          font=('Poppins Medium',20),text_color='#FFFFFF',
                                          fg_color=Color.Blue_Cobalt,corner_radius=5,
                                          command= login
                                          )
        self.login_button.grid(row=7, column=0, sticky='nsew', padx=(42,35),pady=(0,35))

    '''For showing the password'''

    def show_pass(self):
        if self.__is_PasswordVisible is True:
            self.password_entry.configure(show="")
            self.show_pass_btn.configure(image=self.show_icon)
            self.__is_PasswordVisible = False
        else:
            self.password_entry.configure(show="*")
            self.show_pass_btn.configure(image=self.hide_icon)
            self.__is_PasswordVisible = True


if __name__ == '__main__':
    app = loginUI()
    app.mainloop()