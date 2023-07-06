import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
from constants import action
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from decimal import Decimal
import datetime
from PIL import Image
import copy

def show_item_list(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func):
            self._master = master
            width = info[0]
            height = info[1]
            #self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, corner_radius= 0)

            '''event'''
            def proceed(_: any = None):
                if self.item_treeview.data_grid_btn_mng.active:
                    data = self.item_treeview._data[self.item_treeview.data_frames.index(self.item_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[2], data[2])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, data[1]))
                        change_val_func(price_format_to_float(data[2][1:]))
                        #price = price_format_to_float(data_frames.winfo_children()[2]._text[1:])

                        def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            temp_data = root_treeview._data[root_treeview.data_frames.index(temp_frame)]
                            temp_data = (temp_data[0], temp_data[1], spinner.value, '₱' + format_price(price_format_to_float(temp_data[1][1:]) * spinner.value))
                            root_treeview._data[root_treeview.data_frames.index(temp_frame)] = temp_data
                            change_val_func(-price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[2]._text[1:])
                            temp_frame.winfo_children()[4].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func(price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))

                        spinner.configure(command = spinner_command)

                    self.place_forget()

            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))

            self.main_frame = ctk.CTkFrame(self, width=width*0.525, height=height*0.85, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.pack_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.pack(fill="both", expand=0)

            ctk.CTkLabel(self.top_frame, text='Add Items', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3])
            self.content_frame.pack(fill="both", expand=1, padx=width*0.005, pady=height*0.01)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.0075), pady=(height*0.01,0),sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.005))

            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.content_frame,data=self.data, height=height*0.65, width=width*0.505,
                                                      column_format=f"/No:{int(width*.025)}-#r/ItemName:x-tl/Stocks:{int(width*.075)}-tr/Price:{int(width*.1)}-tr!30!30",
                                                      double_click_command= proceed)
            self.item_treeview.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")

            self.bottom_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=width*0.25)
            self.bottom_frame.grid(row=2, column=0 )
            self.bottom_frame.grid_propagate(0)
            self.bottom_frame.grid_columnconfigure(1, weight=1)
            self.back_button = ctk.CTkButton(self.bottom_frame, text='Cancel', width=width*0.1, font=("Arial", 14), command=self.reset)
            self.back_button.grid(row=0, column=0, sticky="w")

            self.select_button = ctk.CTkButton(self.bottom_frame, text='Select', width=width*0.1, font=("Arial", 14), command= proceed)
            self.select_button.grid(row=0, column=1, sticky="e")

            """ self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=self.get_item, width =270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), sticky="se") """

        def place(self, **kwargs):
            self.main_frame.pack()
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            #self.item_treeview.update_table(self.data)
            return super().place(**kwargs)

        def reset(self):
            self.destroy()
            #self.main_frame.place_forget()
            self.place_forget()

        '''def get_item(self, _: any = None):
            #if there's a selected item
            if self.item_treeview.data_grid_btn_mng.active is not None:
                item_name =  self.item_treeview.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_item_data_for_transaction, (item_name, ))[0]
                #collects part of the data needed in the transaction
                items_in_treeview = [s.winfo_children()[2]._text if self._treeview.data_frames != [] else None for s in self._treeview.data_frames]
                #search the tree view if there's an already existing item

                #if there's an already existing item
                if(item_name in items_in_treeview):
                    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[items_in_treeview.index(item_name)].winfo_children()[4].winfo_children()[0]
                    quantity_column.change_value()
                    #change the value of the spinner combo; modifying the record's total price
                else:
                    self._treeview.add_data(transaction_data+(1, transaction_data[2]))
                    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[-1].winfo_children()[4].winfo_children()[0]
                    price_column: ctk.CTkLabel = self._treeview.data_frames[-1].winfo_children()[6]

                    def spinner_command(mul: int = 0):
                        master.change_total_value_item(-float(price_column._text))
                        #before change

                        price_change = quantity_column._base_val * quantity_column.value
                        master.change_total_value_item(price_change)
                        price_column.configure(text = price_change)
                        #after change
                        postdata = list(self._treeview._data[self._treeview.data_frames.index(quantity_column.master.master)])
                        postdata[3] = quantity_column.value
                        postdata[4] = Decimal(price_change)
                        self._treeview._data[self._treeview.data_frames.index(quantity_column.master.master)] = tuple(postdata)
                        #update the treeview's data

                        if quantity_column._base_val * quantity_column.value >= quantity_column._base_val * quantity_column._val_range[1]:
                            quantity_column.num_entry.configure(text_color = 'red')
                            #messagebox.showinfo('NOTE!', 'Maximum stock reached')
                        else:
                            quantity_column.num_entry.configure(text_color = quantity_column._entry_text_color)

                    quantity_column.configure(command = spinner_command, base_val = transaction_data[2], value = 1, val_range = (1
                    , int(self.item_treeview.data_grid_btn_mng.active.winfo_children()[1]._text)))
                    #add a new record
                    master.change_total_value_item(transaction_data[2])

                self.item_treeview.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup """
    return instance(master, info)'''

    return instance(master, info, root_treeview, change_val_func)

