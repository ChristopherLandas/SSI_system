import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import transaction_popups
from decimal import Decimal

ctk.set_appearance_mode('light')


class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        print(type(self))

        frame = ctk.CTkFrame(self, self.screen[0], self.screen[1], fg_color='green')
        frame.pack_propagate(0)
        frame.pack()

        temp =cctk.info_tab(frame, tab_master=frame, tab=transaction_popups.customer_info, tab_size= self.screen)
        self.bind('<Return>', lambda _: print(temp.value))
        temp.place(relx = .5 ,rely = .5, anchor = 'c')

        self.mainloop()


body()
