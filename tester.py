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
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        '''self.infotab = cctk.info_tab(self, self.screen[0] * .8, self.screen[1] * .8)
        self.infotab._tab = transaction_popups.customer_info(self, self.screen, self.infotab)
        self.infotab.button.configure(command = lambda: self.infotab._tab.place(relx = .5, rely = .5, anchor = 'c'))
        self.infotab.place(relx = .5, rely = .5, anchor = 'c')
'''
        cctk.cctkTreeView(self, [(1,2,3)], width = self.screen[0] * .9, height = self.screen[1] * .9, column_format='/test:x-iT/t1:x-tc!30!30').place(relx = .5, rely = .5, anchor = 'c')


        self.mainloop()


body()