def show_services_list(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func, customer_info: cctk.info_tab):
    class instance(ctk.CTkFrame):

        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func, customer_info: cctk.info_tab):
            #self._data_reciever = data_reciever
            self._master = master
            width = info[0]
            height = info[1]
            #self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, corner_radius= 0)

            '''event'''
            def proceed(_: any = None):
                if self.service_treeview.data_grid_btn_mng.active:
                    data = self.service_treeview._data[self.service_treeview.data_frames.index(self.service_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[1], data[1])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, cctk.cctkSpinnerCombo.MAX_VAL))
                        change_val_func(price_format_to_float(data[1][1:]))
                        #price = price_format_to_float(data_frames.winfo_children()[2]._text[1:])

                        """def spinner_command(_: any = None):
                            temp_frame = spinner.master.master
                            change_val_func(-price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))
                            price = price_format_to_float(temp_frame.winfo_children()[2]._text[1:])
                            temp_frame.winfo_children()[4].configure(text = '₱' + format_price(price * spinner.value))
                            change_val_func(price_format_to_float(temp_frame.winfo_children()[4]._text[1:]))

                        spinner.configure(command = spinner_command)"""
                        spinner.add_button.destroy()
                        spinner.sub_button.destroy()
                        spinner.configure(mode = cctk.cctkSpinnerCombo.CLICK_ONLY)
                    customer_info.title = add_data[0]
                    customer_info.button.configure(state = ctk.NORMAL)
                    customer_info.button._command()
                    self.place_forget()

            #ctk.CTkLabel(self, text="HElp").pack()
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))

            self.main_frame = ctk.CTkFrame(self, width=width*0.45, height=height*0.85, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.pack_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.pack(fill="both", expand=0)

            ctk.CTkLabel(self.top_frame, text='Add Service', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3])
            self.content_frame.pack(fill="both", expand=1, padx=width*0.005, pady=height*0.01)
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_propagate(0)

            self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.0075), pady=(height*0.01,0),sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.005))

            #self.data = database.fetch_data(sql_commands.get_services_and_their_price)

            self.service_treeview = cctk.cctkTreeView(self.content_frame, height=height*0.65, width=width*0.425,
                                                      column_format=f"/No:{int(width*.025)}-#r/ServiceName:x-tl/Price:x-tr!30!30",
                                                      double_click_command= proceed)
            self.service_treeview.grid(row=1, column=0, padx=(width*0.005), pady=(height*0.01), sticky="nsew")

            """
            self.service_treeview = cctk.cctkTreeView(self.left_frame, height=self.height*0.65, width =self.width*0.785,
                                                      header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color='black',
                                                       column_format='/Services:x-tl/Price:x-tr!35!30',)



            self.rightmost_frame = ctk.CTkFrame(self.boxframe, height=self.height*0.78, width =self.width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=self.height*0.78, width =self.width*0.312, fg_color='white')
            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")
            """
            self.bottom_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", width=width*0.25)
            self.bottom_frame.grid(row=2, column=0 )
            self.bottom_frame.grid_propagate(0)
            self.bottom_frame.grid_columnconfigure(1, weight=1)
            self.back_button = ctk.CTkButton(self.bottom_frame, text='Cancel', width=width*0.1, font=("Arial", 14), command=self.reset)
            self.back_button.grid(row=0, column=0, sticky="w")

            self.select_button = ctk.CTkButton(self.bottom_frame, text='Select', width=width*0.1, font=("Arial", 14), command= proceed)
            self.select_button.grid(row=0, column=1, sticky="e")

        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            raw_data = database.fetch_data(sql_commands.get_services_and_their_price, None)
            self.main_frame.pack()
            self.data = [(s[1], s[3]) for s in raw_data]
            self.service_treeview.update_table(self.data)
            return super().place(**kwargs)


        def get_service(self, _: any = None):
            #if there's a selected item
            if self.service_treeview.data_grid_btn_mng.active is not None:
                service_name =  self.service_treeview.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_services_data_for_transaction, (service_name, ))[0]
                self._treeview.add_data(transaction_data+(0, transaction_data[2]))
                info_tab:cctk.info_tab = self._treeview.data_frames[-1].winfo_children()[3]
                info_tab._tab = customer_info(self._treeview.master.master, (info[0] * .8, info[1] * .8), info_tab)
                info_tab.button.configure(command = lambda: info_tab._tab.place(relx = .5, rely = .5, anchor = 'c'))
                self._data_reciever.append(info_tab)
                info_tab._tab.place(relx = .5, rely = .5, anchor = 'c')


                master.change_total_value_service(transaction_data[2])
                self.service_treeview.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup
    return instance(master, info, root_treeview, change_val_func, customer_info)

