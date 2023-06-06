import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import tkcalendar
from Theme import Color
from util import database
from tkinter import messagebox
from constants import action
from PIL import Image
from Theme import Color


def status_bar(master, info:tuple, text: str, icon_color: str, count: int):
    class instance(cctk.ctkButtonFrame):
        def __init__(self, master, info:tuple, text: str, icon_color: str, count: int):
            self.width = info[0]
            self.height = info[1]
            print(icon_color)
            super().__init__(master, height=self.height * .2, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum,corner_radius=5,cursor="hand2")

            self.reorder_label = ctk.CTkLabel(self, text=text, font=("DM Sans Medium", 14))
            self.reorder_label.pack(side="left", padx=(self.width*0.04,0))
            self.reorder_light = ctk.CTkLabel(self, text="", height=self.height*0.04, width=self.width*0.03, corner_radius=8, fg_color=icon_color)
            self.reorder_light.pack(side="right", padx=(self.width*0.025,self.width*0.05))
            self.reorder_count = ctk.CTkLabel(self, text=count, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.reorder_count.pack(side="right")
            self.update_children()
    return instance(master, info, text, icon_color, count)
