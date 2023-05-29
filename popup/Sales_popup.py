import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
import tkcalendar
from Theme import Color
from util import database
from tkinter import messagebox
from constants import action
from PIL import Image

def show_sales_record_info(master, info:tuple, sales_info: tuple, sales_content: list) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, sales_info: tuple, sales_content: list):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .8, height=height*0.8, corner_radius= 0)
            self.pack_propagate(0)
            #basic inforamtion needed; measurement

            lbltst = ctk.CTkLabel(self, text='OR#: %s\nCashier: %s\ndate of transaction: %s' % sales_info, text_color='white')
            lbltst._label.configure(justify=ctk.LEFT, )
            lbltst.pack(anchor = 'w')

            self.treeview = cctk.cctkTreeView(self, width= width * .7, height= height *.7, column_format='/No:45-#l/Name:x-tl/Price:150-tr!50!30')
            self.treeview.pack(pady =(12, 0))

            #the actual frame, modification on the frame itself goes here

    return instance(master, info, sales_info, sales_content)