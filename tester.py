import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        #self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)

        #self.transaction = transaction_popups.show_list(self, None, (self.winfo_vrootwidth(), self.winfo_vrootheight(), None, None))
        #self.transaction.place(relx = .5, rely = .5, anchor = 'c')

        #self.combobox = cctk.modified_combobox(self, 140, 28, 12, values=['123','345','456','567','678','789'])
        #self.combobox.place(relx = .75, rely = .5, anchor ='c')
        #self.option_menu = ctk.CTkOptionMenu(self, 140, 28, values=['natsuga','hajimata','kimi ni ochita'], state=ctk.ACTIVE)
        #self.option_menu.place(relx = .5, rely = .5, anchor ='c')

        self.spinner = cctk.cctkSpinnerCombo(self, 100, 30, 12, fg_color='transparent', val_range=(-10, 10))
        self.spinner.pack()

        self.mainloop()

body()