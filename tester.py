import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups
from decimal import Decimal

ctk.set_appearance_mode('dark')


class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        """treeview = cctk.cctkTreeView(self, ('₱2,120.50', '₱0.00'), self.screen[0] * .8, self.screen[1] * .8,
                                     column_format= '/test:x-tl/test2:x-id/test3:x-tl!50!30',
                                     spinner_min_val=(1, cctk.cctkSpinnerCombo.MAX_VAL), spinner_config=(1,0,2, r"[₱,]", '₱{:,.2f}', 'multiply'))"""

        treeview = cctk.cctkTreeView(self, ('2', 'name', '2'), self.screen[0] * .8, self.screen[1] * .8,
                                     column_format= '/test:x-tl/test2:x-id/test3:x-tl/test4:x-tc!50!30',
                                     spinner_min_val=(1, cctk.cctkSpinnerCombo.MAX_VAL), spinner_config=(1,0,3, "", '₱{:,.2f}', 'multiply'))
        treeview.place(relx = .5, rely = .5, anchor = 'c');
        #print(treeview._data)

        self.mainloop()


body()
