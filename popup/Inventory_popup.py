import customtkinter as ctk
import sql_commands
from util import database
from tkinter import messagebox
from constants import action


def add_item(master, obj, info:tuple):
    class add_item(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            print(master)
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .8, height *.8, corner_radius= 0, fg_color='#111111')
            '''events'''
            def reset():
                self.place_forget()

            def add():
                if(self.item_name_entry.get() and self.manufacturer_entry.get() and self.category_entry.get() and self.price_entry.get() and
                self.supplier_entry.get() and self.stock_entry.get()):
                    self.warning_lbl.configure(text = '', fg_color='transparent')
                    uid = str(database.fetch_data('SELECT COUNT(uid) + 1 FROM item_general_info', (None, ))[0][0]).zfill(12)
                    database.exec_nonquery([[sql_commands.add_item_general, (uid, self.item_name_entry.get(), self.manufacturer_entry.get(), self.category_entry.get())],
                                            [sql_commands.add_item_inventory, (uid, int(self.stock_entry.get()), self.expiration_date_entry.get())],
                                            [sql_commands.add_item_settings, (uid, float(self.price_entry.get()), .85, .5, int(self.stock_entry.get()))],
                                            [sql_commands.add_item_supplier, (uid, self.supplier_entry.get(), self.contanct_entry.get())]])
                    messagebox.showinfo('Adding Succesfull')
                    master.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None);
                    master.data_view.update_table(master.data1)
                    reset()
                else:
                    self.warning_lbl.configure(text = 'Enter Required Fields', fg_color='red')

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.grid_propagate(0)
            ctk.CTkLabel(self, text='Add Item', anchor='w').grid(row = 0, column = 0, sticky = 'nsew', pady = (0, 12))

            self.frame = ctk.CTkFrame(self, corner_radius= 12, fg_color='#333333')
            self.frame.grid(row = 1, column = 0, sticky = 'nsew', padx =12, pady = (0,12))

            self.frame.rowconfigure(0, weight= 1)
            self.frame.rowconfigure(1, weight= 1)
            self.frame.columnconfigure(0, weight=1)
            self.frame.columnconfigure(1, weight=1)

            self.item_frame = ctk.CTkFrame(self.frame, corner_radius= 12, fg_color='#444444')
            self.item_frame.grid(row = 0, column = 0, sticky = 'nsew', padx =(12,0), pady = (12,0))
            self.item_frame.columnconfigure(0, weight=1)
            ctk.CTkLabel(self.item_frame, text='Item', anchor='w', font=('Arial', 24)).grid(row = 0, column = 0, sticky = 'nsew', pady = (12,12), padx= (12,0))

            ctk.CTkLabel(self.item_frame, text='Item Name', anchor='w').grid(row = 1, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.item_name_entry = ctk.CTkEntry(self.item_frame, corner_radius= 12, placeholder_text='Required')
            self.item_name_entry.grid(row = 2, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            ctk.CTkLabel(self.item_frame, text='Manufacturer', anchor='w').grid(row = 3, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.manufacturer_entry = ctk.CTkEntry(self.item_frame, corner_radius= 12, placeholder_text='Required')
            self.manufacturer_entry.grid(row = 4, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            ctk.CTkLabel(self.item_frame, text='Category', anchor='w').grid(row = 5, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.category_entry = ctk.CTkEntry(self.item_frame, corner_radius= 12, placeholder_text='Required')
            self.category_entry.grid(row = 6, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            ctk.CTkLabel(self.item_frame, text='Price', anchor='w').grid(row = 7, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.price_entry = ctk.CTkEntry(self.item_frame, corner_radius= 12, placeholder_text='Required')
            self.price_entry.grid(row = 8, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            self.supplier_frame = ctk.CTkFrame(self.frame, corner_radius= 12, fg_color='#444444')
            self.supplier_frame.grid(row = 0, column = 1, sticky = 'nsew', padx =(12,12), pady = (12,0))
            self.supplier_frame.columnconfigure(0, weight=1)
            ctk.CTkLabel(self.supplier_frame, text='Supplier', anchor='w', font=('Arial', 24)).grid(row = 0, column = 0, sticky = 'nsew', pady = (12,12), padx= (12,0))

            ctk.CTkLabel(self.supplier_frame, text='Supplier', anchor='w').grid(row = 1, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.supplier_entry = ctk.CTkEntry(self.supplier_frame, corner_radius= 12, placeholder_text='Required')
            self.supplier_entry.grid(row = 2, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            ctk.CTkLabel(self.supplier_frame, text='Contact', anchor='w').grid(row = 3, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.contanct_entry = ctk.CTkEntry(self.supplier_frame, corner_radius= 12, placeholder_text='')
            self.contanct_entry.grid(row = 4, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            self.inventory_frame = ctk.CTkFrame(self.frame, corner_radius= 12, fg_color='#444444')
            self.inventory_frame.grid(row = 1, column = 0, sticky = 'nsew', padx =(12,0), pady = (12,12))
            self.inventory_frame.columnconfigure(0, weight=1)
            ctk.CTkLabel(self.inventory_frame, text='Inventory', anchor='w', font=('Arial', 24)).grid(row = 0, column = 0, sticky = 'nsew', pady = (12,12), padx= (12,0))

            ctk.CTkLabel(self.inventory_frame, text='Stock', anchor='w').grid(row = 1, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.stock_entry = ctk.CTkEntry(self.inventory_frame, corner_radius= 12, placeholder_text='Required')
            self.stock_entry.grid(row = 2, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            ctk.CTkLabel(self.inventory_frame, text='Expiration Date', anchor='w').grid(row = 3, column = 0, sticky = 'nsew', pady = (12, 0), padx = (12,0))
            self.expiration_date_entry = ctk.CTkEntry(self.inventory_frame, corner_radius= 12, placeholder_text='')
            self.expiration_date_entry.grid(row = 4, column = 0, sticky = 'nsew', pady = (2,0), padx= (12,12))

            self.action_frame = ctk.CTkFrame(self.frame, corner_radius= 12, fg_color='transparent')
            self.action_frame.grid(row = 1, column = 1, sticky = 'nsew', padx =(12,12), pady = (12,12))

            self.warning_lbl = ctk.CTkLabel(self.action_frame, text='', fg_color='transparent')
            self.warning_lbl.pack()
            self.add_btn = ctk.CTkButton(self.action_frame, 140, 28, text='Add', command= add)
            self.add_btn.pack()
            self.cancel_btn = ctk.CTkButton(self.action_frame, 140, 28, text='Cancel', command= reset)
            self.cancel_btn.pack()
    return add_item(master, obj, info)

def restock( master, obj, info:tuple):
    class restock(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .8, height *.8, corner_radius= 0, fg_color='#111111')
            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.grid_propagate(0)

            '''events'''
            def reset():
                self.place_forget()

            def validate_acc(_):
                self.item_uid = database.fetch_data("SELECT uid FROM item_general_info WHERE NAME = ?", (self.item_name_entry.get(),))
                self.item_uid = self.item_uid[0][0] if self.item_uid else None

                if self.item_uid is None:
                    return
                if(database.fetch_data('SELECT Expiry_date FROM item_inventory_info WHERE UID = ?', (self.item_uid, ))is not None):
                    self.expiry_date_entry.configure(state = ctk.NORMAL)
                else:
                    self.expiry_date_entry.configure(state = ctk.DISABLED)
                self.stock_entry.configure(state = ctk.NORMAL)
                self.action_btn.configure(state = ctk.NORMAL)

            def stock():
                inventory_data = database.fetch_data("SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date IS NULL OR Expiry_Date = ?)",
                                                    (self.item_uid, self.expiry_date_entry.get() or '1000-01-01'))

                if inventory_data: # if there was an already existing table; update the existing table
                    if inventory_data[0][2] is None:
                        database.exec_nonquery([[sql_commands.update_non_expiry_stock, (int(self.stock_entry.get()), self.item_uid)]])
                    else:
                        database.exec_nonquery([[sql_commands.update_expiry_stock, (int(self.stock_entry.get()), self.item_uid, inventory_data[0][2])]])
                else:# if there's no exisiting table; create new instance of an item
                    database.exec_nonquery([[sql_commands.add_new_instance, (self.item_uid, self.stock_entry.get(), self.expiry_date_entry.get() or None)]])

                database.exec_nonquery([['INSERT INTO action_history VALUES (?, ?, ?)',
                                        (acc_cred[0], action.RESTOCKED_ITEM % (self.item_uid, self.stock_entry.get(), True))]])
                messagebox.showinfo('Adding Succesfull')
                master.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None);
                master.data_view.update_table(master.data1)
                reset()

            ctk.CTkLabel(self, text='restock', anchor='w').grid(row = 0, column = 0, sticky = 'nsew', pady = (0, 12))

            self.frame = ctk.CTkFrame(self, corner_radius= 12, fg_color='#333333')
            self.frame.grid(row = 1, column = 0, sticky = 'nsew', padx =12, pady = (0,12))

            ctk.CTkLabel(self.frame, text='Item:', anchor='w').grid(row = 0, column = 0, padx = 12, sticky = 'nsew')
            self.item_name_entry = ctk.CTkEntry(self.frame, width *.5, height * .05, placeholder_text='Item Name')
            self.item_name_entry.bind('<Return>', validate_acc)
            self.item_name_entry.bind('<FocusOut>', validate_acc)
            self.item_name_entry.grid(row = 1, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))

            ctk.CTkLabel(self.frame, text='Expiration Date', anchor='w').grid(row = 2, column = 0, padx = 12, sticky = 'nsew')
            self.expiry_date_entry = ctk.CTkEntry(self.frame, width *.5, height * .05, placeholder_text='Expiration Date', state = ctk.DISABLED,
                                                )
            self.expiry_date_entry.grid(row = 3, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))

            ctk.CTkLabel(self.frame, text='Stock', anchor='w').grid(row = 4, column = 0, padx = 12, sticky = 'nsew')
            self.stock_entry = ctk.CTkEntry(self.frame, width *.5, height * .05, placeholder_text='Stock', state = ctk.DISABLED)
            self.stock_entry.grid(row = 5, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))

            self.warning_text =  ctk.CTkLabel(self.frame, text='', anchor='w', text_color='red')
            self.warning_text.grid(row = 6, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))

            self.action_btn = ctk.CTkButton(self.frame, width * .04, height * .05, 12, text='Restock', command=stock, state=ctk.DISABLED)
            self.action_btn.grid(row = 7, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))

            self.leave_btn = ctk.CTkButton(self.frame, width * .04, height * .05, 12, text='Back', command = reset)
            self.leave_btn.grid(row = 8, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))
    return restock(master, obj, info)