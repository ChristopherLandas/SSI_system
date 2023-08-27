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
import datetime

def new_record(master, info:tuple, table_update_callback: callable):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, table_update_callback: callable):

            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")

            self._callback=table_update_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            '''EVENTS'''
            def automate_fields(_: any = None):
                if  self.owner_name_entry._values.index(self.owner_name_entry.get()) != len(self.owner_name_entry._values) - 1:
                    data = database.fetch_data(sql_commands.get_pet_info, (self.owner_name_entry.get(), ))[0]
                    print(data)
                    self.owner_name_entry.configure(ctk.DISABLED)
                    self.address_entry.delete(0, ctk.END)
                    self.address_entry.insert(0, data[8])
                    self.address_entry.configure(state = ctk.DISABLED)
                    self.contact_entry.delete(0, ctk.END)
                    self.contact_entry.insert(0, data[-1])
                    self.contact_entry.configure(state = ctk.DISABLED)
                else:
                    self.owner_name_entry.configure(state = ctk.NORMAL)
                    self.owner_name_entry.set('')
                    if self.address_entry._state == ctk.DISABLED:
                        self.address_entry.configure(state = ctk.NORMAL)
                        self.contact_entry.configure(state = ctk.NORMAL)
                        self.address_entry.delete(0, ctk.END)
                        self.contact_entry.delete(0, ctk.END)

            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            self.new_record = ctk.CTkImage(light_image=Image.open("image/new_record.png"),size=(22,22))

            def reset():
                self.place_forget()
                self.owner_name_entry.set('')
                self.patient_name_entry.delete(0, ctk.END)
                self.breed_option.set("")
                self.type_option.set("")
                self.sex_option.set("")
                self.birthday_entry._text = "Set Birthday"
                self.weight_entry.delete(0, ctk.END)
                self.address_entry.delete(0, ctk.END)
                self.contact_entry.delete(0, ctk.END)
                self._callback()
                
            def proceed():
                if (self.owner_name_entry.get() == '' and self.patient_name_entry.get() == '' and self.breed_option.get() == ''
                    and self.type_option.get() == '' and self.sex_option.get() == '' and self.address_entry.get() == ''
                    and self.address_entry.get() == '' and self.contact_entry.get() == '') or self.birthday_entry._text == 'Set Birthday':
                    messagebox.showwarning('Missing Fields', 'Complete all fields')
                    return
                else:
                    """ ids = [s[0] for s in database.fetch_data(sql_commands.get_ids_pi)]
                    name= generateId('P', 6)
                    bday = str(self.birthday_entry._text)
                    while(uid in ids):
                        uid = generateId('P', 6) """
                    bday = str(self.birthday_entry._text)
                    uid = str(datetime.datetime.now().strftime("%H%M%S"))# temporary fix
                    database.exec_nonquery([[sql_commands.record_patient, (uid, self.owner_name_entry.get(), self.patient_name_entry.get(),
                                                                           self.breed_option.get(), self.type_option.get(), self.sex_option.get(),
                                                                           self.weight_entry.get(), bday, self.address_entry.get(), self.contact_entry.get())]])
                    messagebox.showinfo('Sucess', 'Patient Registered')
                    reset()
                    self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.5, height=height*0.65)
            self.main_frame.grid(row=0, column=0, padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,columnspan=3, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.new_record).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="NEW RECORD", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.sub_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.sub_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure((0,1), weight=1)
            
            self.pet_image_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, width=width*0.11, height=width*0.08,)
            self.pet_image_frame.grid(row=0, column=2, rowspan=3 ,sticky="nsew", padx=(0,width*0.005),  pady=(height*0.01))
            self.pet_image_frame.grid_rowconfigure(0, weight=1)
            
            #self.pet_image = ctk.CTkLabel(self.pet_image_frame, image=self.pet_sample_icon, text='', width=width*0.08, height=width*0.08, fg_color="red", corner_radius=5)
            #self.pet_image.grid(row=0, column=0, sticky="nsew", padx=(width*0.005),  pady=(height*0.01))
            
            '''PET NAME ENTRY'''
            self.pet_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.pet_frame.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            ctk.CTkLabel(self.pet_frame, text="Pet's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.patient_name_entry = ctk.CTkEntry(self.pet_frame, placeholder_text="Pet Name",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum)
            self.patient_name_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''OWNER NAME ENTRY'''
            self.owner_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.owner_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.owner_frame, text="Owner's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.owner_name_entry = ctk.CTkComboBox(self.owner_frame,font=("DM Sans Medium", 14), fg_color=Color.White_Platinum, border_width=0, dropdown_fg_color=Color.White_Lotion, button_color=Color.Blue_Tufts, button_hover_color=Color.Blue_Steel,
                                                    height=height*0.05,command=automate_fields)
            self.owner_name_entry.set('')
            self.owners = [s[0] for s in database.fetch_data(sql_commands.get_owners)]
            self.owners.append('Add new')
            self.owner_name_entry.configure(values = self.owners)
            self.owner_name_entry.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))

            '''PET TYPE ENTRY'''
            self.type_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.type_frame.grid(row=2, column=0, sticky="nsew", padx=(width*0.005,0), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.type_frame, text="Pet Type: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.type_option= ctk.CTkOptionMenu(self.type_frame, values=["Cat", "Dog"], anchor="w", font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts)
            self.type_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''SEX ENTRY'''
            self.sex_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.sex_frame.grid(row=2, column=1, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.sex_frame, text="Sex: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.sex_option= ctk.CTkOptionMenu(self.sex_frame, values=["Male", "Female"], anchor="w", font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts)
            self.sex_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
              
            '''BREED ENTRY'''
            self.breed_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.breed_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.breed_frame, text="Breed: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.breed_option= ctk.CTkComboBox(self.breed_frame, values=["Male", "Female"], font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, border_width=0)
            self.breed_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            self.breed_option.set("")
            
            '''WEIGHT ENTRY'''
            self.weight_entry_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.weight_entry_frame.grid(row=4, column=0, sticky="nsew", padx=(width*0.005,0), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.weight_entry_frame, text="Weight: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.weight_entry = ctk.CTkEntry(self.weight_entry_frame, placeholder_text="Weight",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum)
            self.weight_entry.pack(side="left", fill="both", expand=1, padx=(0), pady=(height*0.005))
            ctk.CTkLabel(self.weight_entry_frame, text="kg",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.095, anchor="w").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            
            '''BDAY'''
            self.bday_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.bday_frame.grid(row=4, column=1, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.bday_frame, text="Birthday: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.birthday_entry = ctk.CTkLabel(self.bday_frame, text="Set Birthday", fg_color=Color.White_Platinum, corner_radius=5,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.birthday_entry.pack(side="left", fill="both", expand=1, padx=(0), pady=(height*0.005))

            self.show_calendar = ctk.CTkButton(self.bday_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.birthday_entry, "%s", date_format="raw", max_date=datetime.datetime.now()))
            self.show_calendar.pack(side="left", padx=(width*0.0025), pady=(height*0.005))
            
            '''ADDRESS ENTRY'''
            self.address_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.address_frame.grid(row=5, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.address_frame, text="Address: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.address_entry = ctk.CTkEntry(self.address_frame, placeholder_text='Address', font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum)
            self.address_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''CONTACT ENTRY'''
            self.contact_frame = ctk.CTkFrame(self.sub_frame, fg_color=Color.White_Lotion, height=height*0.065)
            self.contact_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.contact_frame, text="Contact: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.065, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.contact_entry = ctk.CTkEntry(self.contact_frame, placeholder_text='Contact Number', font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=0, fg_color=Color.White_Platinum)
            self.contact_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
           
            '''BOT FRAME'''
            self.bot_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.bot_frame.grid(row=2,column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
           
            self.cancel_btn = ctk.CTkButton(self.bot_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.add_btn = ctk.CTkButton(self.bot_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Add Record',
                                         command=proceed)
            self.add_btn.pack(side="right", padx = (width*0.0075), pady= height*0.01)

            self.breed_option.set("")
            self.type_option.set("")
            self.sex_option.set("")

        def place(self, **kwargs):
            self.owner_name_entry.configure(values = [s[0] for s in database.fetch_data(sql_commands.get_owners)])
            return super().place(**kwargs)

    return instance(master, info, table_update_callback)


def view_record(master, info:tuple, table_update_callback: callable):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple,table_update_callback: callable ):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")

            self.callback_command=table_update_callback

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
            self.camera_icon = ctk.CTkImage(light_image=Image.open("image/camera.png"), size=(25,25))

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.0225)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1)
            self.main_frame.grid_propagate(0)

            
            def edit_entries():
                
                self.entries_set_state("normal") 
                self.pet_id.configure(state="disabled", fg_color=Color.White_Lotion)
                
                self.edit_info_button.grid_forget()
                self.save_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01))
                
                self.image_edit.grid(row=0, column=0, sticky="se", padx=(width*0.005),  pady=(height*0.01))
                self.cancel_edit.grid(row=0, column=4, sticky="nsw", padx=(width*0.005), pady=(height*0.01))
                
                self.sex_entry_option.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.type_entry_option.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                
                self.sex_entry_option.set(self.sex_entry.get())
                self.type_entry_option.set(self.type_entry.get())
                
                self.type_entry.pack_forget()
                self.sex_entry.pack_forget()
                
            def cancel_changes():
                self.edit_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01)) 
                self.save_info_button.grid_forget()
                self.image_edit.grid_forget()
                
                self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.type_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                
                self.set_entries(self.data)
                self.entries_set_state("disabled")
                
                self.sex_entry_option.pack_forget()
                self.type_entry_option.pack_forget()
                self.cancel_edit.grid_forget()
                
            def save_changes():
                self.edit_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01)) 
                self.save_info_button.grid_forget()
                self.image_edit.grid_forget()
                
                self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.type_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                
                self.sex_entry.delete(0, ctk.END)
                self.type_entry.delete(0, ctk.END)
                self.sex_entry.insert(0, f"{self.sex_entry_option.get()}")
                self.type_entry.insert(0, f"{self.type_entry_option.get()}")
                
                self.entries_set_state("disabled")
                
                self.sex_entry_option.pack_forget()
                self.type_entry_option.pack_forget()
                self.cancel_edit.grid_forget()
                
                database.exec_nonquery([[sql_commands.update_pet_record, (self.owner_name_entry.get(), self.pet_name_entry.get(), self.breed_entry.get(),
                                                                          self.type_entry.get(), self.sex_entry.get(), self.weight_entry.get(),
                                                                          self.birthday_entry.get(), self.address_entry.get(),self.contact_no_entry.get(),
                                                                          self.pet_id.get())]])
                
                messagebox.showinfo(title=None, message="Info Successfully Changed!")
            
            self.header_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0)
            self.header_frame.grid(row=0, column=0, sticky="ew")
            self.header_frame.grid_propagate(0)
            
            ctk.CTkLabel(self.header_frame, image=self.gen_icon, text='').pack(side='left', padx=(width*0.01,width*0.005))
            
            ctk.CTkLabel(self.header_frame, text='PET INFORMATION', font=("DM Sans Medium", 16), text_color=Color.White_Color[3],
                                            height = height*0.05, corner_radius=5).pack(side='left')

            self.close_btn= ctk.CTkButton(self.header_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.pet_info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Platinum)
            self.pet_info_frame.grid(row=1,column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.pet_info_frame.grid_columnconfigure(4, weight=1)
            
            self.pet_image_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Lotion, width=width*0.08, height=width*0.08,)
            self.pet_image_frame.grid(row=0, column=0, rowspan=4 ,sticky="nsew", padx=(width*0.005,0),  pady=(height*0.01))
            self.pet_image_frame.grid_rowconfigure(0, weight=1)
            
            self.pet_image = ctk.CTkLabel(self.pet_image_frame, image=self.pet_sample_icon, text='', width=width*0.08, height=width*0.08, fg_color="transparent", corner_radius=5)
            self.pet_image.grid(row=0, column=0, sticky="nsew", padx=(width*0.005),  pady=(height*0.01))

            self.image_edit = ctk.CTkButton(self.pet_image_frame, image=self.camera_icon, text='', width=width*0.01, height=height*0.05, fg_color="#83bd75", hover_color="#82bd0b",)
            
            self.pet_name_frame = ctk.CTkFrame(self.pet_info_frame, fg_color="transparent")
            self.pet_name_frame.grid(row=0, column=1, stick="nsew",padx=(width*0.005), pady=(height*0.01), columnspan=2,)
            self.pet_id = ctk.CTkEntry(self.pet_name_frame, border_width=0,font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, justify="center")
            self.pet_id.pack(side="left",padx=(0,width*0.005), fill="both", expand=1)
            self.pet_entry_frame = ctk.CTkFrame(self.pet_name_frame, height = height*0.05, fg_color=Color.White_Lotion)
            self.pet_entry_frame.pack(side="left", fill="both",expand=1)
            self.pet_name_entry = ctk.CTkEntry(self.pet_entry_frame, border_width=0, font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5)
            self.pet_name_entry.pack(side="left", fill='x', expand=1,  padx=(width*0.0025), pady=(height*0.0025))
            
            self.edit_info_button = ctk.CTkButton(self.pet_info_frame, image=self.add_icon, text='', width=width*0.01, fg_color="#3b8dd0", command=edit_entries)
            self.edit_info_button.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01))

            self.save_info_button = ctk.CTkButton(self.pet_info_frame, image=self.save_icon, text='', width=width*0.01, fg_color="#83bd75", hover_color="#82bd0b", command=save_changes)
            self.cancel_edit = ctk.CTkButton(self.pet_info_frame, text="Cancel", hover_color=Color.Red_Pastel, fg_color=Color.Red_Tulip, font=("DM Sans Medium", 14), width=width*0.015, command=cancel_changes)
            
            
            '''Breed'''           
            self.breed_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.breed_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.breed_frame, text='Breed:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.breed_entry = ctk.CTkEntry(self.breed_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.breed_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Type'''
            self.type_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.type_frame.grid(row=1, column=1, sticky="nsew", padx=(width*0.005,0),  pady=(0,height*0.01))
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
            self.sex_frame.grid(row=1, column=2, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))                    
            ctk.CTkLabel(self.sex_frame, text='Sex:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.sex_entry = ctk.CTkEntry(self.sex_frame, border_width=0, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Birthday'''
            self.birthday_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.birthday_frame.grid(row=3, column=2, sticky="w", padx=(width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.birthday_frame, text='Birthday:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.birthday_entry = ctk.CTkEntry(self.birthday_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.birthday_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Owner'''
            self.owner_name_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.owner_name_frame.grid(row=1, column=3,columnspan=2, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.owner_name_frame, text='Owner\'s Name:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.owner_name_entry = ctk.CTkEntry(self.owner_name_frame,  border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.owner_name_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Address'''
            self.address_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.address_frame.grid(row=2, column=3,columnspan=2, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.address_frame, text='Address:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.address_entry = ctk.CTkEntry(self.address_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion,)
            self.address_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            '''Contact'''
            self.contact_no_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.contact_no_frame.grid(row=3, column=3,columnspan=2, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
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
    
            #self.set_entries()
            self.entries = (self.pet_id,self.owner_name_entry, self.pet_name_entry,self.breed_entry,self.type_entry, self.sex_entry, self.weight_entry,self.birthday_entry, 
                            self.address_entry,self.contact_no_entry)
            
            '''Replace entries with option mene when editing'''
            self.sex_entry_option = ctk.CTkOptionMenu(self.sex_frame, values=["Male","Female"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum,)
            self.type_entry_option = ctk.CTkOptionMenu(self.type_frame, values=["Dog","Cat"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum,)
            
        def reset(self):
            self.place_forget()
            self.entries_set_state("normal")
            self.reset_entries()
            self.callback_command()
            
        def reset_entries(self):
            for i in range(len(self.entries)):
                self.entries[i].delete(0, tk.END) 

        def entries_set_state(self,state : str = "normal", color_normal :str = Color.White_Platinum, color_disabled :str = Color.White_Lotion):
            for i in range(len(self.entries)):
                if "normal" in state:
                    set_color = color_normal
                elif "disabled" in state:
                    set_color = color_disabled
                self.entries[i].configure(state=state, fg_color=set_color)
            
        def set_entries(self, pet_values):
            self.reset_entries()
            for i in range(len(self.entries)):
                self.entries[i].insert(0, pet_values[0][i])
                
            self.service_title_label.configure(text=f"{pet_values[0][2]}'s Service Record")
            self.pet_id.configure(state="disabled")
            self.entries_set_state("disabled")
            
        def place(self, pet_data, **kwargs):
            
            self.data=database.fetch_data(f"SELECT * FROM pet_info WHERE id='{pet_data[0]}'")
            self.set_entries(self.data)

            return super().place(**kwargs)
    return instance(master, info, table_update_callback)
