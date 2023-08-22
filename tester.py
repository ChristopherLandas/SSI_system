import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups
from decimal import Decimal
from util import *
import sql_commands

ctk.set_appearance_mode('dark')


class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        '''treeview = cctk.cctkTreeView(self, ('2', 'name', '2'), self.screen[0] * .8, self.screen[1] * .8,
                                     column_format= '/test:x-tl/test2:x-id/test3:x-tl/test4:x-tc!50!30',
                                     spinner_min_val=(1, cctk.cctkSpinnerCombo.MAX_VAL), spinner_config=(1,0,3, "", '₱{:,.2f}', 'multiply'))
        treeview.place(relx = .5, rely = .5, anchor = 'c');'''
        
        '''current_stock = database.fetch_data(sql_commands.get_current_stock_group_by_name)
        bought_item = database.fetch_data(sql_commands.get_all_bought_items_group_by_name)
        bought_item = {s[0]: s[1] for s in bought_item}

        inventory_report_data = [(s[0], s[1] + (0 if s[0] not in bought_item else bought_item[s[0]]), s[1]) for s in current_stock]
        print(*inventory_report_data, sep = '\n')'''
        print(database.fetch_data('SELECT ?', ('🠋',))[0][0])
        ctk.CTkLabel(self, text = '🠋', text_color ='green', font=('arial', 30)).place(relx = .5, rely = .5, anchor = 'c')
        self.mainloop()


body()
