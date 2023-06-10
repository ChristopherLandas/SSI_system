import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import tkcalendar
from Theme import Color
from util import database
from tkinter import messagebox
from constants import action
from PIL import Image
from Theme import Color
from customcustomtkinter import customcustomtkinterutil as cctku
from functools import partial


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

            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            
            def reset():
                self.place_forget()
                self.owner_name_entry.delete(0, ctk.END)
                self.patient_name_entry.delete(0, ctk.END)
                self.breed_entry.delete(0, ctk.END)
                self.birthday_entry._text = "Set Birthday"
                self.address_entry.delete(0, ctk.END)
                self.contact_no_entry.delete(0, ctk.END)
                
            def proceed():
                pass
            
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
            self.owner_name_entry = ctk.CTkEntry(self.main_frame, placeholder_text="owner's Name", height=height*0.05, width=width*0.25,font=("Arial", 14))
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
            
            self.cancel_button = ctk.CTkButton(self.bottom_frame, text="Cancel", command=reset)
            self.cancel_button.pack(side="left", padx=(width*0.05,width*0.025))
            
            self.proceed_button = ctk.CTkButton(self.bottom_frame, text="Proceed", command=proceed)
            self.proceed_button.pack(side="right", padx=(width*0.025,width*0.05))
            
    return instance(master, info)


def view_record(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple ):
            
            width = info[0]
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
            load_main_frame(0)
    return instance(master, info)
