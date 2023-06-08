from typing import *
from tkinter import *
from tkinter import messagebox
import customtkinter as ctk

def popup_name_here(master, obj, info:tuple) -> ctk.CTkFrame:
    class add_item(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="#B3B3B3")
            #the actual frame, modification on the frame itself goes here

            '''code goes here'''

            #From here
            #more info button
            self.more_info_btn = ctk.CTkButton(self, text='More Information', command=quit,font=("Poppins-Medium", 25, "normal"), fg_color='#2C74B3', text_color='white')
            self.more_info_btn.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            #pet info frame
            self.pet_info_frame= ctk.CTkFrame(self, fg_color='white')
            self.pet_info_frame.grid(row=1, column=0, padx=10, pady=10, sticky="new")

            #pets info label
            self.update_lbl = ctk.CTkLabel(self.pet_info_frame, text='Pet\'s Information',font=("Poppins", 35), text_color='#06283D')
            self.update_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw", columnspan=2)

            #Patient name title
            self.patient_name_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Patient\'s Name:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.patient_name_title_lbl.grid(row=1, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #Patient name lbl
            self.patient_name_lbl = ctk.CTkLabel(self.pet_info_frame, text='Bugsy',font=("Poppins", 25), text_color='#06283D')
            self.patient_name_lbl.grid(row=1, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #Owner's name title
            self.owner_name_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Owner\'s Name:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.owner_name_title_lbl.grid(row=2, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #owner name lbl
            self.owner_name_lbl = ctk.CTkLabel(self.pet_info_frame, text='Tricia Dela Torre', text_color='#06283D',font=("Poppins", 25))
            self.owner_name_lbl.grid(row=2, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #breed title
            self.breed_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Breed:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.breed_title_lbl.grid(row=3, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #breed lbl
            self.breed_lbl = ctk.CTkLabel(self.pet_info_frame, text='Flemish Giant', text_color='#06283D',font=("Poppins", 25))
            self.breed_lbl.grid(row=3, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #sex title
            self.sex_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Sex:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.sex_title_lbl.grid(row=4, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #sex lbl
            self.sex_lbl = ctk.CTkLabel(self.pet_info_frame, text='Female', text_color='#06283D',font=("Poppins", 25))
            self.sex_lbl.grid(row=4, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #birthday title
            self.birthday_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Birthday:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.birthday_title_lbl.grid(row=5, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #birthday lbl
            self.birthday_lbl = ctk.CTkLabel(self.pet_info_frame, text='March 1, 2023', text_color='#06283D',font=("Poppins", 25))
            self.birthday_lbl.grid(row=5, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #address title
            self.address_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Address:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.address_title_lbl.grid(row=6, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #address lbl
            self.address_lbl = ctk.CTkLabel(self.pet_info_frame, text='STI College Fairview', text_color='#06283D',font=("Poppins", 25))
            self.address_lbl.grid(row=6, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #contact no title
            self.contact_no_title_lbl = ctk.CTkLabel(self.pet_info_frame, text='Contact Number:',font=("Poppins", 25, "bold"), text_color='#06283D')
            self.contact_no_title_lbl.grid(row=7, column=0, padx=(50, 10), pady=(10, 0), sticky="w")
            #contact no lbl
            self.contact_no_lbl = ctk.CTkLabel(self.pet_info_frame, text='12345678', text_color='#06283D',font=("Poppins", 25))
            self.contact_no_lbl.grid(row=7, column=1, padx=(10, 50), pady=(10, 0), sticky="w")

            #vaccination history fram
            self.vac_history_frame= ctk.CTkFrame(self, fg_color='white')
            self.vac_history_frame.grid(row=8, column=0, padx=10, pady=10, sticky="new")
            #vac history lbl
            self.vac_history_lbl = ctk.CTkLabel(self.vac_history_frame, text='Vaccination History',font=("Poppins", 35),text_color='#06283D')
            self.vac_history_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw", columnspan=2)


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