import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
from Theme import Color
from util import database, generateId
from tkinter import messagebox
from PIL import Image
from Theme import Color, Icons
from customcustomtkinter import customcustomtkinterutil as cctku
import sql_commands
import tkinter as tk
import datetime
from popup import audit_popup

def new_record(master, info:tuple, table_update_callback: callable):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, table_update_callback: callable):

            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master,corner_radius= 0, fg_color="transparent")

            self._callback=table_update_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            '''EVENTS'''
            def automate_fields():
                self.owner_name_entry.configure(text=self.customer_selector.get()[1])
                if  self.owner_name_entry._text:
                    data = database.fetch_data(f"SELECT owner_name, address, contact_number FROM pet_owner_info WHERE owner_name = '{self.owner_name_entry._text}'")[0]
                    self.contact_entry.configure(state = ctk.NORMAL)
                    self.address_entry.configure(state = ctk.NORMAL)
                    self.address_entry.delete(0, ctk.END)
                    self.address_entry.insert(0, data[1])
                    self.contact_entry.delete(0, ctk.END)
                    self.contact_entry.insert(0, data[2])
                    self.contact_entry.configure(state = ctk.DISABLED)
                    self.address_entry.configure(state = ctk.DISABLED)
                else:
                    messagebox.showerror("Error", "There is an error in selecting the customer. Please try again", parent = self)
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            self.new_record = ctk.CTkImage(light_image=Image.open("image/new_record.png"),size=(22,22))

            def reset():
                self.address_entry.configure(state=ctk.NORMAL)
                self.contact_entry.configure(state=ctk.NORMAL)
                self.owner_name_entry.configure(text='Select a customer')
                self.patient_name_entry.delete(0, ctk.END)
                self.breed_option.set("")
                self.type_option.set("")
                self.sex_option.set("")
                self.birthday_entry.configure(text = "Set Birthday")
                self.weight_entry.delete(0, ctk.END)
                self.address_entry.delete(0, ctk.END)
                self.contact_entry.delete(0, ctk.END)
                self.place_forget()
                
            def proceed():
                if (self.owner_name_entry._text == '' and self.patient_name_entry.get() == '' and self.breed_option.get() == ''
                    and self.type_option.get() == '' and self.sex_option.get() == '' and self.address_entry.get() == ''
                    and self.address_entry.get() == '' and self.contact_entry.get() == '') or self.birthday_entry._text == 'Set Birthday':
                    messagebox.showwarning('Missing Fields', 'Complete all fields', parent = self)
                    return
                else:
                    bday = str(self.birthday_entry._text)
                    if self.owner_name_entry._text not in self.data:
                        database.exec_nonquery([[sql_commands.insert_new_pet_owner, (f'{self.owner_name_entry._text}',f'{self.address_entry.get()}',f'{self.contact_entry.get()}')]])
                    if self.breed_option.get() not in self.values:
                        database.exec_nonquery([[sql_commands.insert_new_pet_breed, (f'{self.type_option.get()}',f'{self.breed_option.get()}')]])
                    
                    owner_id = (database.fetch_data(f"SELECT owner_id FROM pet_owner_info WHERE owner_name = '{self.owner_name_entry._text}'"))[0][0]
                    database.exec_nonquery([[sql_commands.insert_new_pet_info, (self.pet_id._text, self.patient_name_entry.get(), owner_id, self.breed_option.get(),
                                                                                    self.type_option.get(), self.sex_option.get(), self.weight_entry.get(), bday, acc_cred[0][0])]])
            
                    reset()
                    if self._callback: self._callback()
                    
            def weight_callback(var, mode, index):
                try:
                    (float(self.weight_var.get()))
                except ValueError:
                    self.weight_var.set('')
            
            def contact_callback(var, mode, index):
                if not self.contact_var.get().isnumeric():
                    self.contact_var.set('')
                
            def pet_type_callback(var):
                self.values = [val[0] for val in database.fetch_data(f"SELECT breed From pet_breed WHERE pet_breed.type = '{var}'")]
                self.breed_option.configure(values = self.values)
                
            self.weight_var = ctk.StringVar()
            self.contact_var = ctk.StringVar()
            self.pet_type_var = ctk.StringVar(value='')
            self.pet_type_values = []

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.45, height=height*0.75, border_width=1, border_color=Color.Platinum)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0,columnspan=3, sticky="ew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.new_record).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="NEW RECORD", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            self.sub_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion)
            self.sub_frame.pack(fill="both", expand=1, padx=(width*0.005), pady=(height*0.01))
            self.sub_frame.grid_columnconfigure((0, 1), weight=1)
        
            '''PET ID'''
            self.pet_id_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.075)
            self.pet_id_frame.grid(row=0, column=0, columnspan=3, sticky="nsw", padx=(width*0.005), pady=(height*0.01,0))
            
            
            ctk.CTkLabel(self.pet_id_frame, text="Pet ID: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(0))
            self.pet_id = ctk.CTkLabel(self.pet_id_frame, font=("DM Sans Medium", 14), fg_color=Color.White_Platinum, text="PTESTES", corner_radius=5, width=width*0.1,height=height*0.055)
            self.pet_id.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(0))
        
            
            '''PET NAME ENTRY'''
            self.pet_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.pet_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pet_frame, text="Pet's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.005))
            self.patient_name_entry = ctk.CTkEntry(self.pet_frame, placeholder_text="Pet Name",font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion, height=height*0.055)
            self.patient_name_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(0))
            
            '''OWNER NAME ENTRY'''
            self.owner_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.085)
            self.owner_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            self.owners = [s[0] for s in database.fetch_data(sql_commands.get_owners)] or []
            ctk.CTkLabel(self.owner_frame, text="Owner's Name: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            """ self.owner_name_entry = ctk.CTkOptionMenu(self.owner_frame,values=self.owners, anchor="w", font=("DM Sans Medium", 14), width=width*0.08, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, command=automate_fields) """
            self.owner_name_entry = ctk.CTkButton(self.owner_frame, anchor="w", font=("DM Sans Medium", 14), width=width*0.08, height=height*0.05,
                                                  command=lambda: self.customer_selector.place(relx=0.5, rely=0.5, anchor='c'), text="Select a customer",)
            self.owner_name_entry.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            #self.owner_name_entry.set("Select A Customer")
            '''PET TYPE ENTRY'''
            self.type_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.085)
            self.type_frame.grid(row=3, column=0, sticky="nsew", padx=(width*0.005,0), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.type_frame, text="Pet Type: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.type_option= ctk.CTkOptionMenu(self.type_frame, values=["Cat", "Dog"], anchor="w", font=("DM Sans Medium", 14), width=width*0.08, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, variable=self.pet_type_var, command=pet_type_callback)
            self.type_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''SEX ENTRY'''
            self.sex_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.085)
            self.sex_frame.grid(row=3, column=1, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.sex_frame, text="Sex: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.sex_option= ctk.CTkOptionMenu(self.sex_frame, values=["Male", "Female"], anchor="w", font=("DM Sans Medium", 14), width=width*0.08, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts)
            self.sex_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
              
            '''BREED ENTRY'''
            self.breed_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.085)
            self.breed_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.breed_frame, text="Breed: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.breed_option= ctk.CTkComboBox(self.breed_frame, values=[], font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Platinum,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts, border_width=0)
            self.breed_option.pack(fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            self.breed_option.set("")
            
            '''WEIGHT ENTRY'''
            self.weight_entry_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.085)
            self.weight_entry_frame.grid(row=5, column=0, sticky="nsw", padx=(width*0.005,0), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.weight_entry_frame, text="Weight: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.weight_entry = ctk.CTkEntry(self.weight_entry_frame, placeholder_text="Weight", width=width*0.085,font=("DM Sans Medium", 14), placeholder_text_color="grey",
                                             border_width=2, fg_color=Color.White_Lotion, justify='right', textvariable=self.weight_var)
            self.weight_entry.pack(side="left", fill='y', expand=1, padx=(0), pady=(height*0.005))
            ctk.CTkLabel(self.weight_entry_frame, text="kg",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", anchor="w").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            
            self.weight_var.trace_add('write', weight_callback)
            
            '''BDAY'''
            self.bday_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.bday_frame.grid(row=5, column=1, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.bday_frame, text="Birthday: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.birthday_entry = ctk.CTkLabel(self.bday_frame, text="Set Birthday", fg_color=Color.White_Platinum, corner_radius=5,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.birthday_entry.pack(side="left", fill="both", expand=1, padx=(0), pady=(height*0.005))

            self.show_calendar = ctk.CTkButton(self.bday_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.birthday_entry, "%s", date_format="raw", max_date=datetime.datetime.now()))
            self.show_calendar.pack(side="left", padx=(width*0.0025), pady=(height*0.005))
            
            '''CONTACT ENTRY'''
            self.contact_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.contact_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.contact_frame, text="Contact#: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.contact_entry = ctk.CTkEntry(self.contact_frame, placeholder_text='Contact Number', font=("DM Sans Medium", 14), 
                                              placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion, textvariable=self.contact_var)
            self.contact_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
           
            self.contact_var.trace_add('write', contact_callback)
            
            '''ADDRESS ENTRY'''
            self.address_frame = ctk.CTkFrame(self.sub_frame, fg_color="transparent", height=height*0.065)
            self.address_frame.grid(row=7, column=0, columnspan=3, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
            
            ctk.CTkLabel(self.address_frame, text="Address: ",font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color="transparent", width=width*0.085, anchor="e").pack(side="left", padx=(width*0.005, 0),  pady=(height*0.01))
            self.address_entry = ctk.CTkEntry(self.address_frame, placeholder_text='Address', font=("DM Sans Medium", 14), placeholder_text_color="grey", border_width=2, fg_color=Color.White_Lotion)
            self.address_entry.pack(fill="both", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
           
            '''BOT FRAME'''
            self.bot_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.bot_frame.grid(row=2,column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))
           
            self.cancel_btn = ctk.CTkButton(self.bot_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left",) 
            
            self.add_btn = ctk.CTkButton(self.bot_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Add Record',
                                         command=proceed)
            self.add_btn.pack(side="right",)
            
            self.customer_selector = cctk.cctkSelector(self.master, (width, height), title="Customer Selector",
                                                        selector_table_query=sql_commands.get_all_customer,
                                                        selector_table_setup=f'/No:{int(width*0.035)}-#r/CustomerID:{int(width*0.085)}-tc/CustomerName:x-tl/ContactNumber:{int(width*0.225)}-tl!33!35',
                                                        selector_search_query=sql_commands.get_customer_quary_command,
                                                        command_callback=automate_fields)

            self.breed_option.set("")
            self.type_option.set("")
            self.sex_option.set("") 

            def check_for_names():
                txt = self.patient_name_entry.get()
                char_format = "qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM-' "

                if str.islower(txt[0]):
                    temp = txt[0].upper()
                    self.patient_name_entry.delete(0, 1)
                    self.patient_name_entry.insert(0, temp)

                for i in range(len(txt)):
                    if txt[i] not in char_format:
                        self.patient_name_entry.delete(i, i+1)

            def check_for_number():
                num = self.contact_entry.get()
                char_format = "1234567890"

                if num[0] != '+' or num[0] not in char_format:
                    temp = num[0].upper()
                    self.contact_entry.delete(0, 1)
                    self.contact_entry.insert(0, temp)

                for i in range(1, len(num), 1):
                    if num[i] not in char_format:
                        self.contact_entry.delete(i, i+1)

            self.breed_name_limiter = cctku.entry_limiter(64, self.breed_option._entry)
            self.contact_limiter = cctku.entry_limiter(20, self.contact_entry, check_for_number)
            self.address_limiter = cctku.entry_limiter(256, self.address_entry)
            self.patient_name_limiter = cctku.entry_limiter(128, self.patient_name_entry)

            self.patient_name_entry.configure(textvariable = self.patient_name_limiter)
            #self.owner_name_entry._entry.configure(textvariable = self.owner_name_limiter)
            self.breed_option._entry.configure(textvariable = self.breed_name_limiter)
            self.contact_entry.configure(textvariable = self.contact_limiter)
            self.address_entry.configure(textvariable = self.address_limiter)

        def place(self, **kwargs):
            self.owner_data= database.fetch_data(sql_commands.get_owners)
            self.data=[s[0] for s in self.owner_data] 
            self.pet_id.configure(text=f"{generateId('P', 6).upper()}")
            #self.pet_type_values = [data[0] for data in database.fetch_data("SELECT type From pet_breed")]   
            self.type_option.configure(values =  [data[0] for data in database.fetch_data("SELECT type From pet_breed GROUP BY type")] )
            #self.owner_name_entry.configure(values = [s[0] for s in database.fetch_data(sql_commands.get_owners)])
            return super().place(**kwargs)
    return instance(master, info, table_update_callback)

def view_record(master, info:tuple, table_update_callback: callable):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple,table_update_callback: callable ):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            #print(acc_cred,acc_info)
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

            def reset():
                cancel_changes()
                self.entries_set_state("normal")
                self.reset_entries()
                self.place_forget()
            
            def edit_entries():
                
                self.pet_name_entry.configure(state = ctk.NORMAL)
                self.type_entry.configure(state = ctk.NORMAL)
                self.sex_entry.configure(state = ctk.NORMAL)
                self.breed_entry.configure(state = ctk.NORMAL)
                self.weight_entry.configure(state = ctk.NORMAL)
                self.birthday_entry.configure(state = ctk.NORMAL)
                
                
                
                self.pet_id.configure(state="disabled", fg_color=Color.White_Lotion)
                
                self.edit_info_button.grid_forget()
                self.save_info_button.grid(row=0, column=4, sticky="nse",  pady=(height*0.01))
                
                self.cancel_edit.grid(row=0, column=5, sticky="nsw", padx=(width*0.005), pady=(height*0.01))
                
                self.sex_entry_option.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.type_entry_option.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.breed_entry_option.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.bday_frame.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                
                self.sex_entry_option.set(self.sex_entry.get())
                self.type_entry_option.set(self.type_entry.get())
                self.breed_entry_option.set(self.breed_entry.get())
                self.bday_new_entry.configure(text = self.birthday_entry.get())
                
                self.type_entry.pack_forget()
                self.sex_entry.pack_forget()
                self.breed_entry.pack_forget()
                self.birthday_entry.pack_forget()
                
            def cancel_changes():
                self.edit_info_button.grid(row=0, column=4, sticky="nse",  pady=(height*0.01),padx=(width*0.005)) 
                self.save_info_button.grid_forget()
                #self.image_edit.grid_forget()
                
                self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.type_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.breed_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.birthday_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                
                self.set_entries(self.data)
                self.entries_set_state("disabled")
                
                self.bday_frame.pack_forget()
                self.sex_entry_option.pack_forget()
                self.type_entry_option.pack_forget()
                self.breed_entry_option.pack_forget()
                self.cancel_edit.grid_forget()
                
            def save_changes():
                self.edit_info_button.grid(row=0, column=4, sticky="nse",  pady=(height*0.01),padx=(width*0.005)) 
                self.save_info_button.grid_forget()
                #self.image_edit.grid_forget()
                
                self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.type_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.breed_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                self.birthday_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
                
                self.sex_entry.delete(0, ctk.END)
                self.type_entry.delete(0, ctk.END)
                self.birthday_entry.delete(0, ctk.END)
                self.breed_entry.delete(0, ctk.END)
                
                self.breed_entry.insert(0, f"{self.breed_entry_option.get()}")
                self.sex_entry.insert(0, f"{self.sex_entry_option.get()}")
                self.type_entry.insert(0, f"{self.type_entry_option.get()}")
                self.birthday_entry.insert(0, f"{self.bday_new_entry._text}")
                
                self.entries_set_state("disabled")
                
                self.sex_entry_option.pack_forget()
                self.type_entry_option.pack_forget()
                self.breed_entry_option.pack_forget()
                self.bday_frame.pack_forget()
                self.cancel_edit.grid_forget()
                 
                database.exec_nonquery([[sql_commands.update_pet_record_pet_info, (self.pet_name_entry.get(), self.breed_entry.get(), self.type_entry.get(), self.sex_entry.get(), self.weight_entry.get(), self.birthday_entry.get(), acc_cred[0][0], self.pet_id.get())]])
                                        #[sql_commands.update_pet_record_pet_owner, (self.owner_name_entry.get(), self.address_entry.get(), self.contact_no_entry.get(), self.pet_id.get())]])
            
                messagebox.showinfo(title=None, message="Pet Information Successfully Changed!", parent = self)
                self.callback_command()
            
            def pet_type_callback(var):
                self.values = [val[0] for val in database.fetch_data(f"SELECT breed From pet_breed WHERE pet_breed.type = '{var}'")]
                self.breed_entry_option.configure(values = self.values)
            
            def open_histoy_log():
                temp = database.fetch_data("SELECT added_by, CAST(date_added AS DATE), updated_by, CAST(updated_date AS DATE) FROM pet_info WHERE id = ?", (self.pet_id.get(),))
                self.history_log.place(relx=0.5, rely=0.5, anchor = 'c', info=temp)
            
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
            self.pet_info_frame.grid_columnconfigure(4, weight=1)

            #self.image_edit = ctk.CTkButton(self.pet_image_frame, image=self.camera_icon, text='', width=width*0.01, height=height*0.05, fg_color="#83bd75", hover_color="#82bd0b",)
            
            self.pet_name_frame = ctk.CTkFrame(self.pet_info_frame, fg_color="transparent")
            self.pet_name_frame.grid(row=0, column=1, stick="nsew",padx=(width*0.005), pady=(height*0.01), columnspan=2,)
            self.pet_id = ctk.CTkEntry(self.pet_name_frame, border_width=0,font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, justify="center",height=height*0.05, border_color=Color.White_Lotion)
            self.pet_id.pack(side="left",padx=(0,width*0.005), fill="both", expand=1)
            self.pet_entry_frame = ctk.CTkFrame(self.pet_name_frame, height = height*0.05, fg_color=Color.White_Lotion)
            self.pet_entry_frame.pack(side="left", fill="both",expand=1)
            self.pet_name_entry = ctk.CTkEntry(self.pet_entry_frame, border_width=0, font=("DM Sans Medium", 16), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5,height=height*0.05)
            self.pet_name_entry.pack(side="left", fill='x', expand=1,  padx=(width*0.0025), pady=(height*0.0025))
            
            self.info_log = ctk.CTkButton(self.pet_info_frame, text='', image=Icons.get_image('info_icon', (30,30)),height=height*0.05, width=height*0.05, command=open_histoy_log)
            self.info_log.grid(row=0, column=3, sticky="nsw",  pady=(height*0.01), padx=(0,width*0.005))
            
            self.edit_info_button = ctk.CTkButton(self.pet_info_frame, image=self.add_icon, text='Edit', font=("DM Sans Medium", 14), width=width*0.01, fg_color="#3b8dd0", command=edit_entries)
            self.edit_info_button.grid(row=0, column=4, sticky="nse",  pady=(height*0.01), padx=(width*0.005))

            self.save_info_button = ctk.CTkButton(self.pet_info_frame, image=self.save_icon, text='Update Record',font=("DM Sans Medium", 14), width=width*0.01, fg_color="#83bd75", hover_color=Color.Green_Button_Hover_Color, command=save_changes)
            self.cancel_edit = ctk.CTkButton(self.pet_info_frame, text="Cancel", hover_color=Color.Red_Pastel, fg_color=Color.Red_Tulip, font=("DM Sans Medium", 14), width=width*0.015, command=cancel_changes)
            
            '''Breed'''           
            self.breed_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.breed_frame.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.breed_frame, text='Breed:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.breed_entry = ctk.CTkEntry(self.breed_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.breed_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''Type'''
            self.type_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.type_frame.grid(row=1, column=1, sticky="nsew", padx=(width*0.005,0),  pady=(0,height*0.01))
            ctk.CTkLabel(self.type_frame, text='Pet Type:',  font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.type_entry = ctk.CTkEntry(self.type_frame,border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.type_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''Weight'''
            self.weight_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.weight_frame.grid(row=3, column=1, sticky="nsew", padx=(width*0.005,0),  pady=(0,height*0.01))
            ctk.CTkLabel(self.weight_frame, text='Weight:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.weight_entry = ctk.CTkEntry(self.weight_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.075, justify='right')
            self.weight_entry.pack(side="left", padx=(0, width*0.0025), pady=(height*0.005))
            ctk.CTkLabel(self.weight_frame, text='kg', font=("DM Sans Medium", 14), anchor='e',).pack(side="left", padx=(0, width*0.005))
            
            
            '''Sex'''
            self.sex_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.sex_frame.grid(row=1, column=2, sticky="nsew", padx=(width*0.005),  pady=(0,height*0.01))                    
            ctk.CTkLabel(self.sex_frame, text='Sex:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.sex_entry = ctk.CTkEntry(self.sex_frame, border_width=0, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.sex_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''Birthday'''
            self.birthday_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.birthday_frame.grid(row=3, column=2, sticky="w", padx=(width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.birthday_frame, text='Birthday:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.birthday_entry = ctk.CTkEntry(self.birthday_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.birthday_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''Owner'''
            self.owner_name_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.owner_name_frame.grid(row=1, column=3,columnspan=3, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.owner_name_frame, text='Owner\'s Name:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.owner_name_entry = ctk.CTkEntry(self.owner_name_frame,  border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.owner_name_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''Address'''
            self.address_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.address_frame.grid(row=2, column=3,columnspan=3, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.address_frame, text='Address:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.address_entry = ctk.CTkEntry(self.address_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.address_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            '''Contact'''
            self.contact_no_frame = ctk.CTkFrame(self.pet_info_frame, fg_color=Color.White_Color[3])
            self.contact_no_frame.grid(row=3, column=3,columnspan=3, sticky="nsew", padx=(0,width*0.005),  pady=(0,height*0.01))
            ctk.CTkLabel(self.contact_no_frame, text='Contact#:', font=("DM Sans Medium", 14), width=width*0.05, anchor='e',).pack(side="left", padx=(width*0.005, width*0.001))
            self.contact_no_entry = ctk.CTkEntry(self.contact_no_frame, border_width=0,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, height=height*0.05)
            self.contact_no_entry.pack(side="left", fill="x", expand=1, padx=(0, width*0.0025), pady=(height*0.005))
            
            self.pet_service_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Platinum)
            self.pet_service_frame.grid(row=2,column=0, sticky="nsew", padx=(width*0.005), pady=(0,height*0.01))

            self.service_title_frame = ctk.CTkFrame(self.pet_service_frame, fg_color="transparent")
            self.service_title_frame.pack(fill = 'x', padx=(width*0.005),  pady=(height*0.01))
            
            self.service_title_label = ctk.CTkLabel(self.service_title_frame, text="Service Record", font=("DM Sans Medium", 14), height=height*0.055,corner_radius=5,
                                                    fg_color=Color.White_Color[3], text_color=Color.Blue_Maastricht, padx=width*0.05)
            self.service_title_label.pack(side="left")
            self.refresh_btn = ctk.CTkButton(self.service_title_frame, image=self.refresh_icon, text='', width=height*0.055, height=height*0.055, fg_color="#83bd75", hover_color=Color.Green_Button_Hover_Color, command = self.refresh)
            self.refresh_btn.pack(side="left",  padx=(width*0.005))
            
            self.service_treeview_frame = ctk.CTkFrame(self.pet_service_frame, fg_color="transparent")
            self.service_treeview_frame.pack(fill='both', expand=1,  padx=(width*0.005),  pady=(0,height*0.01))
            
            '''Service Record Treeview'''
            
            self.pet_data_view = cctk.cctkTreeView(self.service_treeview_frame, data=[],width= width * 0.795, height= height * 0.45, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/Service:x-tl/Date:{int(width*.2)}-tc/Cashier:{int(width*.15)}-tl!33!35',)
            self.pet_data_view.pack()
            #self.set_entries()
            self.entries = (self.pet_id, self.pet_name_entry, self.type_entry, self.sex_entry, self.breed_entry, 
                             self.weight_entry, self.birthday_entry, 
                            self.owner_name_entry, self.address_entry,self.contact_no_entry)
            
            '''Replace entries with option mene when editing'''
            self.sex_entry_option = ctk.CTkOptionMenu(self.sex_frame, values=["Male","Female"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum, height=height*0.05)
            self.type_entry_option = ctk.CTkOptionMenu(self.type_frame, values=["Dog","Cat"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum, height=height*0.05, command=pet_type_callback)
            self.breed_entry_option = ctk.CTkOptionMenu(self.breed_frame, values=["Dog","Cat"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum, height=height*0.05)
        
            self.bday_frame = ctk.CTkFrame(self.birthday_frame, fg_color="transparent", height=height*0.065)
            
            self.bday_new_entry = ctk.CTkLabel(self.bday_frame, text="Set Birthday", fg_color=Color.White_Platinum,  width=width*0.1, corner_radius=5,font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht)
            self.bday_new_entry.pack(side="left", fill="both", expand=1, padx=(0), pady=(height*0.001))

            self.show_calendar = ctk.CTkButton(self.bday_frame, text="",image=Icons.get_image('calendar_icon', (20,20)), height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.bday_new_entry, "%s", date_format="raw", max_date=datetime.datetime.now()))
            self.show_calendar.pack(side="left", padx=(width*0.0025), pady=(height*0.001))
        
            self.history_log = audit_popup.audit_info(self, (width, height))
        
            self.no_service_data = ctk.CTkLabel(self.pet_data_view, text="No service data for this record.", font=("DM Sans Medium",14), )

        def refresh(self):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.pet_data_view.pack_forget()
            self.load_history()
            self.pet_data_view.pack()
            self.refresh_btn.after(100, lambda: self.refresh_btn.configure(state = ctk.NORMAL))

            
        def reset_entries(self):
            for i in range(len(self.entries)):
                self.entries[i].delete(0, tk.END) 

        def entries_set_state(self,state : str = "normal", color_normal :str = Color.White_Lotion, color_disabled :str = Color.White_Lotion):
            for i in range(len(self.entries)):
                if "normal" in state:
                    set_color = color_normal
                    bd = 2
                elif "disabled" in state:
                    set_color = color_disabled
                    bd = 0
                self.entries[i].configure(state=state, fg_color=set_color, border_width = bd)
            
        def set_entries(self, pet_values):
            self.reset_entries()
            for i in range(len(self.entries)):
                self.entries[i].insert(0, pet_values[0][i])
            
            self.service_title_label.configure(text=f"{pet_values[0][1]}'s Service Record")
            #self.pet_id.configure(state="disabled")
            self.entries_set_state("disabled")
            
        def place(self, pet_data, **kwargs):
            self.data = database.fetch_data(sql_commands.get_pet_view_record, (f'{pet_data[0]}',))
            breed = [data[0] for data in database.fetch_data("SELECT breed FROM pet_breed")]
            self.breed_entry_option.configure(values = breed)
            self.set_entries(self.data)
            self.load_history()
            
            
            return super().place(**kwargs)
        
        def load_history(self):
            svc_data = database.fetch_data(sql_commands.get_specific_pet_record, (self.pet_id.get(), ))
            self.pet_data_view.update_table(svc_data)
            self.no_service_data.place(relx=0.5, rely=0.5, anchor='c') if not svc_data else self.no_service_data.place_forget()
            
            #data = '''
    return instance(master, info, table_update_callback)