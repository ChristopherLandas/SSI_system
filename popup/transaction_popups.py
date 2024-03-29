import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
from constants import action
import datetime
from datetime import date
from datetime import datetime
from datetime import timedelta
from PIL import Image
import copy
import network_socket_util as nsu
import json
from popup import dashboard_popup, mini_popup

from popup import preview_pdf_popup as ppdfp

IP_Address = json.load(open("Resources\\network_settings.json"))
PORT_NO: dict = json.load(open("Resources\\port_no.json"))
GEN_SETTINGS: dict = json.load(open("Resources\\general_settings.json"))

def scheduled_services(master, info:tuple, parent= None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)

            global IP_Address, PORT_NO
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

            def hide():
                self.place_forget()

            self._master = master

            self.main_frame = ctk.CTkFrame(self, width=width*0.815, height=height*0.885, corner_radius=0)
            self.main_frame.pack(padx=1,pady=1)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Scheduled Services', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=hide).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=5)
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(2, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            self.content_frame.grid_propagate(0)

            """ self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.005),pady=(height*0.01), sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("DM Sans Medium", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="grey",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.0025)) """

            self.resched_option_btn = ctk.CTkButton(self.content_frame, width * .075, height*0.05, text='Reschedule', font= ("DM Sans Medium", 14), command= self.resched_btn_callback)
            self.resched_option_btn.grid(row=0, column=1,padx=(width*0.005),pady=(height*0.01),sticky="w")

            self.refresh_btn = ctk.CTkButton(self.content_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command= self.update_treeview)
            self.refresh_btn.grid(row=0, column=2,padx=(0,width*0.005),pady=(height*0.01),sticky="w")

            self.sched_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.sched_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))

            self.sched_treeview = cctk.cctkTreeView(self.sched_frame, data =[], width=width*0.8, height=height*0.7,
                                                    column_format=f'/No:{int(width*.035)}-#r/ReceptionID:{int(width*.115)}-tc/Owner:x-tl/Pet:x-tl/Service:{int(width*.12)}-tl/Total:{int(width*.085)}-tr/Date:{int(width*.135)}-tc!33!35',)
            #                                   column_format=f'/No:{int(width*.025)}-#r/OR:{int(width*0.05)}-tc/ClientName:x-tl/Service:{int(width*.15)}-tr/Schedule:{int(width*.1)}-tc/Action:{int(width*.08)}-bD!30!30',)
            self.update_treeview()
            self.sched_treeview.pack()

        def update_treeview(self):
            self.sched_treeview.pack_forget()
            self.sched_treeview.update_table(database.fetch_data(sql_commands.get_all_schedule))
            self.sched_treeview.pack()

        def resched_btn_callback(self, _: any = None):
            if self.sched_treeview.get_selected_data():
                dashboard_popup.rescheduling_service_info(self, (self.width, self.height)).place(relx = .5, rely = .5, anchor = 'c', uid= self.sched_treeview.get_selected_data()[0], update_treeview_callback= self.update_treeview)
                #code for reshceduling here
            else:
                messagebox.showerror("Unable to Proceed", "Select a service to resched", parent = self)

    return instance(master, info, parent)