def show_transaction_proceed(master, info:tuple, service_price, item_price, total_price, patient_info, transaction_content, service, customer_info, parent_treeview, service_dict) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, service_price, item_price, total_price, patient_info, transaction_content, service, customer_info, parent_treeview, service_dict):
            width = info[0]
            height = info[1]
            self.acc_cred = info[2]
            self._service_price = service_price
            self._item_price = item_price
            self._total_price = total_price
            self._patient_info = patient_info
            self._transaction_content = transaction_content
            self.service = service
            self._customer_info = customer_info
            self.service_dict = service_dict
            #item_info: list, services_info, total_price: float, customer_info: str, pets_info: List
            #item_info: list, services_info, total_price: float, customer_info: str, pets_raw_info: List
            #basic inforamtion needed; measurement
            """
            self._pets_raw_info = pets_raw_info
            if(self._pets_raw_info is not None):
                self.pets_info = [s.value for s in self._pets_raw_info]
            self.acc_cred = info[3]
            self._treeview = info[2]
            self._item_info = item_info
            self._services_info = services_info
            self._total_price = total_price """
            #encapsulation

            super().__init__(master, corner_radius= 0, fg_color='white')
            #the actual frame, modification on the frame itself goes here

            '''events'''
            def auto_pay(_: any = None):
                self.payment_entry.delete(0, ctk.END)
                #self.payment_entry.insert(0, self._total_price)
                record_transaction()

            def record_transaction():
                #return
                record_id =  database.fetch_data(sql_commands.generate_id_transaction, (None))[0][0]
                if (float(self.payment_entry.get() or '0')) < price_format_to_float(self.total_amount._text[1:]):
                    messagebox.showinfo('Invalid', 'Pay the right amount')
                    return
                #if self.service:
                print(self._transaction_content)

                list_of_service = database.fetch_data(sql_commands.get_services_names)
                list_of_service = [s[0] for s in list_of_service]

                service = [s for s in self._transaction_content if s[0] in list_of_service]
                item = [s for s in self._transaction_content if s[0] not in list_of_service]

                if(len(service) > 0):
                    temp_service_data = []
                    for i in range(len(service)):
                        for j in self.service_dict[service[i][0]]:
                            temp_service_data.append((record_id, database.fetch_data(sql_commands.get_service_uid,(service[i][0],))[0][0], service[i][0], j[1][0], j[1][1], price_format_to_float(service[i][1][1:]), 0, 0))
                    service = temp_service_data
                if(len(item) > 0):
                    item = [(record_id, database.fetch_data(sql_commands.get_uid, (s[0], ))[0][0], s[0], s[2], price_format_to_float(s[1][1:]), 0) for s in item]
                #making a modification through the old process
                print((record_id, self.acc_cred[0], self._customer_info, price_format_to_float(self.total_amount._text[1:])))
                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.acc_cred[0][0], self._customer_info, price_format_to_float(self.total_amount._text[1:]))]])
                #record the transaction

                #modified_items_list = [(record_id, s[0], s[1], s[3], float(s[2]), 0) for s in item]
                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in item])
                #record the items from eithin the transaction

                #modified_services_list = [(record_id, s[0], s[1], customer_info, str(datetime.datetime.strptime(self.pets_info[0][2], '%m-%d-%Y').strftime('%Y-%m-%d')), float(s[2]), 0, 0) for s in self._services_info]
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
                #modify the stock

                payment = float(self.payment_entry.get())
                self.change_amount.configure(text = format_price(payment - price_format_to_float(self.total_amount._text[1:])))
                #calculate and show the change

                #master.reset()
                parent_treeview.master.master.reset()
                messagebox.showinfo('Sucess', 'Transaction Complete')

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

            ctk.CTkLabel(self.service_frame, text='Services Availed:',font=("Arial", 14), fg_color="transparent").grid(row=0, column=0, padx=width*0.005, pady=(0,height*0.005), sticky="w")

            #self.service_data = [(f'{s[1]}', format_price(float(s[4]))) for s in self._services_info]
            self.service_list = cctk.cctkTreeView(self.service_frame, data=None, height=height*0.245, width=width*0.545,
                                                  column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Quantity:{int(width*0.1)}-tr/Price:{int(width * .05)}-tr!30!30')
            self.service_list.grid(row=1, column=0)

            '''self.service_total_frame = ctk.CTkFrame(self.service_frame, width=width*0.15, height=height*0.05, fg_color="light grey")
            self.service_total_frame.pack_propagate(0)
            self.service_total_frame.grid(row=2,column=0, sticky="e", pady=(5,0))

            ctk.CTkLabel(self.service_total_frame, text="Services Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.service_total_amount = ctk.CTkLabel(self.service_total_frame, text="0,000.00", font=("Arial", 14))
            self.service_total_amount.pack(side="right",  padx=(0,width*0.0075))'''

            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0, fg_color="transparent")
            self.item_frame.grid(row=2, column=0, padx=10, pady=(0,10), sticky="nsew")
            self.item_frame.grid_columnconfigure(0, weight=1)

            ctk.CTkLabel(self.item_frame, text='Items Availed:',font=("Arial", 14), fg_color="transparent").grid(row=0, column=0, padx=width*0.005, pady=(0,height*0.005), sticky="w")

            #self.item_data = [(f'{s[1]} * {s[3]}', format_price(float(s[4]))) for s in self._item_info]
            self.item_list = cctk.cctkTreeView(self.item_frame, data=None, height=height*0.245, width=width*0.545,
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Quantity:{int(width*0.1)}-tr/Price:{int(width * .05)}-tr!30!30')
            self.item_list.grid(row=1, column=0)

            '''self.item_total_frame = ctk.CTkFrame(self.item_frame, width=width*0.15, height=height*0.05, fg_color="light grey")
            self.item_total_frame.pack_propagate(0)
            self.item_total_frame.grid(row=2,column=0, sticky="e", pady=(5,0))

            ctk.CTkLabel(self.item_total_frame, text="Items Total:", font=("Arial", 14)).pack(side="left", padx=(width*0.0075,0))
            self.item_total_amount = ctk.CTkLabel(self.item_total_frame, text="0,000.00", font=("Arial", 14))
            self.item_total_amount.pack(side="right",  padx=(0,width*0.0075))'''

            ctk.CTkButton(self.content_frame, text="Cancel", command=self.reset).grid(row=3, column=0, padx=10, pady=(0,10), sticky="w")

            self.payment_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[3],width=width*0.225)
            self.payment_frame.grid(row=1,column=1, padx=(0,width*0.005), pady=height*0.01, stick="nsew")
            self.payment_frame.pack_propagate(0)

            self.payment_service_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.payment_service_frame.pack_propagate(0)
            self.payment_service_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_service_frame, text="Service:", font=("Arial", 16)).pack(side="left", padx=(width*0.0075,0))
            self.payment_service_amount = ctk.CTkLabel(self.payment_service_frame, text="0,000.00", font=("Arial", 16))
            self.payment_service_amount.pack(side="right",  padx=(0,width*0.0075))

            self.payment_item_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.payment_item_frame.pack_propagate(0)
            self.payment_item_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_item_frame, text="Items:", font=("Arial", 16)).pack(side="left", padx=(width*0.0075,0))
            self.payment_item_amount = ctk.CTkLabel(self.payment_item_frame, text="0,000.00", font=("Arial", 16))
            self.payment_item_amount.pack(side="right",  padx=(0,width*0.0075))

            self.total_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.total_frame.pack_propagate(0)
            self.total_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.total_frame, text="Total:", font=("Arial", 20)).pack(side="left", padx=(width*0.0075,0))
            self.total_amount = ctk.CTkLabel(self.total_frame, text="0,000.00", font=("Arial", 20), width=width*0.15, fg_color="light grey", corner_radius=5,
                                             anchor="e")
            self.total_amount.pack(side="right",  padx=(0,width*0.0075))

            self.payment_entry_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, fg_color="transparent")
            self.payment_entry_frame.pack_propagate(0)
            self.payment_entry_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.payment_entry_frame, text="Enter Payment:", font=("Arial", 20)).pack(padx=(width*0.0075,0), anchor="w")
            self.payment_entry = ctk.CTkEntry(self.payment_entry_frame, placeholder_text="Payment here...", font=("Arial", 20),height=height*0.05, justify="right")
            self.payment_entry.pack(fill="x", padx=(width*0.0075))

            self.change_frame = ctk.CTkFrame(self.payment_frame, width=width*0.15, height=height*0.05, fg_color="transparent")
            self.change_frame.pack_propagate(0)
            self.change_frame.pack(fill="x", pady=(height*0.005))

            ctk.CTkLabel(self.change_frame, text="Change:", font=("Arial", 20)).pack(side="left", padx=(width*0.0075,0))
            self.change_amount = ctk.CTkLabel(self.change_frame, text="0,000.00", font=("Arial", 20), width=width*0.15, fg_color="light grey", corner_radius=5, anchor="e")
            self.change_amount.pack(side="right",  padx=(0,width*0.0075))

            self.proceed_button = ctk.CTkButton(self.payment_frame, text='Proceed', font=("Arial", 20), height=height*0.085, command=record_transaction)
            self.proceed_button.pack(fill="x",side="bottom", pady=height*0.025, padx=(width*0.025))
            """
            self.total_frame = ctk.CTkFrame(self.rightmost_frame)
            self.total_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan = 2)

            self.total_lbl = ctk.CTkLabel(self.total_frame, text='Total:',font=("Arial", 25))
            self.total_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.total_val = ctk.CTkEntry(self.total_frame, height=height*0.12, width=width*0.31, font=('DM Sans Medium', 35))
            #self.total_val.insert(0, format_price(self._total_price))
            self.total_val.configure(state = 'readonly')
            self.total_val.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.payment_options_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_options_frame.grid(row=1, column=0, padx=10, pady=(10, height*0.22), sticky="new", columnspan = 2)

            self.payment_lbl = ctk.CTkLabel(self.payment_options_frame, text='Payment Method:', font=("Poppins", 25))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_method_cbox = ctk.CTkOptionMenu(self.payment_options_frame, values=["Cash"], font=("Poppins", 25), height=height*0.08,width=width*0.31
                                                         ,fg_color='white', button_color='#dddddd', text_color='black')
            self.payment_method_cbox.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ew")

            self.payment_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_frame.grid(row=3, column=0, padx=10, pady=(20, 10), sticky="new", columnspan = 2)

            self.payment_lbl = ctk.CTkLabel(self.payment_frame, text='Payment:',font=("Poppins", 25))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_entry = ctk.CTkEntry(self.payment_frame, height=height*0.12, width=width*0.31, font=('DM Sans Medium', 35))
            self.payment_entry.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.proceed_button = ctk.CTkButton(self.rightmost_frame, text='Proceed', command=record_transaction, width=135, font=("Poppins-Bold", 45))
            self.proceed_button.grid(row=4, column=0, padx=(40, 50), pady =(10,10), sticky="ew")

            self.cancel_button = ctk.CTkButton(self.rightmost_frame, text='Cancel', command=self.reset, width=135, font=("Poppins-Bold", 45))
            self.cancel_button.grid(row=4, column=1, padx=(40, 50), pady =(10,10), sticky="ew")
            """
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
    return instance(master, info, service_price, item_price, total_price, patient_info, transaction_content, service, customer_info, parent_treeview, service_dict)

