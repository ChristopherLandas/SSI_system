#from typing import Callable, Optional, Tuple, Union
import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import notif_popup_entities as ntf
#from decimal import Decimal
from util import *
#import sql_commands
#import PyPDF2
#from tkinter import filedialog
#import network_socket_util as nsu

ctk.set_appearance_mode('dark')


class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        #print(os.path.isdir("C:\\Users\\chris\\Desktop\\Devstuff\\SSI_system"))
        '''self.notif_frame = ctk.CTkScrollableFrame(self, self.screen[0] * .15, self.screen[1] * .35, fg_color= 'red', scrollbar_button_color='#ffaaaa');
        self.notif_frame.place(relx = .5, rely = .5, anchor = 'c')
        self.update()
        print(self.screen[0] * .15)
        ntf.create_entity(self.notif_frame, 'hehe', 'this is a test this is a test this', 250, 100)'''


        #data = {s[1]: s[0] for s in database.fetch_data('SELECT UID, NAME FROM ITEM_GENERAL_INFO')}

        ''' ids = database.fetch_data('SELECT ID, NAME FROM RECIEVING_ITEM')
        for t in ids:
            database.exec_nonquery([['UPDATE RECIEVING_ITEM SET ITEM_UID = ? WHERE ID = ?', (data[t[1]], t[0])]])'''
        '''notif_entity_example = ntf.create_entity(self.notif_frame, "Reorder Alert",
                                                 "The product Insert Product Name here was only at 50 percent",
                                                 datetime.datetime(2023, 9, 22), '#00fc56', self.notif_frame._desired_width-10, 100, 'white')'''
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
        """btn = cctk.ctkButtonFrame(self, 200, 60, fg_color='#1101ff')
        ctk.CTkLabel(btn, text = 'Test Button 1', font=('Arial', 24)).place(relx = .5, rely = .5, anchor = 'c')
        btn.place(relx = .5, rely = .5, anchor = 'c')"""

        #spnr = cctk.cctkSpinnerCombo(self, 200, 60, fg_color='White')
        #spnr.num_entry.configure(font = ("Arial", 32))
        #spnr.place(relx = .5, rely = .5, anchor = 'c')

        #cs = nsu.network_sender("192.168.1.7", 90, "192.168.1.2", 92)

        '''treeview = cctk.cctkTreeView(self, ('P2.00', 'name', '2'), round(self.screen[0] * .8), round(self.screen[1] * .8),
                                     column_format= '/test:x-tl/test2:x-id/test3:x-tl/test4:x-tc!50!30',
                                     spinner_val_range=(1, cctk.cctkSpinnerCombo.MAX_VAL), spinner_config=(1,0,3, r'(\d+\.\d+)', '₱{:,.2f}', 'multiply'),
        )
        print(treeview._data)
        #treeview.configure(spinner_command = lambda: print(treeview._data))
        treeview.place(relx = .5, rely = .5, anchor = 'c')'''

        '''receiver = nsu.network_receiver('127.0.0.1', 250, lambda m: print(m))
        receiver.start_receiving()

        sender = nsu.network_sender('127.0.0.1', 250, '127.0.0.1', 252)
        sender.send("Hello123123")'''


        command = "SELECT item_general_info.UID,\
                   avg(case when MONTH(transaction_record.transaction_date) < MONTH(CURRENT_DATE)\
                       then (COALESCE(item_transaction_content.quantity, 0))\
                       ELSE 0\
                       END)\
                   FROM item_general_info\
                   LEFT JOIN item_transaction_content\
                       ON item_general_info.UID = item_transaction_content.Item_uid\
                   LEFT JOIN transaction_record\
                       ON item_transaction_content.transaction_uid = transaction_record.transaction_uid\
                   GROUP BY item_general_info.UID;"
        for b in[database.exec_nonquery([["INSERT INTO item_statistic_info VALUES (?, ?)", s]]) for s in database.fetch_data(command)]:
            print(b)
        
        self.mainloop()
body()
    #lbl.configure(text = ''.join(txt_dvd))