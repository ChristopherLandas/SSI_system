import customtkinter as ctk
from popup import transaction_popups

class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)

        self.transaction = transaction_popups.show_list(self, None, (self.winfo_vrootwidth(), self.winfo_vrootheight(), None, None))
        self.transaction.place(relx = .5, rely = .5, anchor = 'c')
        self.mainloop()

#body()
print(float('00,000,000.00'.replace(',','')))