def add_particulars(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func_item, change_val_func_service, service_dict: dict, change_total_val_serv_callback: callable) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func_item, change_val_func_service, service_dict: dict, change_total_val_serv_callback: callable):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            global IP_Address, PORT_NO

            '''internal data'''
            self.total_transaction_count = 0
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self._service_dict = service_dict
            self.change_total_val_serv_callback = change_total_val_serv_callback

            def hide():
                self.place_forget()
            def item_proceed(_: any = None):
                if self.item_treeview.get_selected_data() or self.service_treeview.get_selected_data():
                    data = self.item_treeview._data[self.item_treeview.data_frames.index(self.item_treeview.data_grid_btn_mng.active)]
                    add_data = (data[1], data[3], data[3])
                    #print(add_data)
                    if data[1] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[1])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, data[2]))
                        change_val_func_item(price_format_to_float(data[3][1:]))
                        #price = price_format_to_float(data_frames.winfo_children()[2]._text[1:])

                        def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            temp_data = root_treeview._data[root_treeview.data_frames.index(temp_frame)]
                            temp_data = (temp_data[0], temp_data[1], spinner.value, '₱' + format_price(price_format_to_float(temp_data[1][1:]) * spinner.value))
                            root_treeview._data[root_treeview.data_frames.index(temp_frame)] = temp_data
                            change_val_func_item(-price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[2]._text[1:])
                            temp_frame.winfo_children()[4].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func_item(price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))

                        spinner.configure(command = spinner_command)
                    self.place_forget()

                
            def service_proceed(_: any = None):
                
                if len(self.client) < 1:
                    messagebox.showerror('Invalid Process', 'The client have no customer record or pet in the record', parent = self)
                    return
                elif self.service_treeview.data_grid_btn_mng.active:
                    data = self.service_treeview._data[self.service_treeview.data_frames.index(self.service_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[1], data[1])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[2].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        data_frames: cctk.ctkButtonFrame = root_treeview.data_frames[-1]

                        label: ctk.CTkLabel = data_frames.winfo_children()[1]
                        label_text = copy.copy(label._text)
                        label.destroy()
                        #destroy the label

                        import serviceAvailing
                        def proceed_command(data):
                            self._service_dict[label_text] = data

                        new_button = ctk.CTkButton(data_frames, corner_radius= 0, anchor= 'w', font=self.service_treeview.row_font,
                                                   text="  "+label_text, width = root_treeview.column_widths[1])
                        def temp_command():
                            new_button.configure(state = ctk.DISABLED)
                            serviceAvailing.pets(root_treeview.master.master, spinner.value, label_text, [s[1] for s in self.client],
                                                 proceed_command, None, width=width, height=height,fg_color= 'transparent').place(relx = .5, rely = .5, anchor = 'c',
                                                                                                                                                        service_dict= self._service_dict,
                                                                                                                                                        root_treeview=root_treeview,
                                                                                                                                                        change_total_val_serv_callback= self.change_total_val_serv_callback,
                                                                                                                                                        master_frame= data_frames,
                                                                                                                                                        master_btn= new_button)
                        new_button.configure(command = temp_command)
                        #make a button
                        for i in data_frames.winfo_children():
                            i.pack_forget()
                        modified_data_frames:list = data_frames.winfo_children()
                        modified_data_frames.insert(1, new_button)
                        for i in modified_data_frames:
                            i.pack(fill = 'y', side = 'left', padx = (1,0))
                        #repack the button frame/data frame
                        #make the label as button for patient access

                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data

                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[2].winfo_children()[0]
                        spinner.configure(val_range = (1, len(self.client)))
                        change_val_func_service(price_format_to_float(data[1][1:]))
                        def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            temp_data = root_treeview._data[root_treeview.data_frames.index(temp_frame)]
                            temp_data = (temp_data[0], temp_data[1], spinner.value, '₱' + format_price(price_format_to_float(temp_data[1][1:]) * spinner.value))
                            root_treeview._data[root_treeview.data_frames.index(temp_frame)] = temp_data
                            change_val_func_service(-price_format_to_float(temp_frame.winfo_children()[3]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[1]._text[1:])
                            temp_frame.winfo_children()[3].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func_service(price_format_to_float(temp_frame.winfo_children()[3]._text[1:]))
                        spinner.configure(command = spinner_command)
                        spinner.configure(mode = cctk.cctkSpinnerCombo.CLICK_ONLY)
                        #set the spinner combo of the table
                self.place_forget()
                
            def filter_func(value):
                if "All" in value:
                    self.service_frame.grid_forget()
                    self.item_frame.grid_forget()
                    self.service_frame.grid(row=1,column=0, columnspan=2, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
                    self.item_frame.grid(row=2, column=0, columnspan=2 ,sticky="nsew",  padx=(width*0.005),pady=(0, height*0.01))
                    
                    self.service_treeview.pack()
                    self.service_treeview.configure(height=height*0.4)
                    self.item_treeview.pack()
                    self.item_treeview.configure(height=height*0.4)
                elif "Service" in value:
                    self.service_frame.grid(row=1,column=0, columnspan=2, rowspan=2, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
                    self.service_treeview.pack()
                    
                    self.item_frame.grid_forget()
                    self.item_treeview.pack_forget()
                    self.service_treeview.configure(height=height*0.75)
                    
                elif "Item" in value:
                    self.item_frame.grid(row=1, column=0, columnspan=2 , rowspan=2 ,sticky="nsew",  padx=(width*0.005),pady=(0, height*0.01))
                    self.item_treeview.pack()
                    
                    self.service_frame.grid_forget()
                    self.service_treeview.pack_forget()
                    self.item_treeview.configure(height=height*0.75)
                    
                    
                    
            self.filter_optionmenu_var = ctk.StringVar(value="All") 

            self.main_frame = ctk.CTkFrame(self, width=width*0.815, height=height*0.875, corner_radius=0,fg_color=Color.White_Color[3])
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='PARTICULARS', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.content_frame.grid(row=1, column=0,columnspan=2, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure((1,2), weight=1)
                
            self.filter_optionmenu = ctk.CTkOptionMenu(self.content_frame, width=width*0.1, height=height*0.045, fg_color=Color.Blue_Tufts, values=["All", "Services", "Items"], anchor="center", font=("DM Sans Medium", 14),
                                                       dropdown_font=("DM Sans Medium",14))
            self.filter_optionmenu.configure(command=filter_func)
            self.filter_optionmenu.grid(row=0, column=0, sticky="nsw", padx=(width*0.005), pady=(height*0.01))
            
            self.service_frame = ctk.CTkFrame(self.content_frame, corner_radius=0)
            self.service_frame.pack_propagate(0)
            
            self.service_treeview = cctk.cctkTreeView(self.service_frame, height=height*0.4, width=width*0.805,corner_radius=0,double_click_command=service_proceed, column_format=f"/No:{int(width*.035)}-#r/ServiceName:x-tl/Price:x-tr!30!30")

            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0)
            self.item_frame.pack_propagate(0)
            
            #self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.item_frame, data=[], height=height*0.4, width=width*0.805,double_click_command=item_proceed, column_format=f"/No:{int(width*.035)}-#r/ItemBrand:{int(width*.085)}-tl/ItemDescription:x-tl/StockPcs:{int(width*.115)}-tr/Price:{int(width*.115)}-tr!30!30",)
            #self.item_treeview.pack()
            
            filter_func("All")
            
        def reset(self):
            
            self.place_forget()

        def place(self, **kwargs):
            try:
                if('client' in kwargs):
                    self.check_client(kwargs['client'])
                    kwargs.pop('client')
                return super().place(**kwargs)
            finally:
                count_temp = database.fetch_data("SELECT COUNT(*) FROM transaction_record")[0][0]
                if count_temp != self.total_transaction_count or count_temp == 0:
                    self.service_treeview.pack_forget()
                    self.item_treeview.pack_forget()
                    self.update_service()
                    self.update_items_stocks()
                    self.total_transaction_count = count_temp
                    self.service_treeview.pack()
                    self.item_treeview.pack()

            #update the particulars if it's not been updated yet
            #update could be triggered by every invoice saved
            
        
        def update_service(self):
            raw_data = database.fetch_data(sql_commands.get_services_and_their_price_test)
            self.service_treeview.update_table([(s[1], s[2]) for s in raw_data])

        def update_items_stocks(self):
            data = [(data[0], f"{data[1]} ({data[2]})", data[3], data[4]) if data[2] else (data[0], data[1], data[3], data[4]) for data in database.fetch_data(sql_commands.get_item_and_their_total_stock, None)]
            self.item_treeview.update_table(data)
        
        def check_client(self, client_name: str):
            self.client = database.fetch_data(sql_commands.get_pet_info, (client_name, ))

        def place_forget(self):
            if self.item_treeview.data_grid_btn_mng.active:
                self.item_treeview.data_frames[self.item_treeview._data.index(self.item_treeview.get_selected_data())].response()
            if self.service_treeview.data_grid_btn_mng.active:
                self.service_treeview.data_frames[self.service_treeview._data.index(self.service_treeview.get_selected_data())].response()
            return super().place_forget()
            
    return instance(master, info, root_treeview, change_val_func_item, change_val_func_service, service_dict, change_total_val_serv_callback)

def add_invoice(master, info:tuple, treeview_content_update_callback: callable, attendant: str):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, treeview_content_update_callback: callable):
            width = info[0]
            height = info[1]
            super().__init__(master,width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")
            self.services_lists = [s[0] for s in database.fetch_data("SELECT service_name FROM service_info_test GROUP BY UID")]
            self.invoice_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
            self._attentdant: str = attendant
            self.customer_infos = []
            self.service_dict: dict = {}

            self._treeview_content_update_callback = treeview_content_update_callback

            '''constants'''
            self.services = [s[0] for s in database.fetch_data(sql_commands.get_service_data)]

            global IP_Address, PORT_NO

            '''events'''
            def bd_commands(i):
                if self.transact_treeview._data[i][0] in [s[0] for s in database.fetch_data(sql_commands.get_services_names)]:
                    #self.patient_info.value = None
                    self.change_total_value_service(-price_format_to_float(self.transact_treeview._data[i][-1][1:]))
                else:
                    self.change_total_value_item(-price_format_to_float(self.transact_treeview._data[i][3][1:]))

            def change_customer_callback(_:any):
                if len(self.transact_treeview._data) != 0:
                    if messagebox.askyesno('Change Customer', 'Changing customer will reset the content of treeview', parent = self):
                        client = self.client_name_entry.get()
                        self.client_name_entry.set(client)

                        self.save_invoice_btn.configure(state = ctk.NORMAL)
                        self.cancel_invoice_btn.configure(state = ctk.NORMAL)
                        self.transact_treeview.delete_all_data()
                        self.services_total_amount.configure(text = format_price(0))
                        self.item_total_amount.configure(text = format_price(0))
                        self.price_total_amount.configure(text = format_price(0))
                        self.service_dict.clear()
                        del client

                        '''initial process'''

            def save_invoice_callback():
                
                if self.client_name_entry.get().strip() == "":
                    messagebox.showwarning("Warning", "There is no client name")
                    return
                if len(self.transact_treeview._data) == 0:
                    messagebox.showwarning("Warning", "There is no record to be saved")
                    return
                for dt in self.transact_treeview._data:
                    if(dt[0] in self.service_dict and dt[0] in self.services_lists):
                        for li in self.service_dict[dt[0]]:
                            if li[0] == '':
                                messagebox.showwarning("Cannot Proceed", "Fill the remaining Information", parent = self)
                                return
                    elif(dt[0] not in self.service_dict and dt[0] in self.services_lists):
                        messagebox.showwarning("Cannot Proceed", "Fill the remaining Information", parent = self)
                        return
                
                services = []
                items = []
                for st in self.transact_treeview._data:
                    if(st[0] in self.service_dict):
                        services.append(st)
                    else:
                        items.append(st)
                formatted_svc_data = []
                
                uid = self.invoice_id_label._text
                uid_base = uid[0:-2]
                uid_count = int(uid[-2:])

                prev_date = None
                cur_index = -1
                for svc_k in self.service_dict.keys():
                    for inf in self.service_dict[svc_k]:
                        owner = database.fetch_data("SELECT owner_id from pet_owner_info WHERE owner_name = ?", (self.client_name_entry.get(), ))[0][0]
                        pet_uid = database.fetch_data("SELECT id FROM pet_info WHERE p_name = ? AND owner_id = ?", (inf[0], owner))[0][0]
                        if prev_date != inf[1]:
                            prev_date = inf[1]
                            cur_index += 1
                            formatted_svc_data.append([])

                        modifiable_svc = database.fetch_data("SELECT service_name, price FROM service_info_test")
                        svc_prices = {s[0]: s[1] for s in modifiable_svc}
                        
                        if len(inf) == 2:
                            #formatted_svc_data[cur_index].append((f"{uid_base}{str(int(uid_count) + cur_index).zfill(2)}", database.fetch_data(sql_commands.get_service_uid, (svc_k, ))[0][0], svc_k, pet_uid, inf[0], inf[1], svc_prices[svc_k], 0, None, None, None))
                            formatted_svc_data[cur_index].append((database.fetch_data(sql_commands.get_service_uid, (svc_k, ))[0][0], svc_k, pet_uid, inf[0], inf[1], svc_prices[svc_k], 0, None, None, None))
                            #scheduled service
                        if len(inf) == 3:
                            prevtime = datetime.strptime(inf[2], '%Y-%m-%d') - datetime.strptime(inf[1], '%Y-%m-%d')
                            #formatted_svc_data[cur_index].append((f"{uid_base}{str(int(uid_count) + cur_index).zfill(2)}", database.fetch_data(sql_commands.get_service_uid, (svc_k, ))[0][0], svc_k, pet_uid, inf[0], inf[1], (svc_prices[svc_k] * (prevtime.days + 1)), 0, inf[2], None, None))
                            formatted_svc_data[cur_index].append((database.fetch_data(sql_commands.get_service_uid, (svc_k, ))[0][0], svc_k, pet_uid, inf[0], inf[1], (svc_prices[svc_k] * (prevtime.days + 1)), 0, inf[2], None, None))
                            #periodic service
                        if len(inf) == 4:
                            price = svc_prices[svc_k] * int(inf[3])
                            #formatted_svc_data[cur_index].append((f"{uid_base}{str(int(uid_count) + cur_index).zfill(2)}", database.fetch_data(sql_commands.get_service_uid, (svc_k, ))[0][0], svc_k, pet_uid, inf[0], inf[1], price, 0, None, int(inf[2]), int(inf[3])))
                            formatted_svc_data[cur_index].append((database.fetch_data(sql_commands.get_service_uid, (svc_k, ))[0][0], svc_k, pet_uid, inf[0], inf[1], price, 0, None, int(inf[2]), int(inf[3])))
                            #multiple instance periodic service

                
                """RECORDING THE INVOICE"""
                if len(items)> 0:
                    if database.exec_nonquery([[sql_commands.insert_invoice_data, (uid, self._attentdant, self.client_name_entry.get() or 'Client Name' , price_format_to_float(self.item_total_amount._text[1:]), None, datetime.now().strftime('%Y-%m-%d'), 0, None, 0)]]):
                        for it in items:
                            temp = (split_unit(it[0])+(it[1:]))
                            #print(temp, len(temp))
                            if len(temp) == 5: # WIth UNIT SAVING
                                database.exec_nonquery([[sql_commands.insert_invoice_item_data, (uid, database.fetch_data(sql_commands.get_uid, (temp[0], temp[1]))[0][0], f'{temp[0]} ({temp[1]})', temp[3], price_format_to_float(temp[2][1:]), 0)]])
                            else: # WITHOUT UNIT SAVING
                                database.exec_nonquery([[sql_commands.insert_invoice_item_data, (uid, database.fetch_data(sql_commands.get_uid_null_unit, (temp[0],))[0][0], temp[0], temp[2], price_format_to_float(temp[1][1:]), 0)]])
                        uid_count += 1
                    #recording of item based on the invoice_id

                #services_price = sum([sum([s[6] for s in li]) for li in formatted_svc_data])
                if len(formatted_svc_data) > 0:
                    for svcs in formatted_svc_data:
                        for li in svcs:
                            svc_uid = uid_base + str(uid_count).zfill(2)
                            if database.exec_nonquery([[sql_commands.insert_invoice_data, (svc_uid, self._attentdant, self.client_name_entry.get() or 'Client Name', li[-5], None, datetime.now().strftime('%Y-%m-%d'), 0, None, 1)]]):
                                database.exec_nonquery([[sql_commands.insert_invoice_service_data, (svc_uid, ) + li]])
                                uid_count += 1
                #recording of service based on the invoice_id



                self._treeview_content_update_callback()
                self.save_invoice_btn.configure(state = ctk.DISABLED)
                self.cancel_invoice_btn.configure(state = ctk.DISABLED)
                record_action(self._attentdant, action.INVOICE_TYPE, action.MAKE_INVOICE % (self._attentdant, uid))
                messagebox.showinfo('Success', 'Reception record is saved', parent = self)
                self.reset(True)
                
            def open_particulars():
                if self.client_name_entry.get().strip() =="":
                    messagebox.showwarning("Missing Input", "Select a customer or enter their surname for identification.", parent=self)
                else:
                    self.show_particulars.place(relx=0.5, rely=0.5, anchor="c", client = self.client_name_entry.get())

                
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], corner_radius=0)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.02)

            self.main_frame.grid_columnconfigure(2, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
            self.top_frame.pack_propagate(0)
            #self.invoice_icon
            ctk.CTkLabel(self.top_frame, text='',image=Icons.get_image('histlogs_icon', (15,18))).pack(side="left", padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text='ADD TRANSACTION RECORD', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.005,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.025, command=self.reset).pack(side="right", padx=(0,width*0.01))

            self.invoice_id_label =ctk.CTkLabel(self.main_frame, text="__",  width=width*0.085, height=height*0.055, font=("DM Sans Medium", 16), fg_color=Color.White_Platinum, corner_radius=5)
            self.invoice_id_label.grid(row=1, column=0, sticky="w", padx=(width*0.005), pady=(height*0.01))

            self.client_name_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum, width=width*0.35, height=height*0.055)
            self.client_name_frame.grid(row=1, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))
            self.client_name_frame.pack_propagate(0)

            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
            self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

            self.client_name_entry = ctk.CTkOptionMenu(self.client_name_frame,font=("DM Sans Medium", 15), fg_color="white", text_color=Color.Blue_Maastricht, command= change_customer_callback, dropdown_font=("DM Sans Medium", 14),
                                                     height=height*0.055, button_color=Color.Blue_Steel, button_hover_color=Color.Blue_Cobalt)
            self.client_name_entry.set('')
            self.client_names = [s[0] for s in database.fetch_data(sql_commands.get_owners)]
            self.client_name_entry.configure(values = self.client_names)
            self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005,width*0.0025), pady=(width*0.0025))
            
            self.add_particulars: add_particulars = ctk.CTkButton(self.main_frame,text="Add Particulars", width=width*0.125, height=height*0.055, image=self.add_icon, font=("DM Sans Medium", 14),
                                               command=open_particulars)
            self.add_particulars.grid(row=1, column=2, sticky="w")

            self.transact_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0 )
            self.transact_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0))

            self.transact_treeview = cctk.cctkTreeView(self.transact_frame, data=[], width=width*0.8, height=height*0.685,
                                                    column_format=f'/No:{int(width*0.035)}-#r/Particulars:x-tl/UnitPrice:{int(width*0.1)}-tr/Quantity:{int(width*0.115)}-id/Total:{int(width*0.1)}-tr/Action:{int(width*.065)}-bD!33!35')
            self.transact_treeview.pack(pady=(0,0))
            self.transact_treeview.bd_commands = bd_commands
            
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=height*0.055)
            self.bottom_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=(width*0.005), pady=(height*0.01))

            #self.add_particulars = ctk.CTkButton(self.bottom_frame, width=width*0.125, height=height*0.05, text='Add Particulars',
            #                                   image=self.add_icon, command=lambda:self.show_particulars.place(relx=0.5, rely=0.5, anchor="c", client = self.client_name_entry.get()))
            
            self.price_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.185, height=height*0.055, fg_color=Color.White_Platinum)
        
            ctk.CTkLabel(self.price_total_frame, fg_color=Color.White_Platinum, text="Grand Total:", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.0075,0))
            self.price_total_amount = ctk.CTkLabel(self.price_total_frame, text="₱0,000.00", fg_color=Color.White_Platinum, font=("DM Sans Medium", 16))
            self.price_total_amount.pack(side="right",  padx=(0,width*0.0075))
            
            self.item_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.185, height=height*0.055, fg_color=Color.White_Platinum)

            ctk.CTkLabel(self.item_total_frame, text="Item Total:", fg_color=Color.White_Platinum, font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.0075,0))
            self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text="₱0,000.00", fg_color=Color.White_Platinum, font=("DM Sans Medium", 16))
            self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))

            self.services_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.185, height=height*0.055, fg_color=Color.White_Platinum)
        
            ctk.CTkLabel(self.services_total_frame, text="Service Total:", fg_color=Color.White_Platinum, font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.0075,0))
            self.services_total_amount = ctk.CTkLabel(self.services_total_frame, text="₱0,000.00", fg_color=Color.White_Platinum, font=("DM Sans Medium", 16))
            self.services_total_amount.pack(side="right",  padx=(0,width*0.0075)) 
            
            self.services_total_frame.pack(side="left", padx=(0,width*0.0075),)
            self.services_total_frame.pack_propagate(0)
            self.item_total_frame.pack(side="left", padx=(0,width*0.0075))
            self.item_total_frame.pack_propagate(0)
            self.price_total_frame.pack(side="left")
            self.price_total_frame.pack_propagate(0)
 
            self.save_invoice_btn = ctk.CTkButton(self.bottom_frame,text="Save Record",image=Icons.get_image('save_icon', (25,25)),height=height*0.055, width=width*0.09, font=("DM Sans Medium", 16), command= save_invoice_callback)
            self.save_invoice_btn.pack(side="right")
            
            self.cancel_invoice_btn = ctk.CTkButton(self.bottom_frame,text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover, height=height*0.055, width=width*0.06, font=("DM Sans Medium", 16))
            self.cancel_invoice_btn.configure(command=self.reset)
            self.cancel_invoice_btn.pack(side="right", padx=(width*0.005))
            
            self.show_particulars:add_particulars = add_particulars(self, (width, height), self.transact_treeview, self.change_total_value_item, self.change_total_value_service, self.service_dict, self.change_total_value_service)
            
        def change_total_value_item(self, value: float):
            value = float(value)
            self.item_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.item_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))

        def change_total_value_service(self, value: float):
            value = float(value)
            self.services_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.services_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))


        def reset(self, bypass_warning: bool = False):
            if self.client_name_entry.get() != "" or len(self.transact_treeview._data) > 0:
                if bypass_warning or messagebox.askyesno("Cancel Reception", "Are you sure you want to discard the reception record", parent = self):
                    self.save_invoice_btn.configure(state = ctk.NORMAL)
                    self.cancel_invoice_btn.configure(state = ctk.NORMAL)
                    self.client_name_entry.set("")
                    self.transact_treeview.delete_all_data()
                    self.services_total_amount.configure(text = format_price(0))
                    self.item_total_amount.configure(text = format_price(0))
                    self.price_total_amount.configure(text = format_price(0))
                    self.service_dict.clear()
                    self.invoice_id_label.configure(text = "__")
                    print(self.transact_treeview.data_frames.__len__())
                else:
                    return
            self.place_forget()  
        
        def place(self, **kwargs):
            self.client_names = [s[0] for s in database.fetch_data(sql_commands.get_owners)]
            self.client_name_entry.configure(values = self.client_names)
            client_name = database.fetch_data("SELECT CONCAT('client ', FORMAT(COUNT(*), .3),' ', DATE_FORMAT(CURRENT_DATE, '%m/%d/%y')) FROM invoice_record WHERE invoice_uid LIKE DATE_FORMAT(CURRENT_DATE, '%y%m%d%')")[0][0]
            self.client_name_entry.set(client_name)

            if self.invoice_id_label._text.endswith("_"):
                count = database.fetch_data("SELECT COUNT(*) FROM invoice_record WHERE invoice_uid LIKE CONCAT(DATE_FORMAT(CURRENT_DATE, '%y%m%d'), '%')")[0][0]
                self.invoice_id_label.configure(text = '%s%s' % (datetime.now().strftime('%y%m%d'), str(count).zfill(2)))
            return super().place(**kwargs)
        
    return instance(master, info, treeview_content_update_callback)

