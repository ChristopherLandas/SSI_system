from typing import *
import customtkinter as ctk

def popup_name_here(master, obj, info:tuple) -> ctk.CTkFrame:
    class add_item(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0)
            #the actual frame, modification on the frame itself goes here

            '''code goes here'''

            #From here

            self.left_frame = ctk.CTkFrame(self, bg_color='#c3c3c3')
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.services_lbl = ctk.CTkLabel(self.left_frame, text='Services:',font=("Poppins", 45))
            self.services_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            self.services_entry = ctk.CTkEntry(self.left_frame, placeholder_text='item1', height=height*0.65, width=width*0.785)
            self.services_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ns")



            self.rightmost_frame = ctk.CTkFrame(self, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=height*0.78, width=width*0.312, fg_color='white')

            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', width=270, font=("Poppins-Bold", 45))

            self.back_button.grid(row=0, column=1, padx=20, sticky='s')


            self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=quit, width=270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), sticky="se")


            #on out

    return add_item(master, obj, info)
    #return the class as the frame

x,y = 1920,1080
ctk1 = ctk.CTk()
ctk1.state("zoomed")
ctk1.update()
ctk1.attributes("-fullscreen", True)
frame = popup_name_here(ctk1, None, (x * .8, y * .8))
frame.place(relx = .5, rely = .5, anchor = 'c')
ctk1.mainloop()
#for running and testing