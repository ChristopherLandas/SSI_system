import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
import tkcalendar
from Theme import Color
from util import database
from tkinter import messagebox
from constants import action
from PIL import Image

def add_item(master, info:tuple):
    class add_item(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color="transparent")

            '''default'''
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))

            #set to transparent to prevent clicking other buttons inside the inventory
            '''events'''
            def reset():
                self.place_forget()

            def add():
                if(self.item_name_entry.get() and self.manufacturer_entry.get() and self.category_entry.get() and self.price_entry.get() and
                self.supplier_entry.get() and self.stock_entry.get()):
                    self.warning_lbl.configure(text = '', fg_color='transparent')
                    uid = str(database.fetch_data('SELECT COUNT(uid) + 1 FROM item_general_info', (None, ))[0][0]).zfill(5)
                    database.exec_nonquery([[sql_commands.add_item_general, (uid, self.item_name_entry.get(), self.category_entry.get(), 0)],
                                            [sql_commands.add_item_inventory, (uid, int(self.stock_entry.get()), self.expiration_date_entry.cget("text") or None)],
                                            [sql_commands.add_item_settings, (uid, float(self.price_entry.get()) / 1.1, .1, .85, .5, int(self.stock_entry.get()))],
                                            [sql_commands.add_item_supplier, (uid, self.supplier_entry.get(), self.contact_entry.get())]])
                    messagebox.showinfo('Adding Succesfull')
                    master.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None);
                    master.data_view.update_table(master.data1)
                    reset()
                else:
                    self.warning_lbl.configure(text = 'Enter Required Fields', fg_color='red')

            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], corner_radius=0)
            self.main_frame.grid(row=0, column=0, sticky="ew", padx=width*0.01, pady=height*0.02)

            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='ADD ITEM', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.025, command=reset).pack(side="right", padx=(0,width*0.01))

            self.item_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.item_frame.grid(row = 1, column = 0, sticky = 'new', padx =(width*0.01), pady = (height*0.015,0))
            self.item_frame.columnconfigure((1), weight=1)
            ctk.CTkLabel(self.item_frame, text='ITEM', anchor='w', font=('DM Sans Medium', 18), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            ctk.CTkLabel(self.item_frame, text='Item Name', anchor='w', font=("DM Sans Medium", 14)).grid(row = 1, column = 0, columnspan=2, sticky = 'nsew', pady = (height*0.005,0), padx = (width*0.01))
            self.item_name_entry = ctk.CTkEntry(self.item_frame, corner_radius=3, placeholder_text='Required', font=("DM Sans Medium",14))
            self.item_name_entry.grid(row = 2, column = 0,columnspan=2, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            ctk.CTkLabel(self.item_frame, text='Manufacturer', anchor='w', font=("DM Sans Medium", 14)).grid(row = 3, column = 0, columnspan=2, sticky = 'nsew', pady = (height*0.005,0), padx = (width*0.01))
            self.manufacturer_entry = ctk.CTkEntry(self.item_frame, corner_radius=3, placeholder_text='Required', font=("DM Sans Medium",14))
            self.manufacturer_entry.grid(row = 4, column = 0,columnspan=2, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            ctk.CTkLabel(self.item_frame, text='Category', anchor='w', font=("DM Sans Medium", 14)).grid(row = 5, column = 0,columnspan=2, sticky = 'nsew',  pady = (height*0.005,0), padx = (width*0.01))
            self.category_entry = ctk.CTkComboBox(self.item_frame, corner_radius=3, values=["Vaccine", "Medicine", "Accessories", "Leash", "Shampoo"], font=("DM Sans Medium",14))
            self.category_entry.grid(row = 6, column = 0,columnspan=2, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            ctk.CTkLabel(self.item_frame, text='Price: ', font=("DM Sans Medium", 14), anchor="e").grid(row = 7, column = 0, sticky="nsew",pady = (height*0.005,0), padx = (width*0.0125,0))
            self.price_entry = cctk.cctkSpinnerCombo(self.item_frame, step_count=5, entry_font=("DM Sans Medium",14), val_range=(0, cctk.cctkSpinnerCombo.MAX_VAL))
            self.price_entry.grid(row = 7, column = 1, sticky = 'w', pady = (height*0.005, height*0.01), padx = (width*0.005,width*0.01))

            self.supplier_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.supplier_frame.grid(row = 2, column = 0, sticky = 'new', padx =(width*0.01), pady = (height*0.015))
            self.supplier_frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(self.supplier_frame, text='SUPPLIER', anchor='w',  font=("DM Sans Medium", 18)).grid(row = 0, column = 0, sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            ctk.CTkLabel(self.supplier_frame, text='Supplier', anchor='w', font=("DM Sans Medium",14)).grid(row = 1, column = 0, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))
            self.supplier_entry = ctk.CTkEntry(self.supplier_frame, corner_radius= 3, placeholder_text='Required', font=("DM Sans Medium",14))
            self.supplier_entry.grid(row = 2, column = 0, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            ctk.CTkLabel(self.supplier_frame, text='Contact', anchor='w', font=("DM Sans Medium",14)).grid(row = 3, column = 0, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))
            self.contact_entry = ctk.CTkEntry(self.supplier_frame, corner_radius= 3, placeholder_text='', font=("DM Sans Medium",14))
            self.contact_entry.grid(row = 4, column = 0, sticky = 'nsew', pady = (0,height*0.025), padx = (width*0.01))

            self.inventory_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.inventory_frame.grid(row = 1, column = 1, sticky = 'nsew', padx =(0,width*0.01), pady = (height*0.015,0))

            ctk.CTkLabel(self.inventory_frame, text='INVENTORY', anchor='w', font=('DM Sans Medium', 18)).grid(row = 0, column = 0,columnspan=2, sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            ctk.CTkLabel(self.inventory_frame, text='Stock: ',anchor="e", font=("DM Sans Medium", 14)).grid(row = 1, column = 0, sticky = 'w',padx = (width*0.01,0))
            self.stock_entry = cctk.cctkSpinnerCombo(self.inventory_frame, entry_font=("DM Sans Medium",14))
            self.stock_entry.grid(row = 1, column = 1, sticky = 'w',padx=(0,width*0.01), columnspan=2)

            ctk.CTkLabel(self.inventory_frame, text='Expiration Date', anchor='w', font=("DM Sans Medium", 14)).grid(row = 3, column = 0, sticky = 'nsew', pady = (0), padx = (12,0))
            self.expiration_date_entry = ctk.CTkLabel(self.inventory_frame, corner_radius= 5, text='Set Expiry Date',fg_color="white", width=width*0.15,height=height*0.05, font=("DM Sans Medium", 14))
            self.expiration_date_entry.grid(row = 4, column = 0, sticky = 'nsew',columnspan=2, pady = (height*0.015), padx = (width*0.01))

            self.show_calendar = ctk.CTkButton(self.inventory_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03,
                                               command=lambda: cctk.tk_calendar(self.expiration_date_entry, "%s"), corner_radius=3 )
            self.show_calendar.grid(row=4, column=2, padx = (0,width*0.01), sticky="w")

            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 2, column = 1, sticky = 'nsew', padx=(0,width*0.01), pady = (height*0.015))

            self.warning_lbl = ctk.CTkLabel(self.action_frame, text='', fg_color='transparent', font=("DM Sans Medium",14))
            self.warning_lbl.pack(pady=(height*0.025))
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.05, height=height*0.05,corner_radius=3, font=("DM Sans Medium", 14), text='Cancel', command= reset)
            self.cancel_btn.pack(side="left", padx=(width*0.025,width*0.005))
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.125, height=height*0.05,corner_radius=3, font=("DM Sans Medium", 14), text='Add New Item', command= add)
            self.add_btn.pack(side="left", padx=(width*0.005, width*0.025))

    return add_item(master, info)

def restock( master, info:tuple):
    class restock(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
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

              # database.exec_nonquery([['INSERT INTO action_history VALUES (?, ?, ?)',
                   #                     (acc_cred[0], action.RESTOCKED_ITEM % (self.item_uid, self.stock_entry.get(), True))]])
                messagebox.showinfo('Adding Succesfull')
                master.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None);
                master.data_view1.update_table(master.data1)
                master.data_view2.update_table(master.data2)
                reset()

            ctk.CTkLabel(self, text='restock', anchor='w').grid(row = 0, column = 0, sticky = 'nsew', pady = (0, 12))

            self.frame = ctk.CTkFrame(self, corner_radius= 12, fg_color='#333333')
            self.frame.grid(row = 1, column = 0, sticky = 'nsew', padx =12, pady = (0,12))

            ctk.CTkLabel(self.frame, text='Item:', anchor='w').grid(row = 0, column = 0, padx = 12, sticky = 'nsew')

            item = [c[0] for c in database.fetch_data(sql_commands.show_all_items, None)]
            self.item_name_entry = cctk.selection_comboBox(self.frame, width * .5, height * .05, hover = False, command= validate_acc,
                                                           values= list(item))
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
    return restock(master, info)