def add_item(master, info:tuple, root_treeview: cctk.cctkTreeView, service_dict: dict) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, service_dict: dict):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            global IP_Address, PORT_NO

            '''internal data'''
            self.total_transaction_count = 0
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self._service_dict = service_dict

            def item_proceed(_: any = None):
                selected_item = self.item_treeview.get_selected_data()
                #print(selected_item)
                if selected_item:
                    items_in_billing = [s[0] for s in root_treeview._data]
                    if selected_item[1] in items_in_billing:
                        frame:cctk.ctkButtonFrame = root_treeview.data_frames[items_in_billing.index(selected_item[1])]
                        spinner: cctk.cctkSpinnerCombo = frame.winfo_children()[-3].winfo_children()[0]
                        spinner.change_value()
                    else:
                        root_treeview.add_data((selected_item[1], selected_item[3], 1))
                        children_frames = root_treeview.data_frames[-1].winfo_children()
                        children_frames[-3].winfo_children()[-1].configure(value = 1, val_range = (1, selected_item[2]))
                    self.place_forget()
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.815, height=height*0.875, corner_radius=0,fg_color=Color.White_Color[3])
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='ADD ITEM', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0,columnspan=2, sticky="nsew", padx=width*0.005, pady=width*0.005)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure(0, weight=1)
                
            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color=Color.White_Platinum)
            self.item_frame.pack_propagate(0)
            self.item_frame.grid(row=0, column=0, sticky="nsew",padx=width*0.005, pady=width*0.005)
            
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.item_frame, data=self.data, height=height*0.8, width=width*0.795,double_click_command=item_proceed, 
                                                   column_format=f"/No:{int(width*.035)}-#r/ItemBrand:{int(width*.1)}-tl/ItemDescpription:x-tl/Stocks:{int(width*.075)}-tr/Price:{int(width*.115)}-tr!30!30",)
            self.item_treeview.pack()
            
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            count_temp = database.fetch_data("SELECT COUNT(*) FROM transaction_record")[0][0]
            if count_temp != self.total_transaction_count:
                self.update_items_stocks()
                self.total_transaction_count = count_temp
            return super().place(**kwargs)
        
        def update_items_stocks(self):
            data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.data = [(data[0], f"{data[1]} ({data[2]})") + data[3:] if data[2] else (data[0], data[1], ) + data[3:] for data in data]
            print(self.data)
            self.item_treeview.update_table(self.data)
        
        def place_forget(self):
            if self.item_treeview.data_grid_btn_mng.active:
                self.item_treeview.data_frames[self.item_treeview._data.index(self.item_treeview.get_selected_data())].response()
            return super().place_forget()
            
    return instance(master, info, root_treeview, service_dict)

