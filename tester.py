#from typing import Callable, Optional, Tuple, Union
from typing import Optional, Tuple, Union
import customtkinter as ctk
from tkinter import messagebox
from customcustomtkinter import customcustomtkinter as cctk
from popup import notif_popup_entities as ntf, service_popup as svc_p
#from decimal import Decimal
from util import *
#import sql_commands
#import PyPDF2
#from tkinter import filedialog
#import network_socket_util as nsu
import winsound
from datetime import datetime as dt

ctk.set_appearance_mode('dark')

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        self.entry = ctk.CTkEntry(self, font= ('Arial', 24))
        self.entry.place(relx = .5, rely = .35, anchor = 'c')
        
        self.lbl = ctk.CTkLabel(self, text = 'Timer here', font= ('Arial', 24))
        self.lbl.place(relx = .5, rely = .4, anchor = 'c')

        self.lbl1 = ctk.CTkLabel(self, text = 'Timer here', font= ('Arial', 24))
        self.lbl1.place(relx = .5, rely = .45, anchor = 'c')

        self.lbl2 = ctk.CTkLabel(self, text = 'Timer here', font= ('Arial', 24))
        self.lbl2.place(relx = .5, rely = .5, anchor = 'c')

        self.button = ctk.CTkButton(self, command= self.click)
        self.button.place(relx = .5, rely = .55, anchor = 'c')
        self.mainloop()
    
    def click(self):
        self.button.configure(state = ctk.DISABLED)
        self.lbl.configure(text = dt.now().time().__str__())
        self.after(int(self.entry.get()) * 1000 if self.entry.get().isdecimal() else 2000, lambda: self.button.configure(state = ctk.NORMAL))
        self.timer()

    def timer(self):
        if self.button._state == ctk.DISABLED:
            def temp():
                self.lbl1.configure(text = dt.now().time().__str__())
                self.timer()
            self.lbl1.after(20, temp)
        else:
            f1 = float(self.lbl._text.split(':')[-1])
            f2 = float(self.lbl1._text.split(':')[-1])
            self.lbl2.configure(text = '%.3f' % (f2 - f1))
        
body()
    #lbl.configure(text = ''.join(txt_dvd))