from typing import Callable, Optional, Tuple, Union
import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups, notif_popup_entities as ntf
from decimal import Decimal
from util import *
import sql_commands
import PyPDF2
from tkinter import filedialog

ctk.set_appearance_mode('dark')


class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        #print(os.path.isdir("C:\\Users\\chris\\Desktop\\Devstuff\\SSI_system"))
        self.notif_frame = ctk.CTkScrollableFrame(self, self.screen[0] * .15, self.screen[1] * .35, fg_color= 'red', scrollbar_button_color='#ffaaaa');
        self.notif_frame.place(relx = .5, rely = .5, anchor = 'c')
        self.update()
        self.notif_frame._parent_canvas.configure(bg =  'green')


        data = {s[1]: s[0] for s in database.fetch_data('SELECT UID, NAME FROM ITEM_GENERAL_INFO')}

        ''' ids = database.fetch_data('SELECT ID, NAME FROM RECIEVING_ITEM')
        for t in ids:
            database.exec_nonquery([['UPDATE RECIEVING_ITEM SET ITEM_UID = ? WHERE ID = ?', (data[t[1]], t[0])]])'''
        '''notif_entity_example = ntf.create_entity(self.notif_frame, "Reorder Alert",
                                                 "The product Insert Product Name here was only at 50 percent",
                                                 datetime.datetime(1967, 8, 10), self.notif_frame._desired_width-10, 100, 'white')'''
        #inventory_report_data = [(s[0], s[1] + (0 if s[0] not in bought_item else bought_item[s[0]]), s[1]) for s in current_stock]
        #print(*inventory_report_data, sep = '\n')
        '''
        print(database.fetch_data('SELECT ?', ('🠋',))[0][0])
        ctk.CTkLabel(self, text = '🠋', text_color ='green', font=('arial', 30)).place(relx = .5, rely = .5, anchor = 'c')
        self.mainloop()'''
        #notif test here
        

        lbl = ctk.CTkLabel(self, 120, 28, text="fejorifjireofjerfioerjfeiorfjerifjerfierfjejorfo", fg_color='red')
        lbl.pack()
        text_overflow_elipsis(lbl)


        treeview = cctk.cctkTreeView(self, ("j", "1"), self.screen[0] * .5, self.screen[1] * .5,
                                     column_format="/Title2:120-tl/Title3:x-tl!30!30")
        treeview.place(relx = .5, rely = .5, anchor = 'c')
        self.mainloop()
body()
    #lbl.configure(text = ''.join(txt_dvd))