def additional_option_invoice(master, info:tuple, attendant: str, uid: str, update_callback):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, attendant: str, uid: str, update_callback):
            width = info[0]
            height = info[1]
            super().__init__(master,width * .815, height=height*0.875, corner_radius= 0, fg_color="transparent")
            self.invoice_icon = ctk.CTkImage(light_image=Image.open("image/histlogs.png"), size=(18,21))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(17,17))
            self._attentdant: str = attendant
            self._uid: str = uid
            self.update_callback = update_callback
            global IP_Address, PORT_NO

            '''events'''
            def bd_commands(i):
                deduct = price_format_to_float(self.transact_treeview._data[i][-1][1:])
                self.change_total_value_item(-deduct)

            def update_billing_callback():
                if len(self.transact_treeview._data) == 0:
                    messagebox.showerror('Cannot Proceed', "Cannot proceed with an empty content", parent = self)
                    return
                for li in self.transact_treeview._data:
                    #add_additional_in_invoice = "INSERT INTO invoice_item_content VALUES(?, ?, ?, ?, ?, 0)"
                    if not li[0] in self.enlisted_services:
                        if li[0] in self.enlisted_items:
                            index = self.enlisted_items.index(li[0])
                            if li[2] != self.enlisted_items[index][2]:
                                database.exec_nonquery([[sql_commands.update_existing_item_in_invoice, (li[2] ,self._uid, li[0])]])
                            self.enlisted_items.pop(index)
                        else:
                            uid = database.fetch_data(sql_commands.get_uid, split_unit(li[0]))[0][0] if len(split_unit(li[0])) == 2  else database.fetch_data(sql_commands.get_uid_null_unit, (li[0], ))[0][0]
                            database.exec_nonquery([[sql_commands.add_additional_in_invoice, (self._uid, uid, li[0], li[2], price_format_to_float(li[1][1:]))]])
                #modifying the item

                database.exec_nonquery([[sql_commands.delete_existing_item_in_invoice, (s, )] for s in self.enlisted_items])
                #deleting an item

                database.exec_nonquery([[sql_commands.update_invoice_total_amount, (price_format_to_float(self.price_total_amount._text[1:]), self._uid)]])
                #updating the invoice record data
                

                self.update_callback()
                messagebox.showinfo("Success", "Info added", parent = self)
                self.transact_treeview.delete_all_data()
                self.place_forget()

            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], corner_radius=0)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.02)

            self.main_frame.grid_columnconfigure(2, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='',image=self.invoice_icon).pack(side="left", padx=(width*0.015,0))
            ctk.CTkLabel(self.top_frame, text='ADD RECORD', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.005,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.025, command=self.reset).pack(side="right", padx=(0,width*0.01))

            self.invoice_id_label =ctk.CTkLabel(self.main_frame, text= self._uid,  width=width*0.085, height=height*0.05, font=("DM Sans Medium", 14), fg_color="light grey", corner_radius=5)
            self.invoice_id_label.grid(row=1, column=0, sticky="w", padx=(width*0.005), pady=(height*0.01))

            self.client_name_frame = ctk.CTkFrame(self.main_frame, fg_color="light grey", width=width*0.35, height=height*0.05)
            self.client_name_frame.grid(row=1, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))
            self.client_name_frame.pack_propagate(0)

            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
            self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

            self.client_name_entry = ctk.CTkEntry(self.client_name_frame)
            client = database.fetch_data(sql_commands.get_client_by_invoice_uid, (self._uid, ))[0][0]
            self.client_name_entry.insert(0, client)
            self.client_name_entry.configure(state = "readonly")
            self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005), pady=(height*0.005))
            
            self.add_particulars: add_particulars = ctk.CTkButton(self.main_frame,text="Add Particulars", width=width*0.125, height=height*0.05, image=self.add_icon, font=("DM Sans Medium", 14),
                                               command=lambda:self.show_particulars.place(relx=0.5, rely=0.5, anchor="c"))
            self.add_particulars.grid(row=1, column=2, sticky="w")

            self.transact_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3])
            self.transact_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", pady=(0))

            self.transact_treeview = cctk.cctkTreeView(self.transact_frame, data=[], width=width*0.8, height=height*0.685,
                                                    column_format=f'/No:{int(width*0.025)}-#r/Particulars:x-tl/UnitPrice:{int(width*0.085)}-tr/Quantity:{int(width*0.1)}-id/Total:{int(width*0.085)}-tr/Action:{int(width*.065)}-bD!30!30',
                                                    spinner_config=(3, 2, 4, ',₱', '₱{:,.2f}', 'multiply'), spinner_initial_val= 1)
            self.transact_treeview.configure(spinner_command = lambda _:self.change_total_value_item())
            self.transact_treeview.pack(pady=(0,0))
            self.transact_treeview.bd_commands = bd_commands
            
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=height*0.05)
            self.bottom_frame.grid(row=3, column=0, columnspan=3, sticky="ew", padx=(width*0.005), pady=(height*0.01))

            #self.add_particulars = ctk.CTkButton(self.bottom_frame, width=width*0.125, height=height*0.05, text='Add Particulars',
            #                                   image=self.add_icon, command=lambda:self.show_particulars.place(relx=0.5, rely=0.5, anchor="c",  ))
            
            prices = database.fetch_data(sql_commands.get_prices_of_invoice, (self._uid, ))[0]
            self.price_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        
            ctk.CTkLabel(self.price_total_frame, text="Total:", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.0075,0))
            self.price_total_amount = ctk.CTkLabel(self.price_total_frame, text=f"₱{format_price(sum(prices))}", font=("DM Sans Medium", 14))
            self.price_total_amount.pack(side="right",  padx=(0,width*0.0075))
            
            self.item_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")

            ctk.CTkLabel(self.item_total_frame, text="Item:", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.0075,0))
            self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text= f'₱{format_price(int(prices[0]))}', font=("DM Sans Medium", 14))
            self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))

            self.services_total_frame = ctk.CTkFrame(self.bottom_frame, width=width*0.125, height=height*0.05, fg_color="light grey")
        
            ctk.CTkLabel(self.services_total_frame, text="Services:", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.0075,0))
            self.services_total_amount = ctk.CTkLabel(self.services_total_frame, text=f'₱{format_price(int(prices[1]))}', font=("DM Sans Medium", 14))
            self.services_total_amount.pack(side="right",  padx=(0,width*0.0075)) 
            
            self.services_total_frame.pack(side="left", padx=(0,width*0.0075))
            self.services_total_frame.pack_propagate(0)
            self.item_total_frame.pack(side="left", padx=(0,width*0.0075))
            self.item_total_frame.pack_propagate(0)
            self.price_total_frame.pack(side="left")
            self.price_total_frame.pack_propagate(0)
 
            self.save_invoice_btn = ctk.CTkButton(self.bottom_frame,text="Save Record",height=height*0.05, width=width*0.09, font=("DM Sans Medium", 16), command = update_billing_callback)
            self.save_invoice_btn.pack(side="right")
            
            self.cancel_invoice_btn = ctk.CTkButton(self.bottom_frame,text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip, height=height*0.05, width=width*0.06, font=("DM Sans Medium", 16))
            self.cancel_invoice_btn.configure(command=self.reset)
            self.cancel_invoice_btn.pack(side="right", padx=(width*0.005))

            self.fill_record()
            
            self.show_particulars:add_particulars = add_item(self, (width, height), self.transact_treeview, {})
            
        def change_total_value_item(self, change_value:int = None):
            value = sum([price_format_to_float(s[1][1:]) * s[2] for s in self.transact_treeview._data]) - price_format_to_float(self.services_total_amount._text[1:])
            if change_value is not None:
                value = change_value
                self.item_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.item_total_amount._text[1:])) + value))
                self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))
            else:
                self.item_total_amount.configure(text = f'₱{format_price(value)}');
                self.price_total_amount.configure(text = f'₱{format_price(price_format_to_float(self.services_total_amount._text[1:]) + value)}')

        def change_total_value_service(self, value: float):
            value = float(value)
            self.services_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.services_total_amount._text[1:])) + value))
            self.price_total_amount.configure(text = '₱' + format_price(float(price_format_to_float(self.price_total_amount._text[1:])) + value))

        def reset(self):
            self.destroy()

        def fill_record(self):
            services = database.fetch_data(sql_commands.get_services_invoice_by_id, (self._uid, ))
            self.enlisted_services = [s[2] for s in services]
            for li in [(s[2], f'₱{format_price(s[6])}', f'₱{format_price(s[6])}') for s in services]:
                self.transact_treeview.add_data(li)
                
                self.transact_treeview.data_frames[-1].configure(og_color = "green")
                children_frames = self.transact_treeview.data_frames[-1].winfo_children()
                children_frames[-1].winfo_children()[-1].destroy()
                children_frames[-2].configure(fg_color = "yellow")
                children_frames[-3].winfo_children()[-1].configure(state = ctk.DISABLED, mode = 'click_only')
            #for services

            items = database.fetch_data(sql_commands.get_item_invoice_by_id, (self._uid, ))
            self.enlisted_items = [s[2] for s in items]
            stocks = {s[2]:  database.fetch_data(sql_commands.get_item_and_their_uid_and_stock, (s[1], ))[0][0] for s in items}
            for li in [(s[2], f'₱{format_price(s[4])}', s[3]) for s in items]:
                self.transact_treeview.add_data(li)
                children_frames = self.transact_treeview.data_frames[-1].winfo_children()
                children_frames[-3].winfo_children()[-1].configure(value = li[-1], val_range = (1, int(stocks[li[0]])))
                
    return instance(master, info, attendant, uid, update_callback)

