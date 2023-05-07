import customtkinter as ctk
import sql_commands
from util import database
from tkinter import messagebox


def add_item(master, obj):
    class add_item(ctk.CTkFrame):
        def __init__(self, master, obj):
            width = master.width
            height = master.height
            acc_cred = master.acc_cred
            acc_info = master.acc_info
            super().__init__(master, width * .8, height *.8, corner_radius= 0, fg_color='#111111')
            '''events'''
            def reset():
                master.add_item_popup = add_item(master)
                self.destroy()

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

def test():
    class instance():
        print('hello')