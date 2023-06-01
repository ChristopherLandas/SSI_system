import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
from constants import action
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from decimal import Decimal
import datetime

def show_item_list(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            self._master = master
            self.width = info[0]
            self.height = info[1]
            self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, self.width * .8, self.height *.8, corner_radius= 0)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.grid_propagate(0)

            self.upper_frame = ctk.CTkFrame(self, height= self.height * .075, corner_radius= 0, fg_color='#222222')
            self.upper_frame.pack_propagate(0)
            self.upper_frame.grid(row = 0, column = 0, sticky = 'we')
            ctk.CTkLabel(self.upper_frame, text='Add Item', font=('Arial', 24)).pack(side=ctk.LEFT, padx = (12, 0))
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.lower_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='#111111')
            self.item_table = cctk.cctkTreeView(self.lower_frame, self.data, self.width * .75, self.height * .65,
                                                column_format='/name:x-tl/quantity:250-tl!50!30',
                                                double_click_command= self.get_item)
            self.item_table.pack(pady = (12, 0), fill='y')
            self.select_btn = ctk.CTkButton(self.lower_frame, 120, 30, text='select', command= self.get_item)
            self.select_btn.pack(pady = (0, 12))
            self.lower_frame.grid(row = 1, column = 0, sticky = 'nsew')
            #self.back_btn = ctk.CTkButton(self, width*.03, height * .4, text='back', command= reset).pack(pady = (12, 0))

        def place(self, **kwargs):
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.item_table.update_table(self.data)
            return super().place(**kwargs)

        def reset(self):
            self.place_forget()

        def get_item(self, _: any = None):
            #if there's a selected item
            if self.item_table.data_grid_btn_mng.active is not None:
                item_name =  self.item_table.data_grid_btn_mng.active.winfo_children()[0]._text
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
                    self._treeview.add_data(transaction_data+(0, transaction_data[2]))
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
                    , int(self.item_table.data_grid_btn_mng.active.winfo_children()[1]._text)))
                    #add a new record
                    master.change_total_value_item(transaction_data[2])

                self.item_table.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup
    return instance(master, info)


def show_services_list(master, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            self._master = master
            self.width = info[0]
            self.height = info[1]
            self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, self.width * .8, self.height *.8, corner_radius= 0)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.grid_propagate(0)

            self.upper_frame = ctk.CTkFrame(self, height= self.height * .075, corner_radius= 0, fg_color='#222222')
            self.upper_frame.pack_propagate(0)
            self.upper_frame.grid(row = 0, column = 0, sticky = 'we')
            ctk.CTkLabel(self.upper_frame, text='Add Service', font=('Arial', 24)).pack(side=ctk.LEFT, padx = (12, 0))
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.lower_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='#111111')
            self.service_table = cctk.cctkTreeView(self.lower_frame, self.data, self.width * .75, self.height * .65,
                                                column_format='/Name:x-tl/Price:250-tl!50!30',
                                                double_click_command= self.get_item)
            self.service_table.pack(pady = (12, 0), fill='y')
            self.select_btn = ctk.CTkButton(self.lower_frame, 120, 30, text='select', command= self.get_item)
            self.select_btn.pack(pady = (0, 12))
            self.lower_frame.grid(row = 1, column = 0, sticky = 'nsew')
            #self.back_btn = ctk.CTkButton(self, width*.03, height * .4, text='back', command= reset).pack(pady = (12, 0))

        def place(self, **kwargs):
            raw_data = database.fetch_data(sql_commands.get_services_and_their_price, None)
            self.data = [(s[1], s[3]) for s in raw_data]
            self.service_table.update_table(self.data)
            return super().place(**kwargs)

        def reset(self):
            self.place_forget()

        def get_item(self, _: any = None):
            #if there's a selected item
            if self.service_table.data_grid_btn_mng.active is not None:
                service_name =  self.service_table.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_services_data_for_transaction, (service_name, ))[0]
                #collects part of the data needed in the transaction
                service_in_treeview = [s.winfo_children()[2]._text if self._treeview.data_frames != [] else None for s in self._treeview.data_frames]
                #search the tree view if there's an already existing item

                #if there's an already existing item
                #if(service_name in service_in_treeview):
                #    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[service_in_treeview.index(service_name)].winfo_children()[3].winfo_children()[0]
                #    quantity_column.change_value()
                #    #change the value of the spinner combo; modifying the record's total price
                #else:
                self._treeview.add_data(transaction_data+(0, transaction_data[2]))
                quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[-1].winfo_children()[3].winfo_children()[0]
                price_column: ctk.CTkLabel = self._treeview.data_frames[-1].winfo_children()[6]

                '''def spinner_command(mul: int = 0):
                    master.change_total_value_service(-float(price_column._text))
                    #before change

                    price_change = quantity_column._base_val * quantity_column.value
                    master.change_total_value_service(price_change)
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
                    , int(self.item_table.data_grid_btn_mng.active.winfo_children()[1]._text)))'''
                    #add a new record

                master.change_total_value_service(transaction_data[2])
                self.service_table.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup
    return instance(master, info)

