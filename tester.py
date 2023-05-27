import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups
from decimal import Decimal

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)

        #self.transaction = transaction_popups.show_list(self, None, (self.winfo_vrootwidth(), self.winfo_vrootheight(), None, None))
        #self.transaction.place(relx = .5, rely = .5, anchor = 'c')

        #self.combobox = cctk.modified_combobox(self, 140, 28, 12, values=['123','345','456','567','678','789'])
        #self.combobox.place(relx = .75, rely = .5, anchor ='c')
        #self.option_menu = ctk.CTkOptionMenu(self, 140, 28, values=['natsuga','hajimata','kimi ni ochita'], state=ctk.ACTIVE)
        #self.option_menu.place(relx = .5, rely = .5, anchor ='c')

        self.spinner = cctk.cctkSpinnerCombo(self, 100, 30, 12, fg_color='transparent', val_range=(-10, 10), mode="num_only")
        self.spinner.pack()

        #self.transaction_proceeding = transaction_popups.show_transaction_proceed(self, (self.winfo_width(), self.winfo_height()))
        #self.transaction_proceeding.place(relx = .5, rely = .5, anchor = 'c')

        '''val = [(Decimal('1.00'), 1), (Decimal('2.00'), 2)]
        temp = [v[0] for v in val]
        print(temp)'''
        '''width = self.winfo_screenheight()
        height = self.winfo_screenheight()
        self.item_data = [(1,2),(1,2)]
        self.item_list = cctk.cctkTreeView(self, self.item_data, height=height*0.65, width=width*0.2,
                                               column_format=f'/No:{int(width * .01)}-#c/Name:x-tl/Price:{int(width * .05)}-tr!50!30')
        self.item_list.place(relx = .5, rely = .5, anchor = 'c')'''

        self.mainloop()

body()
#print('#' in str(['2#','tc','loof']))