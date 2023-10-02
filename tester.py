from typing import Callable, Optional, Tuple, Union
import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups, notif_popup_entities as ntf
from decimal import Decimal
from util import *
import sql_commands
import PyPDF2
from tkinter import filedialog
import network_socket_util as nsu

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
        #ntf.create_entity(self.notif_frame, 'hehe', 'tes2323827342372389 23848 92 28347 82937', datetime.datetime.now(), 200, 200, ('Arial', 12))


        #data = {s[1]: s[0] for s in database.fetch_data('SELECT UID, NAME FROM ITEM_GENERAL_INFO')}

        ''' ids = database.fetch_data('SELECT ID, NAME FROM RECIEVING_ITEM')
        for t in ids:
            database.exec_nonquery([['UPDATE RECIEVING_ITEM SET ITEM_UID = ? WHERE ID = ?', (data[t[1]], t[0])]])'''
        notif_entity_example = ntf.create_entity(self.notif_frame, "Reorder Alert",
                                                 "The product Insert Product Name here was only at 50 percent",
                                                 datetime.datetime(2023, 9, 22), '#00fc56', self.notif_frame._desired_width-10, 100, 'white')
        #inventory_report_data = [(s[0], s[1] + (0 if s[0] not in bought_item else bought_item[s[0]]), s[1]) for s in current_stock]
        #print(*inventory_report_data, sep = '\n')
        '''
        print(database.fetch_data('SELECT ?', ('🠋',))[0][0])
        ctk.CTkLabel(self, text = '🠋', text_color ='green', font=('arial', 30)).place(relx = .5, rely = .5, anchor = 'c')
        self.mainloop()'''
        #notif test here

        #entry = ctk.CTkEntry(self, width= 100)
        #print(entry._textvariable)
        '''data = [('1', '2', '3'), ('4', '5', '6'), ('7', '8', '9')]
        self.treeview = cctk.cctkTreeView(self, data, self.screen[0] * .8, self.screen[1] * .7, column_format= '/Test1:x-tc/Test:x-tc/Test:x-tc/Action:x-bD!30!20')
        self.treeview.pack(pady = 12)

        self.btn = ctk.CTkButton(self, 140, 28, text="remove", command = self.treeview.remove_selected_data)
        self.btn.pack()
        self.add_btn = ctk.CTkButton(self, 140, 28, text="ADD", command = lambda: self.treeview.add_data((1,2,3), True))
        self.add_btn.pack()'''


        #nsu.server_listener('wss://demo.piesocket.com/v3/channel_123?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self', )
        self.mainloop()
body()
    #lbl.configure(text = ''.join(txt_dvd))