def show_transaction_proceed(master, info:tuple, item_info: list, services_info, total_price: float) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, item_info: list, services_info, total_price: float):
            width = info[0] * .99
            height = info[1] * .99
            #basic inforamtion needed; measurement

            self.acc_cred = info[3]
            self._treeview = info[2]
            self._item_info = item_info
            self._services_info = services_info
            self._total_price = total_price
            #encapsulation

            super().__init__(master, width, height=height, corner_radius= 0, fg_color='white')
            #the actual frame, modification on the frame itself goes here

            '''events'''
            def auto_pay(_: any = None):
                self.payment_entry.delete(0, ctk.END)
                self.payment_entry.insert(0, self._total_price)
                record_transaction()

            def record_transaction():
                if (float(self.payment_entry.get() or '0')) < self._total_price:
                    messagebox.showinfo('Kulang', 'Ano to utang? Magbayad ka ng buo')
                    return
                record_id =  database.fetch_data(sql_commands.generate_id_transaction, (None))[0][0]
                database.exec_nonquery([[sql_commands.record_transaction, (record_id, self.acc_cred[0], self._total_price)]])
                #record the transaction

                modified_items_list = [(record_id, s[0], s[1], s[3], float(s[2]), 0) for s in self._item_info]
                database.exec_nonquery([[sql_commands.record_item_transaction_content, s] for s in modified_items_list])
                #record the items from eithin the transaction

                modified_services_list = [(record_id, s[0], s[1], 'fredo', str(datetime.datetime.now().date()), float(s[2]), 0) for s in self._services_info]
                database.exec_nonquery([[sql_commands.record_services_transaction_content, s] for s in modified_services_list])
                #record the services from eithin the transaction

                for item in modified_items_list:
                    stocks = database.fetch_data(sql_commands.get_specific_stock, (item[1], ))
                    if stocks[0][2] is None:
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (-item[3], item[1])]])
                    else:
                        quan = item[3]
                        for st in stocks:
                            if st[1] < quan:
                                quan -= st[1]
                                database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                            elif st[1] > quan:
                                database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, item[1], st[2])]])
                                break
                            else:
                                if stocks[-1] == st:
                                    database.exec_nonquery([[sql_commands.update_expiry_stock, (-quan, item[1], st[2])]])
                                else:
                                    database.exec_nonquery([['DELETE FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?', (st[0], st[2])]])
                                break
                #modify the stock

                payment = float(self.payment_entry.get())
                self.payment_entry.configure(text_color = 'red')
                self.payment_entry.delete(0, ctk.END)
                self.payment_entry.insert(0, format_price(round(self._total_price - payment, 2)))
                #calculate and show the change

                master.reset()
                messagebox.showinfo('Sucess', 'Transaction Complete')
                self._treeview[0].delete_all_data()
                self._treeview[1].delete_all_data()
                self.destroy()
                #reset into its default state

            self.left_frame = ctk.CTkFrame(self)
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.services_lbl = ctk.CTkLabel(self.left_frame, text='Services:',font=("Poppins", 45))
            self.services_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            '''self.services_entry = ctk.CTkEntry(self.left_frame,  height=height*0.78, width=width*0.2)
            self.services_entry.grid(row=1, column=0, padx=10, pady=10, sticky="ns")'''
            self.service_data = [('Service1', format_price(float(s[4]))) for s in self._services_info]
            self.service_list = cctk.cctkTreeView(self.left_frame, self.service_data, height=height*0.75, width=width*0.2,
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Price:{int(width * .05)}-tr!50!30')
            self.service_list.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

            self.right_frame = ctk.CTkFrame(self)
            self.right_frame.grid(row=0, column=1, padx=20, pady=10, sticky="nsew")

            self.items_lbl = ctk.CTkLabel(self.right_frame, text='Items:',font=("Poppins", 45))
            self.items_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")

            self.item_data = [('item1', format_price(float(s[4]))) for s in self._item_info]
            self.item_list = cctk.cctkTreeView(self.right_frame, self.item_data, height=height*0.75, width=width*0.2,
                                               column_format=f'/No:{int(width * .03)}-#c/Name:x-tl/Price:{int(width * .05)}-tr!50!30')
            self.item_list.grid(row=1, column=0, padx=10, pady=10, sticky="ns")

            self.rightmost_frame = ctk.CTkFrame(self, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=0, column=2, padx=10, pady=10, sticky="nse")


            self.total_frame = ctk.CTkFrame(self.rightmost_frame)
            self.total_frame.grid(row=0, column=0, padx=10, pady=10, sticky="new", columnspan = 2)

            self.total_lbl = ctk.CTkLabel(self.total_frame, text='Total:',font=("Poppins", 25))
            self.total_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.total_val = ctk.CTkEntry(self.total_frame, height=height*0.12, width=width*0.31, font=('DM Sans Medium', 35))
            self.total_val.insert(0, format_price(self._total_price))
            self.total_val.configure(state = 'readonly')
            self.total_val.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="n")

            self.payment_options_frame = ctk.CTkFrame(self.rightmost_frame)
            self.payment_options_frame.grid(row=1, column=0, padx=10, pady=(10, height*0.22), sticky="new", columnspan = 2)

            self.payment_lbl = ctk.CTkLabel(self.payment_options_frame, text='Payment Method:', font=("Poppins", 25))
            self.payment_lbl.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

            self.payment_method_cbox = ctk.CTkOptionMenu(self.payment_options_frame, values=["Cash", "Card", "Bank Statement"], font=("Poppins", 25), height=height*0.08,width=width*0.31
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

            self.cancel_button = ctk.CTkButton(self.rightmost_frame, text='Cancel', command= lambda: self.destroy(), width=135, font=("Poppins-Bold", 45))
            self.cancel_button.grid(row=4, column=1, padx=(40, 50), pady =(10,10), sticky="ew")

            self.payment_entry.focus_force()
            self.payment_entry.bind('<Shift-Return>', auto_pay)
    return instance(master, info, item_info, services_info, total_price)

def customer_info(master, info:tuple, parent= None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, parent):
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="red")
            #the actual frame, modification on the frame itself goes here
            self.value:tuple = (None, None, None, None)

            def hide():
                self.place_forget()
                self.pack_forget()
                self.grid_forget()

            def discard():
                if messagebox.askyesno('NOTE!', 'all changes will be discarded?'):
                    self.pet_name.delete(0, ctk.END)
                    self.animal_breed_entry.delete(0, ctk.END)
                    self.scheduled_service_entry.delete(0, ctk.END)
                    self.note_entry.delete(0, ctk.END)
                    self.pet_name.insert(0, self.value[0] or '')
                    self.animal_breed_entry.insert(0, self.value[1] or '')
                    self.scheduled_service_entry.insert(0, self.value[2] or '')
                    self.note_entry.insert(0, self.value[3] or '')
                    hide()


            def record():
                self.value = (self.pet_name.get(), self.animal_breed_entry.get(), self.scheduled_service_entry.get(), self.note_entry.get())
                if isinstance(parent, cctk.info_tab):
                    parent.value = self.value
                hide()


            self.left_frame = ctk.CTkFrame(self, bg_color='#c3c3c3')
            self.left_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsw")

            self.pet_info_lbl = ctk.CTkLabel(self.left_frame, text='Pet Info',font=("Poppins", 45))
            self.pet_info_lbl.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
            #Name label
            self.Name_lbl = ctk.CTkLabel(self.left_frame, text='Name:',font=("Poppins", 25))
            self.Name_lbl.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Name entry
            self.pet_name = ctk.CTkEntry(self.left_frame, placeholder_text='chao pan', height=height*0.09, width=width*0.795, font=("Poppins", 25))
            self.pet_name.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="ns")
            #Breed and Animal Type label
            self.animal_breed_lbl = ctk.CTkLabel(self.left_frame, text='Breed and Animal Type:',font=("Poppins", 25))
            self.animal_breed_lbl.grid(row=3, column=0, padx=10, pady=(10, 0), sticky="nw")
            #Breed and Animal Type entry
            self.animal_breed_entry = ctk.CTkEntry(self.left_frame, placeholder_text='dog', height=height*0.09, width=width*0.795, font=("Poppins", 25))
            self.animal_breed_entry.grid(row=4, column=0, padx=10, pady=(0, 10), sticky="ns")
            #calendar and note frame
            self.middle_frame = ctk.CTkFrame(self.left_frame, bg_color='#D9D9D9', fg_color='#D9D9D9')
            self.middle_frame.grid(row=5, column=0, padx=10, pady=(20, 10), sticky="nsw")
            #sched service frame
            self.schedule_service_frame = ctk.CTkFrame(self.middle_frame, bg_color='#D9D9D9')
            self.schedule_service_frame.grid(row=0, column=0, padx=10, pady=(20, 10), sticky="nsw")
            #Scheduled service label
            self.scheduled_service_lbl = ctk.CTkLabel(self.schedule_service_frame, text='Scheduled Service:',font=("Poppins", 25))
            self.scheduled_service_lbl.grid(row=0, column=0, padx=(10, 0), pady=(0, 10), sticky="nw")
            #Scheduled service entry
            self.scheduled_service_entry = ctk.CTkEntry(self.schedule_service_frame, placeholder_text='date', height=height*0.09, width=width*0.285, font=("Poppins", 25))
            self.scheduled_service_entry.grid(row=1, column=0, padx=(10, 0), pady=(0, 10), sticky="ns")
            #note frame
            self.note_frame = ctk.CTkFrame(self.middle_frame, bg_color='#D9D9D9')
            self.note_frame.grid(row=0, column=1, padx=10, pady=(20, 10), sticky="nsw")
            #note label
            self.note_lbl = ctk.CTkLabel(self.note_frame, text='Note:',font=("Poppins", 25))
            self.note_lbl.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="nw")
            #note entry
            self.note_entry = ctk.CTkEntry(self.note_frame, placeholder_text='a dog', height=height*0.25, width=width*0.445, font=("Poppins", 25))
            self.note_entry.grid(row=1, column=1, padx=10, pady=(0, 10), sticky="ns")


            self.rightmost_frame = ctk.CTkFrame(self, height=height*0.78, width=width*0.312, fg_color='white')
            self.rightmost_frame.grid(row=2, column=0, padx=10, pady=10, sticky="es")

            self.x_fr = ctk.CTkFrame(self.rightmost_frame, height=height*0.78, width=width*0.312, fg_color='white')

            self.x_fr.grid(row=2, column=0, padx=10, pady=10, sticky="s")

            self.back_button = ctk.CTkButton(self.x_fr, text='Back', command=discard, width=270, font=("Poppins-Bold", 45))

            self.back_button.grid(row=0, column=1, padx=20, pady=(15, 15), sticky='s')

            self.select_button = ctk.CTkButton(self.x_fr, text='Select', command=record, width=270, font=("Poppins-Bold", 45))
            self.select_button.grid(row=0, column=2, padx=(0, 20), pady=(15, 15), sticky="se")
            #on out
    return instance(master, info, parent)