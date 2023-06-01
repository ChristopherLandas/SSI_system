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

        self.infotab = cctk.info_tab(self, self.screen[0] * .8, self.screen[1] * .8)
        self.infotab._tab = transaction_popups.customer_info(self, self.screen, self.infotab)
        self.infotab.button.configure(command = lambda: self.infotab._tab.place(relx = .5, rely = .5, anchor = 'c'))
        self.infotab.place(relx = .5, rely = .5, anchor = 'c')

        self.mainloop()

body()