def customer_info(master, info:tuple, parent_value: cctk.info_tab = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent_value: tuple = None):
            self.service = None
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, corner_radius= 0, fg_color="transparent")
            #the actual frame, modification on the frame itself goes here

            #self.grid_propagate(0)
            self.value: tuple = None
            self._parent_value = parent_value
            self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))
            self.sched_switch_var = ctk.StringVar(value="off")

            def automate_fill(_: any= None):
                print(database.fetch_data(sql_commands.get_pet_info_for_cust_info, (self.pet_name.get())))
                data = database.fetch_data(sql_commands.get_pet_info_for_cust_info, (self.pet_name.get(), ))[0]
                self.animal_breed_entry.delete(0, ctk.END)
                self.animal_breed_entry.insert(0, data[0])
                self.animal_breed_entry.configure(state = ctk.DISABLED)

            def hide():
                self.place_forget()

            def discard():
                if (self.pet_name.get() != self.value[0] or self.animal_breed_entry.get() != self.value[1] or
                self.scheduled_service_val._text != self.value[2] or self.note_entry.get() != self.value[3]):
                    if messagebox.askyesno('NOTE!', 'all changes will be discarded?'):
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

            self.client_name_label = ctk.CTkLabel(self.content_frame, text="Client's Pet Information",font=("Arial",18))
            self.client_name_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Name label
            ctk.CTkLabel(self.content_frame, text='Select Pet:',font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
            """ self.pet_frame = ctk.CTkScrollableFrame(self.content_frame, height=height*0.15, fg_color="transparent")
            self.pet_frame.grid(row=2,column=0, sticky="we") """
            self.tables = database.fetch_data(sql_commands.get_pet_name)
            self.pet_values = [s[1] for s in self.tables]
            """ 
            for pet_index in range(len(self.pet_values)):
                ctk.CTkButton(self.pet_frame, text=self.pet_values[pet_index]).pack() """
            self.pet_name = ctk.CTkOptionMenu(self.content_frame, width=width*0.45, font=("Arial", 14), values=self.pet_values, command= automate_fill)
            self.pet_name.set('')
            self.pet_name.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ns")
            
            self.animal_breed_lbl = ctk.CTkLabel(self.content_frame, text='Breed and Animal Type:',font=("Arial", 14))
            self.animal_breed_lbl.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Breed and Animal Type entry
            self.animal_breed_entry = ctk.CTkEntry(self.content_frame, width=width*0.45, font=("Arial", 14))
            self.animal_breed_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ns")
            
            self.schedule_service_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.schedule_service_frame.grid(row=5,  column=0, padx=10, pady=(10), sticky="ew")
            #Scheduled service label
            self.sched_switch = ctk.CTkSwitch(self.schedule_service_frame, text="Schedule Client?", command=sched_swtich_event, variable=self.sched_switch_var,
                                              onvalue="on", offvalue="off")
            self.sched_switch.grid(row=0, column=0, padx=(10, 0), pady=(0, 10), sticky="nw")

            self.scheduled_service_lbl = ctk.CTkLabel(self.schedule_service_frame, text="Set Schedule",font=("Arial", 14))
            self.scheduled_service_lbl.grid(row=1, column=0, padx=(10, 0), sticky="nw")
            #Scheduled service label
            self.scheduled_service_val = ctk.CTkLabel(self.schedule_service_frame, width=width*0.25, height=height*0.05,font=("Arial", 14), fg_color='light grey', text="Set Date", text_color="grey")
            self.scheduled_service_val.grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="nsew")
            self.show_calendar = ctk.CTkButton(self.schedule_service_frame, text="",height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,image=self.cal_icon,
                                               command=lambda: cctk.tk_calendar(self.scheduled_service_val, "%s"), corner_radius=3)
            self.show_calendar.grid(row=2, column=1, padx = (width*0.005,0), pady = (0,height*0.015), sticky="e")

            self.x_fr = ctk.CTkFrame(self.content_frame, height=height*0.78, width=width*0.312, fg_color="transparent")

            self.x_fr.grid(row=6, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', command=discard, font=("Arial", 20))
            self.back_button.grid(row=0, column=1, padx=20, pady=(15, 15), sticky='s')

            self.select_button = ctk.CTkButton(self.x_fr, text='Confirm', command=record, font=("Arial", 20))
            self.select_button.grid(row=0, column=2, padx=(0, 20), pady=(15, 15), sticky="se")

            sched_swtich_event()
            #on out

    return instance(master, info, parent_value)

def scheduled_services(master, info:tuple, parent= None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))

            def hide():
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, width=width*0.75, height=height*0.75, corner_radius=0)
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Scheduled Services', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=hide).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[3], corner_radius=0)
            self.content_frame.grid(row=1,column=0, padx=width*0.005, pady=height*0.01, sticky="nsew")
            self.content_frame.grid_columnconfigure(2, weight=1)
            self.content_frame.grid_rowconfigure(1, weight=1)
            self.content_frame.grid_propagate(0)

            self.search_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.35, height = height*0.05,)
            self.search_frame.grid(row=0, column=0,padx=(width*0.005),pady=(height*0.01), sticky="w")
            self.search_frame.pack_propagate(0)

            ctk.CTkLabel(self.search_frame,text="Search", font=("Arial", 14), text_color="grey", fg_color="transparent").pack(side="left", padx=(width*0.0075,width*0.0025))
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Type here...", border_width=0, corner_radius=5, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)
            self.search_btn = ctk.CTkButton(self.search_frame, text="", image=self.search, fg_color="white", hover_color="grey",
                                            width=width*0.005)
            self.search_btn.pack(side="left", padx=(0, width*0.0025))

            self.refresh_btn = ctk.CTkButton(self.content_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75")
            self.refresh_btn.grid(row=0, column=2,padx=(0,width*0.005),pady=(height*0.01),sticky="w")

            self.sched_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.sched_frame.grid(row=1, column=0, columnspan=3, sticky="nsew",padx=(width*0.005), pady=(0,height*0.01))

            self.sched_treeview = cctk.cctkTreeView(self.sched_frame, data =[], width=width*0.725, height=height*0.7,
                                               column_format=f'/No:{int(width*.025)}-#r/OR:{int(width*0.05)}-tc/ClientName:x-tl/Service:{int(width*.15)}-tr/Schedule:{int(width*.1)}-tc/Action:{int(width*.08)}-bD!30!30',)
            self.sched_treeview.pack()

    return instance(master, info, parent)

def add_particulars(master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func_item, change_val_func_service, service_dict: dict) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, root_treeview: cctk.cctkTreeView, change_val_func_item, change_val_func_service, service_dict: dict):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color="transparent")

            '''internal data'''
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(15,15))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self._service_dict = service_dict

            def hide():
                self.place_forget()
            def item_proceed(_: any = None):
                if self.item_treeview.data_grid_btn_mng.active:
                    data = self.item_treeview._data[self.item_treeview.data_frames.index(self.item_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[2], data[2])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[3].winfo_children()[0]
                        spinner.change_value()
                    else: #if there's none
                        root_treeview.add_data(add_data)
                        temp_data = root_treeview._data[-1]
                        temp_data = (temp_data[0], temp_data[1], 1, temp_data[2])
                        root_treeview._data[-1] = temp_data
                        data_frames = root_treeview.data_frames[-1]
                        spinner: cctk.cctkSpinnerCombo = data_frames.winfo_children()[3].winfo_children()[0]

                        spinner.configure(val_range = (1, data[1]))
                        change_val_func_item(price_format_to_float(data[2][1:]))
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
                    messagebox.showerror('Invalid Process', 'Assign the Client first')
                elif self.service_treeview.data_grid_btn_mng.active:
                    data = self.service_treeview._data[self.service_treeview.data_frames.index(self.service_treeview.data_grid_btn_mng.active)]
                    add_data = (data[0], data[1], data[1])
                    if data[0] in [s[0] for s in root_treeview._data]: # if there's existing record
                        print(*root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children(), sep = '\n')
                        spinner:cctk.cctkSpinnerCombo = root_treeview.data_frames[[s[0] for s in root_treeview._data].index(data[0])].winfo_children()[4].winfo_children()[0]
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
                            print(self._service_dict)

                        new_button = ctk.CTkButton(data_frames, corner_radius= 0,
                                                   text=label_text, width = root_treeview.column_widths[1],
                                                   command= lambda: serviceAvailing.pets(root_treeview.master, spinner.value, label_text, [s[2] for s in self.client],
                                                                                         proceed_command, None, self.winfo_screenwidth() * .65,
                                                                                         self.winfo_screenheight() * .6, fg_color= 'transparent').place(relx = .5, rely = .5,anchor = 'c'))
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

            self.main_frame = ctk.CTkFrame(self, width=width*0.815, height=height*0.875, corner_radius=0,fg_color=Color.White_Color[3])
            self.main_frame.pack()
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

            ctk.CTkLabel(self.top_frame, text='Particulars', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=self.reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.content_frame.grid(row=1, column=0,columnspan=2, sticky="nsew")
            
            self.content_frame.grid_columnconfigure(0, weight=1)
            self.content_frame.grid_rowconfigure((1,2), weight=1)
                
            self.client_name_frame = ctk.CTkFrame(self.content_frame, fg_color="light grey", width=width*0.4, height=height*0.045,)
            self.client_name_frame.grid(row=0, column=0, sticky="w", padx=(width*0.005), pady=(height*0.005))
            self.client_name_frame.pack_propagate(0)

            self.client_name_label = ctk.CTkLabel(self.client_name_frame, text="Client:",font=("DM Sans Medium", 15))
            self.client_name_label.pack(side="left",  padx=(width*0.01, 0), pady=(height*0.01))

            self.client_name_entry = ctk.CTkEntry(self.client_name_frame,font=("DM Sans Medium", 15), border_width=0, fg_color="white")
            self.client_name_entry.pack(side="left", fill="x", expand=1, padx=(width*0.005), pady=(height*0.005))

            self.service_frame = ctk.CTkFrame(self.content_frame, corner_radius=0)
            self.service_frame.grid(row=1,column=0, sticky="nsew", padx=(width*0.005),pady=(0,height*0.01))
            self.service_frame.pack_propagate(0)
            
            self.service_treeview = cctk.cctkTreeView(self.service_frame, height=height*0.4, width=width*0.8,corner_radius=0,double_click_command=service_proceed, column_format=f"/No:{int(width*.025)}-#r/ServiceName:x-tl/Price:x-tr!30!30")
            self.service_treeview.pack()
            
            self.item_frame = ctk.CTkFrame(self.content_frame, corner_radius=0)
            self.item_frame.grid(row=2, column=0, sticky="nsew",  padx=(width*0.005),pady=(0, height*0.01))
            self.item_frame.pack_propagate(0)
            
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_treeview = cctk.cctkTreeView(self.item_frame, data=self.data, height=height*0.4, width=width*0.8,double_click_command=item_proceed, column_format=f"/No:{int(width*.025)}-#r/ItemName:x-tl/Stocks:{int(width*.075)}-tr/Price:x-tr!30!30",)
            self.item_treeview.pack()
            
        def reset(self):
            self.place_forget()

        def place(self, **kwargs):
            if('client' in kwargs):
                self.check_client(kwargs['client'])
                kwargs.pop('client')
            raw_data = database.fetch_data(sql_commands.get_services_and_their_price, None)
            self.main_frame.pack()
            self.data = [(s[1], s[3]) for s in raw_data]
            self.service_treeview.update_table(self.data)
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            return super().place(**kwargs)
        
        def check_client(self, client_name: str):
            self.client = database.fetch_data(sql_commands.get_pet_info, (client_name, ))
        

        def get_service(self, _: any = None):
            #if there's a selected item
            if self.service_treeview.data_grid_btn_mng.active is not None:
                service_name =  self.service_treeview.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_services_data_for_transaction, (service_name, ))[0]
                self._treeview.add_data(transaction_data+(0, transaction_data[2]))
                return
                info_tab:cctk.info_tab = self._treeview.data_frames[-1].winfo_children()[3]
                info_tab._tab = customer_info(self._treeview.master.master, (info[0] * .8, info[1] * .8), info_tab)
                info_tab.button.configure(command = lambda: info_tab._tab.place(relx = .5, rely = .5, anchor = 'c'))
                self._data_reciever.append(info_tab)
                info_tab._tab.place(relx = .5, rely = .5, anchor = 'c')


                master.change_total_value_service(transaction_data[2])
                self.service_treeview.data_grid_btn_mng.deactivate_active()
                self.reset()
    return instance(master, info, root_treeview, change_val_func_item, change_val_func_service, service_dict)