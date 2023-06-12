import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
import tkcalendar
from Theme import Color
from util import database, generateId
from tkinter import messagebox
from constants import action
import datetime
from PIL import Image
import datetime
from functools import partial
from typing import *

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
                self.item_name_entry.delete(0, ctk.END)
                self.place_forget()

            def add():
                if(self.item_name_entry.get() and self.unit_price_entry.get() and self.markup_price_entry.get()
                   and self.category_entry.get() and self.supplier_entry.get() and self.stock_entry.get() and
                   ((self.expiration_date_entry._text != 'Set Expiry Date' and self.expiry_switch_val.get())
                   or self.expiry_switch_val.get() == 'disabled')):
                    self.warning_lbl.configure(text = '', fg_color='transparent')
                    uid = 'I'+str(database.fetch_data('SELECT COUNT(uid) + 1 FROM item_general_info', (None, ))[0][0]).zfill(5)
                    modified_dt: str = str(datetime.datetime.strptime(self.expiration_date_entry._text, '%m-%d-%Y').strftime('%Y-%m-%d')) if self.expiration_date_entry._text != 'Set Expiry Date' else None
                    database.exec_nonquery([[sql_commands.add_item_general, (uid, self.item_name_entry.get(), self.category_entry.get(), 0 if self.expiry_switch_val.get() == 'disabled' else 1)],
                                            [sql_commands.add_item_inventory, (uid, int(self.stock_entry.get()), modified_dt)],
                                            [sql_commands.add_item_settings, (uid, float(self.unit_price_entry.get()), float(self.markup_price_entry.get())/100, .75, .5, int(self.stock_entry.get()))],
                                            [sql_commands.add_item_supplier, (uid, self.supplier_entry.get(), self.contact_entry.get())]])
                    messagebox.showinfo('Adding Succesfull')
                    master.reset()
                    reset()
                else:
                    self.warning_lbl.configure(text = 'Enter Required Fields', text_color='red')
            def expiry_switch_event():
                self.show_calendar.configure(state=self.expiry_switch_val.get())
                if(self.expiry_switch_val.get()=="normal"):
                    self.show_calendar.configure(fg_color=Color.Blue_Yale)
                    self.expiration_date_entry.configure(fg_color="white", text_color="black")
                    self.expiry_switch.configure(text="Yes")
                else:
                    self.expiry_switch.configure(text="No")
                    self.show_calendar.configure(fg_color="light grey")
                    self.expiration_date_entry.configure(fg_color="light grey", text_color="grey")

            def markup_callback(_ = None, *__):
                self.selling_price_entry.configure(state = ctk.NORMAL)
                self.selling_price_entry.delete(0, ctk.END)
                if self.markup_price_entry.get():
                    if self.unit_price_entry.get() and self.markup_price_entry.get():
                        markup = round(float(self.unit_price_entry.get()) * (float(self.markup_price_entry.get()) / 100), 2)
                        self.selling_price_entry.insert(0, float(self.unit_price_entry.get()) + markup)
                self.selling_price_entry.configure(state = 'readonly')

            def selling_callback(_ = None, *__):
                self.markup_price_entry.delete(0, ctk.END)
                if (not self.markup_price_entry.get()) and self.unit_price_entry.get() and self.selling_price_entry.get():
                    self.markup_price_entry.insert(0, round(float(self.unit_price_entry.get()) / (float(self.selling_price_entry.get()) / 100), 2))

            def category_expiry_callback(category):
                if ("Vaccine" in category or "Medicine" in category):
                    self.expiry_switch.select()
                else:
                    self.expiry_switch.deselect()
                expiry_switch_event()

                print(category)
                pass


            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            self.item_category = ["Vaccine","Medicine","Accessories"]

            self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Color[3], corner_radius=0)
            self.main_frame.grid(row=0, column=0, sticky="new", padx=width*0.01, pady=height*0.02)

            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='ADD ITEM', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.025, command=reset).pack(side="right", padx=(0,width*0.01))

            '''Item Frame'''
            self.item_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.item_frame.grid(row = 1, column = 0, sticky = 'new', padx =(width*0.01), pady = (height*0.015,0))
            self.item_frame.columnconfigure((5), weight=1)
            ctk.CTkLabel(self.item_frame, text='ITEM', anchor='w', font=('DM Sans Medium', 18), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            ctk.CTkLabel(self.item_frame, text='Item Name', anchor='w', font=("DM Sans Medium", 14)).grid(row = 1, column = 0, columnspan=2, sticky = 'nsew', pady = (height*0.005,0), padx = (width*0.01))
            self.item_name_entry = ctk.CTkEntry(self.item_frame, corner_radius=3, placeholder_text='Required', font=("DM Sans Medium",14))
            self.item_name_entry.grid(row = 2, column = 0,columnspan=6, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            ctk.CTkLabel(self.item_frame, text='Category', anchor='w', font=("DM Sans Medium", 14)).grid(row = 5, column = 0,columnspan=2, sticky = 'nsew',  pady = (height*0.025,0), padx = (width*0.01))
            self.category_entry = ctk.CTkComboBox(self.item_frame, corner_radius=3, values=self.item_category, font=("DM Sans Medium",14),command=partial(category_expiry_callback))
            self.category_entry.grid(row = 6, column = 0,columnspan=6, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            self.category_entry.set(self.item_category[2])

            ctk.CTkLabel(self.item_frame, text='Unit Price: ', font=("DM Sans Medium", 14), anchor="e").grid(row = 7, column = 0, sticky="w",pady = (height*0.025,0), padx = (width*0.0125,0))
            self.unit_price_entry = ctk.CTkEntry(self.item_frame, width=width*0.3, textvariable= ctk.StringVar())
            #self.unit_price_entry._textvariable.trace_add('write', lambda: None)
            self.unit_price_entry.grid(row = 7, column = 1, sticky = 'w', pady = (height*0.025,0), padx = (width*0.0125,0))

            ctk.CTkLabel(self.item_frame, text='Mark Up: ', font=("DM Sans Medium", 14), anchor="e").grid(row = 9, column = 0, sticky="w",pady = (height*0.008,0), padx = (width*0.0125,0))
            self.markup_price_entry = ctk.CTkEntry(self.item_frame, width=width*0.3, textvariable= ctk.StringVar())
            self.markup_price_entry._textvariable.trace_add('write', markup_callback)
            self.markup_price_entry.grid(row = 9, column = 1, sticky = 'w', pady = (height*0.025,0), padx = (width*0.0125,0))

            ctk.CTkLabel(self.item_frame, text='Selling Price: ', font=("DM Sans Medium", 14), anchor="e").grid(row = 11, column = 0, sticky="w",pady = (height*0.008,0), padx = (width*0.0125,0))
            self.selling_price_entry = ctk.CTkEntry(self.item_frame, width=width*0.3, textvariable= ctk.StringVar(), state='readonly')
            #self.selling_price_entry._textvariable.trace_add('write', selling_callback)
            self.selling_price_entry.grid(row = 11, column = 1, sticky = 'w', pady = (height*0.025,0), padx = (width*0.0125,0))

            '''Supplier Frame'''
            self.supplier_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.supplier_frame.grid(row = 2, column = 0,rowspan=2, sticky = 'new', padx =(width*0.01), pady = (height*0.015))
            self.supplier_frame.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(self.supplier_frame, text='SUPPLIER', anchor='w',  font=("DM Sans Medium", 18)).grid(row = 0, column = 0, sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            ctk.CTkLabel(self.supplier_frame, text='Supplier', anchor='w', font=("DM Sans Medium",14)).grid(row = 1, column = 0, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))
            self.supplier_entry = ctk.CTkEntry(self.supplier_frame, corner_radius= 3, placeholder_text='Required', font=("DM Sans Medium",14))
            self.supplier_entry.grid(row = 2, column = 0, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))

            ctk.CTkLabel(self.supplier_frame, text='Contact', anchor='w', font=("DM Sans Medium",14)).grid(row = 3, column = 0, sticky = 'nsew', pady = (0,height*0.005), padx = (width*0.01))
            self.contact_entry = ctk.CTkEntry(self.supplier_frame, corner_radius= 3, placeholder_text='', font=("DM Sans Medium",14))
            self.contact_entry.grid(row = 4, column = 0, sticky = 'nsew', pady = (0,height*0.025), padx = (width*0.01))

            '''Inventory Frame'''
            self.inventory_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.inventory_frame.grid(row = 1, column = 1,rowspan=2, sticky = 'nsew', padx =(0,width*0.01), pady = (height*0.015,0))
            self.inventory_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(self.inventory_frame, text='INVENTORY', anchor='w', font=('DM Sans Medium', 18)).grid(row = 0, column = 0,columnspan=2, sticky = 'nsew', pady = (height*0.01), padx= (width*0.01))

            ctk.CTkLabel(self.inventory_frame, text='Stock: ',anchor="e", font=("DM Sans Medium", 14)).grid(row = 1, column = 0, sticky = 'w',padx = (width*0.01,0))
            self.stock_entry = cctk.cctkSpinnerCombo(self.inventory_frame, entry_font=("DM Mono Medium",14), val_range=(0, cctk.cctkSpinnerCombo.MAX_VAL))
            self.stock_entry.grid(row = 1, column = 1,columnspan=2, sticky = 'e',padx=(0,width*0.01))

            ctk.CTkLabel(self.inventory_frame, text='Expiration Date', anchor='w', font=("DM Sans Medium", 14)).grid(row = 3, column = 0,columnspan=2, sticky = 'nsew', pady = (height*0.01,height*0.005), padx = (12,0))
            ctk.CTkLabel(self.inventory_frame, text="Has Expiry? ", font=("DM Sans Medium", 14)).grid(row=4,column=0, sticky="e", padx=(width*0.015,0.005))

            self.expiry_switch_val= ctk.StringVar(value="disabled")
            self.expiry_switch = ctk.CTkSwitch(self.inventory_frame, text="Yes", variable=self.expiry_switch_val, onvalue="normal", offvalue="disabled",
                                               command=expiry_switch_event, font=("DM Sans Medium", 14))
            self.expiry_switch.grid(row=4,column=1, sticky="w", )

            self.expiration_date_entry = ctk.CTkLabel(self.inventory_frame, corner_radius= 5, text='Set Expiry Date',fg_color="white",height=height*0.05, font=("DM Sans Medium", 14), text_color="grey")
            self.expiration_date_entry.grid(row = 5, column = 0, sticky = 'nsew',columnspan=2, pady = (0,height*0.015), padx = (width*0.01,width*0.005 ))

            self.show_calendar = ctk.CTkButton(self.inventory_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.expiration_date_entry, "%s", date_format="raw", min_date=datetime.datetime.now()), corner_radius=3, state="disabled",  )
            self.show_calendar.grid(row=5, column=2, padx = (0,width*0.01), pady = (0,height*0.015), sticky="e")

            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 3, column = 1, sticky = 'nsew', padx=(0,width*0.01), pady = (height*0.015))
            self.action_frame.grid_columnconfigure((0,1), weight=1)

            self.warning_lbl = ctk.CTkLabel(self.action_frame, text='', text_color="red", font=("DM Sans Medium",14))
            self.warning_lbl.pack(pady=(height*0.025, 0))

            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.125, height=height*0.05,corner_radius=3, font=("DM Sans Medium", 14), text='Add New Item', command= add)
            self.add_btn.pack(pady=(height*0.025, 0))

            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.05, height=height*0.05,corner_radius=3, font=("DM Sans Medium", 14), text='Cancel', command= reset)
            self.cancel_btn.pack(pady = (height*0.025, height*0.01))

            category_expiry_callback(self.item_category[2])
    return add_item(master, info)