def show_payment_proceed(master, info:tuple,update_mainfames_callback):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple,):
            width = info[0]
            height = info[1]
            self.screen = (width, height)
            self.update_mainframes = update_mainfames_callback
            super().__init__(master,  width=width*0.815, height=height*0.875, corner_radius= 0, fg_color="transparent")

            global IP_Address, PORT_NO, GEN_SETTINGS

            self.sender_to_receptionist = nsu.network_sender(IP_Address["RECEPTIONIST_IP"], PORT_NO['DashB_stat_ref'], IP_Address["MY_NETWORK_IP"], 200)
            self.sender_to_admin = nsu.network_sender(IP_Address["ADMIN_IP"], PORT_NO['DashB_stat_ref'], IP_Address["MY_NETWORK_IP"], 201)
            
            self.payment_icon = ctk.CTkImage(light_image=Image.open("image/payment_cash.png"), size=(28,28))
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.8155, height=height*0.885, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.payment_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="PAYMENT", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)
            
            self.content_frame.grid_rowconfigure(1, weight=1)

            '''events'''
            def record_transaction():

                global list_of_items
                global list_of_services
                global client_pet_name
                client_pet_name = None
                list_of_items = []
                list_of_services = []
                if (float(self.payment_entry.get() or '0') + float(self.deduction_entry.get() or 0)) < price_format_to_float(self.grand_total._text[1:]):
                    messagebox.showinfo('Invalid', 'Pay the right amount', parent = self)
                    return

                record_id =  int(self.or_button._text[5:])
                owner_id = 0
                if len(self.services) > 0:
                    owner_id = database.fetch_data("SELECT owner_id FROM pet_owner_info WHERE owner_name = ?", (self.client_name._text,))[0][0]
                
                self.complete_button.configure(state="disabled")
                self.cancel_button.configure(state="disabled")
                
                print(self.items)
                temp = [(split_unit(data[0]) + data[1:]) for data in self.items]
                item = [(record_id, database.fetch_data(sql_commands.get_uid,(s[0], s[1]))[0][0], f'{s[0]} ({s[1]})', s[2], (price_format_to_float(s[3]) / s[2]), 0) if len(s) >= 4 
                        else (record_id, database.fetch_data(sql_commands.get_uid_null_unit,(s[0],))[0][0], s[0], s[1], (price_format_to_float(s[2]) / s[1]), 0) for s in temp]

                for _service in self.services:
                    list_of_services.append(_service)

                service = [(record_id, database.fetch_data(sql_commands.get_service_uid, (s[0], ))[0][0],
                            s[0], database.fetch_data("SELECT id FROM pet_info WHERE p_name = ? AND owner_id = ?", (s[1], owner_id))[0][0],
                            s[1], s[2], price_format_to_float(s[-1 ]), 0, 0, s[3], s[4], s[5]) for s in self.services]

                client_id = database.fetch_data(sql_commands.get_id_owner, (self.client_name._text, ))
                client_id = None if len(client_id) == 0 else client_id[0][0]

                if not database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.cashier_name._text, client_id, self.client_name._text, price_format_to_float(self.grand_total._text[1:]), self.deduction_entry.get() or 0)]]):
                    messagebox.showerror("Can't Proceed", "An error occurred")
                    return
                #record the transaction

                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in item])
                #record the items from within the transaction

                database.exec_nonquery([[sql_commands.record_services_transaction_content, s] for s in service])
                #record the services from within the transaction

                for _item in item:
                    does_expire = bool(database.fetch_data(sql_commands.check_item_if_it_expire_by_categ, (_item[1], ))[0][0])
                    quantity_needed = _item[3]
                    stocks = database.fetch_data(sql_commands.get_specific_stock_ordered_by_expiry if does_expire
                                                 else sql_commands.get_specific_stock_ordered_by_date_added, (_item[1], ))
                    
                    for st in stocks:
                        if st[2] == quantity_needed and st == stocks[-1]:
                            database.exec_nonquery([[sql_commands.null_stocks_by_id, (st[0], )]])
                        elif st[2] > quantity_needed:
                            database.exec_nonquery([[sql_commands.deduct_stocks_by_id, (quantity_needed, st[0])]])
                            quantity_needed = 0
                            break
                            #if the  stock of an instance is higher than needed stock
                        elif st[2] <= quantity_needed:
                            database.exec_nonquery([[sql_commands.delete_stocks_by_id, (st[0], )]])
                            quantity_needed -= st[2]
                            #if the stock needed is higher than stock instance

                for _item in item:
                    list_of_items.append(_item)
                    
                for s in service:
                    if s[-1]:
                        for i in range(s[-1] - 1):
                            targeted_date = (datetime.now() + timedelta(days= (s[-2] * (i + 1))))
                            database.exec_nonquery([[sql_commands.add_preceeding_schedule, (s[0], s[1], s[2], f'Dose {i+2}', targeted_date)]])
                    if s[-3]:
                            database.exec_nonquery([[sql_commands.add_preceeding_schedule, (s[0], s[1], s[2], f'Release', s[-3])]])
                #generating a preeceding schedules for multiple instance services

                payment = float(self.payment_entry.get())
                #calculate and show the change
                database.exec_nonquery([[sql_commands.set_invoice_transaction_to_recorded, (datetime.now(), self._invoice_id)]])

                messagebox.showinfo('Succeed', 'Transaction Recorded', parent = self)

                if IP_Address['MY_NETWORK_IP'] != IP_Address['RECEPTIONIST_IP']:
                    self.sender_to_receptionist.send("_")
                if IP_Address['MY_NETWORK_IP'] != IP_Address['ADMIN_IP']:
                    self.sender_to_admin.send("_")
                    
                record_action(self.cashier_name._text, action.TRANSACTION_TYPE, action.MAKE_TRANSACTION % (self.cashier_name._text, self.or_button._text[5:]))
                #update the table

                for i in range(len(list_of_services)):
                    li = list(list_of_services[i])
                    li[-1] =  price_format_to_float(li[-1])
                    list_of_services[i] = tuple(li)

                ppdfp.preview_pdf_popup(receipt=1, ornum=record_id, cashier=self.cashier_name._text, client=self.client_name._text, pet='s[1]', item=list_of_items, service=list_of_services, total=price_format_to_float(self.grand_total._text[1:]), paid=payment, deduction= self.deduction_entry.get() or 0,
                                        title="Transaction Receipt Viewer", service_provider= self.svc_provider, is_receipt=1)

                self._treeview_callback()
                self.place_forget()
                self.complete_button.configure(state="normal")
                self.cancel_button.configure(state="normal")
                self.reset()
                self.update_mainframes()

            #Payment Callback
            def payment_callback(var, index, mode):
                if re.search(r'[0-9\.]$', self.payment_entry.get() or "") is None and self.payment_entry._is_focused and self.payment_entry.get():
                        l = len(self.payment_entry.get())
                        self.payment_entry.delete(l-1, l)
                
                payment = 0 if self.payment_entry.get() == '' else self.payment_entry.get()
                
                self.payment_total.configure(text=f"{'₱{:0,.2f}'.format(float(payment))}")

                total_change = float(payment) - price_format_to_float(self.grand_total_second._text[1:])
                self.change_total.configure(text = "Invalid" if total_change < 0 else f'₱{  format_price(total_change)}')
                    
            self.payment_var = ctk.StringVar()

            def deduction_callback(var, index, mode):
                if re.search(r'[0-9\.]$', self.deduction_entry.get() or "") is None and self.deduction_entry._is_focused and self.deduction_entry.get():
                        l = len(self.deduction_entry.get())
                        self.deduction_entry.delete(l-1, l)

                _payment = 0 if self.payment_entry.get() == '' else self.payment_entry.get()
                _deduction = 0 if self.deduction_entry.get() == '' else self.deduction_entry.get()

                if float(_deduction) >= price_format_to_float(self.grand_total._text[1:]):
                    self.deduction_entry.delete(0, ctk.END)
                    self.deduction_entry.insert(0, price_format_to_float(self.grand_total._text[1:]) - 1)
                    self.grand_total_second.configure(text = f'₱{format_price(1)}')
                    return

                self.grand_total_second.configure(text = f'₱{format_price(price_format_to_float(self.grand_total._text[1:]) - float(_deduction))}')
                total_change = (float(_payment) + float(_deduction)) - price_format_to_float(self.grand_total._text[1:])
                self.change_total.configure(text = "Invalid" if total_change < 0 else f'₱{  format_price(total_change)}')
                    
            self.deduction_var = ctk.StringVar()
            
            '''Transaction Info'''
            self.client_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=0, column=0,sticky="nsew", columnspan=2, padx=width*0.005, pady=height*0.01)
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            
            self.cashier_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05,)
            self.cashier_frame.grid(row=0, column=0, padx=(width*0.005,0), pady= height*0.007)
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01))
            self.cashier_name = ctk.CTkLabel(self.cashier_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.cashier_name.pack(side="left",padx=(0,width*0.005))
            
            self.time_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.time_frame.grid(row=0, column=3, padx=width*0.005, pady= height*0.007, sticky="nse")
            
            self.date_label = ctk.CTkLabel(self.time_frame, fg_color=Color.White_Platinum, corner_radius=5, font=("DM Sans Medium", 14), text=date.today().strftime('%B %d, %Y'), width=width*0.1)
            self.date_label.pack(side="right", padx=(width*0.005))
            
            self.receipt_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.receipt_frame.grid(row=1, column=0, sticky="nsew",padx=width*0.005, pady=(0,height*0.01))
            self.receipt_frame.grid_rowconfigure(1, weight=1)
            self.receipt_frame.grid_columnconfigure(1,weight=1)
            
            self.or_button = ctk.CTkButton(self.receipt_frame,  text="OR#: ___",  font=("DM Sans Medium", 14),  height=height*0.05, width=width*0.1)
            self.or_button.grid(row=0, column=0, padx=width*0.005, pady= height*0.007)

            self.client_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= height*0.007)
            self.client_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.client_name.pack(side="left") 
            
            self.receipt_table_frame = ctk.CTkFrame(self.receipt_frame,)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(0,height*0.007) )
            self.receipt_table_frame.grid_columnconfigure(0,weight=1)
            self.receipt_table_frame.grid_rowconfigure(0, weight=1)
            
            '''TABLE SETUP'''
            
            """ self.receipt_table_style = ttk.Style()
            self.receipt_table_style.theme_use("clam")
            self.receipt_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
            self.receipt_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
            self.receipt_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
            self.receipt_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
            self.columns = ("rec_no", "particulars","qty","total")
            
            self.receipt_tree = ttk.Treeview(self.receipt_table_frame, columns=self.columns, show="headings",)
           
            self.receipt_tree.heading("rec_no", text="No")
            self.receipt_tree.heading("particulars", text="Particulars")
            self.receipt_tree.heading("qty", text="Qty")
            #self.receipt_tree.heading("unit_price", text="UnitPrice")
            self.receipt_tree.heading("total", text="Total")

            self.receipt_tree.column("rec_no", width=int(width*0.001),anchor="e")
            self.receipt_tree.column("particulars", width=int(width*0.4), anchor="w")
            self.receipt_tree.column("qty", width=int(width*0.085), anchor="e")
            #self.receipt_tree.column("unit_price", width=int(width*0.1), anchor="e")
            self.receipt_tree.column("total", width=int(width*0.12), anchor="e")
            
            self.receipt_tree.tag_configure("odd",background=Color.White_AntiFlash)
            self.receipt_tree.tag_configure("even",background=Color.White_Ghost)
            
            self.receipt_tree.grid(row=0, column=0, sticky="nsew")
            
            self.y_scrollbar = ttk.Scrollbar(self.receipt_table_frame, orient=tk.VERTICAL, command=self.receipt_tree.yview)
            self.receipt_tree.configure(yscroll=self.y_scrollbar.set)
            self.y_scrollbar.grid(row=0, column=1, sticky="ns") """

            self.particulars_treeview = cctk.cctkTreeView(self.receipt_table_frame, data=[], width= width*0.515, height= height*0.625, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/Particulars:x-tl/Quantity:{int(width*.1)}-tr/TotalPrice:{int(width*.085)}-tr!30!35',
                                           bd_message="Are you sure want to remove this item?")
            self.particulars_treeview.pack()
            
            '''END TABLE SETUP'''
            self.receipt_total_frame = ctk.CTkFrame(self.receipt_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.grid(row=2, column=2, padx=(0,width*0.005), pady= (0,height*0.007), sticky="e")
            self.receipt_total_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ 0.00",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
            
            self.payment_frame= ctk.CTkFrame(self.content_frame, width=width*0.275, fg_color=Color.White_Platinum)
            self.payment_frame.grid(row=1, column=1, sticky="nsew", padx=(0,width*0.005), pady=(0,height*0.01))
            self.payment_frame.grid_columnconfigure((0,1), weight=1)
            self.payment_frame.grid_rowconfigure(0, weight=1)
            self.payment_frame.grid_propagate(0)
            
            self.pay_frame = ctk.CTkFrame(self.payment_frame, fg_color=Color.White_Lotion)
            self.pay_frame.grid(row=0, column=0, columnspan=2, padx=(width*0.005), pady=(height*0.007,0), sticky="nsew")
            self.pay_frame.grid_columnconfigure(1, weight=1)
            self.pay_frame.grid_rowconfigure(5, weight=1)
            
            ctk.CTkLabel(self.pay_frame, text="Services: ", font=("DM Sans Medium",16),).grid(row=0, column=0, padx=(width*0.01), pady=(height*0.025,0), sticky="w")
            self.services_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.services_total.grid(row=0, column=2, padx=(width*0.01), pady=(height*0.025,0), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Items: ", font=("DM Sans Medium",16),).grid(row=1, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.items_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor= 'e')
            self.items_total.grid(row=1, column=2, padx=(width*0.01), pady=(height*0.005,height*0.01), sticky = 'e')
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=2, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pay_frame, text="Sub-total: ", font=("DM Sans Medium",16),).grid(row=3, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.grand_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.grand_total.grid(row=3, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Amount Tendered: ", font=("DM Sans Medium",16),).grid(row=4, column=0, padx=(width*0.01), pady=(height*0.025,0), sticky="w")
            self.payment_entry = ctk.CTkEntry(self.pay_frame, font=("DM Sans Medium",16), justify="right", height=height*0.055, textvariable=self.payment_var)
            self.payment_entry.grid(row=4, column=2, padx=(width*0.01), pady=(height*0.025,height*0.01),)
            
            ctk.CTkLabel(self.pay_frame, text="Deduction: ", font=("DM Sans Medium",16),).grid(row=5, column=0, padx=(width*0.01), pady=(height*0.025,0), sticky="w")
            self.deduction_entry = ctk.CTkEntry(self.pay_frame, font=("DM Sans Medium",16), justify="right", height=height*0.055, textvariable=self.deduction_var)

            self.authorization_btn = ctk.CTkButton(self.pay_frame, font=("DM Sans Medium",16), height=height*0.055, text="Add", state = ctk.DISABLED, fg_color= Color.Grey_Bright)
            self.authorization_btn.grid(row=5, column=2, padx=(width*0.01), pady=(height*0.025,height*0.01),)

            self.payment_var.trace_add("write", callback=payment_callback)
            self.deduction_var.trace_add("write", callback=deduction_callback)
                        
            ctk.CTkLabel(self.pay_frame, text="Total: ", font=("DM Sans Medium",16),).grid(row=6, column=0, padx=(width*0.01), pady=(0), sticky="w")
            self.grand_total_second = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e', text_color='green')
            self.grand_total_second.grid(row=6, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')

            ctk.CTkLabel(self.pay_frame, text="Payment: ", font=("DM Sans Medium",16),).grid(row=7, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.payment_total = ctk.CTkLabel(self.pay_frame, text="₱ --.--", font=("DM Sans Medium",16), anchor='e')
            self.payment_total.grid(row=7, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')

            '''ctk.CTkLabel(self.pay_frame, text="Deduction: ", font=("DM Sans Medium",16),).grid(row=7, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.deduction_total = ctk.CTkLabel(self.pay_frame, text="₱ --.--", font=("DM Sans Medium",16), anchor='e')
            self.deduction_total.grid(row=7, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')'''
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=9, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pay_frame, text="Change: ", font=("DM Sans Medium",16),).grid(row=10, column=0, padx=(width*0.01), pady=(height*0.01,height*0.1), sticky="w")
            self.change_total = ctk.CTkLabel(self.pay_frame, text="₱ --.--", font=("DM Sans Medium",18), text_color= 'red')
            self.change_total.grid(row=10, column=2, padx=(width*0.01), pady=(height*0.005, height*0.1), sticky = 'e')
            self.change_total.focus()
            
            self.complete_button = ctk.CTkButton(self.payment_frame, text="Complete",font=("DM Sans Medium",16), command= record_transaction)
            self.complete_button.grid(row=2, column=1, sticky="nsew", padx=(width*0.005), pady=(height*0.007))
            
            self.cancel_button = ctk.CTkButton(self.payment_frame, text="Cancel", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip
                                               ,font=("DM Sans Medium",16), width=width*0.065, height=height*0.05)
            self.cancel_button.configure(command=self.reset)
            self.cancel_button.grid(row=2, column=0, sticky="nsew", padx=(width*0.005,0), pady=(height*0.007))

            self.authorization_popup = mini_popup.authorization(self, (width, height), self.authorization_command)
            self.authorization_btn.configure(command = lambda: self.authorization_popup.place(relx = .5, rely = .5, anchor = 'c'))

        def authorization_command(self):
            self.authorization_btn.grid_forget()
            self.deduction_entry.grid(row=5, column=2, padx=(self.screen[0]*0.01), pady=(self.screen[1]*0.025,self.screen[1]*0.01),)
            
        def reset(self):
            self.deduction_entry.grid_forget()
            self.authorization_btn.grid(row=5, column=2, padx=(self.screen[0]*0.01), pady=(self.screen[1]*0.025,self.screen[1]*0.01),)
            self.or_button.configure(text = '_')
            self.payment_entry.delete(0, ctk.END)
            self.payment_total.configure(text = "₱ --.--")
            self.change_total.configure(text = "--.--")
            self.or_button.configure(text= "OR#: ___")
            self.place_forget()
            self.deduction_entry.delete(0, ctk.END)

        def place(self, invoice_data: tuple, cashier: str, treeview_callback: callable, **kwargs):
            if self.or_button._text.endswith("_"):
                count = database.fetch_data("SELECT transaction_uid FROM transaction_record ORDER BY CAST(transaction_uid AS INT) desc")
                count = 1 if len(count) < 1 else count[0][0]
                self.or_button.configure(text = f"OR#: {str(int(count)+1).zfill(3)}")
            #set up the or button

            self.cashier_name.configure(text = cashier)
            self.client_name.configure(text = invoice_data[1])
            self.services_total.configure(text = invoice_data[2])
            self.items_total.configure(text = invoice_data[3])
            self.grand_total.configure(text = invoice_data[4])
            self.grand_total_second.configure(text = invoice_data[4])
            self.receipt_total_amount.configure(text= invoice_data[4])
            self._treeview_callback = treeview_callback
            self._invoice_id = invoice_data[0]

            self.svc_provider = database.fetch_data(sql_commands.get_provider_to_invoice, (invoice_data[0], ))[0]
            self.svc_provider = 'N/A' if len(self.svc_provider) < 1 else self.svc_provider[0]

            #emptied out the treeview

            client_cred = database.fetch_data(sql_commands.check_if_customer_is_considered_regular, (GEN_SETTINGS, invoice_data[1]))
            if len(client_cred) > 0:
                if client_cred[0][-1] == 1:
                    self.authorization_btn.configure(state = ctk.NORMAL, fg_color = "#36719f")

            self.services = database.fetch_data(sql_commands.get_invoice_service_content_by_id, (invoice_data[0], )) or []
            self.items = database.fetch_data(sql_commands.get_invoice_item_content_by_id, (invoice_data[0], ))

            #modified_services = [(f' {s[0]}  P:{s[1]} D:%s %s%s' % (s[2].strftime('%m/%d/%y'), ), 1,  f"₱{s[3]}") for s in self.services]
            modified_services = []
            for s in self.services:
                if s[3] is not None:
                    modified_services.append((f' {s[0]}  P:{s[1]} D:%s-%s' % (s[2].strftime('%m/%d/%y'), s[3].strftime('%m/%d/%y')), 1,  f"₱{s[-1]}"))
                elif s[4] is not None:
                    modified_services.append((f' {s[0]}  P:{s[1]} D:%s %s' % (s[2].strftime('%m/%d/%y'), f'{s[5]}x for every {s[4]} day/s'), 1,  f"₱{s[-1]}"))
                else:
                    modified_services.append((f' {s[0]}  P:{s[1]} D:%s' % s[2].strftime('%m/%d/%y') , 1,  f"₱{s[-1]}"))

            modified_items = [(f" {s[0]}", s[1], f"₱{s[2]}") for s in self.items]
            
            temp = modified_items + modified_services
            
            self.particulars_treeview.update_table(temp)
            
            return super().place(**kwargs)
    return instance(master, info)  

def show_invoice_content(master, info:tuple,):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master,  width=width*0.815, height=height*0.875, corner_radius= 0, fg_color="transparent")
            
            global IP_Address, PORT_NO

            self.payment_icon = ctk.CTkImage(light_image=Image.open("image/payment_cash.png"), size=(28,28))
        
            def close():
                self.place_forget()

                
            self.main_frame = ctk.CTkFrame(self, width=width*0.8155, height=height*0.885, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")



            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.payment_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="PAYMENT", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=close).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)
            
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            '''Transaction Info'''
            self.client_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=0, column=0,sticky="nsew", columnspan=2, padx=width*0.005, pady=height*0.01)
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            
            self.cashier_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05,)
            self.cashier_frame.grid(row=0, column=0, padx=(width*0.005,0), pady= height*0.007)
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,0))
            self.cashier_name = ctk.CTkLabel(self.cashier_frame, text="Jane Doe",  font=("DM Sans Medium", 14), fg_color="transparent" )
            self.cashier_name.pack(side="left",padx=(0), fill='x', expand=1)
            
            self.time_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.time_frame.grid(row=0, column=3, padx=width*0.005, pady= height*0.007, sticky="nse")
            
            self.date_label = ctk.CTkLabel(self.time_frame, fg_color=Color.White_Platinum, corner_radius=5, font=("DM Sans Medium", 14), text=date.today().strftime('%B %d, %Y'), width=width*0.1)
            self.date_label.pack(side="right", padx=(width*0.005))
            
            self.receipt_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.receipt_frame.grid(row=1, column=0, sticky="nsew",padx=width*0.005, pady=(0,height*0.01))
            self.receipt_frame.grid_rowconfigure(1, weight=1)
            self.receipt_frame.grid_columnconfigure(1,weight=1)
            
            #self.or_button = ctk.CTkButton(self.receipt_frame,  text="OR#: ___",  font=("DM Sans Medium", 14),  height=height*0.05, width=width*0.1)
            #self.or_button.grid(row=0, column=0, padx=width*0.005, pady= height*0.007)
            self.or_lbl = ctk.CTkLabel(self.receipt_frame,  text="OR#: ___",  font=("DM Sans Medium", 14),  height=height*0.05, width=width*0.1, fg_color=Color.White_Lotion, padx=width*0.01, corner_radius=5)
            self.or_lbl.grid(row=0, column=0, padx=width*0.005, pady= height*0.007)

            self.client_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= height*0.007)
            self.client_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,0))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14), fg_color="transparent")
            self.client_name.pack(side="left", fill='x', expand=1) 
            
            self.receipt_table_frame = ctk.CTkFrame(self.receipt_frame,)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(0,height*0.007) )
            self.receipt_table_frame.grid_columnconfigure(0,weight=1)
            self.receipt_table_frame.grid_rowconfigure(0, weight=1)
            
            '''TABLE SETUP'''
            
            self.receipt_table_style = ttk.Style()
            self.receipt_table_style.theme_use("clam")
            self.receipt_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
            self.receipt_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
            self.receipt_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
            self.receipt_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
            self.columns = ("rec_no", "particulars","qty","total")
            
            self.receipt_tree = ttk.Treeview(self.receipt_table_frame, columns=self.columns, show="headings",)
           
            self.receipt_tree.heading("rec_no", text="No")
            self.receipt_tree.heading("particulars", text="Particulars")
            self.receipt_tree.heading("qty", text="Qty")
            #self.receipt_tree.heading("unit_price", text="UnitPrice")
            self.receipt_tree.heading("total", text="Total")

            self.receipt_tree.column("rec_no", width=int(width*0.001),anchor="e")
            self.receipt_tree.column("particulars", width=int(width*0.4), anchor="w")
            self.receipt_tree.column("qty", width=int(width*0.085), anchor="e")
            #self.receipt_tree.column("unit_price", width=int(width*0.1), anchor="e")
            self.receipt_tree.column("total", width=int(width*0.12), anchor="e")
            
            self.receipt_tree.tag_configure("odd",background=Color.White_AntiFlash)
            self.receipt_tree.tag_configure("even",background=Color.White_Ghost)
            
            self.receipt_tree.grid(row=0, column=0, sticky="nsew")
            
            self.y_scrollbar = ttk.Scrollbar(self.receipt_table_frame, orient=tk.VERTICAL, command=self.receipt_tree.yview)
            self.receipt_tree.configure(yscroll=self.y_scrollbar.set)
            self.y_scrollbar.grid(row=0, column=1, sticky="ns")

            '''END TABLE SETUP'''
            self.receipt_total_frame = ctk.CTkFrame(self.receipt_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.grid(row=2, column=2, padx=(0,width*0.005), pady= (0,height*0.007), sticky="e")
            self.receipt_total_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ 0.00",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
            
            self.payment_frame= ctk.CTkFrame(self.content_frame, width=width*0.275, fg_color=Color.White_Platinum)
            self.payment_frame.grid(row=1, column=1, sticky="nsew", padx=(0,width*0.005), pady=(0,height*0.01))
            self.payment_frame.grid_columnconfigure((0,1), weight=1)
            self.payment_frame.grid_rowconfigure(0, weight=1)
            self.payment_frame.grid_propagate(0)
            
            self.pay_frame = ctk.CTkFrame(self.payment_frame, fg_color=Color.White_Lotion)
            self.pay_frame.grid(row=0, column=0, columnspan=2, padx=(width*0.005), pady=(height*0.007,0), sticky="nsew")
            self.pay_frame.grid_columnconfigure(1, weight=1)
            self.pay_frame.grid_rowconfigure(5, weight=1)
            
            ctk.CTkLabel(self.pay_frame, text="Services: ", font=("DM Sans Medium",16),).grid(row=0, column=0, padx=(width*0.01), pady=(height*0.025,0), sticky="w")
            self.services_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.services_total.grid(row=0, column=2, padx=(width*0.01), pady=(height*0.025,0), sticky = 'e')
            
            ctk.CTkLabel(self.pay_frame, text="Items: ", font=("DM Sans Medium",16),).grid(row=1, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.items_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor= 'e')
            self.items_total.grid(row=1, column=2, padx=(width*0.01), pady=(height*0.005,height*0.01), sticky = 'e')
            
            ctk.CTkFrame(self.pay_frame, fg_color="black", height=height*0.005).grid(row=2, column=0, columnspan=3, sticky="ew", padx=(width*0.01),pady=(height*0.01,0))
            
            ctk.CTkLabel(self.pay_frame, text="Total: ", font=("DM Sans Medium",16),).grid(row=3, column=0, padx=(width*0.01), pady=(height*0.01,0), sticky="w")
            self.grand_total = ctk.CTkLabel(self.pay_frame, text="₱ 0.00", font=("DM Sans Medium",16), anchor='e')
            self.grand_total.grid(row=3, column=2, padx=(width*0.01), pady=(height*0.01,height*0.01), sticky = 'e')
            
            self.cancel_button = ctk.CTkButton(self.payment_frame, text="Close", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip
                                               ,font=("DM Sans Medium",16), width=width*0.05, height=height*0.05)
            self.cancel_button.configure(command=close)
            self.cancel_button.grid(row=2, column=0, sticky='nsw',padx=(width*0.005,0), pady=(height*0.007))
            
        def place(self, invoice_id: str, **kwargs):
            print(invoice_id)
            general_invoice_data = database.fetch_data('SELECT * FROM invoice_record WHERE invoice_uid = ?', (str(invoice_id), ))[0]
            service_total = database.fetch_data("SELECT CONCAT('₱ ', FORMAT(SUM(price), 2)) FROM invoice_service_content WHERE invoice_uid = ?", (str(invoice_id), ))[0][0]
            item_total = database.fetch_data("SELECT CONCAT('₱ ', FORMAT(SUM(price * quantity), 2)) FROM invoice_item_content WHERE invoice_uid = ?", (str(invoice_id), ))[0][0]
            
            #print(general_invoice_data)
            #print(general_invoice_data, '\n', service_total, '\n', item_total)
            
            
            self.or_lbl.configure(text = f"Reception Code:   {invoice_id}")
            self.cashier_name.configure(text = general_invoice_data[1])
            self.client_name.configure(text = general_invoice_data[2])
            self.date_label.configure(general_invoice_data[5].strftime('%B %d, %Y'))
            self.services_total.configure(text = service_total or "₱ 0.00")
            self.items_total.configure(text = item_total or "₱ 0.00")
            self.grand_total.configure(text = "₱ {:.2f}".format(general_invoice_data[3]))
            self.services = database.fetch_data(sql_commands.get_invoice_service_content_by_id, (invoice_id, ))
            self.items = database.fetch_data(sql_commands.get_invoice_item_content_by_id, (invoice_id, ))
            self.receipt_total_amount.configure(text= general_invoice_data[3])

            for i in self.receipt_tree.get_children():
                self.receipt_tree.delete(i)

            self.services = database.fetch_data(sql_commands.get_invoice_service_content_by_id, (invoice_id, ))
            self.items = database.fetch_data(sql_commands.get_invoice_item_content_by_id, (invoice_id, ))

            #modified_services = [(f' {s[0]}  P:{s[1]} D:%s %s%s' % (s[2].strftime('%m/%d/%y'), ), 1,  f"₱{s[3]}") for s in self.services]
            modified_services = []
            for s in self.services:
                if s[3] is not None:
                    modified_services.append((f' {s[0]}  P:{s[1]} D:%s-%s' % (s[2].strftime('%m/%d/%y'), s[3].strftime('%m/%d/%y')), 1,  f"₱{s[-1]}"))
                elif s[4] is not None:
                    modified_services.append((f' {s[0]}  P:{s[1]} D:%s %s' % (s[2].strftime('%m/%d/%y'), f'{s[5]}x for{s[4]}days interval'), 1,  f"₱{s[-1]}"))
                else:
                    modified_services.append((f' {s[0]}  P:{s[1]} D:%s' % s[2].strftime('%m/%d/%y') , 1,  f"₱{s[-1]}"))

            modified_items = [(f" {s[0]}", s[1], f"₱{s[2]}") for s in self.items]
            
            temp = modified_items + modified_services
            
            for i in range(len(temp)):
                if (i % 2) == 0:
                    tag = "even"
                else:
                    tag ="odd"
                self.receipt_tree.insert(parent='', index='end', iid=i, text="", values=(i+1, ) +temp[i],tags=tag)
            
    return instance(master, info)

def svc_provider(master, info:tuple, parent= None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)

            global IP_Address, PORT_NO
            self.width = self.winfo_screenwidth()
            self.height = self.winfo_screenheight()
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

            def hide():
                self.place_forget()

            self._master = master

            self.main_frame = ctk.CTkFrame(self, width=width*0.3, height=height*0.3, corner_radius=0)
            self.main_frame.pack(padx=1,pady=1)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Select Service_provider', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=hide).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=5)
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(2, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            self.content_frame.grid_propagate(0)

            self.selection = ctk.CTkOptionMenu(self.content_frame, self.width * .25, self.height * .055, 12, font=("DM Sans Medium", 16))
            self.selection.pack(pady = (self.height * .05, self.height * .025))

            self.ok_btn = ctk.CTkButton(self.content_frame, self.width * .2, self.height * .05, text = 'Select' )
            self.ok_btn.pack()

        def update_treeview(self):
            self.sched_treeview.pack_forget()
            self.sched_treeview.update_table(database.fetch_data(sql_commands.get_all_schedule))
            self.sched_treeview.pack()

        def resched_btn_callback(self, _: any = None):
            if self.sched_treeview.get_selected_data():
                dashboard_popup.rescheduling_service_info(self, (self.width, self.height)).place(relx = .5, rely = .5, anchor = 'c', uid= self.sched_treeview.get_selected_data()[0], update_treeview_callback= self.update_treeview)
                #code for reshceduling here
            else:
                messagebox.showerror("Unable to Proceed", "Select a service to resched", parent = self)

    return instance(master, info, parent)

'''def show_transaction_proceed(master, info:tuple, service_price, item_price, total_price, transaction_content, customer_info, parent_treeview, service_dict) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, service_price, item_price, total_price, transaction_content, customer_info, parent_treeview, service_dict):
            width = info[0]
            height = info[1]
            self.acc_cred = info[2]
            self._service_price = service_price
            self._item_price = item_price
            self._total_price = total_price
            self._transaction_content = transaction_content
            self._customer_info = customer_info
            self.service_dict = service_dict
            #encapsulation

            global IP_Address, PORT_NO

            super().__init__(master, corner_radius= 0, fg_color='white')
            #the actual frame, modification on the frame itself goes here

            def auto_pay(_: any = None):
                self.payment_entry.delete(0, ctk.END)
                #self.payment_entry.insert(0, self._total_price)
                record_transaction()

            def record_transaction():
                #return
                record_id =  database.fetch_data(sql_commands.generate_id_transaction, (None))[0][0]
                if (float(self.payment_entry.get() or '0')) < price_format_to_float(self.total_amount._text[1:]):
                    messagebox.showinfo('Invalid', 'Pay the right amount', parent = self)
                    return
                #if self.service:

                list_of_service = database.fetch_data(sql_commands.get_services_names)
                list_of_service = [s[0] for s in list_of_service]

                service = [s for s in self._transaction_content if s[0] in list_of_service]
                item = [s for s in self._transaction_content if s[0] not in list_of_service]

                if(len(service) > 0):
                    temp_service_data = []
                    for i in range(len(service)):
                        for j in self.service_dict[service[i][0]]:
                            temp_service_data.append((record_id, database.fetch_data(sql_commands.get_service_uid,(service[i][0],))[0][0], service[i][0], j[0], j[1], price_format_to_float(service[i][1][1:]), 0, 0))
                    service = temp_service_data

                if(len(item) > 0):
                    item = [(record_id, database.fetch_data(sql_commands.get_uid, (s[0], ))[0][0], s[0], s[2], price_format_to_float(s[1][1:]), 0) for s in item]
                #making a modification through the old process
                
                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.acc_cred[0][0], self._customer_info, price_format_to_float(self.total_amount._text[1:])), self.dis]])
                #record the transaction

                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in item])
                #record the items from within the transaction
                database.exec_nonquery([[sql_commands.record_services_transaction_content, s] for s in service])
                #record the services from within the transaction

                for _item in item:
                    stocks = database.fetch_data(sql_commands.get_specific_stock, (_item[1], ))
                    if stocks[0][2] is None:
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (-_item[3], _item[1])]])
                    else:
                        quan = _item[3]
                        for st in stocks:
                            if st[1] < quan:
                                quan -= st[1]
                                database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                            elif st[1] > quan:
                                database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, _item[1], st[2])]])
                                break
                            else:
                                if stocks[-1] == st:
                                    database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, _item[1], st[2])]])
                                else:
                                    database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                                break
                #modify the stock, applying the FIFO

                payment = float(self.payment_entry.get())
                self.change_amount.configure(text = format_price(payment - price_format_to_float(self.total_amount._text[1:])))
                #calculate and show the change

                #master.reset()
                parent_treeview.master.master.reset()
                messagebox.showinfo('Sucess', 'Transaction Complete', parent = self)
                #record_action(self.acc_cred[0][0], action.TRANSACTION_TYPE, action.MAKE_TRANSACTION % (self.acc_cred[0][0], self.or))
                self.destroy()
                #reset into its default state """

            self.main_frame = ctk.CTkFrame(self, width=width*0.8, height=height*0.85, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Payment', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            self.content_frame.grid(row=1,column=0, padx=width*0.005, pady=height*0.01, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.service_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
            self.service_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
            self.service_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(self.service_frame, text='Services Availed:',font=("DM Sans Medium", 14), fg_color="transparent").grid(row=0, column=0, padx=width*0.005, pady=(0,height*0.005), sticky="w")

            #self.service_data = [(f'{s[1]}', format_price(float(s[4]))) for s in self._services_info]
            self.service_list = cctk.cctkTreeView(self.service_frame, data=None, height=height*0.245, width=width*0.545,
                                                  column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Quantity:{int(width*0.1)}-tr/Price:{int(width * .05)}-tr!30!30')
            self.service_list.grid(row=1, column=0)

            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
            self.item_frame.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")
            self.item_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(self.item_frame, text='Items Availed:',font=("DM Sans Medium", 14), fg_color="transparent").grid(row=0, column=0, padx=width*0.005, pady=(0,height*0.005), sticky="w")

            #self.item_data = [(f'{s[1]} * {s[3]}', format_price(float(s[4]))) for s in self._item_info]
            self.item_list = cctk.cctkTreeView(self.item_frame, data=None, height=height*0.245, width=width*0.545,
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Quantity:{int(width*0.1)}-tr/Price:{int(width * .05)}-tr!30!30')
            self.item_list.grid(row=1, column=0)

            ctk.CTkButton(self.content_frame, text="Cancel", command=self.reset).grid(row=3, column=0, padx=10, pady=(0,10), sticky="w")

            self.payment_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[3],width=width*0.225)
            self.payment_frame.grid(row=1,column=1, padx=(0,width*0.005), pady=height*0.01, stick="nsew")
            self.payment_frame.pack_propagate(0)

            self.payment_service_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.payment_service_frame.pack_propagate(0)
            self.payment_service_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_service_frame, text="Service:", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.0075,0))
            self.payment_service_amount = ctk.CTkLabel(self.payment_service_frame, text="0,000.00", font=("DM Sans Medium", 16))
            self.payment_service_amount.pack(side="right",  padx=(0,width*0.0075))

            self.payment_item_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.payment_item_frame.pack_propagate(0)
            self.payment_item_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_item_frame, text="Items:", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.0075,0))
            self.payment_item_amount = ctk.CTkLabel(self.payment_item_frame, text="0,000.00", font=("DM Sans Medium", 16))
            self.payment_item_amount.pack(side="right",  padx=(0,width*0.0075))

            self.total_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.total_frame.pack_propagate(0)
            self.total_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.total_frame, text="Total:", font=("DM Sans Medium", 20)).pack(side="left", padx=(width*0.0075,0))
            self.total_amount = ctk.CTkLabel(self.total_frame, text="0,000.00", font=("DM Sans Medium", 20), width=width*0.15, fg_color="light grey", corner_radius=5,
                                             anchor="e")
            self.total_amount.pack(side="right",  padx=(0,width*0.0075))

            self.payment_entry_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, fg_color="transparent")
            self.payment_entry_frame.pack_propagate(0)
            self.payment_entry_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_entry_frame, text="Enter Payment:", font=("DM Sans Medium", 20)).pack(padx=(width*0.0075,0), anchor="w")
            self.payment_entry = ctk.CTkEntry(self.payment_entry_frame, placeholder_text="Payment here...", font=("DM Sans Medium", 20),height=height*0.05, justify="right")
            self.payment_entry.pack(fill="x", padx=(width*0.0075))

            self.change_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.change_frame.pack_propagate(0)
            self.change_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.change_frame, text="Change:", font=("DM Sans Medium", 20)).pack(side="left", padx=(width*0.0075,0))
            self.change_amount = ctk.CTkLabel(self.change_frame, text="0,000.00", font=("DM Sans Medium", 20), width=width*0.15, fg_color="light grey", corner_radius=5, anchor="e")
            self.change_amount.pack(side="right",  padx=(0,width*0.0075))

            self.proceed_button = ctk.CTkButton(self.payment_frame, text='Proceed', font=("DM Sans Medium", 20), height=height*0.085, command=record_transaction)
            self.proceed_button.pack(fill="x",side="bottom", pady=height*0.025, padx=(width*0.025))
            self.payment_entry.focus_force()
            self.payment_entry.bind('<Shift-Return>', auto_pay)
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            self.payment_service_amount.configure(text = self._service_price)
            self.payment_item_amount.configure(text = self._item_price)
            self.total_amount.configure(text = self._total_price)
            return super().place(**kwargs)
            #item_info, services_info, total_price, customer_info, pets_info
    return instance(master, info, service_price, item_price, total_price, transaction_content, customer_info, parent_treeview, service_dict)'''

'''def customer_info(master, info:tuple, parent_value = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent_value: tuple = None):
            self.service = None
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            global IP_Address, PORT_NO

            super().__init__(master, corner_radius= 0, fg_color="transparent")
            #the actual frame, modification on the frame itself goes here

            #self.grid_propagate(0)
            self.value: tuple = None
            self._parent_value = parent_value
            self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))
            self.sched_switch_var = ctk.StringVar(value="off")

            def automate_fill(_: any= None):
                data = database.fetch_data(sql_commands.get_pet_info_for_cust_info, (self.pet_name.get(), ))[0]
                """ self.animal_breed_entry.delete(0, ctk.END)
                self.animal_breed_entry.insert(0, data[0])
                self.animal_breed_entry.configure(state = ctk.DISABLED) """

            def hide():
                self.place_forget()

            def discard():
                if (self.pet_name.get() != self.value[0] or self.animal_breed_entry.get() != self.value[1] or
                self.scheduled_service_val._text != self.value[2] or self.note_entry.get() != self.value[3]):
                    if messagebox.askyesno('NOTE!', 'all changes will be discarded?', parent = self):
                        self.pet_name.set('')
                        self.animal_breed_entry.delete(0, ctk.END)
                        self.note_entry.delete(0, ctk.END)
                        self.pet_name.insert(0, self.value[0] or '')
                        self.animal_breed_entry.insert(0, self.value[1] or '')
                        self.scheduled_service_val.configure( text = self.value[2] or '')
                        self.note_entry.insert(0, self.value[3] or '')
                hide()


            def record():
                date = self.scheduled_service_val._text if self.scheduled_service_val._text != 'Set Date' else str(datetime.date.today())
                self.value:tuple = (self.tables[self.pet_values.index(self.pet_name.get())] + (date, ))
                self._parent_value.value = self.value
                hide()

            def sched_swtich_event():
                if self.sched_switch_var.get() == "on":
                    self.show_calendar.configure(state="normal")
                    self.show_calendar.configure(fg_color=Color.Blue_Yale)
                else:
                    self.show_calendar.configure(state="disabled")
                    self.show_calendar.configure(fg_color="light grey")

            self.main_frame = ctk.CTkFrame(self, width=width*0.5, height=height*0.65, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Pet Info', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=hide).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            self.content_frame.grid(row=1,column=0, padx=width*0.005, pady=height*0.01, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.client_name_label = ctk.CTkLabel(self.content_frame, text="Client's Pet Information",font=("DM Sans Medium",18))
            self.client_name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Name label
            ctk.CTkLabel(self.content_frame, text='Select Pet:',font=("DM Sans Medium", 14)).grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
            """ self.pet_frame = ctk.CTkScrollableFrame(self.content_frame, height=height*0.15, fg_color="transparent")
            self.pet_frame.grid(row=2,column=0, sticky="we") """
            self.tables = database.fetch_data(sql_commands.get_pet_name)
            self.pet_values = [s[1] for s in self.tables]
            """ 
            for pet_index in range(len(self.pet_values)):
                ctk.CTkButton(self.pet_frame, text=self.pet_values[pet_index]).pack() """
            self.pet_name = ctk.CTkOptionMenu(self.content_frame, width=width*0.45, font=("DM Sans Medium", 14), values=self.pet_values, command= automate_fill)
            self.pet_name.set('')
            self.pet_name.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ns")
            
            self.animal_breed_lbl = ctk.CTkLabel(self.content_frame, text='Breed and Animal Type:',font=("DM Sans Medium", 14))
            self.animal_breed_lbl.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Breed and Animal Type entry
            self.animal_breed_entry = ctk.CTkEntry(self.content_frame, width=width*0.45, font=("DM Sans Medium", 14))
            self.animal_breed_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ns")
            
            self.schedule_service_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.schedule_service_frame.grid(row=5,  column=0, padx=10, pady=(10), sticky="ew")
            #Scheduled service label
            self.sched_switch = ctk.CTkSwitch(self.schedule_service_frame, text="Schedule Client?", command=sched_swtich_event, variable=self.sched_switch_var,
                                              onvalue="on", offvalue="off")
            self.sched_switch.grid(row=0, column=0, padx=(10, 0), pady=(0, 10), sticky="nw")

            self.scheduled_service_lbl = ctk.CTkLabel(self.schedule_service_frame, text="Set Schedule",font=("DM Sans Medium", 14))
            self.scheduled_service_lbl.grid(row=1, column=0, padx=(10, 0), sticky="nw")
            #Scheduled service label
            self.scheduled_service_val = ctk.CTkLabel(self.schedule_service_frame, width=width*0.25, height=height*0.05,font=("DM Sans Medium", 14), fg_color='light grey', text="Set Date", text_color="grey")
            self.scheduled_service_val.grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="nsew")
            self.show_calendar = ctk.CTkButton(self.schedule_service_frame, text="",height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,image=self.cal_icon,
                                               command=lambda: cctk.tk_calendar(self.scheduled_service_val, "%s"), corner_radius=3)
            self.show_calendar.grid(row=2, column=1, padx = (width*0.005,0), pady = (0,height*0.015), sticky="e")

            self.x_fr = ctk.CTkFrame(self.content_frame, height=height*0.78, width=width*0.312, fg_color="transparent")

            self.x_fr.grid(row=6, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', command=discard, font=("DM Sans Medium", 20))
            self.back_button.grid(row=0, column=1, padx=20, pady=(15, 15), sticky='s')

            self.select_button = ctk.CTkButton(self.x_fr, text='Confirm', command=record, font=("DM Sans Medium", 20))
            self.select_button.grid(row=0, column=2, padx=(0, 20), pady=(15, 15), sticky="se")

            sched_swtich_event()
            #on out

    return instance(master, info, parent_value)'''

'''def payment_confirm(master, info:tuple,):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")
            
            global IP_Address, PORT_NO

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.payment_icon = ctk.CTkImage(light_image=Image.open("image/payment_cash.png"), size=(28,28))
            
            self.main_frame = ctk.CTkFrame(self, width=width*0.35, height=height*0.4 ,corner_radius=0, fg_color="transparent")
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            
            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.055)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.payment_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="TRANSACTION SUCCESSFUL", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)

            
    return instance(master, info)  '''

'''def show_invoice_record(master, info:tuple,):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master,  width=width*0.815, height=height*0.875, corner_radius= 0, fg_color="transparent")
            
            global IP_Address, PORT_NO

            self.cat_icon = ctk.CTkImage(light_image=Image.open("image/cat.png"), size=(28,28))
                
            self.main_frame = ctk.CTkFrame(self, width=width*0.8155, height=height*0.885, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.cat_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="RECEPTION", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            
            self.content_frame.grid(row=1,column=0, sticky="nsew")
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)
            
            self.content_frame.grid_rowconfigure(1, weight=1)
            
            self.client_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=0, column=0,sticky="nsew", columnspan=2, padx=width*0.005, pady=height*0.01)
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            
            self.cashier_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05,)
            self.cashier_frame.grid(row=0, column=0, padx=(width*0.005,0), pady= height*0.007)
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01))
            self.cashier_name = ctk.CTkLabel(self.cashier_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.cashier_name.pack(side="left",padx=(0,width*0.005))
            
            self.time_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.time_frame.grid(row=0, column=3, padx=width*0.005, pady= height*0.007, sticky="nse")
            
            self.date_label = ctk.CTkLabel(self.time_frame, corner_radius=5, font=("DM Sans Medium", 14), text="RECEPTION DATE", width=width*0.15)
            self.date_label.pack(side="right", padx=(width*0.005))
            
            self.receipt_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum)
            self.receipt_frame.grid(row=1, column=0, sticky="nsew",padx=width*0.005, pady=(0,height*0.01))
            self.receipt_frame.grid_rowconfigure(1, weight=1)
            self.receipt_frame.grid_columnconfigure(1,weight=1)
            
            self.or_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.125)
            self.or_frame.grid(row=0, column=0, padx=(width*0.005), pady= height*0.007, sticky="nsw")
            self.or_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.or_frame, text="RECEPTIONID", font=("DM Sans Medium", 14)).pack(fill="both", expand=1, padx=(width*0.01,width*0.0165))    

            
            self.client_frame = ctk.CTkFrame(self.receipt_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.15)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= height*0.007, sticky="nsw")
            self.client_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14))
            self.client_name.pack(side="left") 
            
            self.receipt_table_frame = ctk.CTkFrame(self.receipt_frame,)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(0,height*0.007) )
            self.receipt_table_frame.grid_columnconfigure(0,weight=1)
            self.receipt_table_frame.grid_rowconfigure(0, weight=1)
            
            
            self.receipt_table_style = ttk.Style()
            self.receipt_table_style.theme_use("clam")
            self.receipt_table_style.configure("Treeview", rowheight=int(height*0.065), background=Color.White_Platinum, foreground=Color.Blue_Maastricht, bd=0,  highlightthickness=0, font=("DM Sans Medium", 16) )
            
            self.receipt_table_style.configure("Treeview.Heading", font=("DM Sans Medium", 18), background=Color.Blue_Cobalt, borderwidth=0, foreground=Color.White_AntiFlash)
            self.receipt_table_style.layout("Treeview",[("Treeview.treearea",{"sticky": "nswe"})])
            self.receipt_table_style.map("Treeview", background=[("selected",Color.Blue_Steel)])
            
            
            self.columns = ("rec_no", "particulars","qty","total")
            
            self.receipt_tree = ttk.Treeview(self.receipt_table_frame, columns=self.columns, show="headings",)
           
            self.receipt_tree.heading("rec_no", text="No")
            self.receipt_tree.heading("particulars", text="Particulars")
            self.receipt_tree.heading("qty", text="Qty")
            self.receipt_tree.heading("total", text="Total")

            self.receipt_tree.column("rec_no", width=int(width*0.001),anchor="e")
            self.receipt_tree.column("particulars", width=int(width*0.4), anchor="w")
            self.receipt_tree.column("qty", width=int(width*0.085), anchor="e")
            self.receipt_tree.column("total", width=int(width*0.12), anchor="e")
            
            self.receipt_tree.tag_configure("odd",background=Color.White_AntiFlash)
            self.receipt_tree.tag_configure("even",background=Color.White_Ghost)
            
            self.receipt_tree.grid(row=0, column=0, sticky="nsew")
            
            self.y_scrollbar = ttk.Scrollbar(self.receipt_table_frame, orient=tk.VERTICAL, command=self.receipt_tree.yview)
            self.receipt_tree.configure(yscroll=self.y_scrollbar.set)
            self.y_scrollbar.grid(row=0, column=1, sticky="ns")

            self.receipt_total_frame = ctk.CTkFrame(self.receipt_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.grid(row=2, column=2, padx=(0,width*0.005), pady= (0,height*0.007), sticky="e")
            self.receipt_total_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 16)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ 0.00",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
            
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            return super().place(**kwargs)
    return instance(master, info)'''