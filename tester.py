import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from popup import dashboard_popup
from decimal import Decimal

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.screen = (self.winfo_screenwidth(), self.winfo_screenheight())

        test = dashboard_popup.status_bar(self, (250, 75), 'hello', '#121212', 12)
        test.place(relx = .5, rely = .5, anchor = 'c')

        self.mainloop()


#body()

i = [1,3,5,9]
j = [2,4,6,8]

for (t, s) in (i, j):
    print(t, s)

#print((s[1], t[1], s[2], t[2] for s, t in i, j))