def restock( master, info:tuple, data_view: Optional[cctk.cctkTreeView] = None):
    class restock(ctk.CTkFrame):
        def __init__(self, master, info:tuple, data_view: Optional[cctk.cctkTreeView] = None):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            super().__init__(master,  width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            '''events'''
            def reset():
                self.place_forget()

            def validate_acc(_):
                self.item_uid = database.fetch_data("SELECT uid FROM item_general_info WHERE NAME = ?", (self.item_name_entry.get(),))
                self.item_uid = self.item_uid[0][0] if self.item_uid else None
                if self.item_uid is None:
                    return
                if database.fetch_data('SELECT Expiry_date FROM item_inventory_info WHERE UID = ?', (self.item_uid, ))is not None:
                    self.show_calendar.configure(state = ctk.NORMAL)
                else:
                    self.show_calendar.configure(state = ctk.DISABLED)
                self.stock_entry.configure(state = ctk.NORMAL)
                self.action_btn.configure(state = ctk.NORMAL)

            def recieve_stock():
                uid = database.fetch_data(sql_commands.get_uid, (self.item_name_entry.get(), ))[0][0]
                supplier = database.fetch_data(sql_commands.get_supplier, (uid, ))[0][0]
                expiry = None if 'Set'in self.expiry_date_entry._text else datetime.datetime.strptime(self.expiry_date_entry._text, '%m-%d-%Y').strftime('%Y-%m-%d')
                #item information

                data = (generateId('R', 6), self.item_name_entry.get(), self.stock_entry.get(), supplier, expiry, None, 1, None)
                database.exec_nonquery([[sql_commands.record_recieving_item, data]])
                if data_view :
                    data_view.update_table(database.fetch_data(sql_commands.get_recieving_items))
                messagebox.showinfo("Sucess", "Order process success\nCheck the recieving tab")
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.45, height=height*0.8)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.pack_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.pack(fill="both", expand=0)

            """ ctk.CTkLabel(self.top_frame, text='RESTOCK', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)

            self.item_frame =ctk.CTkFrame(self.main_frame, corner_radius=0)
            self.item_frame.pack(fill="x", expand=0, padx=width*0.008, pady=height*0.01)
            self.item_frame.grid_columnconfigure(1, weight=1)

            ctk.CTkLabel(self.item_frame, text='ITEM', anchor='w', font=('DM Sans Medium', 18), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))
            ctk.CTkLabel(self.item_frame, text='Item Name', anchor='w').grid(row = 1, column = 0, padx = 12, sticky = 'nsew')

            item = [c[0] for c in database.fetch_data(sql_commands.show_all_items, None)]

            self.item_name_entry = ctk.CTkOptionMenu(self.item_frame, height * .05, hover = False, command= validate_acc,
                                                           values= list(item),)

            self.item_name_entry.grid(row = 2, column = 0,columnspan=2, sticky = 'nsew', padx = 12, pady = (0, 12))

            ctk.CTkLabel(self.item_frame, text="Initial Price Change:").grid(row=3, column=0, sticky="w",pady = (height*0.01,0), padx= (width*0.01))
            self.item_init_price_change =ctk.CTkEntry(self.item_frame)
            self.item_init_price_change.grid(row=3, column=1, sticky="w")

            ctk.CTkLabel(self.item_frame, text="Narkup Change:").grid(row=4, column=0,sticky="w",pady = (height*0.01), padx= (width*0.01))
            self.item_markup_change =ctk.CTkEntry(self.item_frame)
            self.item_markup_change.grid(row=4, column=1,  sticky="w")

            self.restock_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
            self.restock_frame.pack(fill="both", expand=1, padx=width*0.008, pady=(0,height*0.01))
            self.restock_frame.grid_columnconfigure((1,2), weight=1)

            ctk.CTkLabel(self.restock_frame, text='INVENTORY', anchor='w', font=('DM Sans Medium', 18), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))
            ctk.CTkLabel(self.restock_frame, text='Expiration Date', anchor='w').grid(row = 1, column = 0, columnspan=4, padx = 12, sticky = 'nsew')
            self.expiry_date_entry = ctk.CTkLabel(self.restock_frame, height * .05, fg_color="white", text="Set Expiry Date", text_color="grey", corner_radius=3)
            self.expiry_date_entry.grid(row = 2, column = 0, columnspan=3,sticky = 'nsew', padx = 12, pady = (0, 12))

            self.show_calendar = ctk.CTkButton(self.restock_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.expiry_date_entry, "%s", date_format="numerical", min_date=datetime.datetime.now()))
            self.show_calendar.grid(row=2, column=3, padx = (0,width*0.01), pady = (0,height*0.015), sticky="w")

            ctk.CTkLabel(self.restock_frame, text='Stock', anchor='w').grid(row = 3, column = 0, padx = 12, sticky = 'nsew')
            self.stock_entry = cctk.cctkSpinnerCombo(self.restock_frame, entry_font=("DM Mono Medium",14), val_range=(1, cctk.cctkSpinnerCombo.MAX_VAL), state=ctk.DISABLED)
            self.stock_entry.grid(row = 3, column = 1, columnspan=2, sticky = 'w',padx=(0,width*0.01))

            self.action_frame = ctk.CTkFrame(self.main_frame, height=height*0.15,corner_radius=0)
            self.action_frame.pack(fill="x", expand=0,padx=width*0.008, pady=(0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)

            self.warning_text =  ctk.CTkLabel(self.action_frame, text='TEST', text_color='red')
            self.warning_text.grid(row = 0, column = 0,columnspan=2, sticky = 'nsew', padx = 12, pady = (0, 12))

            self.leave_btn = ctk.CTkButton(self.action_frame, width * .04, height * .05, corner_radius=3, text='Back', command = reset)
            self.leave_btn.grid(row = 1, column = 0, sticky = 'nsew', padx = 12, pady = (0, 12))

            self.action_btn = ctk.CTkButton(self.action_frame, width * .04, height * .05, corner_radius=3, text='Restock', command=recieve_stock, state=ctk.DISABLED)
            self.action_btn.grid(row = 1, column = 1, sticky = 'nsew', padx = 12, pady = (0, 12)) """

            #top bar
            ctk.CTkLabel(self.top_frame, text='RESTOCK', anchor='w', corner_radius=0, font=("Arial", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            #change here go reset
            self.item_frame =ctk.CTkFrame(self.main_frame, corner_radius=0)
            self.item_frame.pack(fill="x", expand=0, padx=width*0.008, pady=height*0.01)
            self.item_frame.grid_columnconfigure(1, weight=1)
            #item title
            ctk.CTkLabel(self.item_frame, text='ITEM', anchor='w', font=('Arial', height*0.03), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))
            #item name title
            ctk.CTkLabel(self.item_frame, text='Item Name', anchor='w', font=('Arial', height*0.024)).grid(row = 1, column = 0, padx= (width*0.02), pady=(0, height*0.005), sticky = 'nsew')

            item = [c[0] for c in database.fetch_data(sql_commands.show_all_items, None)]

            self.item_name_entry = ctk.CTkOptionMenu(self.item_frame, height * .05, hover = False, command= validate_acc,
                                                           values= list(item),)
            self.item_name_entry.configure(font=('Arial', height*0.024), dropdown_font=('Arial', height*0.02))
            self.item_name_entry.grid(row = 2, column = 0,columnspan=2, sticky = 'nsew', padx= (width*0.02), pady = (0, height*0.01))

            #category entry
            ctk.CTkLabel(self.item_frame, text="Category:", font=('Arial', height*0.024)).grid(row=3, column=0, sticky="w",pady = (height*0.01), padx= (width*0.02))
            self.category_entry =ctk.CTkEntry(self.item_frame, state="disabled", font=('Arial', height*0.024), width=width*0.12)
            self.category_entry.grid(row=3, column=1, sticky="w", pady = (height*0.01))

            #supplier combobox
            ctk.CTkLabel(self.item_frame, text="Supplier:", font=('Arial', height*0.024)).grid(row=4, column=0, sticky="w",pady = (height*0.01), padx= (width*0.02))
            self.supplier_combo_box =ctk.CTkComboBox(self.item_frame, values=["ABD", "J&J", "Pfizer"], state='readonly', font=('Arial', height*0.024), width=width*0.12, dropdown_font=('Arial', height*0.02))
            self.supplier_combo_box.grid(row=4, column=1, sticky="w", pady = (height*0.01,0))

            #initial price change
            ctk.CTkLabel(self.item_frame, text="Initial Price Change:", font=('Arial', height*0.024)).grid(row=5, column=0, sticky="w",pady = (height*0.01), padx= (width*0.02))
            self.item_init_price_change =ctk.CTkEntry(self.item_frame, font=('Arial', height*0.024), width=width*0.12, justify='right', state='disabled')
            self.item_init_price_change.grid(row=5, column=1, sticky="w", pady = (height*0.01,0))

            #markup change
            ctk.CTkLabel(self.item_frame, text="Markup Change:", font=('Arial', height*0.024)).grid(row=6, column=0,sticky="w",pady = (height*0.01), padx= (width*0.02))
            self.item_markup_change =ctk.CTkEntry(self.item_frame, font=('Arial', height*0.024), width=width*0.12, justify='right')
            self.item_markup_change.grid(row=6, column=1,  sticky="w", pady = (height*0.01,0))

            #eend of a

            self.restock_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
            self.restock_frame.pack(fill="both", expand=1, padx=width*0.008, pady=(0,height*0.01))
            self.restock_frame.grid_columnconfigure((1,2), weight=1)
            #inventory title
            ctk.CTkLabel(self.restock_frame, text='INVENTORY', anchor='w', font=('Arial', height*0.03), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            #initial stock
            ctk.CTkLabel(self.restock_frame, text="Initial Stock:", font=('Arial', height*0.024)).grid(row=1, column=0,sticky="w",pady = (height*0.01), padx= (width*0.02))
            self.initial_stock_entry =ctk.CTkEntry(self.restock_frame, state='disabled', width=width*0.06, justify='right', font=('Arial', height*0.024))
            self.initial_stock_entry.grid(row=1, column=1,  sticky="w")
            #Restock 
            ctk.CTkLabel(self.restock_frame, text='Restock Amount:', anchor='w', font=('Arial', height*0.024)).grid(row = 2, column = 0, padx= (width*0.02))
            self.stock_entry = cctk.cctkSpinnerCombo(self.restock_frame, val_range=(0, cctk.cctkSpinnerCombo.MAX_VAL), state=ctk.NORMAL, width=width*0.04)
            self.stock_entry.grid(row = 2, column = 1, columnspan=2, sticky = 'w',padx=(0,width*0.01))

            #expiration set
            ctk.CTkLabel(self.restock_frame, text='Expiration Date:', anchor='w', font=('Arial', height*0.024)).grid(row = 3, column = 0, columnspan=4, padx = (width*0.02), sticky = 'nsew',pady = (height*0.01))
            self.expiry_date_entry = ctk.CTkLabel(self.restock_frame, height * .05, fg_color="white", text="Set Expiry Date", text_color="grey", corner_radius=3, font=('Arial', height*0.024))
            self.expiry_date_entry.grid(row = 4, column = 0, columnspan=3,sticky = 'nsew', padx = ((width*0.02),(width*0.008)), pady = (0, 12))

            self.show_calendar = ctk.CTkButton(self.restock_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.expiry_date_entry, "%s", date_format="numerical", min_date=datetime.datetime.now()))
            self.show_calendar.grid(row=4, column=3, padx = (0,width*0.01), pady = (0,height*0.015), sticky="w")
            #end of expiration setter
            #bottom buttons frame
            self.action_frame = ctk.CTkFrame(self.main_frame, height=height*0.15,corner_radius=0, fg_color='transparent')
            self.action_frame.pack(padx=width*0.008, pady=(0,height*0.01))
            #removed
            '''self.warning_text =  ctk.CTkLabel(self.action_frame, text='TEST', text_color='red')
            self.warning_text.grid(row = 0, column = 0,columnspan=2, sticky = 'nsew', padx = 12, pady = (0, 12))'''
            #end removed
            self.leave_btn = ctk.CTkButton(self.action_frame, width * .15, height * .05, corner_radius=3, text='BACK', command = reset, font=('Arial', 14))
            self.leave_btn.pack(side="left", padx=(width*0.025))

            self.action_btn = ctk.CTkButton(self.action_frame, width * .15, height * .05, corner_radius=3, text='RESTOCK', state=ctk.DISABLED, font=('Arial', 14))
            self.action_btn.pack(side="right",  padx=(width*0.025))
            
        def place(self, default_data: str, update_cmds: list = None, **kwargs):
            self.update_cmds = update_cmds
            if default_data:
                self.item_name_entry._current_value = default_data.winfo_children()[1]._text
                self.item_name_entry._text_label.configure(text = default_data.winfo_children()[1]._text)
                self.item_name_entry._command(None)
            else:
                self.item_name_entry._current_value = self.item_name_entry._values[0]
                self.item_name_entry._text_label.configure(text = self.item_name_entry._values[0])
            self.item_name_entry.configure(values = [c[0] for c in database.fetch_data(sql_commands.show_all_items, None)])
            return super().place(**kwargs)

        def stock (self, inventory_info: Optional[Union[tuple, cctk.cctkTreeView]] = None, acc_name: str = None):
            if not messagebox.askyesno("Restock Item", "Are you sure you want to proceed?"):
                return

            if isinstance(inventory_info, cctk.cctkTreeView):
                temp: cctk.cctkTreeView = inventory_info
                if temp.data_grid_btn_mng.active:
                    self._inventory_info = temp._data[temp.data_frames.index(temp.data_grid_btn_mng.active)]
                    del temp
            elif isinstance(inventory_info, tuple):
                self._inventory_info = inventory_info
            else:
                return
            #to generalize the value of inventory_info to a tuple

            uid = database.fetch_data(sql_commands.get_uid, (self._inventory_info[1], ))[0][0]
            #item uid
            receiving_expiry = database.fetch_data(sql_commands.get_receiving_expiry_by_id, (self._inventory_info[0], ))[0][0]

            inventory_data = database.fetch_data("SELECT * FROM item_inventory_info WHERE UID = ? AND (Expiry_Date IS NULL OR Expiry_Date = ?)",
                                                 (uid, receiving_expiry))
            if inventory_data: # if there was an already existing table; update the existing table
                if inventory_data[0][2] is None:#updating non-expiry stock
                    database.exec_nonquery([[sql_commands.update_non_expiry_stock, (self._inventory_info[2], uid)]])
                else: #updating expiry stock
                    database.exec_nonquery([[sql_commands.update_expiry_stock, (self._inventory_info[2], uid, inventory_data[0][2])]])
            else:# if there's no exisiting table; create new instance of an item
                database.exec_nonquery([[sql_commands.add_new_instance, (uid, self._inventory_info[2], receiving_expiry or None)]])

            database.exec_nonquery([[sql_commands.update_recieving_item, (acc_name or 'klyde', self._inventory_info[0])]])

            if isinstance(inventory_info, cctk.cctkTreeView):
                inventory_info.update_table(database.fetch_data(sql_commands.get_recieving_items))

            messagebox.showinfo('Success', 'Restocking Successful')
    return restock(master, info, data_view)

def show_status(master, info:tuple,):
    class show_status(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            def reset():
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.5, height=height*0.85)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2,weight=1)


            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="Inventory Status", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.status_frame = ctk.CTkFrame(self.main_frame, height=height*0.065, width=width*0.25)
            self.status_frame.grid(row=1, column=0,sticky="w", padx=width*0.005, pady=height*0.01)
            self.status_frame.pack_propagate(0)

            self.status_label = ctk.CTkLabel(self.status_frame, text="", font=("DM Sans Medium", 18))
            self.status_label.pack(side="left", padx=width*0.015)

            self.status_count = ctk.CTkLabel(self.status_frame, text="#", font=("DM Sans Medium", 18))
            self.status_count.pack(side="right", padx=width*0.015)

            self.db_inventory_frame = ctk.CTkFrame(self.main_frame)
            self.db_inventory_frame.grid(row=2, column=0, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            self.db_inventory_treeview = cctk.cctkTreeView(self.db_inventory_frame, width=width*0.5, height=height*0.85,
                                               column_format=f'/No:{int(width*.025)}-#c/ItemName:x-tl/Quantity:{int(width*0.075)}-tr/Action:{int(width*0.05)}-tc!30!30',
                                               header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent')
            self.db_inventory_treeview.pack()
        def update_treeview(self, data):
            self.db_inventory_treeview.update_table(data)

    return show_status(master, info,)

def supplier_list(master, info:tuple,):
    class supplier_list(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
            self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
            self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
            self.trash_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
            self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))

            def reset():
                self.place_forget()

            def show_supplier_popup():
                self.create_supplier.place(relx=0.5, rely=0.5, anchor="center")

            def hide_supplier_popup():
                self.create_supplier.place_forget()
                self.supplier_name.delete(0, "end")
                self.supplier_contact.delete(0, "end")

            def update_tables(_ :any = None):
                self.refresh_btn.configure(state = ctk.DISABLED)
                self.refresh_btn.after(1000, self.refresh_btn.configure(state = ctk.NORMAL))

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.75, height=height*0.85)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(3, weight=1)
            self.main_frame.grid_rowconfigure(2,weight=1)

            self.create_supplier = ctk.CTkFrame(self,height=height*0.35, width=width*0.35,fg_color=Color.White_Color[3],)
            self.create_supplier.grid_columnconfigure(1, weight=1)
            self.create_supplier.grid_rowconfigure((1,2), weight=1)
            self.create_supplier.grid_rowconfigure((3), weight=2)
            self.create_supplier.grid_propagate(0)
            self.create_supplier.pack_propagate(0)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="Supplier List", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.search_frame = ctk.CTkFrame(self.main_frame,width=width*0.3, height = height*0.05)
            self.search_frame.grid(row=1, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))

            self.search_frame.pack_propagate(0)
            ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

            self.add_item_btn = ctk.CTkButton(self.main_frame,width=width*0.1, height = height*0.05, text="Add Supplier",image=self.add_icon, font=("DM Sans Medium", 14),
                                           command=show_supplier_popup)
            self.add_item_btn.grid(row=1, column=1, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

            self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75",
                                              command=update_tables)
            self.refresh_btn.grid(row=1, column=2, sticky="w")

            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            #self.data1 = database.fetch_data(sql_commands.get_inventory_by_group, None)
            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * .735, height= height * .725, corner_radius=0,
                                            column_format=f'/No:{int(width*.025)}-#r/SupplierName:x-tl/Contact:{int(width*.25)}-tc/Action:{int(width*.075)}-tc!30!30',
                                            header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                            row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
            self.data_view1.pack()

            self.pop_top_frame = ctk.CTkFrame(self.create_supplier, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.pop_top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.pop_top_frame.pack_propagate(0)

            ctk.CTkLabel(self.pop_top_frame, text="Create Supplier", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.pop_close_btn= ctk.CTkButton(self.pop_top_frame, text="X", height=height*0.04, width=width*0.025, command=hide_supplier_popup)
            self.pop_close_btn.pack(side="right", padx=width*0.005)

            ctk.CTkLabel(self.create_supplier, text="Supplier Name: ", font=("Arial",16)).grid(row=1, column=0, padx=width*0.005, pady=height*0.005)
            self.supplier_name = ctk.CTkEntry(self.create_supplier, placeholder_text="Supplier Name", font=("Arial",14),height=height*0.05)
            self.supplier_name.grid(row=1,column=1, sticky="ew",padx=width*0.005, pady=height*0.005)

            ctk.CTkLabel(self.create_supplier, text="Supplier Contact: ", font=("Arial",16)).grid(row=2, column=0,padx=width*0.005, pady=height*0.005)
            self.supplier_contact = ctk.CTkEntry(self.create_supplier, placeholder_text="Supplier Contact", font=("Arial",14), height=height*0.05)
            self.supplier_contact.grid(row=2,column=1, sticky="ew",padx=width*0.005, pady=height*0.005)

            self.bottom_frame= ctk.CTkFrame(self.create_supplier, fg_color="transparent")
            self.bottom_frame.grid(row=3, column=0, columnspan=2)

            self.cancel_btn = ctk.CTkButton(self.bottom_frame, text="Cancel", command=hide_supplier_popup)
            self.cancel_btn.pack(side="left",padx=(0,width*0.005))

            self.proceed_btn = ctk.CTkButton(self.bottom_frame, text="Proceed")
            self.proceed_btn.pack(side="left",padx=(0,width*0.005))
    return supplier_list(master, info)

def receive_history(master, info:tuple,):
    class receive_history(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
            self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
            self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
            self.trash_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
            self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))

            def reset():
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.85, height=height*0.85)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((1,2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="Received History", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * .8, height= height * .775, corner_radius=0,
                                            column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Stock:{int(width*0.05)}-tr/SupplierName:x-tl/DateReceived:{int(width*.12)}-tc/ReceivedBy:{int(width*.15)}-tc!30!30',
                                            header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                            row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
            self.data_view1.pack()

        def place(self, **kwargs):
            self.data_view1.update_table(database.fetch_data(sql_commands.show_reveiving_hist))
            return super().place(**kwargs)

    return receive_history(master, info)

def disposal_history(master, info:tuple,):
    class disposal_history(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            from datetime import date

            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
            self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
            self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
            self.trash_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
            self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))

            def reset():
                self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.85, height=height*0.85)
            self.main_frame.grid(row=0, column=0, sticky="n", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((1,2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="Disposal", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            ctk.CTkLabel(self.main_frame, text=f"{date.today().strftime('%B %d, %Y')}", font=("Arial", 14), corner_radius=5,
                         fg_color=Color.White_Color[7], width=width*0.085, height=height*0.085).grid(row=1, column=0, sticky="e", padx=width*0.005, pady=(height*0.01))
            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            data = database.fetch_data(sql_commands.get_disposal_hist)
            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, data=data,width= width * .8, height= height * .775, corner_radius=0,
                                             column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/Quantity:{int(width*0.07)}-tr/DateDisposed:{int(width*.2)}-tc/DisposedBy:{int(width*.15)}-tc!30!30',
                                            header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                            row_font=("Arial", 16),navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
            self.data_view1.pack()

        def place(self, **kwargs):
            self.data_view1.update_table(database.fetch_data(sql_commands.get_disposal_hist))
            return super().place(**kwargs)

    return disposal_history(master, info)
