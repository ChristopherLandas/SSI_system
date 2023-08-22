import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import tkcalendar
from Theme import Color
from util import database, generateId
from tkinter import messagebox
from constants import action
from PIL import Image
from Theme import Color
from customcustomtkinter import customcustomtkinterutil as cctku
from functools import partial
import sql_commands
import tkinter as tk
from tkinter import ttk

def new_record(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple ):

            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            '''EVENTS'''
            def automate_fields(_: any = None):
                if  self.owner_name_entry._values.index(self.owner_name_entry.get()) != len(self.owner_name_entry._values) - 1:
                    data = database.fetch_data(sql_commands.get_pet_info, (self.owner_name_entry.get(), ))[0]
                    self.owner_name_entry.configure(ctk.DISABLED)
                    self.address_entry.delete(0, ctk.END)
                    self.address_entry.insert(0, data[6])
                    self.address_entry.configure(state = ctk.DISABLED)
                    self.contact_no_entry.delete(0, ctk.END)
                    self.contact_no_entry.insert(0, data[-1])
                    self.contact_no_entry.configure(state = ctk.DISABLED)
                else:
                    self.owner_name_entry.configure(state = ctk.NORMAL)
                    self.owner_name_entry.set('')
                    if self.address_entry._state == ctk.DISABLED:
                        self.address_entry.configure(state = ctk.NORMAL)
                        self.contact_no_entry.configure(state = ctk.NORMAL)
                        self.address_entry.delete(0, ctk.END)
                        self.contact_no_entry.delete(0, ctk.END)

            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))

            def reset():
                self.place_forget()
                self.owner_name_entry.set('')
                self.patient_name_entry.delete(0, ctk.END)
                self.breed_entry.delete(0, ctk.END)
                self.birthday_entry._text = "Set Birthday"
                self.address_entry.delete(0, ctk.END)
                self.contact_no_entry.delete(0, ctk.END)
                self.warning_label.configure(text = '')

            def proceed():
                if (self.owner_name_entry.get() == '' and self.patient_name_entry.get() == '' and self.breed_entry.get() == ''
                    and self.address_entry.get() == '' and self.contact_no_entry.get() == '') or self.birthday_entry._text == 'Set Birthday':
                    self.warning_label.configure(text = 'Fill all the fields')
                    return
                else:
                    ids = [s[0] for s in database.fetch_data(sql_commands.get_ids_pi)]
                    name= generateId('P', 6)
                    bday = str(self.birthday_entry._text)
                    while(uid in ids):
                        uid = generateId('P', 6)
                    database.exec_nonquery([[sql_commands.record_patient, (uid, self.owner_name_entry.get(), self.patient_name_entry.get(),
                                                                           self.breed_entry.get(), self.sex_entry.get(), bday,
                                                                           self.address_entry.get(), self.contact_no_entry.get())]])
                    messagebox.showinfo('Sucess', 'Patient Registered')
                    reset()
                    self.place_forget()


            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.4, height=height*0.75)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,columnspan=3, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="New Record", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            #Owner's name label
            ctk.CTkLabel(self.main_frame, text='Owner\'s Name:',font=("Arial", 14), text_color="#06283D").grid(row=1, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            #self.owner_name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="owner's Name", height=height*0.05, width=width*0.25,font=("Arial", 14))
            self.owner_name_entry = ctk.CTkComboBox(self.main_frame, height=height*0.05, width=width*0.25,font=("Arial", 14), text_color_disabled=('black', 'white')
                                                    ,command=automate_fields)
            self.owner_name_entry.set('')
            self.owners = [s[0] for s in database.fetch_data(sql_commands.get_owners)]
            self.owners.append('Add new')
            self.owner_name_entry.configure(values = self.owners)
            self.owner_name_entry.grid(row=1, column=1,columnspan=2, padx=(width*0.005, width*0.01), pady=10, sticky="ew")

             #Patient name label
            ctk.CTkLabel(self.main_frame, text='Patient\'s Name:',font=("Arial", 14), text_color="#06283D").grid(row=2, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            self.patient_name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Pet's Name", height=height*0.05, width=width*0.25,font=("Arial", 14))
            self.patient_name_entry.grid(row=2, column=1,columnspan=2,  padx=(width*0.005, width*0.01), pady=10, sticky="ew")

            #breed label
            ctk.CTkLabel(self.main_frame, text='Breed:',font=("Arial", 14), text_color="#06283D").grid(row=3, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            self.breed_entry = ctk.CTkEntry(self.main_frame, placeholder_text='Flemish Giant', height=height*0.05, width=width*0.25,font=("Arial", 14))
            self.breed_entry.grid(row=3, column=1,columnspan=2, padx=(width*0.005, width*0.01), pady=10, sticky="ew")

            #sex label
            ctk.CTkLabel(self.main_frame, text='Sex:',font=("Arial", 14), text_color="#06283D").grid(row=4, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            self.sex_entry = ctk.CTkComboBox(self.main_frame, height=height*0.05, width=width*0.25,font=("Arial", 14), values=["Male","Female"])
            self.sex_entry.grid(row=4, column=1,columnspan=2,  padx=(width*0.005, width*0.01), pady=10, sticky="ew")

            #birthday label
            ctk.CTkLabel(self.main_frame, text='Birthday:',font=("Arial", 14),text_color="#06283D").grid(row=5, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            self.birthday_entry = ctk.CTkLabel(self.main_frame,text="Set Birthday", fg_color="#DBDBDB",corner_radius=5, height=height*0.05, width=width*0.25,font=("Arial", 14), text_color="grey")
            self.birthday_entry.grid(row=5, column=1,  padx=(width*0.005, width*0.01), pady=10, sticky="ew")

            self.show_calendar = ctk.CTkButton(self.main_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.birthday_entry, "%s", date_format="raw", min_date=None))
            self.show_calendar.grid(row=5, column=2, padx = (0,width*0.01), sticky="e")

            #address label
            ctk.CTkLabel(self.main_frame, text='Address:',font=("Arial", 14), text_color="#06283D").grid(row=6, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            self.address_entry = ctk.CTkEntry(self.main_frame, placeholder_text='STI College Fairview', height=height*0.05, width=width*0.25,font=("Arial", 14))
            self.address_entry.grid(row=6, column=1,columnspan=2, padx=(width*0.005, width*0.01), pady=10, sticky="ew")

            #contact no label
            ctk.CTkLabel(self.main_frame, text='Contact Number:',font=("Arial", 14), text_color="#06283D").grid(row=7, column=0, padx=width*0.005, pady=(10, 0), sticky="e")
            self.contact_no_entry = ctk.CTkEntry(self.main_frame, placeholder_text='12345678', height=height*0.05, width=width*0.25,font=("Arial", 14))
            self.contact_no_entry.grid(row=7, column=1,columnspan=2,  padx=(width*0.005, width*0.01), pady=10, sticky="ew")


            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.bottom_frame.grid(row=8, column=0, columnspan=2)

            self.warning_label = ctk.CTkLabel(self.bottom_frame, text='', fg_color='transparent', text_color='red')
            self.warning_label.pack()

            self.cancel_button = ctk.CTkButton(self.bottom_frame, text="Cancel", command=reset)
            self.cancel_button.pack(side="left", padx=(width*0.05,width*0.025))

            self.proceed_button = ctk.CTkButton(self.bottom_frame, text="Proceed", command=proceed)
            self.proceed_button.pack(side="right", padx=(width*0.025,width*0.05))
        
        def place(self, **kwargs):
            self.owner_name_entry.configure(values = [s[0] for s in database.fetch_data(sql_commands.get_owners)])
            return super().place(**kwargs)

    return instance(master, info)


def view_record(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple ):

            """ width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")

            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(15,15))

            selected_color = Color.Blue_Yale
            self.gen_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(18,20))
            self.ser_icon = ctk.CTkImage(light_image=Image.open("image/patient.png"),size=(18,20))

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color="transparent", width=width*0.8, height=height*0.875)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_columnconfigure(2, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1)
            self.main_frame.grid_propagate(0)

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.tab_frame=ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3],corner_radius=0)

            self.gen_info_frame = ctk.CTkFrame(self.tab_frame,fg_color="transparent")
            self.vac_info_frame = ctk.CTkFrame(self.tab_frame,fg_color="transparent")

            self.report_frames=[self.gen_info_frame, self.vac_info_frame]
            self.active_report = None

            def reset():
                self.place_forget()

            def load_main_frame(cur_frame: int):
                if self.active_report is not None:
                    self.active_report.pack_forget()
                self.active_report = self.report_frames[cur_frame]
                self.active_report.pack(fill="both", expand=1)

            def update_tables(_ :any = None):
                self.refresh_btn.configure(state = ctk.DISABLED)
                self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

            self.gen_info_btn = cctk.ctkButtonFrame(self.main_frame, cursor="hand2", height=height*0.055, width=width*0.115,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

            self.gen_info_btn.grid(row=0, column=0, sticky="s", padx=(0,width*0.0025), pady=0)
            self.gen_info_btn.configure(command=partial(load_main_frame, 0))
            self.gen_info_icon = ctk.CTkLabel(self.gen_info_btn, text="",image=self.gen_icon)
            self.gen_info_icon.pack(side="left", padx=(width*0.01,width*0.005))
            self.gen_info_label = ctk.CTkLabel(self.gen_info_btn, text="GENERAL INFO", text_color="white",)
            self.gen_info_label.pack(side="left")
            self.gen_info_btn.grid()
            self.gen_info_btn.update_children()

            self.service_btn = cctk.ctkButtonFrame(self.main_frame, cursor="hand2", height=height*0.055, width=width*0.125,
                                                       fg_color=Color.White_Color[7], corner_radius=0, hover_color=Color.Blue_LapisLazuli_1, bg_color=selected_color)

            self.service_btn.grid(row=0, column=1, sticky="s", padx=(0,width*0.0025), pady=0)
            self.service_btn.configure(command=partial(load_main_frame,1))
            self.service_icon = ctk.CTkLabel(self.service_btn, text="",image=self.ser_icon)
            self.service_icon.pack(side="left", padx=(width*0.01,width*0.005))
            self.service_label = ctk.CTkLabel(self.service_btn, text="VACCINE HISTORY", text_color="white",)
            self.service_label.pack(side="left")
            self.service_btn.grid()
            self.service_btn.update_children()

            ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=selected_color, height=height*0.0075, bg_color=selected_color).grid(row=1, column=0, columnspan=4, sticky="nsew")

            self.button_manager = cctku.button_manager([self.gen_info_btn, self.service_btn], selected_color, False, 0)
            self.button_manager._state = (lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),
                                        lambda: self.button_manager.active.winfo_children()[0].configure(fg_color="transparent"),)
            self.button_manager.click(self.button_manager._default_active, None)

            self.tab_frame.grid(row=2, column=0, columnspan=4, sticky="nsew")

            self.close_btn= ctk.CTkButton(self.main_frame, text="X", height=height*0.04, width=width*0.025, command=reset, fg_color=selected_color, corner_radius=0,
                                          bg_color=selected_color)
            self.close_btn.grid(row=0, column=3, sticky="nsew")


            #self.gen_info_frame.pack(fill="both", expand=1)

            '''GENERRAL INFO FRAME:START'''
            self.pet_info_frame = ctk.CTkFrame(self.gen_info_frame)
            self.pet_info_frame.pack(fill="x", expand=0, padx=(width*0.005), pady=(height*0.0075))
            self.pet_info_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(self.pet_info_frame, text="Pet's Information", font=("Arial",18)).grid(row=0,column=0, sticky="w",
                                                                                                padx=(width*0.005))

            self.pet_frame=ctk.CTkFrame(self.pet_info_frame, fg_color="transparent")
            self.pet_frame.grid(row=1, column=0, padx=width*0.05, pady=(0,height*0.0025))

            '''Pet Infos'''

            '''Labels'''
            ctk.CTkLabel(self.pet_frame, text="Pet's Name: ",font=("Arial",16)).grid(row=0,column=0,sticky="e")
            ctk.CTkLabel(self.pet_frame, text="Owner's Name: ",font=("Arial",16)).grid(row=1,column=0,sticky="e")
            ctk.CTkLabel(self.pet_frame, text="Breed: ",font=("Arial",16)).grid(row=2,column=0,sticky="e")
            ctk.CTkLabel(self.pet_frame, text="Sex: ",font=("Arial",16)).grid(row=3,column=0,sticky="e")
            ctk.CTkLabel(self.pet_frame, text="Birthday: ",font=("Arial",16)).grid(row=0,column=2,sticky="e", padx=(width*0.05,0))
            ctk.CTkLabel(self.pet_frame, text="Address: ",font=("Arial",16)).grid(row=1,column=2,sticky="e", padx=(width*0.05,0))
            ctk.CTkLabel(self.pet_frame, text="Contact #: ", font=("Arial",16)).grid(row=2,column=2,sticky="e",padx=(width*0.05,0))

            '''Values'''
            self.pet_name=ctk.CTkLabel(self.pet_frame, text="Spinoza",font=("Arial",16), fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_name.grid(row=0,column=1,sticky="w", pady=(0, height*0.005))

            self.pet_owners=ctk.CTkLabel(self.pet_frame, text="God",font=("Arial",16),  fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_owners.grid(row=1,column=1,sticky="w", pady=(0, height*0.005))

            self.pet_breed=ctk.CTkLabel(self.pet_frame, text="Cat",font=("Arial",16),  fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_breed.grid(row=2,column=1,sticky="w", pady=(0, height*0.005))

            self.pet_sex=ctk.CTkLabel(self.pet_frame, text="Male",font=("Arial",16),  fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_sex.grid(row=3,column=1,sticky="w", pady=(0, height*0.005))

            self.pet_birthday=ctk.CTkLabel(self.pet_frame, text="2023-10-06",font=("Arial",16),  fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_birthday.grid(row=0,column=3,sticky="w", pady=(0, height*0.005))

            self.pet_address=ctk.CTkLabel(self.pet_frame, text="Earth",font=("Arial",16),  fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_address.grid(row=1,column=3,sticky="w", pady=(0, height*0.005))

            self.pet_contact=ctk.CTkLabel(self.pet_frame, text="0920-568-1648", font=("Arial",16),  fg_color=Color.White_Color[3], corner_radius=5,
                                        width=width*0.15, anchor="w")
            self.pet_contact.grid(row=2,column=3,sticky="w", pady=(0, height*0.005))

            self.service_frame = ctk.CTkFrame(self.gen_info_frame)
            self.service_frame.pack(fill="both", expand=1, padx=(width*0.005), pady=(0,height*0.0075))
            self.service_frame.grid_columnconfigure(1, weight=1)
            self.service_frame.grid_rowconfigure(1, weight=1)

            ctk.CTkLabel(self.service_frame, text="Service History", font=("Arial",18)).grid(row=0,column=0, sticky="w", padx=(width*0.005))

            self.refresh_btn = ctk.CTkButton(self.service_frame,text="", width=width*0.015, height = height*0.04, image=self.refresh_icon, fg_color="#83BD75",
                                              command=update_tables)
            self.refresh_btn.grid(row=0, column=1, sticky="e", padx=(width*0.005), pady=(height*0.005))

            self.treeview_frame = ctk.CTkFrame(self.service_frame, fg_color="transparent")
            self.treeview_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0,height*0.0075))

            self.service_history_treeview = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * .778, height= height * .5, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/ServiceConducted:x-tl/Attendant:x-tr/DateConducted:x-tr!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
            self.service_history_treeview.pack()
            '''GENERRAL INFO FRAME:END'''

            '''VACCINE FRAME:START'''

            self.vac_info_frame.grid_columnconfigure(1, weight=1)
            self.vac_info_frame.grid_rowconfigure(1, weight=1)

            ctk.CTkLabel(self.vac_info_frame, text="Vaccine Record", font=("Arial",18)).grid(row=0,column=0, sticky="w", padx=(width*0.005))
            self.refresh_btn = ctk.CTkButton(self.vac_info_frame,text="", width=width*0.015, height = height*0.04, image=self.refresh_icon, fg_color="#83BD75",
                                              command=update_tables)
            self.refresh_btn.grid(row=0, column=1, sticky="e", padx=(width*0.005), pady=(height*0.005))

            self.treeview_frame = ctk.CTkFrame(self.vac_info_frame, fg_color="transparent")
            self.treeview_frame.grid(row=1, column=0, sticky="nsew", columnspan=2, padx=(width*0.005), pady=(0,height*0.0075))

            self.vac_history_treeview = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * .785, height= height * .75, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/DateVaccinated:x-tc/Weight:x-tl/Manufacturer:x-tl/Vaccine:x-tr/Attendant:x-tr!30!30',
                                           header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                           row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
            self.vac_history_treeview.pack()
            '''VACCINE FRAME:END'''
            load_main_frame(0) """
    
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.gen_icon = ctk.CTkImage(light_image=Image.open("image/patient_icon.png"),size=(18,20))
            self.save_icon = ctk.CTkImage(light_image=Image.open("image/save.png"), size=(20,20))
            self.ser_icon = ctk.CTkImage(light_image=Image.open("image/patient.png"),size=(18,20))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(20,20))
            self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))
            self.trash_icon = ctk.CTkImage(light_image= Image.open("image/trash.png"), size=(22,25))
            self.pet_sample_icon = ctk.CTkImage(light_image=Image.open("image/pholder.png"),size=(160,160))

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.0225)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1)
            self.main_frame.grid_propagate(0)

            

            def reset():
                self.place_forget()
                entries_set_state("disabled")

            def update_tables(_ :any = None):
                self.refresh_btn.configure(state = ctk.DISABLED)
                self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

            def edit_entries():
                entries_set_state("normal")  
                self.edit_info_button.grid_forget()
                self.save_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01))
                
            def save_changes():
                entries_set_state("disabled")
                self.edit_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01)) 
                self.save_info_button.grid_forget()
                messagebox.showinfo(title=None, message="Info Successfully Changed!")
        
            def entries_set_state(state : str = "normal", color_normal :str = Color.White_Platinum, color_disabled :str = Color.White_Lotion):
                entries = (self.breed_entry, self.type_entry, self.sex_entry, self.weight_entry, self.birthday_entry, self.owner_name_entry, self.address_entry,
                           self.contact_no_entry, self.pet_name_entry) 
                for i in range(len(entries)):
                    if "normal" in state:
                        set_color = color_normal
                    elif "disabled" in state:
                        set_color = color_disabled
                    entries[i].configure(state=state, fg_color=set_color)
            
            self.header_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0)
            self.header_frame.grid(row=0, column=0, sticky="ew")
            self.header_frame.grid_propagate(0)
            
            ctk.CTkLabel(self.header_frame, image=self.gen_icon, text='').pack(side='left', padx=(width*0.01,width*0.005))
            
            ctk.CTkLabel(self.header_frame, text='PET INFORMATION', font=("DM Sans Medium", 16), text_color=Color.White_Color[3],
                                            height = height*0.05, corner_radius=5).pack(side='left')

            self.close_btn= ctk.CTkButton(self.header_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.pet_info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Platinum)
            self.pet_info_frame.grid(row=1,column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.pet_info_frame.grid_columnconfigure(3, weight=1)
            
            self.pet_image = ctk.CTkLabel(self.pet_info_frame, image=self.pet_sample_icon, text='', width=width*0.08, height=width*0.08, fg_color=Color.White_Lotion, corner_radius=5)
            self.pet_image.grid(row=0, column=0, rowspan=4 ,sticky="nsew", padx=(width*0.005,0),  pady=(height*0.01))

            self.pet_name_frame = ctk.CTkFrame(self.pet_info_frame, fg_color="transparent")
            self.pet_name_frame.grid(row=0, column=1, stick="nsew",padx=(width*0.005), pady=(height*0.01), columnspan=2,)
            self.pet_id = ctk.CTkLabel(self.pet_name_frame, text='PPBIG', font=("DM Sans Medium", 14), height = height*0.05, fg_color=Color.White_Lotion,corner_radius=5, width=width*0.1)
            self.pet_id.pack(side="left",padx=(0,width*0.005))
            self.pet_entry_frame = ctk.CTkFrame(self.pet_name_frame, height = height*0.05, fg_color=Color.White_Lotion)
            self.pet_entry_frame.pack(side="left", fill="both",expand=1)
            self.pet_name_entry = ctk.CTkEntry(self.pet_entry_frame, border_width=0, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5)
            self.pet_name_entry.pack(side="left", fill='x', expand=1,  padx=(width*0.0025), pady=(height*0.0025))
            
            self.edit_info_button = ctk.CTkButton(self.pet_info_frame, image=self.add_icon, text='', width=width*0.01, fg_color="#3b8dd0", command=edit_entries)
            self.edit_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01))

            self.save_info_button = ctk.CTkButton(self.pet_info_frame, image=self.save_icon, text='', width=width*0.01, fg_color="#83bd75", hover_color="#82bd0b", command=save_changes)
            #self.save_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01))
            
            '''Breed'''           
            self.breed_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.breed_frame.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.breed_frame, text='Breed:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.breed_entry = ctk.CTkEntry(self.breed_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.breed_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Type'''
            self.type_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.type_frame.grid(row=2, column=1, sticky="nsew", padx=(width*0.005,0),  pady=(0,height*0.01))
            ctk.CTkLabel(self.type_frame, text='Type:',  font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.type_entry = ctk.CTkEntry(self.type_frame,border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.type_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Weight'''
            self.weight_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.weight_frame.grid(row=3, column=1, sticky="nsew", padx=(width*0.005,0),  pady=(0,height*0.01))
            ctk.CTkLabel(self.weight_frame, text='Weight:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.weight_entry = ctk.CTkEntry(self.weight_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.weight_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Sex'''
            self.sex_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.sex_frame.grid(row=2, column=2, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))                    
            ctk.CTkLabel(self.sex_frame, text='Sex:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.sex_entry = ctk.CTkEntry(self.sex_frame,border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Birthday'''
            self.birthday_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.birthday_frame.grid(row=3, column=2, sticky="w", padx=(width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.birthday_frame, text='Birthday:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.birthday_entry = ctk.CTkEntry(self.birthday_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.birthday_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Owner'''
            self.owner_name_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.owner_name_frame.grid(row=1, column=3, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.owner_name_frame, text='Owner\'s Name:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.owner_name_entry = ctk.CTkEntry(self.owner_name_frame,  border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.owner_name_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Address'''
            self.address_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.address_frame.grid(row=2, column=3, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.address_frame, text='Address:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.address_entry = ctk.CTkEntry(self.address_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.address_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Contact'''
            self.contact_no_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.contact_no_frame.grid(row=3, column=3, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.contact_no_frame, text='Contact#:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.contact_no_entry = ctk.CTkEntry(self.contact_no_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.contact_no_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            self.pet_service_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Platinum)
            self.pet_service_frame.grid(row=2,column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))

            self.service_title_frame = ctk.CTkFrame(self.pet_service_frame, fg_color="transparent")
            self.service_title_frame.pack(fill = 'x', padx=(width*0.005),  pady=(height*0.01))
            
            self.service_title_label = ctk.CTkLabel(self.service_title_frame, text="Service Record", font=("DM Sans Medium", 14), height=height*0.045,corner_radius=5,
                                                    fg_color=Color.White_Color[3], text_color=Color.Blue_Maastricht)
            self.service_title_label.pack(side="left")
            self.refresh_btn = ctk.CTkButton(self.service_title_frame, image=self.refresh_icon, text='', width=height*0.045, height=height*0.045, fg_color="#83bd75", hover_color="#82bd0b")
            self.refresh_btn.pack(side="left",  padx=(width*0.005))
            
            self.service_treeview_frame = ctk.CTkFrame(self.pet_service_frame, fg_color="blue")
            self.service_treeview_frame.pack(fill='both', expand=1,  padx=(width*0.005),  pady=(0,height*0.01))
            self.service_treeview_frame.grid_rowconfigure(0, weight=1)
            self.service_treeview_frame.grid_columnconfigure(0, weight=1)
            
            '''Service Record Treeview'''
            #style
            self.tkstyle = ttk.Style()
            self.tkstyle.theme_use('clam')
            self.tkstyle.configure("Treeview", rowheight=int(height*0.045), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            self.tkstyle.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
            self.tkstyle.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
            self.tkstyle.map("Treeview", background=[("selected",Color.Blue_Steel)])
            self.service_record_data_view = ttk.Treeview(self.service_treeview_frame, show = 'headings')

            self.service_record_data_view['columns'] = ('#', 'Service', 'Date', 'Attendant')
            #create headings 
            self.service_record_data_view.heading('#', text='#', anchor=tk.CENTER)
            self.service_record_data_view.heading('Service', text='Service', anchor=tk.CENTER)
            self.service_record_data_view.heading('Date', text='Date', anchor=tk.CENTER)     
            self.service_record_data_view.heading('Attendant', text='Attendant', anchor=tk.CENTER)
            #define columns
            self.service_record_data_view.column('#', anchor="e", width=int(width*0.001))
            self.service_record_data_view.column('Service', anchor="w", width=int(width*0.475))
            self.service_record_data_view.column('Date', anchor="center", width=int(width*0.2))
            self.service_record_data_view.column('Attendant', anchor="w", width=int(width*0.285))

            #add sample data
            service_data = ["Service 1", "Service 2", "Service 3", "Service 4", "Service 5", "Service 6", "Service 7", "Service 8", "Service 9", "Service 10", "Service 11", "Service 12", "Service 13", "Service 14", "Service 15", "Service 16"]

            data_rows = []
            for i in range(len(service_data)):
                if (i % 2) == 0:
                    tag = "even"
                else:
                    tag ="odd"
                data = (f"{i+1} ", service_data[i], "MM-DD-YYYY", service_data[i])
                data_rows.append(data)
                self.service_record_data_view.insert(parent = '', index = "end", values = data, tags=tag)
            
            self.service_record_data_view.tag_configure("odd",background=Color.White_AntiFlash)
            self.service_record_data_view.tag_configure("even",background=Color.White_Ghost)
            
            self.service_record_data_view.grid(row=0, column=0, sticky="nsew")
            #scrollbar
            self.y_scrollbar_service_record = ttk.Scrollbar(self.service_treeview_frame, orient=tk.VERTICAL, command=self.service_record_data_view.yview)
            self.service_record_data_view.configure(yscroll=self.y_scrollbar_service_record.set)
            self.y_scrollbar_service_record.grid(row=0, column=1, sticky="ns")   
            '''GENERRAL INFO FRAME:END'''
    
            self.set_entries()
            entries_set_state("disabled")
            
        def set_entries(self):
            self.pet_id.configure(text="P00001")
            self.pet_name_entry.insert(0, "Brutus")
            self.service_title_label.configure(text="Brutus Service Record")
            self.breed_entry.insert(0, "Mini Pinscher")
            self.type_entry.insert(0, "Dog")
            self.sex_entry.insert(0, "Male")
            self.weight_entry.insert(0, "4.5kg")
            self.birthday_entry.insert(0, "October 9, 2020")
            self.owner_name_entry.insert(0, "James Vinas")
            self.address_entry.insert(0, "Tala, Caloocan City")
            self.contact_no_entry.insert(0, "09208902063")
    return instance(master, info)
