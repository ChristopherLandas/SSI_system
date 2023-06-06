import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import tkcalendar
from Theme import Color
from util import database
from tkinter import messagebox
from constants import action
from PIL import Image
from Theme import Color


def status_bar(master, info:tuple, text: str, icon_color: str, count: int, window: callable, data: dict):
    class instance(cctk.ctkButtonFrame):
        def __init__(self, master, info:tuple, text: str, icon_color: str, count: int, window: callable, data: dict):
            self.width = info[0]
            self.height = info[1]
            self._window = window
            self._data = data

            super().__init__(master, height=self.height * .2, fg_color=Color.White_AntiFlash ,hover_color=Color.Platinum,corner_radius=5,cursor="hand2")

            self.status_label = ctk.CTkLabel(self, text=text, font=("DM Sans Medium", 14))
            self.status_label.pack(side="left", padx=(self.width*0.04,0))
            self.status_light = ctk.CTkLabel(self, text="", height=self.height*0.04, width=self.width*0.03, corner_radius=8, fg_color=icon_color)
            self.status_light.pack(side="right", padx=(self.width*0.025,self.width*0.05))
            self.status_count = ctk.CTkLabel(self, text=count, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.status_count.pack(side="right")
            self.update_children()

        def response(self, _):
            self._window(self.status_label._text, self._data[self.status_label._text])
            print(self._data[self.status_label._text])
            return super().response(_)


    return instance(master, info, text, icon_color, count, window, data)
