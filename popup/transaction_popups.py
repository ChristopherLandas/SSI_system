import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import database
from tkinter import messagebox
from constants import action

def show_list(master, obj, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .8, height *.8, corner_radius= 0, fg_color='#111111')

            def reset():
                self.place_forget()

            self.back_btn = ctk.CTkButton(self, width*.03, height * .4, text='back', command= reset).place(relx = .5, rely = .5, anchor = 'c')
    return instance(master, obj, info)