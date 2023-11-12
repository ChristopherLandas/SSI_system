import tkinter as tk
import re
import customtkinter as ctk
import sql_commands
import tkcalendar
import util
from typing import Optional, Tuple, Union
from customcustomtkinter import customcustomtkinter as cctk
from Theme import Color
from util import database, generateId
from util import *
from tkinter import messagebox
from datetime import date, datetime
from constants import action
from PIL import Image
from functools import partial
from typing import *

def add_item(master, info:tuple, command_callback :Optional[callable] = None):
    class add_item(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback :Optional[callable]):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_info = info[3][0]
            super().__init__(master, corner_radius= 0, fg_color="transparent")
            
            '''default'''
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            self.add_item = ctk.CTkImage(light_image=Image.open("image/add_item.png"), size=(25,25))
            #set to transparent to prevent clicking other buttons inside the inventory
            '''events'''
            def reset():
                self.item_name_entry.delete(0, ctk.END)
                self.unit_price_entry.delete(0, ctk.END)
                self.markup_price_entry.delete(0, ctk.END)
                self.expiration_date_entry.configure(text="Set Expiry Date")
                self.change_entries_state('normal')
                for entries in self.supplier_entries: entries.delete(0,ctk.END)
                self.change_entries_state('disabled')
                self.supplier_entry.set("")
                self.expiry_switch.deselect()
                self.stock_entry.set(0)
                self.item_num_unit_entry.delete(0, ctk.END)
                self.item_unit_dbox.set('')
                self.item_brand_entry.set('')
                self.place_forget()

            def add_item_callback():
                unit = unit_process()
                if (self.item_brand_entry.get() and self.item_name_entry.get() and self.unit_price_entry.get() and self.markup_price_entry.get()
                   and self.category_entry.get() and self.stock_entry.get() and ((self.expiration_date_entry._text != 'Set Expiry Date' and self.expiry_switch_val.get()) or self.expiry_switch_val.get() == 'disabled') and ((self.uom_var.get() == 'on' and self.item_num_unit_entry.get() and self.item_unit_dbox.get()) or (self.uom_var.get() == 'off'))):
                    
                    _date = None if str(self.expiration_date_entry._text).startswith("Set") else self.expiration_date_entry._text
                    
                    #check if the item is already in the database
                    if (self.item_brand_entry.get(), self.item_name_entry.get(), unit) in database.fetch_data('SELECT brand,name, unit from item_general_info'):
                        messagebox.showerror("Duplicate Entry", "The item is already in the inventory", parent = self)
                    else:
                        output = database.exec_nonquery([[sql_commands.add_item_general, (self.item_name_id._text, self.item_name_entry.get(), self.category_entry.get(), self.item_brand_entry.get(), unit, acc_info[0])],
                                                [sql_commands.add_item_settings, (self.item_name_id._text, float(self.unit_price_entry.get()), float(self.markup_price_entry.get())/100, .85, .5, self.stock_entry.get(), 0)],
                                                [sql_commands.add_item_supplier, (self.item_name_id._text, self.supplier_id)],
                                                [sql_commands.set_supplier_items, (self.supplier_id, self.item_name_id._text)],
                                                [sql_commands.add_item_inventory, (self.item_name_id._text, self.stock_entry.get(), _date)],
                                                [sql_commands.add_item_statistic, (self.item_name_id._text, )]])
                        
                        if output:
                            messagebox.showinfo('Item Added Succesfully', f"{self.item_name_entry.get()} is added in the inventory", parent = self)
                            reset()
                            if self.command_callback: self.command_callback()
                        else:
                            messagebox.showwarning("Error", "There is an error in inserting an inventory.", parent = self)
                else:
                    messagebox.showwarning("Missing Field Entry", "Enter required fields\nAll fields with '*' is required.", parent = self)

            def unit_process():
                if self.uom_var.get() == 'on' and self.item_name_entry.get() and self.item_unit_dbox.get():
                    unit = re.search(r'\(([^)]+)\)', self.item_unit_dbox.get()).group(1)
                    return f"{self.item_num_unit_entry.get()}{unit}"
                else:
                    return None
            def markup_callback(_ = None, *__):
                self.selling_price_entry.configure(state = ctk.NORMAL)
                self.selling_price_entry.delete(0, ctk.END)
                if self.markup_price_entry.get():
                    if self.unit_price_entry.get() and self.markup_price_entry.get():
                        markup = round(float(self.unit_price_entry.get()) * (float(self.markup_price_entry.get()) / 100), 2)
                        self.selling_price_entry.insert(0, float(self.unit_price_entry.get()) + markup)
                self.selling_price_entry.configure(state = 'readonly')

            
            def selling_callback(_ = None, *__):
                
                if re.search(r'[0-9\.]$', self.markup_price_entry.get() or "") is None and self.markup_price_entry._is_focused and self.markup_price_entry.get():
                        #print(self.markup_price_entry.get())
                        l = len(self.markup_price_entry.get())
                        self.markup_price_entry.delete(l-1, l)

                if re.search(r'[0-9\.]$', self.unit_price_entry.get() or "") is None and self.unit_price_entry._is_focused and self.unit_price_entry.get():
                        l = len(self.unit_price_entry.get())
                        self.unit_price_entry.delete(l-1, l)
                
                if not self.markup_price_entry.get() or not self.unit_price_entry.get():
                    self.selling_price_entry.configure(state = ctk.NORMAL)
                    self.selling_price_entry.delete(0, ctk.END)
                    self.selling_price_entry.configure(state = 'readonly')
                    return

                if  self.markup_price_entry.get() and self.unit_price_entry.get():
                    markup = 1 + (float(self.markup_price_entry.get() or 0)/100)
                    price = float(self.unit_price_entry.get())
                    self.selling_price_entry.configure(state = ctk.NORMAL)
                    self.selling_price_entry.delete(0, ctk.END)
                    self.selling_price_entry.insert(0, format((markup * price), ".2f"))
                    self.selling_price_entry.configure(state = 'readonly')
                    
            def expiry_switch_event():
                self.show_calendar.configure(state=self.expiry_switch_val.get())
                if(self.expiry_switch_val.get()=="normal"):
                    self.show_calendar.configure(fg_color=Color.Blue_Yale)
                    self.expiration_date_entry.configure(fg_color=Color.White_Platinum, text_color="black")
                else:
                    self.show_calendar.configure(fg_color=Color.Grey_Bright_2)
                    self.expiration_date_entry.configure(fg_color=Color.Grey_Bright_2, text_color="grey")

            def category_expiry_callback(category):
                for i in range(len(self.data)):
                    if category in self.data[i][0]:
                        self.expiry_switch.select(); self.expiry_switch.configure(state='disabled', text='Required') if self.data[i][1] == 1 else self.expiry_switch.configure(state='normal', text=''); self.expiry_switch.deselect()
                expiry_switch_event()
                
            def supplier_callback(supplier):
                for res in self.supplier_data:
                    if supplier in res:
                        self.change_entries_state('normal')
                        for entries in self.supplier_entries: entries.delete(0,ctk.END)
                        self.supplier_id = res[0]
                        self.contact_person_entry.insert(0, f"{res[1]}")
                        self.contact_num_entry.insert(0, f"{res[2]}")
                        self.contact_email_entry.insert(0, f"{res[3] or ''}")
                        self.address_entry.insert(0,  f"{res[4]}")
                        self.change_entries_state('disabled')
            
            def uom_callback():
                if self.uom_var.get() == 'off':
                    self.item_num_unit_entry.delete(0, ctk.END)
                    self.item_num_unit_entry.configure(state='disabled', fg_color=Color.White_Platinum,)
                    self.item_unit_dbox.set('')
                    self.item_unit_dbox.configure(state='disabled')
                elif self.uom_var.get() == 'on':
                    self.item_num_unit_entry.delete(0, ctk.END)
                    self.item_num_unit_entry.configure(state='normal', fg_color=Color.White_Lotion,)
                    self.item_unit_dbox.set('')
                    self.item_unit_dbox.configure(state='normal')
            
            def is_digit_valid(var, mode, index):
                if (re.search(r'[0-9\.]$', self.unit_var.get() or "") is None):
                    l = len(self.item_num_unit_entry.get())
                    self.item_num_unit_entry.delete(l-1, l)
                # if not self.unit_var.get().isdigit():
                #    self.item_num_unit_entry.delete(0, "end")
            
            self.command_callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.item_category = []
            self.supplier_id = None
            uom = ['milligram (mg)','gram (g)','kilogram (kg)','milliliter (mL)','liter (L)','millimeter (mm)','centimeter (cm)','meter (m)']
            self.uom_var = ctk.StringVar(value='on')
            self.brand_list = []
            self.unit_var = ctk.StringVar()
        
            self.main_frame = ctk.CTkFrame(self, width= width*0.75, fg_color=Color.White_Color[3], corner_radius=0, border_color=Color.White_Platinum, border_width=1)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((1,2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.add_item, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='ADD ITEM', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            ctk.CTkButton(self.top_frame, text="X",width=width*0.025, command=reset).pack(side="right", padx=(0,width*0.01))

            '''Item Frame'''
            self.item_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[2])
            self.item_frame.grid(row = 1, column = 0, sticky = 'nsew', padx =(width*0.005), pady = (height*0.01,0))
            self.item_frame.columnconfigure((0), weight=1)
        
            self.item_name_frame = ctk.CTkFrame(self.item_frame, fg_color=Color.White_Lotion, width=width*0.35)
            self.item_name_frame.grid(row=0,column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.007),)
            self.item_name_frame.grid_propagate(1)
            self.item_name_frame.grid_columnconfigure(4, weight=1)
            
            '''ITEM ID'''
            ctk.CTkLabel(self.item_name_frame, text='Item Code: ', anchor='e', font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent",).grid(row = 0, column = 0, sticky = 'nsew', pady = (height*0.025,height*0.01), padx = (width*0.005,0))
            self.item_name_id = ctk.CTkLabel(self.item_name_frame, fg_color=Color.White_Platinum, corner_radius=5, font=("DM Sans Medium",14), height=height*0.0475,width=width*0.125)
            self.item_name_id.grid(row = 0, column = 1,sticky = 'nsw', pady = (height*0.025,0), padx = (0, width*0.01), columnspan=5)
            
            '''ITEM CATEGORY'''
            ctk.CTkLabel(self.item_name_frame, text='Item Category: ', anchor='e', font=("DM Sans Medium", 14),  width=width*0.075,).grid(row = 2, column = 0, sticky = 'nsew',  pady = (0,height*0.01), padx = (width*0.005,0))
            self.category_entry = ctk.CTkOptionMenu(self.item_name_frame, corner_radius=5, values=self.item_category, font=("DM Sans Medium",14), height=height*0.0475, width=width*0.275 ,command=category_expiry_callback)
            self.category_entry.grid(row = 2, column = 1, sticky = 'nsew', pady = (height*0.01), padx = (0, width*0.01), columnspan=5)
            
            '''ITEM BRAND'''
            ctk.CTkLabel(self.item_name_frame, text='Item Brand*: ', anchor='e', font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent",).grid(row = 3, column = 0, sticky = 'nsew',  pady = (0,height*0.01), padx = (width*0.005,0))
            self.item_brand_entry = ctk.CTkComboBox(self.item_name_frame, values=self.brand_list, corner_radius=5, font=("DM Sans Medium",14), height=height*0.0475)
            self.item_brand_entry.set('')
            self.item_brand_entry.grid(row = 3, column = 1,sticky = 'ew', pady = (0, height*0.01), padx = (0, width*0.01), columnspan=5)
            
            '''ITEM NAME'''
            ctk.CTkLabel(self.item_name_frame, text='Item Description*: ', anchor='e', font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent").grid(row = 4, column = 0, sticky = 'nsew', pady = (0,height*0.01), padx = (width*0.005,0))
            self.item_name_entry = ctk.CTkEntry(self.item_name_frame, corner_radius=5, placeholder_text='Required', font=("DM Sans Medium",14), height=height*0.0475)
            self.item_name_entry.grid(row = 4, column = 1,sticky = 'ew', pady = (0,height*0.01), padx = (0, width*0.01), columnspan=5)

            '''ITEM UNIT'''
            self.unit_check = ctk.CTkCheckBox(self.item_name_frame, text="Unit of Measure: ", variable=self.uom_var, font=("DM Sans Medium", 14), bg_color='transparent', width=width*0.005,
                                              command=uom_callback, onvalue="on", offvalue="off")
            self.unit_check.select()
            self.unit_check.grid(row = 5, column = 0, sticky='e', pady = (0,height*0.01), padx = (width*0.005,0))
           
            self.item_num_unit_entry = ctk.CTkEntry(self.item_name_frame, textvariable=self.unit_var, width=width*0.15, height=height*0.0475,  font=("DM Sans Medium",14),justify="right",corner_radius=5,)
            self.item_num_unit_entry.grid(row = 5, column = 1, columnspan=1, sticky = 'ew', pady = (0,height*0.01), padx = (0, width*0.004))
            self.unit_var.trace_add('write', is_digit_valid)
            
            self.item_unit_dbox = ctk.CTkOptionMenu(self.item_name_frame, corner_radius=5, values=uom, font=("DM Sans Medium",14), height=height*0.0475)
            self.item_unit_dbox.set('')
            self.item_unit_dbox.grid(row = 5, column = 2, sticky = 'ew', pady = (0, height*0.01), padx = (0, width*0.01), columnspan=5)
            
            '''ITEM UNIT PRICE'''
            ctk.CTkLabel(self.item_name_frame, text='Unit Price*: ', font=("DM Sans Medium", 14),  width=width*0.075, anchor="e").grid(row = 6, column = 0, sticky="nsew",pady = (0,height*0.01), padx = (width*0.004,0))
            self.unit_price_entry = ctk.CTkEntry(self.item_name_frame, width=width*0.15, textvariable= ctk.StringVar(), height=height*0.0475,  font=("DM Sans Medium",14),justify="right",corner_radius=5,)
            self.unit_price_entry._textvariable.trace_add('write', selling_callback)
            self.unit_price_entry.grid(row = 6, column = 1, columnspan=1, sticky = 'nsew', pady = (0,height*0.01), padx = (0, width*0.004))
            
            '''ITEM MARKUP'''
            ctk.CTkLabel(self.item_name_frame, text='Mark Up*: ', font=("DM Sans Medium", 14), anchor="e").grid(row = 6, column = 2, sticky="nsew",pady = (0,height*0.01), padx = (width*0.005,0))
            self.markup_price_entry = ctk.CTkEntry(self.item_name_frame, width=width*0.05, textvariable= ctk.StringVar(), height=height*0.0475, justify="right",  font=("DM Sans Medium",14),corner_radius=5,)
            self.markup_price_entry._textvariable.trace_add('write', selling_callback)
            self.markup_price_entry.grid(row = 6, column = 3, sticky = 'nsew', pady = (0,height*0.01), padx = (0))
            ctk.CTkLabel(self.item_name_frame, text=' %', font=("DM Sans Medium", 14), anchor="w").grid(row = 6, column = 4, sticky="nsew",pady = (0,height*0.01), padx = (0))
            
            '''ITEM SELLING'''
            ctk.CTkLabel(self.item_name_frame, text='Selling Price: ', font=("DM Sans Medium", 14), width=width*0.075, anchor="e").grid(row = 7, column = 0, sticky="nsew",pady = (0,height*0.01), padx = (width*0.005,0))
            self.selling_price_frame = ctk.CTkFrame(self.item_name_frame, fg_color=Color.White_Color[2], height=height*0.05, width=width*0.075)
            self.selling_price_frame.grid(row = 7, column = 1, sticky = 'nsw', pady = (0,height*0.01), padx = (0, width*0.005), columnspan=2)
            ctk.CTkLabel(self.selling_price_frame, text='₱ ', font=("DM Sans Medium", 14), anchor="e" ).pack(padx=(width*0.005,0), side="left", pady=(height*0.01))
            self.selling_price_entry = ctk.CTkEntry(self.selling_price_frame, width=width*0.1, textvariable= ctk.StringVar(), state='readonly', height=height*0.0475, justify="right",  font=("DM Sans Medium",14),
                                                    border_width=0, fg_color="white")
            self.selling_price_entry.pack(side="left",padx=(0,width*0.005))

            '''Supplier Frame'''
            self.supplier_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2], width=width*0.115)
            self.supplier_frame.grid(row = 1, column = 1, rowspan=2, sticky = 'nsew', padx=(0,width*0.005), pady = (height*0.01))
            self.supplier_frame.grid_columnconfigure(0, weight=1)
            self.supplier_frame.grid_rowconfigure(0, weight=1)

            self.supplier_name_frame = ctk.CTkFrame(self.supplier_frame, fg_color=Color.White_Lotion, width=width*0.35)
            self.supplier_name_frame.grid(row=0,column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.007),)
            self.supplier_name_frame.grid_propagate(0)
            self.supplier_name_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(self.supplier_name_frame, text='SUPPLIER', anchor='w',  font=("DM Sans Medium", 14)).grid(row = 0, column = 0, sticky = 'nsew', pady = (height*0.005,0), padx= (width*0.01))
            '''SUPPLIER NAME'''
            ctk.CTkLabel(self.supplier_name_frame, text='Supplier Name*: ', anchor='e', font=("DM Sans Medium", 14), width=width*0.085, ).grid(row = 1, column = 0, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.005,0))
            self.supplier_entry = ctk.CTkOptionMenu(self.supplier_name_frame, corner_radius= 5, font=("DM Sans Medium",14), height=height*0.045, command=supplier_callback)
            self.supplier_entry.grid(row = 1, column = 1, columnspan=2, sticky="ew", pady = (height*0.005, height*0.01), padx = (0, width*0.01))
            self.supplier_entry.set("")

            '''CONTACT PERSON'''
            ctk.CTkLabel(self.supplier_name_frame, text='Contact Person: ', anchor='e', font=("DM Sans Medium",14), width=width*0.085,).grid(row = 2, column = 0, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.005,0))
            self.contact_person_entry = ctk.CTkEntry(self.supplier_name_frame, corner_radius=5, placeholder_text='', font=("DM Sans Medium",14), state="disable", height=height*0.045)
            self.contact_person_entry.grid(row = 2, column = 1, columnspan=2, sticky="ew", pady = (height*0.005, height*0.01), padx = (0, width*0.01))
            
            '''CONTACT NUMBER'''
            ctk.CTkLabel(self.supplier_name_frame, text='Contact#: ', anchor='e', font=("DM Sans Medium",14), width=width*0.085,).grid(row = 3, column = 0, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.005,0))
            self.contact_num_entry = ctk.CTkEntry(self.supplier_name_frame, corner_radius=5, placeholder_text='', font=("DM Sans Medium",14), state="disable", height=height*0.045)
            self.contact_num_entry.grid(row = 3, column = 1, columnspan=2, sticky="ew", pady = (height*0.005, height*0.01), padx = (0, width*0.01))
            
            '''CONTACT EMAIL'''
            ctk.CTkLabel(self.supplier_name_frame, text='Email: ', anchor='e', font=("DM Sans Medium",14), width=width*0.085,).grid(row = 4, column = 0, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.005,0))
            self.contact_email_entry = ctk.CTkEntry(self.supplier_name_frame, corner_radius=5, placeholder_text='', font=("DM Sans Medium",14), state="disable", height=height*0.045)
            self.contact_email_entry.grid(row = 4, column = 1, columnspan=2, sticky="ew", pady = (height*0.005, height*0.01), padx = (0, width*0.01))
            
            '''ADDRESS'''
            ctk.CTkLabel(self.supplier_name_frame, text='Address: ', anchor='e', font=("DM Sans Medium",14), width=width*0.085,).grid(row = 5, column = 0, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.005,0))
            self.address_entry = ctk.CTkEntry(self.supplier_name_frame, corner_radius=5, placeholder_text='', font=("DM Sans Medium",14), state="disable", height=height*0.045)
            self.address_entry.grid(row = 5, column = 1, columnspan=2, sticky="ew", pady = (height*0.005, height*0.01), padx = (0, width*0.01))

            self.supplier_entries = [self.contact_person_entry, self.contact_num_entry, self.contact_email_entry, self.address_entry]
            
            '''Inventory Frame'''
            self.inventory_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2])
            self.inventory_frame.grid(row = 2, column = 0, rowspan=2,sticky = 'nsew', padx=(width*0.005), pady = (height*0.01))
            self.inventory_frame.grid_columnconfigure(0, weight=1)
            self.inventory_frame.grid_rowconfigure(0, weight=1)
            
            self.inventory_name_frame = ctk.CTkFrame(self.inventory_frame, corner_radius=5, fg_color=Color.White_Lotion,  width=width*0.225, )
            self.inventory_name_frame.grid(row=0, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.007),)
            self.inventory_name_frame.grid_propagate(0)
            self.inventory_name_frame.grid_columnconfigure((1), weight=1)
             
            ctk.CTkLabel(self.inventory_name_frame, text='INVENTORY', anchor='w', font=('DM Sans Medium', 14)).grid(row = 0, column = 0, sticky = 'nsew', pady = (height*0.005,0), padx= (width*0.01))
            
            ctk.CTkLabel(self.inventory_name_frame, text='Initial Stock: ',anchor="e", font=("DM Sans Medium", 14), width=width*0.085, ).grid(row = 1, column = 0, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.0075,0))
            self.stock_entry = cctk.cctkSpinnerCombo(self.inventory_name_frame, entry_font=("DM Mono Medium",14), val_range=(0, cctk.cctkSpinnerCombo.MAX_VAL))
            self.stock_entry.grid(row = 1, column = 1, columnspan=2 ,pady = (height*0.005, height*0.01), padx = (0, width*0.01), sticky="w")
            
            ctk.CTkLabel(self.inventory_name_frame, text='Expiration Date: ', anchor='w', font=("DM Sans Medium", 14), width=width*0.085, ).grid(row = 2, column = 0, sticky = 'nsew', pady = (height*0.005,0), padx = (width*0.0075,0))

            self.expiry_switch_val= ctk.StringVar(value="disabled")
            self.expiry_switch = ctk.CTkSwitch(self.inventory_name_frame, text="", variable=self.expiry_switch_val, onvalue="normal", offvalue="disabled",
                                               command=expiry_switch_event, font=("DM Sans Medium", 14))
            self.expiry_switch.grid(row=2,column=1, sticky="w")
            
            self.expiration_date_entry = ctk.CTkLabel(self.inventory_name_frame, corner_radius= 5, text='Set Expiry Date',fg_color=Color.Grey_Bright_2,height=height*0.05, font=("DM Sans Medium", 14), text_color="grey")
            self.expiration_date_entry.grid(row = 3, column = 0, columnspan=2, sticky = 'nsew', pady = (height*0.005,height*0.01), padx = (width*0.0075,0))

            self.show_calendar = ctk.CTkButton(self.inventory_name_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Blue_Yale,
                                               command=lambda: cctk.tk_calendar(self.expiration_date_entry, "%s", date_format="raw", min_date=datetime.now()), corner_radius=5, state="disabled",  )
            self.show_calendar.grid(row=3, column=2, pady = (height*0.005,height*0.01), padx = (0, width*0.01), sticky="e")

            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2], height=height*0.085)
            self.action_frame.grid(row = 3, column = 1, sticky = 'nsew', padx=(0,width*0.005), pady = (0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command= reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Add New Item', command= add_item_callback)
            self.add_btn.pack(side="right",  padx = (width*0.0075), pady= height*0.01)

            expiry_switch_event()
            
        def change_entries_state(self, state):
            if 'disabled' in state:
                color, width = Color.White_Platinum, 0
            elif 'normal' in state:
                color, width = Color.White_Lotion, 2
            for entries in self.supplier_entries: entries.configure(fg_color = color, border_width = width ,state = state)
            
        def set_categories(self):
            self.data = database.fetch_data("SELECT * FROM categories where state = 1")
            self.supplier_data = database.fetch_data("SELECT supp_id, supp_name, contact_person, contact_number, contact_email, address FROM supplier_info")
            
            self.supplier_option = [data[1] for data in self.supplier_data]
            
            self.category_data = []
            for i in range(len(self.data)):
                self.category_data.append(self.data[i][0])
            
            self.supplier_entry.configure(values = self.supplier_option)
            self.category_entry.configure(values=self.category_data)
            self.category_entry.set(self.category_data[0])
  
        def place(self, **kwargs):
            self.brand_list = [brand[0] for brand in database.fetch_data('SELECT DISTINCT brand FROM item_general_info')]
            self.item_brand_entry.configure(values = self.brand_list)
            uid = generateId('I', 6).upper()
            self.item_name_id.configure(text=uid)
            
            self.set_categories()
            return super().place(**kwargs)
    return add_item(master, info, command_callback)

def restock( master, info:tuple, data_view: Optional[cctk.cctkTreeView] = None, command_callback:callable = None):
    class restock(ctk.CTkFrame):
        def __init__(self, master, info:tuple, data_view: Optional[cctk.cctkTreeView] = None, command_callback:callable = None):
            width = info[0]
            height = info[1]
            acc_cred = info[2]
            acc_name = info[3][0]
            super().__init__(master, corner_radius= 0, fg_color='transparent')
            
            self.does_expire = False
            self.command_calback = command_callback
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            '''events'''
            def reset():
                self.place_forget()

            def validate_acc(_):
                item_info  = split_unit(self.item_name_entry.get())
                query = f"SELECT uid FROM item_general_info WHERE name = '{item_info[0]}' AND unit IS NULL" if len(item_info) == 1 else f"SELECT uid FROM item_general_info WHERE name = '{item_info[0]}' AND unit = '{item_info[1]}'"
                
                self.item_uid = database.fetch_data(query)[0][0]
                self.supplier = database.fetch_data(sql_commands.get_supplier_base_item, (self.item_uid, ) )[0]
                
                self.supplier_code.configure(text=self.supplier[0])
                self.supplier_name_entry.set(self.supplier[1])
                
                self.item_code.configure(text=self.item_uid)    
                self.supplier_name_entry.configure(values=[data[0] for data in database.fetch_data(sql_commands.get_item_supplier_name, (self.item_code._text,))])

                self.stock_entry.configure(state = ctk.NORMAL)
                self.stock_entry.set(1)
                self.add_btn.configure(state = ctk.NORMAL)
                
            def supplier_callback(_):
                self.supplier_id = database.fetch_data("SELECT supp_id FROM supplier_info WHERE supp_name = ?", (self.supplier_name_entry.get(),))[0][0]
                self.supplier_code.configure(text=self.supplier_id)
                
            def recieve_stock():
                if self.item_name_entry.get() == "Select an Item" or self.item_code._text=="" or self.supplier_code._text=="":
                    messagebox.showerror("Info Missing", "Fill the required information", parent = self)
                    return

                
                data = (generateId('R', 6).upper(), self.item_name_entry.get(), self.item_uid, acc_name[0], self.stock_entry.get(), self.stock_entry.get(), self.supplier_code._text, None)
                database.exec_nonquery([[sql_commands.record_recieving_item, data]])
                if data_view :
                    #data_view.update_table(database.fetch_data(sql_commands.get_recieving_items_state))
                    messagebox.showinfo("Sucess", "Order process success. Check the orders tab", parent = self)
                    record_action(acc_cred[0][0], action.ADD_ITEM_TYPE, action.ADD_ITEM % (acc_cred[0][0], self.item_uid))
                    self.command_calback()
                    self.place_forget()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], border_color=Color.White_Platinum, border_width=1)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            
            self.top_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.05)
            self.top_frame.grid(row=0, column=0,sticky="nsew", padx=(1), pady=(1,0))

            ctk.CTkLabel(self.top_frame, text='PLACE ORDER', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.015,0))
            ctk.CTkButton(self.top_frame, text="X",width=height*0.045, command=reset).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
            
            '''ITEM INFO'''

            self.item_border = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Platinum)
            self.item_border.grid(row=1, column=0,sticky="nsew", padx=width*0.005, pady=height*0.01)
            
            self.item_frame = ctk.CTkFrame(self.item_border, corner_radius=5, fg_color=Color.White_Lotion)
            self.item_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.item_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(self.item_frame, text='ITEM', anchor='w', font=('DM Sans Medium', 16), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))

            '''ITEM CODE'''
            ctk.CTkLabel(self.item_frame, text='Item Code: ', anchor='e', font=('DM Sans Medium', 14), width=width*0.09).grid(row = 1, column = 0, padx= (0,width*0.01), pady = (0), sticky = 'nsew')
            self.item_code = ctk.CTkLabel(self.item_frame, height = height *0.05, width=width*0.1, text="", fg_color=Color.White_Platinum, font=('DM Sans Medium', 14), corner_radius=5)
            self.item_code.grid(row =1, column = 1, columnspan=2, sticky = 'nsw',padx= (0), pady = (0))
            
            '''ITEM NAME'''
            ctk.CTkLabel(self.item_frame, text='Item Name: ', font=('DM Sans Medium', 14), anchor='e',  width=width*0.09).grid(row = 2, column = 0, pady = (height*0.01), padx= (width*0.01), sticky = 'nsew')
            
            self.item_name_entry = ctk.CTkOptionMenu(self.item_frame,  width=width*0.35, height=height*0.05, font=('DM Sans Medium', 14), command= validate_acc)
            self.item_name_entry.grid(row = 2, column = 1, columnspan=2, sticky = 'nsew', pady = (height*0.01), padx= (0,width*0.01))
            self.item_name_entry.set("")

            '''INVENTORY INFO'''
            self.restock_border = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Platinum)
            self.restock_border.grid(row=3, column=0,sticky="nsew", padx=width*0.005, pady=(0, height*0.01))
            self.restock_border.grid_columnconfigure(0, weight=1)
            
            self.restock_frame = ctk.CTkFrame(self.restock_border, corner_radius=5, fg_color=Color.White_Lotion)
            self.restock_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.restock_frame.grid_columnconfigure((1,2), weight=1)

            ctk.CTkLabel(self.restock_frame, text='INVENTORY', anchor='w', font=('DM Sans Medium', 16), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))
            
            '''STOCK'''
            
            ctk.CTkLabel(self.restock_frame, text='Order Quantity: ', anchor='e', font=('DM Sans Medium', 14), width=width*0.09).grid(row = 1, column = 0, pady = (height*0.01), padx= (width*0.01), sticky = 'nsew')
            self.stock_entry = cctk.cctkSpinnerCombo(self.restock_frame, entry_font=("DM Mono Medium",14), val_range=(1, cctk.cctkSpinnerCombo.MAX_VAL), state=ctk.DISABLED)
            self.stock_entry.grid(row = 1, column = 1, columnspan=2, sticky = 'w',padx=(0,width*0.01), pady = (height*0.01))
            
            '''EXPIRY'''
            #ctk.CTkLabel(self.restock_frame, text='Expiration Date: ', font=('DM Sans Medium', 14), anchor='e',  width=width*0.09).grid(row = 2, column = 0, padx= (width*0.01), sticky = 'nsew')
            #self.expiry_date_entry = ctk.CTkLabel(self.restock_frame, height * .05, fg_color=Color.White_Platinum, text="Set Expiry Date", font=('DM Sans Medium', 14), text_color="grey", corner_radius=3)
            #self.expiry_date_entry.grid(row =2, column = 1, columnspan=2, sticky = 'nsew',padx= (0), pady = (height*0.01))
            
            #self.show_calendar = ctk.CTkButton(self.restock_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03, fg_color=Color.Grey_Davy, state = ctk.DISABLED,
            #                                   command=lambda: cctk.tk_calendar(self.expiry_date_entry, "%s", date_format="numerical", min_date=datetime.now()))
            #self.show_calendar.grid(row=2, column=3, padx = (width*0.005,width*0.01), pady = (height*0.01), sticky="w")
            
            
            '''SUPPLIER INFO'''
            self.supplier_border = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Platinum)
            self.supplier_border.grid(row=2, column=0,sticky="nsew", padx=width*0.005, pady=(0, height*0.01))
            self.supplier_border.grid_columnconfigure(0, weight=1)
            
            self.supplier_frame = ctk.CTkFrame(self.supplier_border, corner_radius=5, fg_color=Color.White_Lotion)
            self.supplier_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.supplier_frame.grid_columnconfigure((1,2), weight=1)

            ctk.CTkLabel(self.supplier_frame, text='SUPPLIER', anchor='w', font=('DM Sans Medium', 16), text_color=Color.Blue_Maastricht).grid(row = 0, column = 0, columnspan=2,sticky = 'nsew', pady = (height*0.01,0), padx= (width*0.01))
            
            '''SUPPLIER CODE'''
            ctk.CTkLabel(self.supplier_frame, text='Supplier Code: ', anchor='e', font=('DM Sans Medium', 14), width=width*0.09).grid(row = 1, column = 0, padx= (0,width*0.01), pady = (height*0.01,0), sticky = 'nsew')
            self.supplier_code = ctk.CTkLabel(self.supplier_frame, height = height *0.05, width=width*0.1, text="",fg_color=Color.White_Platinum, font=('DM Sans Medium', 14), corner_radius=5)
            self.supplier_code.grid(row =1, column = 1, columnspan=2, sticky = 'nsw',padx= (0), pady = (0))
            
            '''SUPPLIER NAME'''
            ctk.CTkLabel(self.supplier_frame, text='Supplier Name: ', font=('DM Sans Medium', 14), anchor='e',  width=width*0.09).grid(row = 2, column = 0, pady = (height*0.01), padx= (width*0.01), sticky = 'nsew')
            
            self.supplier_name_entry = ctk.CTkOptionMenu(self.supplier_frame,  width=width*0.35, height=height*0.05, font=('DM Sans Medium', 14), command= supplier_callback)
            self.supplier_name_entry.grid(row = 2, column = 1, columnspan=2, sticky = 'nsew', pady = (height*0.01), padx= (0,width*0.01))
            self.supplier_name_entry.set("")
            
            '''BOT FRAME'''
            self.action_frame = ctk.CTkFrame(self.main_frame, height=height*0.15, corner_radius=5, fg_color=Color.White_Platinum)
            self.action_frame.grid(row=4, column=0,sticky="nsew", padx=width*0.005, pady=(0, height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
    
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left", padx=(width*0.005), pady=(height*0.01)) 
            
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Place Order',
                                         command=recieve_stock)
            self.add_btn.pack(side="right", padx=(width*0.005), pady=(height*0.01))

        def set_selections(self):
            self.item = [c[0] for c in database.fetch_data(sql_commands.show_all_items, None)]
            self.supplier_selection = [c[0] for c in database.fetch_data("SELECT supp_name FROM supplier_info")]
            self.item_name_entry.set("Select an item")
            self.supplier_name_entry.set("")
            self.item_code.configure(text="")
            self.supplier_code.configure(text="")
            self.stock_entry.set(0)
            

        def place(self, default_data: Optional[str] = None, update_cmds: callable = None, **kwargs):
            self.update_cmds = update_cmds
            if default_data:
                self.item_name_entry.set(default_data[2])
                self.item_name_entry._command(None)
            else:
                self.set_selections()
            self.item_name_entry.configure(values = item_unit(database.fetch_data(sql_commands.show_all_items, None)))
            return super().place(**kwargs)

        def stock (self, inventory_info: Optional[Union[tuple, cctk.cctkTreeView]] = None, acc_name: str = None):
            if not messagebox.askyesno("Restock Item", "Are you sure you want to proceed?", parent = self):
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
            '''if inventory_data: # if there was an already existing table; update the existing table
                if inventory_data[0][2] is None:#updating non-expiry stock
                    database.exec_nonquery([[sql_commands.update_non_expiry_stock, (self._inventory_info[2], uid)]])
                else: #updating expiry stock
                    database.exec_nonquery([[sql_commands.update_expiry_stock, (self._inventory_info[2], uid, inventory_data[0][2])]])
            else:# if there's no exisiting table; create new instance of an item
                database.exec_nonquery([[sql_commands.add_item_inventory, (uid, self._inventory_info[2], receiving_expiry or None)]])'''
            #temporary disabled to change the addign item inventory
            database.exec_nonquery([[sql_commands.add_item_inventory, (uid, self._inventory_info[2], receiving_expiry or None)]])
            database.exec_nonquery([[sql_commands.update_recieving_item, (acc_name, self._inventory_info[0])]])

            if isinstance(inventory_info, cctk.cctkTreeView):
                inventory_info.update_table(database.fetch_data(sql_commands.get_recieving_items))
            
            self.update_cmds()
            messagebox.showinfo('Success', 'Restocking Successful', parent = self)
    return restock(master, info, data_view, command_callback)

def show_status(master, info:tuple,):
    class show_status(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master,  corner_radius= 0, fg_color='transparent')

            def reset():
                self.place_forget()
                
            def page_callback():
                self.update_table()

            self.page_row_count = 14
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.65, height=height*0.86,
                                           border_width=1, border_color=Color.White_Platinum)
            self.main_frame.grid(row=0, column=0, sticky="n")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2,weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.top_frame, text="", image=Icons.inventory_status, font=("DM Sans Medium", 14)).pack(side="left",padx=(width*0.004, width*0.0035))
            ctk.CTkLabel(self.top_frame, text="INVENTORY STATUS", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=(0,width*0.015))
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.status_frame = ctk.CTkFrame(self.main_frame, height=height*0.06, width=width*0.2, fg_color=Color.White_Platinum)
            self.status_frame.grid(row=1, column=0,sticky="w", padx=width*0.005, pady=height*0.01)
            self.status_frame.pack_propagate(0)

            self.status_label = ctk.CTkLabel(self.status_frame, text="", font=("DM Sans Medium", 14))
            self.status_label.pack(side="left", padx=width*0.015)

            self.status_count = ctk.CTkLabel(self.status_frame, text="", font=("DM Sans Medium", 14))
            self.status_count.pack(side="right", padx=width*0.015)

            self.db_inventory_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,corner_radius=0)
            self.db_inventory_frame.grid(row=2, column=0, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            self.db_inventory_treeview = cctk.cctkTreeView(self.db_inventory_frame, width=width*0.64, height=height*0.85,
                                               column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*0.1)}-tl/ItemDescription:x-tl/QuantityPcs:{int(width*0.125)}-tr!30!30',)
            self.db_inventory_treeview.pack()
            
            self.page_counter = cctk.cctkPageNavigator(self.main_frame,  width=width*0.125, height=height*0.055, fg_color=Color.White_Platinum, page_fg_color=Color.White_Lotion, 
                                             font=("DM Sans Medium", 14), page_limit=1, disable_timer=100, command=page_callback,)
            self.page_counter.grid(row=3, column=0, sticky="ns", padx=width*0.005, pady=(0,height*0.01))
            
            self.no_data_label = ctk.CTkLabel(self.db_inventory_frame, text="", font=("DM Sans Medium", 14))
        
        def set_table(self, given:Optional[list] = None):      
            self.raw_list = given if given else self.raw_data
            self.pages, self.page_count = list_to_parted_list(self.raw_list, self.page_row_count, 1)
            self.page_counter.update_page_limit(self.page_count)
            self.update_table()
        
        def update_table(self):
            self.temp = self.pages[self.page_counter.get()-1] if self.pages else []
            if len(self.pages) != 0:
                self.temp = self.pages[self.page_counter.get()-1]; 
                self.no_data_label.place_forget() 
            else:
                self.temp = []
                self.no_data_label.configure(text=f'No {self.status_label._text.lower()} status data yet to show.')
                self.no_data_label.place(relx=0.5, rely=0.5, anchor='c')
            self.db_inventory_treeview.update_table(self.temp)
         
        def place(self, data, title, color, count, processing: Optional[bool] = True,**kwargs):
            try:
                return super().place(**kwargs)
            finally:
                self.raw_data = [(data[0], f'{data[1]} ({data[2]})', data[3]) if data[2] else (data[0],data[1], data[3]) for data in data] if processing else data
                self.status_frame.configure(fg_color=color)
                self.status_label.configure(text=title)
                self.status_count.configure(text=count)
                self.set_table()      

    return show_status(master, info,)

def supplier_list(master, info:tuple,):
    class supplier_list(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color='transparent', width=width * .835, height=height*0.92,)
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

            def update_tables(_ :any = None):
                self.refresh_btn.configure(state = ctk.DISABLED)
                self.refresh_btn.after(5000, lambda:self.refresh_btn.configure(state = ctk.NORMAL))
                
                self.supplier_treeview.pack_forget()
                data = database.fetch_data(sql_commands.get_supplier_info)
                self.supplier_treeview.update_table(data)
                self.supplier_treeview.pack()
            
            def view_record():
                if self.supplier_treeview.get_selected_data():
                    view_supplier(self, info, update_tables).place(relx=0.5, rely=0.5, anchor="c", record_id = self.supplier_treeview.get_selected_data()[0])
                else:
                    messagebox.showwarning('Warning','No record is selected', parent=self) 
                    
                

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.025)
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

            ctk.CTkLabel(self.top_frame, text="SUPPLIER LIST", text_color="white", font=("DM Sans Medium", 16)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.search_frame = ctk.CTkFrame(self.main_frame,width=width*0.3, height = height*0.05)
            self.search_frame.grid(row=1, column=0,sticky="w", padx=(width*0.005), pady=(height*0.01))

            self.search_frame.pack_propagate(0)
            ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0, fg_color="white")
            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

            self.add_item_btn = ctk.CTkButton(self.main_frame,width=width*0.1, height = height*0.05, text="Add Supplier",image=self.add_icon, font=("DM Sans Medium", 14),
                                           command=lambda: new_supplier(self, info, update_tables).place(relx=0.5, rely=0.5, anchor="c"))
            self.add_item_btn.grid(row=1, column=2, sticky="w", padx=(width*0.005), pady=(height*0.01))

            self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75",
                                              command=update_tables)
            self.refresh_btn.grid(row=1, column=1, sticky="w")
            
            self.view_btn = ctk.CTkButton(self.main_frame,width=width*0.085, height = height*0.05, text="View Record", font=("DM Sans Medium", 14),
                                           command=view_record)
            self.view_btn.grid(row=1, column=3, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            self.supplier_treeview = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * .8, height= height * .725, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/SupplierNo:{int(width*.085)}-tc/SupplierName:x-tl/ContactPerson:{int(width*.15)}-tl/ContactNo:{int(width*.135)}-tc/Address:{int(width*.185)}-tl!30!30')
            self.supplier_treeview.pack()
            
        def place(self, **kwargs):
            
            data = database.fetch_data(sql_commands.get_supplier_info)
            self.supplier_treeview.update_table(data)
            
            return super().place(**kwargs)
    return supplier_list(master, info)

def new_supplier(master, info:tuple, command_callback: Optional[callable] = None):
    class new_supplier(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback ):
            width = info[0]
            height = info[1]
            user = info[3]
            super().__init__(master, corner_radius= 0, fg_color='transparent')
           
            self._callback = command_callback
            
            def reset():
                for entries in self.entries: entries.delete(0, "end")
                self.place_forget()
            
            def validate_contact(var, mode, index):
                if not validate_contact_num(self.contact_var.get()):
                    self.supplier_number_entry.delete(0, "end")

            def add_supplier():
                
                if self.supplier_name_entry.get() == "" and self.supplier_person_entry.get() == "" and self.supplier_number_entry.get() == "" and self.supplier_address_entry.get() == "":
                    messagebox.showerror("Missing Information", "Please fill required fields", parent=self)
                    
                elif self.supplier_email_entry.get() and not validate_email(self.supplier_email_entry.get()):
                    messagebox.showerror("Invalid Entry", "Please enter a valid email address.", parent=self)
                    
                else:
                    database.exec_nonquery([[sql_commands.insert_supplier_info, (self.supplier_id._text, self.supplier_name_entry.get(), self.supplier_tele_entry.get(),
                                                                                 self.supplier_person_entry.get(), self.supplier_number_entry.get(),
                                                                                 self.supplier_email_entry.get() or 'NULL', self.supplier_address_entry.get(),
                                                                                 user[0][0])]])
                    messagebox.showinfo("Success", f"{self.supplier_id._text} is successfully added.", parent=self)
                    if self._callback: self._callback()
                    reset()
            
            self.contact_var = ctk.StringVar()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, height=height*0.65, fg_color=Color.White_Lotion, border_width=1, border_color=Color.Platinum)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="NEW SUPPLIER", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.border_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,)
            self.border_frame.grid(row=1, column=0, sticky="nsew", padx=width*0.005, pady=height*0.01)
            
            self.content_frame = ctk.CTkFrame(self.border_frame, fg_color=Color.White_Lotion,)
            self.content_frame.pack(fill="both", expand=1, padx=width*0.005, pady=height*0.01)
            self.content_frame.grid_columnconfigure(1, weight=1)
            
            '''SUPPLIER ID'''
            ctk.CTkLabel(self.content_frame, text="Supplier Number: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=0, column=0,  sticky="nsew", padx=width*0.005, pady=(height*0.025, height*0.01))
            self.supplier_id = ctk.CTkLabel(self.content_frame, font=("DM Sans Medium", 14), width=width*0.1, height=height*0.05, corner_radius=5,fg_color=Color.White_Platinum)
            self.supplier_id.grid(row=0, column=1, sticky="nsw", padx=(0, width*0.005), pady=(height*0.025,height*0.01))
            
            ctk.CTkLabel(self.content_frame, text="Supplier Information ", fg_color="transparent", font=("DM Sans Medium", 14), text_color=Color.Grey_Davy, width=width*0.0825, anchor="w").grid(row=1, column=0,  sticky="nsew", padx=width*0.005, pady=(height*0.001))
            
            '''SUPPLIER NAME'''
            ctk.CTkLabel(self.content_frame, text="Supplier Name: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=2, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.supplier_name_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.25)
            self.supplier_name_entry.grid(row=2, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01))
            
            '''SUPPLIER TELEPHONE'''
            ctk.CTkLabel(self.content_frame, text="Supplier Telephone#: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=3, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.supplier_tele_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.25)
            self.supplier_tele_entry.grid(row=3, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01))
            
            '''SUPPLIER PERSONNEL'''
            ctk.CTkLabel(self.content_frame, text="Contact Person: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=4, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.supplier_person_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.25)
            self.supplier_person_entry.grid(row=4, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01))
            
            '''CONTACT NUMBER''' 
            ctk.CTkLabel(self.content_frame, text="Contact Number: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=5, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.supplier_number_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.25, textvariable=self.contact_var)
            self.supplier_number_entry.grid(row=5, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01))
            self.contact_var.trace_add('write', validate_contact)
                       
            '''CONTACT EMAIL'''
            ctk.CTkLabel(self.content_frame, text="Email: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=6, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.01)
            self.supplier_email_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.25)
            self.supplier_email_entry.grid(row=6, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01))
                        
            '''ADDRESS'''
            ctk.CTkLabel(self.content_frame, text="Address: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=7, column=0,  sticky="nsew", padx=width*0.005, pady=(height*0.01, height*0.025))
            self.supplier_address_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.25)
            self.supplier_address_entry.grid(row=7, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.01, height*0.025))            
            
            
            '''BOTTOM FRAME'''
            self.bot_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,)
            self.bot_frame.grid(row=2, column=0, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))
            
            self.cancel_btn = ctk.CTkButton(self.bot_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command=reset)
            self.cancel_btn.pack(side="left", padx=(width*0.005), pady=(height*0.01)) 
            
            self.add_btn = ctk.CTkButton(self.bot_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Add Supplier',
                                         command=add_supplier)
            self.add_btn.pack(side="right", padx=(width*0.005), pady=(height*0.01))
            
            self.entries = [self.supplier_name_entry, self.supplier_person_entry, self.supplier_tele_entry, self.supplier_number_entry, self.supplier_email_entry, self.supplier_address_entry]
            
        def place(self, **kwargs):
            self.supplier_id.configure(text=generateId(initial = 'SUP', length = 6).upper())
            
            return super().place(**kwargs)
        
    return new_supplier(master, info, command_callback)

def view_supplier(master, info:tuple, command_callback: Optional[callable] = None):
    class view_supplier(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback):
            width = info[0]
            height = info[1]
            user = info[3]
            super().__init__(master, corner_radius= 0, fg_color='transparent')
            
            self._callback = command_callback
            self.save_icon = ctk.CTkImage(light_image=Image.open("image/save.png"), size=(20,20))
            self.edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(20,20))
            
            def reset():
                self.change_entries_state("normal")
                [entry.delete(0, "end") for entry in self.entries]
                self.place_forget()
            
            def validate_contact(var, mode, index):
                if not validate_contact_num(self.contact_var.get()):
                    self.supplier_number_entry.delete(0, "end")
            
            def validate_tele(var, mode, index):
                if not validate_contact_num(self.tele_var.get()):
                    self.supplier_tele_entry.delete(0, "end")        
                
            def edit_record():
                self.edit_info_button.pack_forget()
                
                self.cancel_edit.pack(side="right")
                self.save_info_button.pack(side="right")
                
                self.change_entries_state("normal")
                
            def cancel_edit():
                self.cancel_edit.pack_forget()
                self.save_info_button.pack_forget()
                
                self.edit_info_button.pack(side="right")
                self.set_entries()
                
            def refresh_table():
                self.raw_item_data = database.fetch_data(sql_commands.get_supplier_items, (self.supplier_id._text,))
                self.item_data = [(item[0], item[1], f'{item[2]} ({item[3]})') if item[3] else (item[0], item[1], item[2]) for item in self.raw_item_data]
                self.item_treeview.update_table(self.item_data)
                
            def update_record():
                
                if self.supplier_name_entry.get() == "" and self.supplier_person_entry.get() == "" and self.supplier_number_entry.get() == "" and self.supplier_address_entry.get() == "":
                    messagebox.showerror("Missing Information", "Please fill required fields", parent=self)
                    
                elif self.supplier_email_entry.get() and not validate_email(self.supplier_email_entry.get()):
                    messagebox.showerror("Invalid Entry", "Please enter a valid email address.", parent=self)
                    
                else:
                    database.exec_nonquery([[sql_commands.update_supplier_info, (self.supplier_name_entry.get(), self.supplier_tele_entry.get(), self.supplier_person_entry.get(),
                                                                                 self.supplier_number_entry.get(), self.supplier_email_entry.get(),
                                                                                 self.supplier_address_entry.get(), self.supplier_id._text)]])
                    messagebox.showinfo("Success", f"{self.supplier_id._text} is successfully updated.",parent=self)
                    
                    self.set_entries()
                    
                    self.cancel_edit.pack_forget()
                    self.save_info_button.pack_forget()
                    
                    self.edit_info_button.pack(side="right")
                    #self._callback()
            
            def add_item_supplier():
                self.raw_item_data = database.fetch_data(sql_commands.get_supplier_items, (self.record_id,))
                add_supplier_item(self, (width, height), command_callback=refresh_table).place(relx=0.5, rely=0.5, anchor='c', items=self.raw_item_data, supplier_id=self.supplier_id._text)
                
            def view_audit_info():
                info = database.fetch_data(sql_commands.get_supplier_audit_trail, (self.supplier_id._text,))
                audit_info(self, (width, height)).place(relx=0.5, rely=0.5, anchor='c', info=info)
                
            def deactive_item_supplier(var):
                database.exec_nonquery([[sql_commands.update_supplier_item_info_deactive, (self.supplier_id._text, self.raw_item_data[var][0])]])
                messagebox.showinfo("Success", "Item is removed for this supplier.", parent = self)
            
            self.contact_var = ctk.StringVar()
            self.tele_var = ctk.StringVar()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, height=height*0.65, fg_color=Color.White_Lotion, border_width=1, border_color=Color.Platinum)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="SUPPLIER INFORMATION", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.border_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,)
            self.border_frame.grid(row=1, column=0, sticky="nsew", padx=width*0.005, pady=height*0.01)
            
            self.content_frame = ctk.CTkFrame(self.border_frame, fg_color="transparent",)
            self.content_frame.pack(fill="both", expand=1, padx=width*0.005, pady=height*0.01)
            self.content_frame.grid_columnconfigure(1, weight=1)
            
            '''SUPPLIER ID'''
            ctk.CTkLabel(self.content_frame, text="Supplier Code: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=0, column=0,  sticky="nsew", padx=width*0.005, pady=(height*0.01, height*0.01))
            self.id_frame= ctk.CTkFrame(self.content_frame, fg_color="transparent")
            self.id_frame.grid(row=0, column=1, columnspan=4, sticky="ew", padx=(0, width*0.005))
            
            self.supplier_id = ctk.CTkLabel(self.id_frame, font=("DM Sans Medium", 14), width=width*0.115, height=height*0.05, corner_radius=5,fg_color=Color.White_Lotion)
            self.supplier_id.pack(side="left")
            
            self.info_btn = ctk.CTkButton(self.id_frame, width=height*0.05, height = height*0.05, image=Icons.info_icon, text="", font=("DM Sans Medium", 14),
                                            command=view_audit_info)
            self.info_btn.pack(side="right", padx=(width*0.005,0))
            
            self.edit_info_button = ctk.CTkButton(self.id_frame, image=self.edit_icon, text='Edit', font=("DM Sans Medium", 14), height=height*0.05, width=width*0.01, fg_color="#3b8dd0", command=edit_record)
            self.edit_info_button.pack(side="right")
            

            self.save_info_button = ctk.CTkButton(self.id_frame, image=self.save_icon, text='Update Record',font=("DM Sans Medium", 14), width=width*0.01, fg_color="#83bd75", height=height*0.05,
                                                  hover_color="#82bd0b", text_color="white", command=update_record)
            self.cancel_edit = ctk.CTkButton(self.id_frame, text="Cancel", hover_color=Color.Red_Tulip, fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14), width=width*0.015, height=height*0.05,
                                             command=cancel_edit)
                        
            '''SUPPLIER NAME'''
            ctk.CTkLabel(self.content_frame, text="Supplier Name: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=1, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.005)
            self.supplier_name_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.275)
            self.supplier_name_entry.grid(row=1, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.005))
            
            '''TELEPHONE'''
            ctk.CTkLabel(self.content_frame, text="Telephone/Landline: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=2, column=0,  sticky="nsew", padx=width*0.005, pady=height*0.005)
            self.supplier_tele_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.275, textvariable=self.tele_var)
            self.supplier_tele_entry.grid(row=2, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.005))
            self.tele_var.trace_add('write', validate_tele)
            
            '''SUPPLIER PERSONNEL'''
            ctk.CTkLabel(self.content_frame, text="Contact Person: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=1, column=3,  sticky="nsew", padx=width*0.005, pady=height*0.005)
            self.supplier_person_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.275)
            self.supplier_person_entry.grid(row=1, column=4, sticky="nsew", padx=(0, width*0.005), pady=(height*0.005))
            
            '''CONTACT NUMBER''' 
            ctk.CTkLabel(self.content_frame, text="Contact Number: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=2, column=3,  sticky="nsew", padx=width*0.005, pady=height*0.005)
            self.supplier_number_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.275, textvariable=self.contact_var)
            self.supplier_number_entry.grid(row=2, column=4, sticky="nsew", padx=(0, width*0.005), pady=(height*0.005))
            self.contact_var.trace_add('write', validate_contact)
                       
            '''CONTACT EMAIL'''
            ctk.CTkLabel(self.content_frame, text="Email: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=3, column=3,  sticky="nsew", padx=width*0.005, pady=(height*0.005, height*0.015))
            self.supplier_email_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.275)
            self.supplier_email_entry.grid(row=3, column=4, sticky="nsew", padx=(0, width*0.005), pady=(height*0.005, height*0.015))
                        
            '''ADDRESS'''
            ctk.CTkLabel(self.content_frame, text="Address: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=3, column=0,  sticky="nsew", padx=width*0.005, pady=(height*0.005, height*0.015))
            self.supplier_address_entry = ctk.CTkEntry(self.content_frame, font=("DM Sans Medium", 14), height=height*0.05, width=width*0.275)
            self.supplier_address_entry.grid(row=3, column=1, sticky="nsew", padx=(0, width*0.005), pady=(height*0.005, height*0.015))            
        
            self.entries = [self.supplier_name_entry, self.supplier_tele_entry, self.supplier_person_entry, self.supplier_number_entry, self.supplier_email_entry, self.supplier_address_entry]
        
            self.item_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum,height=height*0.5)
            self.item_frame.grid(row=2, column=0, sticky="nsew", padx=width*0.005, pady=(0, height*0.01))
            self.item_frame.grid_propagate(0)
            self.item_frame.grid_columnconfigure(0, weight=1)
            self.item_frame.grid_rowconfigure(1, weight=1)
            
            ctk.CTkLabel(self.item_frame, text="Items Delivered", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.0825, anchor="e").grid(row=0, column=0,  sticky="nsw", padx=width*0.005, pady=(height*0.005, height*0.015))
            self.add_item_btn = ctk.CTkButton(self.item_frame, height = height*0.05, text="Add Item", font=("DM Sans Medium", 14),
                                              command=add_item_supplier)
            self.add_item_btn.grid(row=0, column=1, sticky="nse", pady=(height*0.01), padx=(height*0.01))
            
            self.item_treeview_frame = ctk.CTkFrame(self.item_frame, fg_color="transparent")
            self.item_treeview_frame.grid(row=1,column=0, sticky="nsew", columnspan=2, padx=(height*0.01), pady=(0, height*0.01))
            
            self.item_treeview = cctk.cctkTreeView(self.item_treeview_frame, data=[],width= width*0.775, height= height*0.475, corner_radius=0,
                                           column_format=f'/No:{int(width*.03)}-#r/ItemCode:{int(width *.1)}-tc/ItemBrand:{int(width *.1)}-tl/ItemDescription:x-tl/Action:{int(width*.075)}-bD!30!35',
                                           bd_commands=deactive_item_supplier,
                                           )
            self.item_treeview.pack()
            
            
            
        def change_entries_state(self, state):
            if 'disabled' in state:
                color, width = Color.White_Lotion, 0
            elif 'normal' in state:
                color, width = Color.White_Lotion, 2
            
            for entries in self.entries: entries.configure(fg_color = color, border_width = width ,state = state)
        
        def set_entries(self):
            self.data = database.fetch_data(sql_commands.get_supplier_record, (f'{self.record_id}',))[0]
            [entry.delete(0, "end") for entry in self.entries]
            self.change_entries_state("normal")
            self.supplier_id.configure(text=self.data[0])
            self.supplier_name_entry.insert(0, f"{self.data[1]}")
            self.supplier_tele_entry.insert(0, f"{self.data[2]}")
            self.supplier_person_entry.insert(0, f"{self.data[3]}")
            self.supplier_number_entry.insert(0, f"{self.data[4]}")
            self.supplier_email_entry.insert(0, f"{self.data[5] or ''}")
            self.supplier_address_entry.insert(0, f"{self.data[6]}")
            #self.created_by.configure(text=self.data[6])
            #self.date_added.configure(text=self.data[7])
            #self.date_update.configure(text=f"{self.data[8] or 'No Updates'}")
            self.change_entries_state("disabled")
            return
            
        def place(self, record_id, **kwargs):
            self.record_id = record_id
            self.set_entries()
            self.raw_item_data = database.fetch_data(sql_commands.get_supplier_items, (self.record_id,))
            self.item_data = [(item[0], item[1], f'{item[2]} ({item[3]})') if item[3] else (item[0], item[1], item[2]) for item in self.raw_item_data]
            #print(self.item_data)
            self.item_treeview.update_table(self.item_data)
            
            return super().place(**kwargs)
        
    return view_supplier(master, info, command_callback)

def add_supplier_item(master, info:tuple, command_callback: callable = None):
    class add_supplier_item(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback ):
            width = info[0]
            height = info[1]
            super().__init__(master, width*0.65, height=height*0.65, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.command_callback = command_callback
            
            def reset():
                self.place_forget()
            
            
                
            def add_item_to_supplier():
                exist = database.fetch_data(sql_commands.get_supplier_item_info_if_exist, (self.supplier_id, self.item_treeview.get_selected_data()[0]))[0][0]
                if self.item_treeview.get_selected_data():
                    if exist:
                        print("IF")
                        database.exec_nonquery([[sql_commands.update_supplier_item_info_active, (self.supplier_id, self.item_treeview.get_selected_data()[0])]])
                    else:
                        print("ELSE")
                        database.exec_nonquery([[sql_commands.set_supplier_items, (self.supplier_id, self.item_treeview.get_selected_data()[0])]])
                    messagebox.showinfo("Item Added", "Item added to supplier delivery.", parent = self)
                else:
                    messagebox.showwarning('Warning','No record is selected', parent = self)
                self.refresh_table()
                if self.command_callback:
                    self.command_callback()
                    
                    
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], border_width=1, border_color=Color.Platinum)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1,weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=5,sticky="nsew",  padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="SUPPLIER INFORMATION", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.item_treeview_frame = ctk.CTkFrame(self.main_frame, fg_color = Color.White_Platinum)
            self.item_treeview_frame.grid(row=1, column=0, sticky="nsew", pady=(height*0.01), padx=(height*0.01))
            
            self.item_treeview = cctk.cctkTreeView(self.item_treeview_frame, data=[],width= width*0.64, height= height*0.5, corner_radius=0,
                                           column_format=f'/No:{int(width*.03)}-#r/ItemCode:{int(width *.085)}-tc/ItemBrand:{int(width *.1)}-tl/ItemDescription:x-tl!30!35',)
            self.item_treeview.pack()
            
            self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color = Color.White_Platinum)
            self.bottom_frame.grid(row=2, column=0, sticky="nsew", pady=(0, height*0.01), padx=(height*0.01))
            
            self.add_item_btn = ctk.CTkButton(self.bottom_frame, height = height*0.05, text="Add Item", font=("DM Sans Medium", 14),
                                             command=add_item_to_supplier)
            self.add_item_btn.pack(side="right", pady=(height*0.01), padx=(height*0.01))
            
            self.cancel_btn = ctk.CTkButton(self.bottom_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command= reset)
            self.cancel_btn.pack(side="left", pady=(height*0.01), padx=(height*0.01,0))
        
        def refresh_table(self):
            self.raw_item_data = database.fetch_data("SELECT UID, brand, name, unit FROM item_general_info")
            self.item_data = [(item[0], item[1], f'{item[2]} ({item[3]})') if item[3] else (item[0], item[1], item[2]) for item in not_in_set(self.raw_item_data, self.items)]
            self.item_treeview.update_table(self.item_data)
                
        def place(self, items, supplier_id, **kwargs):
            self.items = items
            self.supplier_id = supplier_id
            self.refresh_table()
            return super().place(**kwargs)
        
    return add_supplier_item(master, info, command_callback)

def receive_history(master, info:tuple,):
    class receive_history(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))

            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
            self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
            self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
            self.trash_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
            self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))
            self.generate_report_icon = ctk.CTkImage(light_image=Image.open("image/gen_report.png"),size=(26,26))
            
            self.page_row_count = 12

            def reset():
                self.place_forget()
                
            """ def get_history(_: any = None):
                data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (f'{str(self.month_option.get())} {str(self.year_option.get())}',))
                self.no_order_data.place(relx=0.5, rely=0.5, anchor='c') if not data else self.no_order_data.place_forget()
                self.data_view1.update_table(data) """
                
            def view_details(_:any = None):
                detail_orders(self,(width, height)).place(relx=0.5, rely=0.5, anchor='c', data=self.data_view1.get_selected_data()) if self.data_view1.get_selected_data() else messagebox.showwarning("Warning","Select a record first", parent = self)

            #pagination
            def refresh_treeview(_:any = None):
                self.refresh_btn.configure(state='disabled')
                self.raw_data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (f'{str(self.month_option.get())} {str(self.year_option.get())}',))
                set_table()
            
            def set_table(given:Optional[list] = None):      
                self.raw_list = given if given else self.raw_data
                self.pages, self.page_count = list_to_parted_list(self.raw_list, self.page_row_count, 1)
                self.page_counter.update_page_limit(self.page_count)
                page_update_table()

            def search_callback():
                temp = database.fetch_data(sql_commands.show_receiving_history)
                set_table(list_filterer(self.search_bar.get(), temp))
                
            def page_callback():
                page_update_table()
                
            def page_update_table():
                self.data_view1.pack_forget()
                self.temp = self.pages[self.page_counter.get()-1] if self.pages else []
                if len(self.pages) != 0:
                    self.temp = self.pages[self.page_counter.get()-1]; 
                    self.no_order_data.place_forget() 
                else:
                    self.temp = []
                    self.no_order_data.place(relx=0.5, rely=0.5, anchor='c')
                self.data_view1.update_table(self.temp)
                self.data_view1.pack()
                self.after(100, lambda: self.refresh_btn.configure(state='normal'))
        
            self.operational_year = [str(s[0]) for s in database.fetch_data(sql_commands.get_active_year_transaction)] or [str(datetime.now().year)]
            self.months = ["January", "February", "March","April","May", "June", "July", "August","September","October", "November", "December"]


            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3])
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(2, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=5,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="RECEIVED HISTORY", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
                        
            self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width= height*0.05, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", hover_color=Color.Green_Button_Hover_Color,
                                             command=refresh_treeview)
            self.refresh_btn.grid(row=1, column=1, sticky="w", padx=(0,width*0.005))
            
            self.view_history = ctk.CTkButton(self.main_frame, width=width*0.025, height = height*0.05, text="Vew Order Detail", font=("DM Sans Medium", 14),
                                             command=view_details)
            self.view_history.grid(row=1, column=2, sticky="w", padx=(0,width*0.005), pady=(height*0.01))

            self.date_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.date_frame.grid(row=1, column=3, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.date_frame.propagate(1)
            
            self.month_option = ctk.CTkOptionMenu(self.date_frame, values= self.months, anchor="center", width=width*0.125, font=("DM Sans Medium",14), 
                                                  height=height*0.045, command=refresh_treeview)
            self.month_option.pack(side="left", fill="x", expand=1,  padx=(width*0.0025), pady=(width*0.0025))
            self.month_option.set(f"{date.today().strftime('%B')}")
            
            self.year_option = ctk.CTkOptionMenu(self.date_frame, values=self.operational_year, width=width*0.1, font=("DM Sans Medium",14), 
                                                 height=height*0.045, anchor="center",command=refresh_treeview)
            self.year_option.pack(side="left", fill="x", expand=1,  padx=(0, width*0.0025), pady=(width*0.0025))
            self.year_option.set(f"{date.today().strftime('%Y')}")

            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color=Color.White_Lotion, corner_radius=0)
            self.treeview_frame.grid(row=2, column=0, columnspan=5, sticky="ew", padx=width*0.005, pady=(0,height*0.01))

            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * 0.8, height= height * 0.685, corner_radius=0,
                                            column_format=f'/No:{int(width*.035)}-#r/OrderID:{int(width*0.09)}-tc/ItemName:x-tl/StockPcs:{int(width*0.075)}-tr/SupplierName:{int(width*0.15)}-tl/DateReceived:{int(width*.12)}-tc/ReceivedBy:{int(width*.1)}-tl!33!35',
                                            double_click_command=view_details)
            self.data_view1.pack()
            
            self.bot_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Lotion, height=height*0.055,)
            self.bot_frame.grid(row=3, column=0,columnspan=6, sticky="nsew",padx=(width*0.005), pady=(width*0.005))
            
            self.page_counter = cctk.cctkPageNavigator(self.bot_frame,  width=width*0.125, height=height*0.0575, fg_color=Color.White_Platinum, page_fg_color=Color.White_Lotion, 
                                                font=("DM Sans Medium", 14), page_limit=1, command=page_callback, disable_timer=100)
            self.page_counter.place(relx=0.5,rely=0.5, anchor="c")
    
        
            self.no_order_data = ctk.CTkLabel(self.data_view1, text="No order data yet to show.", font=("DM Sans Medium", 14))
            
            self.search_bar = cctk.cctkSearchBar(self.main_frame, height=height*0.055, width=width*0.325, m_height=height, m_width=width, fg_color=Color.Platinum, command_callback=search_callback,
                                                close_command_callback=refresh_treeview,
                                                quary_command=sql_commands.get_order_history_search_query, dp_width=width*0.25, place_height=height*0.075, place_width=width*0.01, font=("DM Sans Medium", 14))
            self.search_bar.grid(row=1, column=0,sticky="w", padx=(width*0.005), pady=(width*0.005))
        
            #.grid(row=1, column=1, sticky="w", padx=(0,width*0.005))
            refresh_treeview()
        def place(self, **kwargs):
            month_year = date.today().strftime('%B %Y')
            #self.raw_data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (f'{month_year}',))

            #self.data_view1.update_table(data)
            #self.no_order_data.place(relx=0.5, rely=0.5, anchor='c') if not data else self.no_order_data.place_forget()
            return super().place(**kwargs)

    return receive_history(master, info)

def receive_report(master, info:tuple,):
    class receive_report(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.92, corner_radius= 0, fg_color='transparent')
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))

            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
            self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            self.sales_icon = ctk.CTkImage(light_image=Image.open("image/sales_report.png"), size=(16,16))
            self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
            self.trash_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
            self.person_icon = ctk.CTkImage(light_image= Image.open("image/person_icon.png"), size=(24,24))
            self.generate_report_icon = ctk.CTkImage(light_image=Image.open("image/gen_report.png"),size=(26,26))

            def reset():
                self.place_forget()
                
            def get_history(_):
                refresh()
            
            def refresh():
                self.refresh_btn.configure(state = ctk.DISABLED)
                data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (f'{str(self.month_option.get())} {str(self.year_option.get())}',))
                self.no_order_data.place(relx=0.5, rely=0.5, anchor='c') if not data else self.no_order_data.place_forget()
                self.data_view1.update_table(data)
                self.refresh_btn.after(5000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
                
            self.operational_year = [str(s[0]) for s in database.fetch_data(sql_commands.get_active_year_transaction)] or [str(datetime.now().year)]
            self.months = ["January", "February", "March","April","May", "June", "July", "August","September","October", "November", "December"]


            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3])
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.025)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(2, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=5,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="RECEIVED HISTORY", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width= height*0.05, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=refresh )
            self.refresh_btn.grid(row=1, column=1, sticky="w", padx=(0,width*0.005))
            
            self.show_gen_report = ctk.CTkButton(self.main_frame, image=self.generate_report_icon, width=height*0.05,  text="Generate Report", height=height*0.05,  font=("DM Sans Medium", 14),)
            self.show_gen_report.grid(row=1, column=4, sticky="nsew", padx=(0,width*0.005), pady=(height*0.01))

            self.date_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.date_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.date_frame.propagate(1)
            
            self.month_option = ctk.CTkOptionMenu(self.date_frame, values= self.months, anchor="center", width=width*0.125, font=("DM Sans Medium",14), 
                                                  height=height*0.045, command=get_history)
            self.month_option.pack(side="left", fill="x", expand=1,  padx=(width*0.0025), pady=(width*0.0025))
            self.month_option.set(f"{date.today().strftime('%B')}")
            
            self.year_option = ctk.CTkOptionMenu(self.date_frame, values=self.operational_year, width=width*0.1, font=("DM Sans Medium",14), 
                                                 height=height*0.045, anchor="center",command=get_history)
            self.year_option.pack(side="left", fill="x", expand=1,  padx=(0, width*0.0025), pady=(width*0.0025))
            self.year_option.set(f"{date.today().strftime('%Y')}")

            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, columnspan=5, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * 0.8, height= height * 0.73, corner_radius=0,
                                            column_format=f'/No:{int(width*.0325)}-#r/OrderID:{int(width*0.09)}-tc/ItemName:x-tl/StockPcs:{int(width*0.075)}-tr/SupplierName:{int(width*0.15)}-tl/DateReceived:{int(width*.12)}-tc/ReceivedBy:{int(width*.1)}-tl!30!30',
                                            )
            self.data_view1.pack()
            
            self.no_order_data = ctk.CTkLabel(self.data_view1, text="No order data yet to show.", font=("DM Sans Medium", 14))
            
        def place(self, **kwargs):
            month_year = date.today().strftime('%B %Y')
            data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (f'{month_year}',))

            self.data_view1.update_table(data)
            self.no_order_data.place(relx=0.5, rely=0.5, anchor='c') if not data else self.no_order_data.place_forget()
            return super().place(**kwargs)

    return receive_report(master, info)

def detail_orders(master, info:tuple):
    class detail_orders(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)

            self.cal_icon= ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(15,15))

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
                
            def get_history(_):
                data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (f'{str(self.month_option.get())} {str(self.year_option.get())}',))
                #data = database.fetch_data(sql_commands.show_receiving_hist_by_date, (str(self.month_option.get()), str(self.year_option.get())))
                self.data_view1.update_table(data)
                
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.65, height=height*0.65)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure((2),weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="RECEIVE DETAILS", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.015)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
            self.content_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(height*0.01), pady=(height*0.01,0))
            self.content_frame.grid_columnconfigure(1, weight=1)

            '''ORDER INFO FRAME'''
            self.order_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.185)
            self.order_info_frame.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=(0 ,width*0.005),)
            self.order_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.order_info_frame, text="Order Code:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.order_num_label = ctk.CTkLabel(self.order_info_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent")
            self.order_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))        

            '''ITEM INFO FRAME'''
            self.item_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.185)
            self.item_info_frame.grid(row=0, column=1, columnspan=1, sticky="nsew", padx=(0), pady=(0))
            self.item_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_info_frame, text="Item Name:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.item_name_label = ctk.CTkLabel(self.item_info_frame, text="R000000", font=("DM Sans Medium", 14), anchor='w', fg_color="transparent")
            self.item_name_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''ORDER INFO FRAME'''
            self.date_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.185)
            self.date_info_frame.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=(0 ,width*0.005),pady=(width*0.005,0))
            self.date_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.date_info_frame, text="Date Ordered:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.date_num_label = ctk.CTkLabel(self.date_info_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent")
            self.date_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))  
            
            '''ORDER INFO FRAME'''
            self.orderer_info_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Platinum, height=height*0.055, width=width*0.185)
            self.orderer_info_frame.grid(row=1, column=1, columnspan=1, sticky="nsw", padx=(0 ,width*0.005), pady=(width*0.005,0))
            self.orderer_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.orderer_info_frame, text="Order By:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.orderer_name_label = ctk.CTkLabel(self.orderer_info_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent")
            self.orderer_name_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))    
            
            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(height*0.01), pady=(height*0.01))

            self.order_details_treeview = cctk.cctkTreeView(self.treeview_frame, data=[],width= width * 0.635, height= height * 0.5, corner_radius=0,
                                            column_format=f'/No:{int(width*.035)}-#r/OrderID:{int(width*0.1)}-tc/QuantityPcs:{int(width*0.1)}-tr/Expiry:{int(width*0.125)}-tc/ReceivedBy:x-tl/DateReceived:{int(width*0.125)}-tc!33!35',)
            self.order_details_treeview.pack()
            
            self.order_label = [self.order_num_label, self.item_name_label, self.date_num_label, self.orderer_name_label]
            
        def place(self, data, **kwargs):
            self.data = database.fetch_data(sql_commands.get_order_info_history, (data[0],))
            self.other_info = database.fetch_data(sql_commands.get_order_info_history_id, (data[0],))[0]
            self.order_details_treeview.update_table(self.data)
            [self.order_label[i].configure(text=f"{self.other_info[i]}") for i in range(len(self.order_label))]
            
            return super().place(**kwargs)

        
    return detail_orders(master, info)

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

            #data = database.fetch_data(sql_commands.get_disposal_hist)
            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, width= width * .8, height= height * .775, corner_radius=0,
                                            column_format=f'/No:{int(width*.025)}-#r/ItemName:x-tl/InitialQuantity:{int(width*0.1)}-tr/FinalQuantity:{int(width*0.1)}-tr/FullDisposedDate:{int(width*.2)}-tc/DisposedBy:{int(width*.15)}-tc!30!30',
                                            header_color= Color.Blue_Cobalt, data_grid_color= (Color.White_Ghost, Color.Grey_Bright_2), content_color='transparent', record_text_color=Color.Blue_Maastricht,
                                            row_font=("Arial", 16), navbar_font=("Arial",16), nav_text_color="white", selected_color=Color.Blue_Steel,)
            self.data_view1.pack()

        def place(self, **kwargs):
            self.data_view1.update_table(database.fetch_data(sql_commands.get_disposal_hist))
            return super().place(**kwargs)

    return disposal_history(master, info)

def show_category(master, info:tuple):
    class show_category(ctk.CTkFrame):
        def __init__(self, master, info:tuple, ):
            width = info[0]
            height = info[1]
            user = info[3]
            super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)
           
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            def reset():
                self.place_forget()
                
            def deactivate_category(i:int):
                database.exec_nonquery([[sql_commands.update_category_deac, (user[0][0], self.data_view1._data[i][0],)]])

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.65, height=height*0.7 )
            self.main_frame.grid(row=0, column=0, padx=1, pady=1)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(3, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=Icons.get_image('add_item_icon', (22,22)), anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='CATEGORY', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.add_category_btn = ctk.CTkButton(self.main_frame,width=width*0.1, height = height*0.05, text="Add Category",image=Icons.get_image('add_icon', (15,15)), font=("DM Sans Medium", 14),
                                                  command=lambda:add_category(self,(width, height, user[0][0]), self.refresh_table).place(relx=0.5, rely=0.5, anchor="c"))
            self.add_category_btn.grid(row=1, column=1, sticky="e", padx=(width*0.005), pady=(width*0.005))

            self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width=width*0.025, height = height*0.05, image=Icons.get_image('refresh_icon', (20,20)), fg_color="#83BD75",hover_color=Color.Green_Button_Hover_Color,
                                             command=self.refresh_table)
            self.refresh_btn.grid(row=1, column=2, sticky="w")
            
            #self.dis_category_btn = ctk.CTkButton(self.main_frame,width=width*0.1, height = height*0.05, text="Disabled Categories", fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,  font=("DM Sans Medium", 14),
            #                                      command=lambda:show_disabled_category(self,(width, height, user[0][0]), self.refresh_table).place(relx=0.5, rely=0.5, anchor="c"))
            #self.dis_category_btn.grid(row=3, column=0, sticky="w", padx=(width*0.005), pady=(height*0.01))

            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(0,height*0.005))

            #self.category_data = self.conv_data()
            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, width= width*0.635, height= height*0.5, corner_radius=0,
                                            column_format=f'/No:{int(width*.035)}-#r/Category:x-tl/HasExpiry:{int(width*.095)}-tc!30!30', #/Action:{int(width*.055)}-bD
                                            bd_commands=deactivate_category)
            self.data_view1.pack()

        def conv_data(self):
            self.data = database.fetch_data("SELECT categ_name, does_expire FROM categories WHERE state = 1")
            self.ret = []
            for i in range(len(self.data)):
                temp = list(self.data[i])
                if temp[1] == 0:
                    temp[1] = "No"
                else:
                    temp[1] = "Yes" 
                self.ret.append(tuple(temp))
            
            self.data_view1.update_table(self.ret)
            self.data_view1.pack()
            
        def refresh_table(self):
            self.conv_data()
            
        def place(self, **kwargs):
            self.conv_data()
            
            return super().place(**kwargs)
    return show_category(master, info)

def show_disabled_category(master, info:tuple, table_update_callback: callable):
    class show_disabled_category(ctk.CTkFrame):
        def __init__(self, master, info:tuple, table_update_callback: callable):
            width = info[0]
            height = info[1]
            user = info[2]
            super().__init__(master, corner_radius= 0, fg_color='transparent')
           
            self._table_update_callback = table_update_callback 
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)

            self.add_item = ctk.CTkImage(light_image=Image.open("image/add_item.png"), size=(20,20))
            self.refresh_icon = ctk.CTkImage(light_image=Image.open("image/refresh.png"), size=(20,20))
            self.search = ctk.CTkImage(light_image=Image.open("image/searchsmol.png"),size=(16,15))
            self.plus = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(12,13))
            self.add_icon = ctk.CTkImage(light_image=Image.open("image/plus.png"), size=(13,13))
            self.restock_icon = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            self.inventory_icon = ctk.CTkImage(light_image = Image.open("image/inventory.png"), size=(24,25))
            self.trash_icon = ctk.CTkImage(light_image = Image.open("image/stock_sub.png"), size=(20,18))
            
            def reset():
                self.place_forget()
                
            def reactivate_category():
                if self.data_view1.get_selected_data()[0]:
                    database.exec_nonquery([[sql_commands.update_category_reac, (self.data_view1.get_selected_data()[0],)]])
                    self.refresh_table()
                    self._table_update_callback()
                else:
                    messagebox.showerror("Warning", "Select a record first", parent = self)

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3], width=width*0.65, height=height*0.7)
            self.main_frame.grid(row=0, column=0)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(3, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.add_item, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='DISABLED CATEGORY', anchor='w', corner_radius=0, font=("DM Sans Medium", 16), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.search_frame = ctk.CTkFrame(self.main_frame,width=width*0.3, height = height*0.05)
            self.search_frame.grid(row=1, column=0,sticky="w", padx=(width*0.0075,width*0.005), pady=(height*0.01))
            self.search_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.search_frame,text="", image=self.search).pack(side="left", padx=width*0.005)
            self.search_entry = ctk.CTkEntry(self.search_frame, placeholder_text="Search", border_width=0, fg_color="white")

            self.search_entry.pack(side="left", padx=(0, width*0.0025), fill="x", expand=1)

            self.add_category_btn = ctk.CTkButton(self.main_frame,width=width*0.1, height = height*0.05, text="Reactivate Category", font=("DM Sans Medium", 14),
                                                  command=reactivate_category)
            self.add_category_btn.grid(row=1, column=1, sticky="w", padx=(width*0.0025,width*0.005), pady=(height*0.01))

            self.refresh_btn = ctk.CTkButton(self.main_frame,text="", width=width*0.025, height = height*0.05, image=self.refresh_icon, fg_color="#83BD75", command=self.refresh_table)
            self.refresh_btn.grid(row=1, column=2, sticky="w")
        
            self.treeview_frame = ctk.CTkFrame(self.main_frame,fg_color="transparent")
            self.treeview_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(0,height*0.01))

            self.data_view1 = cctk.cctkTreeView(self.treeview_frame, width= width*0.635, height= height*0.55, corner_radius=0,
                                            column_format=f'/No:{int(width*.025)}-#r/CategoryName:x-tl/DisabledBy:{int(width*.165)}-tl/DisableDate:{int(width*.15)}-tc!30!30',
                                            )
            self.data_view1.pack()

        def conv_data(self):
            self.data = database.fetch_data("SELECT categ_name, disabled_by, Date_Format(Cast(disabled_date AS DATE), '%Y-%m-%d') FROM categories WHERE state = 0")
            self.data_view1.update_table(self.data)
            self.data_view1.pack()
            
        def refresh_table(self):
            self.refresh_btn.configure(state = ctk.DISABLED)
            self.conv_data()
            self.refresh_btn.after(5000, lambda: self.refresh_btn.configure(state = ctk.NORMAL))
            
        def place(self, **kwargs):
            self.conv_data()
            
            return super().place(**kwargs)
    return show_disabled_category(master, info, table_update_callback)

def add_category(master, info:tuple, table_update_callback: callable):
    class add_category(ctk.CTkFrame):
        def __init__(self, master, info:tuple, table_update_callback: callable):
            width = info[0]
            height = info[1]
            user = info[2]
            super().__init__(master, width=width*0.35, height=height*0.4, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            #self.add_item = ctk.CTkImage(light_image=Image.open("image/add_item.png"), size=(20,20))
            self._table_update_callback = table_update_callback 
            
            def reset():
                self.place_forget()
                self.category_name_entry.delete(0, tk.END)
                self.expiry_switch.deselect()
                self._table_update_callback()
                
            def add_category():
                if self.category_name_entry.get()=='':
                    messagebox.showwarning("Missing Information", "Complete required fields", parent = self)
                else:
                    database.exec_nonquery([[sql_commands.insert_new_category, (self.category_name_entry.get(),self.expiry_switch.get(),user)]])
                    reset()

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=Icons.get_image('add_item_icon', (20,20)), anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='ADD CATEGORY', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.add_category_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Color[2], height=height*0.085)
            self.add_category_frame.grid(row=1, column=0, sticky="nsew",padx=(width*0.005), pady=(height*0.01))
            self.add_category_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(self.add_category_frame, text="Category Name: ", font=("DM Sans Medium", 14), width=width*0.1, anchor="e").grid(row=0, column=0, pady = (height*0.025,height*0.01), padx = (width*0.01,0))
            self.category_name_entry = ctk.CTkEntry(self.add_category_frame, corner_radius=5, placeholder_text='Required', font=("DM Sans Medium",14), height=height*0.045)
            self.category_name_entry.grid(row = 0, column = 1,sticky = 'nsew', pady = (height*0.025,height*0.01), padx = (0, width*0.01), columnspan=5)
            
            self.expiry_switch_val= ctk.StringVar(value="0")
            ctk.CTkLabel(self.add_category_frame, text="Expiry: ", font=("DM Sans Medium", 14), width=width*0.1, anchor="e").grid(row=1, column=0, pady = (0,height*0.01), padx = (width*0.01,0))
            self.expiry_switch = ctk.CTkSwitch(self.add_category_frame, text="", variable=self.expiry_switch_val, onvalue="1", offvalue="0",

                                                font=("DM Sans Medium", 14))
            self.expiry_switch.grid(row=1,column=1, sticky="w", padx = (width*0.01))
            
            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 2, column = 0, sticky = 'nsew', padx=(width*0.005), pady = (0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command= reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.125, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Add Category',
                                         command=add_category)
            self.add_btn.pack(side="right",  padx = (width*0.0075), pady= height*0.01)
            
    return add_category(master, info, table_update_callback)

def restock_confirmation(master, info:tuple, command_callback: Optional[callable] = None):
    class restock_confirmation(ctk.CTkFrame):
        def __init__(self, master, info:tuple,  command_callback: Optional[callable]):
            global width, height
            width = info[0]
            height = info[1]
            acc_user = info[2][0][0]
            
            super().__init__(master, width=width*0.4, height=height*0.685, corner_radius= 0, fg_color='transparent')
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            self.command_callback = command_callback
            self.does_expire = 0
            
            self.calendar_icon = ctk.CTkImage(light_image=Image.open("image/calendar.png"),size=(18,20))
            
            self.restock = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,18))
            
            def reset():
                self.expiry_date_entry.configure(text="Set Expiry Date")
                self.place_forget()

            def update_stock():
                
                if(self.stock_spinner.value == 0):
                    messagebox.showerror("Fail to proceed", "Stock must be at least 1", parent = self)
                    return
                self.place_forget()
                recieving_info = database.fetch_data("SELECT * FROM recieving_item WHERE id = ?", (self.receiving_id.get(), ))[0]

                '''if self.does_expire and self.expiry_date_entry._text == "Set Expiry Date":
                    messagebox.showinfo("Warning", "Please enter a valid expiry date")
                    return
                    #return none if there's no expiry
                elif self.does_expire and (self.expiry_date_entry._text != "Set Expiry Date"):
                    if database.fetch_data("SELECT COUNT(*) FROM item_inventory_info WHERE UID = ? AND Expiry_Date = ?", (recieving_info[2], self.expiry_date_entry._text))[0][0] == 0:
                        database.exec_nonquery([[sql_commands.add_item_inventory, (recieving_info[2], self.stock_spinner.value, self.expiry_date_entry._text)],])
                    else:
                        database.exec_nonquery([[sql_commands.update_expiry_stock, (self.stock_spinner.value, recieving_info[2],  self.expiry_date_entry._text)]]) 
                    #if the item has expiry
                else:
                    database.exec_nonquery([[sql_commands.update_non_expiry_stock, (self.stock_spinner.value, recieving_info[2])]])
                    #if the item is non-expiry'''
                #disabled to change the the management of stock
                
                if self.does_expire and self.expiry_date_entry._text == "Set Expiry Date":
                    messagebox.showinfo("Warning", "Please enter a valid expiry date", parent = self)
                    return
                    #return none if there's no expiry
                elif self.does_expire and (self.expiry_date_entry._text != "Set Expiry Date"):
                    database.exec_nonquery([[sql_commands.add_item_inventory, (recieving_info[2], self.stock_spinner.value, self.expiry_date_entry._text)],])
                    #if the item has expiry
                else:
                    database.exec_nonquery([[sql_commands.add_item_inventory, (recieving_info[2], self.stock_spinner.value, None,)]])
                    #if the item is non-expiry
                
                if self.stock_spinner.value == self.stock_spinner._val_range[-1]:
                    database.exec_nonquery([[sql_commands.update_recieving_item, (acc_user, self.receiving_id.get())]])
                    messagebox.showinfo("Restocking Sucess", "The item has beed restocked", parent = self)
                else:
                    database.exec_nonquery([[sql_commands.update_recieving_item_partially_received_with_date_receiver, (self.stock_spinner.value, acc_user, self.receiving_id.get())],
                                            [sql_commands.record_partially_received_item, (self.receiving_id.get(), self.item_name_entry.get(), self.stock_spinner.value, self.supplier_name_entry.get(), None, acc_user)]])
                    messagebox.showinfo("Partially Restocking Success", "The item has been partially restocked", parent = self)
                expiry = self.expiry_date_entry._text if self.does_expire else None
                database.exec_nonquery([[sql_commands.insert_receiving_history, (self.receiving_id.get(), self.stock_spinner.value, acc_user, expiry )]])
                self.command_callback()
                reset()  

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.restock, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='CONFIRM RESTOCK', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.confirm_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.confirm_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.confirm_frame.grid_columnconfigure(2, weight=1)
            
            ctk.CTkLabel(self.confirm_frame, text="Receiving Code: ", font=("DM Sans Medium", 14), width=width*0.075, anchor="e").grid(row=0, column=0, pady = (height*0.025,height*0.01), padx = (width*0.01,0))
            self.receiving_id = ctk.CTkEntry(self.confirm_frame, border_width=0, corner_radius=5, font=("DM Sans Medium",14), height=height*0.055, state="disabled")
            self.receiving_id.grid(row = 0, column = 1,sticky = 'nsew', pady = (height*0.025,height*0.01), padx = (0, width*0.01),)
            
            ctk.CTkLabel(self.confirm_frame, text="Item Code: ", font=("DM Sans Medium", 14), height=height*0.055, width=width*0.075, anchor="e").grid(row=1, column=0, pady = (0,height*0.01), padx = (width*0.01,0))
            self.item_id_entry = ctk.CTkEntry(self.confirm_frame, corner_radius=5, border_width=0, font=("DM Sans Medium",14), height=height*0.045, state="disabled")
            self.item_id_entry.grid(row = 1, column = 1,sticky = 'nsew', pady = (0,height*0.01), padx = (0, width*0.01), columnspan=2)
            
            ctk.CTkLabel(self.confirm_frame, text="Item Name: ", font=("DM Sans Medium", 14), height=height*0.055, width=width*0.075, anchor="e").grid(row=2, column=0, pady = (0,height*0.01), padx = (width*0.01,0))
            self.item_name_entry = ctk.CTkEntry(self.confirm_frame, corner_radius=5, border_width=0, font=("DM Sans Medium",14), height=height*0.045, state="disabled")
            self.item_name_entry.grid(row = 2, column = 1,sticky = 'nsew', pady = (0,height*0.01), padx = (0, width*0.01), columnspan=2)
            
            ctk.CTkLabel(self.confirm_frame, text="Supplier: ", font=("DM Sans Medium", 14), height=height*0.055, width=width*0.075, anchor="e").grid(row=3, column=0, pady = (0,height*0.01), padx = (width*0.01,0))
            self.supplier_name_entry = ctk.CTkEntry(self.confirm_frame, corner_radius=5, border_width=0, font=("DM Sans Medium",14), height=height*0.045, state="disabled")
            self.supplier_name_entry.grid(row = 3, column = 1,sticky = 'nsew', pady = (0,height*0.01), padx = (0, width*0.01), columnspan=2)
            
            ctk.CTkLabel(self.confirm_frame, text="Stock: ", font=("DM Sans Medium", 14), width=width*0.075, anchor="e").grid(row=4, column=0, pady = (0,height*0.005), padx = (width*0.01,0))
            self.stock_spinner = cctk.cctkSpinnerCombo(self.confirm_frame, entry_font=("DM Mono Medium",14), val_range=(0, cctk.cctkSpinnerCombo.MAX_VAL))
            self.stock_spinner.grid(row = 4, column = 1,sticky = 'nsew', pady = (0,height*0.005), padx = (0, width*0.01), )

            
            '''EXPIRY'''
            self.expiry_frame= ctk.CTkFrame(self.confirm_frame, fg_color='transparent')
            #self.expiry_frame.grid(row=5, column=0, columnspan =3, sticky='nsew', pady = (height*0.025))
            self.expiry_frame.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(self.expiry_frame, text='Expiration Date: ', font=('DM Sans Medium', 14), anchor='e',  width=width*0.075).grid(row = 0, column = 0, padx= (width*0.01,0), sticky = 'nsew')
            self.expiry_date_entry = ctk.CTkLabel(self.expiry_frame, height * .05, fg_color=Color.White_Lotion, text="Set Expiry Date", font=('DM Sans Medium', 14), text_color=Color.Blue_Maastricht, corner_radius=3)
            self.expiry_date_entry.grid(row =0, column = 1, columnspan=1, sticky = 'nsew',padx= (0), )
            
            self.show_calendar = ctk.CTkButton(self.expiry_frame, text="",image=self.calendar_icon, height=height*0.05,width=width*0.03,
                                               command=lambda: cctk.tk_calendar(self.expiry_date_entry, "%s", date_format="raw", min_date=datetime.now()))
            self.show_calendar.grid(row=0, column=3, padx = (width*0.005,width*0.01), sticky="w")
            
            
            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 2, column = 0, sticky = 'nsew', padx=(width*0.005), pady = (0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command= reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.1, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Confirm',
                                         command = update_stock)
            self.add_btn.pack(side="right",  padx = (width*0.0075), pady= height*0.01)

            #self.does_expire =  database.fetch_data(sql_commands.check_if_item_does_expire, (self.item_uid, ))[0][0] == 1
            #self.place_forget()

            self.entries=[self.receiving_id, self.item_id_entry, self.item_name_entry, self.supplier_name_entry]

        def control_entries(self, value: str):
            [entry.configure(state=value) for entry in self.entries]
        
        def entry_setup(self):
            self.control_entries("normal")
            self.receiving_id.delete(0, ctk.END)
            self.receiving_id.insert(0, self.restocking_info[0])
            self.item_id_entry.delete(0, ctk.END)
            self.item_id_entry.insert(0, self.item_id)
            self.item_name_entry.delete(0, ctk.END)
            self.item_name_entry.insert(0, self.restocking_info[2])
            self.supplier_name_entry.delete(0, ctk.END)
            self.supplier_name_entry.insert(0, self.restocking_info[-2])
            self.control_entries("readonly")
            
            

            self.stock_spinner.configure(val_range = (1, self.restocking_info[3]))
            #self.stock_spinner.set(self.restocking_info[3])
            

        def place_expiry(self):
            global height, width
            self.expiry_frame.grid(row=5, column=0, columnspan =3, sticky='nsew', pady = (height*0.005,0)) if self.does_expire else self.expiry_frame.grid_forget()
                

        def place(self, restocking_info: tuple,  **kwargs):
            temp = database.fetch_data(sql_commands.get_item_does_expiry, (restocking_info[0],))[0]
            self.item_id, self.does_expire = temp[0], temp[1]
            self.place_expiry()
            self.restocking_info = restocking_info
            self.entry_setup()
            
            return super().place(**kwargs)
            
    return restock_confirmation(master, info, command_callback)

def disposal_confirmation(master, info:tuple, command_callback: callable = None):
    class disposal_confirmation(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback):
            width = info[0]
            height = info[1]
            self.acc_user = info[2][0][0]
            super().__init__(master, width=width*0.3, height=height*0.4, corner_radius= 0, fg_color='transparent')
            
            self.command_callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.restock = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,20))
            
            disp_reason = ['Expired', 'Defective/Damaged']
            
            
                    
            self.combo_var = ctk.StringVar(value="")
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=self.restock, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='ORDER DISPOSAL', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.confirm_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.confirm_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.confirm_frame.grid_columnconfigure(0, weight=1)
            
            self.item_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.item_frame.grid(row=0, column=0, sticky='nsew', pady = (height*0.025,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.item_frame, text="Item Name: ", font=("DM Sans Medium", 14), width=width*0.025, ).pack(side='left',pady = (height*0.01), padx = (width*0.05,0))
            self.item_name = ctk.CTkLabel(self.item_frame, text="🐱", font=("DM Sans Medium", 14))
            self.item_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            ctk.CTkLabel(self.confirm_frame, text="Reason for Disposal ", font=("DM Sans Medium", 14), width=width*0.06, anchor="e").grid(row=1, column=0, sticky="nsw",pady = (height*0.01,0), padx = (width*0.01))
            self.disposal_entry = ctk.CTkComboBox(self.confirm_frame, font=("DM Sans Medium",14), height=height*0.045, values=disp_reason, variable=self.combo_var, button_color=Color.Blue_Tufts,
                                                  button_hover_color=Color.Blue_Steel)
            self.disposal_entry.grid(row = 2, column = 0,sticky = 'nsew', pady = (0,height*0.01), padx = (width*0.01))
            self.disposal_entry.set("")
            
            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 2, column = 0, sticky = 'nsew', padx=(width*0.005), pady = (0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Tulip,
                                            font=("DM Sans Medium", 16), text='Cancel', command= self.reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.dispose_btn = ctk.CTkButton(self.action_frame, width=width*0.1, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Confirm Disposal',
                                             command=self.dispose_confirm)
            self.dispose_btn.pack(side="right",  padx = (width*0.0075), pady= height*0.01)
        
        def reset(self):
            self.command_callback()
            self.disposal_entry.set("")
            self.place_forget()
                
        def dispose_confirm(self):
            if self.combo_var.get() == "":
                messagebox.showerror('Missing Field','Enter a reason', parent = self)
            else:
                item_id = database.fetch_data("Select item_uid from recieving_item where id = ?", (self.data[0], ))[0][0]
                database.exec_nonquery([[sql_commands.set_expired_items_from_inventory, (generateId("D",8).upper(), self.data[0], item_id, self.data[2], self.data[3], f'{self.disposal_entry.get()}', self.acc_user)],
                                            ["UPDATE recieving_item SET state = -1 WHERE id = ?", (self.data[0], )]])
                messagebox.showinfo("Succeed", "Item Disposed", parent = self)
                self.reset()
        def place(self, data, **kwargs):
            self.data = data
            self.item_name.configure(text=self.data[2])
            return super().place(**kwargs)
            
    return disposal_confirmation(master, info, command_callback)

def item_disposal_confirmation(master, info:tuple, command_callback: callable = None):
    class item_disposal_confirmation(ctk.CTkFrame):
        def __init__(self, master, info:tuple, command_callback):
            width = info[0]
            height = info[1]
            self.acc_user = info[2][0][0]
            super().__init__(master, width=width*0.3, height=height*0.4, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.command_callback = command_callback
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)

            self.restock = ctk.CTkImage(light_image=Image.open("image/restock_plus.png"), size=(20,20))
            
            disp_reason = ['Expired', 'Defective', 'Damaged']
            self.combo_var = ctk.StringVar(value="")
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=Icons.delete_one_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='DISPOSAL CONFIRMATION', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.confirm_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.confirm_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.confirm_frame.grid_columnconfigure(0, weight=1)
            
            self.item_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.item_frame.grid(row=0, column=0, sticky='nsew', pady = (height*0.025,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.item_frame, text="Reason: ", font=("DM Sans Medium", 14), width=width*0.015, ).pack(side='left',pady = (height*0.01), padx = (width*0.05,0))
            self.item_name = ctk.CTkLabel(self.item_frame, text="🐱", font=("DM Sans Medium", 14))
            self.item_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            
            ctk.CTkLabel(self.confirm_frame, text="Enter Adminisrator Password: ", font=("DM Sans Medium", 14), width=width*0.06, anchor="e").grid(row=1, column=0, sticky="nsw",pady = (height*0.01,0), padx = (width*0.01))
            self.disposal_entry = ctk.CTkEntry(self.confirm_frame, font=("DM Sans Medium",14), height=height*0.045,show='*')
            self.disposal_entry.grid(row = 2, column = 0,sticky = 'nsew', pady = (0,height*0.01), padx = (width*0.01))
            
            '''Action Frame'''
            self.action_frame = ctk.CTkFrame(self.main_frame, corner_radius=5, fg_color=Color.White_Color[2])
            self.action_frame.grid(row = 2, column = 0, sticky = 'nsew', padx=(width*0.005), pady = (0,height*0.01))
            self.action_frame.grid_columnconfigure((0,1), weight=1)
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.075, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Hover,
                                            font=("DM Sans Medium", 16), text='Cancel', command= self.reset)
            self.cancel_btn.pack(side="left",  padx = (width*0.0075,0), pady= height*0.01) 
            
            self.dispose_btn = ctk.CTkButton(self.action_frame, width=width*0.1, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Confirm Disposal',
                                             command=self.dispose_confirm)
            self.dispose_btn.pack(side="right",  padx = (width*0.0075), pady= height*0.01)
        
        def reset(self):
            self.disposal_entry.delete(0, ctk.END)
            self.place_forget()
                
        def dispose_confirm(self):
            if self.disposal_entry.get() == 'testing':
                temp= [(data[0], f"{data[1]} ({data[2]})", data[3]) if data[2] else (data[0],data[1],data[3]) for data in (database.fetch_data(sql_commands.get_expired_items_to_dispose, None))]
                print(temp)
                [database.exec_nonquery([[sql_commands.set_expired_items_from_inventory, (generateId("D",8).upper(), None, items[0], items[1], items[2],  "Expired", self.acc_user)]]) for items in temp] 
                database.exec_nonquery([[sql_commands.update_expired_items, None]])
                messagebox.showinfo("Item Disposal", "Item is fully disposed", parent = self)
                self.command_callback()
                self.reset()
            else: 
                messagebox.showwarning("Wrong Password","Input does not match", parent = self)
        def place(self, data, **kwargs):
            self.item_name.configure(text=data)
            return super().place(**kwargs)
            
    return item_disposal_confirmation(master, info, command_callback)

def audit_info(master, info:tuple, title: Optional[str] = "Record Information"):
    class audit_info(ctk.CTkFrame):
        def __init__(self, master, info:tuple, title: Optional[str]):
            width = info[0]
            height = info[1]
            super().__init__(master, width=width*0.3, height=height*0.4, corner_radius= 0, fg_color='transparent')
            
            self.title = title
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Color[3],)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=Icons.info_icon, anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text=self.title, anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.confirm_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Color[2],)
            self.confirm_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.confirm_frame.grid_columnconfigure(0, weight=1)
            
            '''Added By'''
            self.added_by_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.added_by_frame.grid(row=0, column=0, sticky='nsew', pady = (height*0.025,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.added_by_frame, text="Added By:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e').pack(side='left',pady = (height*0.01), padx = (0))
            self.added_by_name = ctk.CTkLabel(self.added_by_frame, text="🐱", font=("DM Sans Medium", 14))
            self.added_by_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            '''Added Date'''
            self.added_date_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.added_date_frame.grid(row=1, column=0, sticky='nsew', pady = (0,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.added_date_frame, text="Added Date:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e').pack(side='left',pady = (height*0.01), padx = (0))
            self.added_date_entry = ctk.CTkLabel(self.added_date_frame, text="🐱", font=("DM Sans Medium", 14))
            self.added_date_entry.pack(side='left',pady = (height*0.01), padx = (0))
            
            '''Added By'''
            self.updated_by_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.updated_by_frame.grid(row=2, column=0, sticky='nsew', pady = (0,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.updated_by_frame, text="Updated By:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e').pack(side='left',pady = (height*0.01), padx = (0))
            self.updated_by_name = ctk.CTkLabel(self.updated_by_frame, text="🐱", font=("DM Sans Medium", 14))
            self.updated_by_name.pack(side='left',pady = (height*0.01), padx = (0))
            
            '''Added Date'''
            self.updated_date_frame = ctk.CTkFrame(self.confirm_frame, fg_color=Color.White_Lotion)
            self.updated_date_frame.grid(row=3, column=0, sticky='nsew', pady = (0,height*0.01), padx = (width*0.005))
            ctk.CTkLabel(self.updated_date_frame, text="Updated Date:  ", font=("DM Sans Medium", 14), width=width*0.0925, fg_color="transparent", anchor='e' ).pack(side='left',pady = (height*0.01), padx = (0))
            self.updated_date_entry = ctk.CTkLabel(self.updated_date_frame, text="🐱", font=("DM Sans Medium", 14))
            self.updated_date_entry.pack(side='left',pady = (height*0.01), padx = (0))
            
            self.entries = [self.added_by_name, self.added_date_entry, self.updated_by_name, self.updated_date_entry]
        def reset(self):
            self.place_forget()
        
        def set_entries(self):
            for entry in range(len(self.entries)):
                self.entries[entry].configure(text=self.info[entry])
        
        def place(self, info,**kwargs):
            self.info = info[0]
            self.set_entries()
            return super().place(**kwargs)
            
    return audit_info(master, info, title)


def order_info_screen(master, info:tuple):
    class order_info_screen(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color='transparent')

            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, height=height*0.765, width=width*0.45, fg_color=Color.White_Color[3], border_width=1, border_color=Color.White_Gray)
            self.main_frame.grid(row=0, column=0, sticky="nsew")
            self.main_frame.grid_propagate(0)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)

            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=4,sticky="nsew", padx=1, pady=(1,0))
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text='', image=Icons.get_image("info_icon", (35,35)), anchor='w', fg_color="transparent").pack(side="left", padx=(width*0.01,0))    
            ctk.CTkLabel(self.top_frame, text='ORDER INFO', anchor='w', corner_radius=0, font=("DM Sans Medium", 14), text_color=Color.White_Color[3]).pack(side="left", padx=(width*0.0025,0))
            
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=height*0.04, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)

            self.info_frame= ctk.CTkFrame(self.main_frame,fg_color=Color.White_Platinum,)
            self.info_frame.grid(row=1,column=0, sticky="nsew",  padx=(width*0.005), pady = (height*0.01))
            self.info_frame.grid_columnconfigure((0,1), weight=1)
            self.info_frame.grid_propagate(0)
            
            '''ORDER INFO FRAME'''
            self.order_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.order_info_frame.grid(row=0, column=0, columnspan=1, sticky="nsew", padx=(height*0.015,0), pady=(height*0.015,0))
            self.order_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.order_info_frame, text="Order Code:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.order_num_label = ctk.CTkLabel(self.order_info_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent")
            self.order_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))        

            '''DATE INFO FRAME'''
            self.date_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.date_info_frame.grid(row=1, column=0, columnspan=1, sticky="nsew", padx=(height*0.015,0), pady=(height*0.0075, height*0.02))
            self.date_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.date_info_frame, text="Order Date:  " , font=("DM Sans Medium", 14), width=width*0.085, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.date_num_label = ctk.CTkLabel(self.date_info_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent")
            self.date_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''ORDER FRAME'''
            self.order_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.order_info_frame.grid(row=1, column=1, columnspan=1, sticky="nsew", padx=(height*0.015), pady=(height*0.0075, height*0.02))
            self.order_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.order_info_frame, text="Order By:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.order_by_name_label = ctk.CTkLabel(self.order_info_frame, text="100", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w")
            self.order_by_name_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''ITEM NUM FRAME'''
            self.item_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.item_info_frame.grid(row=2, column=0, sticky="nsew",padx=(height*0.015,0), pady=(0, height*0.0075))
            self.item_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_info_frame, text="Item Code:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.item_num_label = ctk.CTkLabel(self.item_info_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent")
            self.item_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))        

            '''ITEM NAME FRAME'''
            self.item_name_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.3)
            self.item_name_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(height*0.015), pady=(0, height*0.0075))
            self.item_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_name_frame, text="Item Name:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.item_name_label = ctk.CTkLabel(self.item_name_frame, text="R000000", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w")
            self.item_name_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))        
        
            '''STATUS FRAME'''
            self.status_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.status_info_frame.grid(row=4, column=0, columnspan=1, sticky="nsew", padx=(height*0.015,0), pady=(height*0.0075))
            self.status_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.status_info_frame, text="Status:  " , font=("DM Sans Medium", 14), width=width*0.075, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.status_label = ctk.CTkLabel(self.status_info_frame, text="Pending", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w")
            self.status_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''QUANTITY FRAME'''
            self.quantity_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.quantity_info_frame.grid(row=5, column=0, columnspan=1, sticky="nsew", padx=(height*0.015,0), pady=(0, height*0.0075))
            self.quantity_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.quantity_info_frame, text="Order Quantity:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.quantity_num_label = ctk.CTkLabel(self.quantity_info_frame, text="100", font=("DM Sans Medium", 14), fg_color=Color.White_AntiFlash, corner_radius=5)
            self.quantity_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.0035), pady=(width*0.0035))
            
            '''PENDING FRAME'''
            self.pending_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.pending_info_frame.grid(row=5, column=1, columnspan=1, sticky="nsew", padx=(height*0.015), pady=(0,height*0.0075))
            self.pending_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.pending_info_frame, text="Partial Quantity:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.pending_num_label = ctk.CTkLabel(self.pending_info_frame, text="100", font=("DM Sans Medium", 14), fg_color=Color.White_AntiFlash, corner_radius=5)
            self.pending_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.0035), pady=(width*0.0035))
                        
            '''SUPPLIER CODE FRAME'''
            self.supplier_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.supplier_info_frame.grid(row=6, column=0, columnspan=1, sticky="nsew", padx=(height*0.015,0), pady=(height*0.015, height*0.0075))
            self.supplier_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.supplier_info_frame, text="Supplier Code:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.supplier_num_label = ctk.CTkLabel(self.supplier_info_frame, text="100", font=("DM Sans Medium", 14), fg_color="transparent")
            self.supplier_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''SUPPLIER NAME FRAME'''
            self.sup_name_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.sup_name_info_frame.grid(row=7, column=0, columnspan=2, sticky="nsew", padx=(height*0.015), pady=(0, height*0.0075))
            self.sup_name_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.sup_name_info_frame, text="Supplier Name:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.sup_name_label = ctk.CTkLabel(self.sup_name_info_frame, text="100", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w")
            self.sup_name_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''SUPPLIER PERSON FRAME'''
            self.supp_person_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.supp_person_info_frame.grid(row=8, column=0, columnspan=2, sticky="nsew", padx=(height*0.015), pady=(0, height*0.0075))
            self.supp_person_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.supp_person_info_frame, text="Contact Person:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.supp_person_num_label = ctk.CTkLabel(self.supp_person_info_frame, text="100", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w")
            self.supp_person_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            '''SUPPLIER CONTACT FRAME'''
            self.supp_contact_info_frame = ctk.CTkFrame(self.info_frame, fg_color=Color.White_Lotion, height=height*0.055, width=width*0.185)
            self.supp_contact_info_frame.grid(row=9, column=0, columnspan=2, sticky="nsew", padx=(height*0.015), pady=(0, height*0.0075))
            self.supp_contact_info_frame.pack_propagate(0)
            ctk.CTkLabel(self.supp_contact_info_frame, text="Contact Number:  " , font=("DM Sans Medium", 14), width=width*0.1, fg_color="transparent", anchor="e").pack(side="left", padx=(width*0.005,0), pady=(width*0.005))
            self.supp_contact_num_label = ctk.CTkLabel(self.supp_contact_info_frame, text="100", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w")
            self.supp_contact_num_label.pack(side="left", expand=1, fill="both", padx=(0, width*0.005), pady=(width*0.005))
            
            self.labels = [self.order_num_label, self.date_num_label,  self.order_by_name_label, self.item_num_label, self.item_name_label,
                           self.status_label, self.quantity_num_label, self.pending_num_label,
                           self.supplier_num_label, self.sup_name_label, self.supp_person_num_label, self.supp_contact_num_label]
            
        def reset(self):
            self.place_forget()
        
        def set_label(self):
            [self.labels[index].configure(text=self.data[index])for index in range(len(self.labels))]
            if self.status_label._text == 'On Order':
                self.pending_num_label.configure(text='0')
                
        def place(self, data, **kwargs):
            self.data = (database.fetch_data(sql_commands.get_order_info, (data[0],)))[0]
            self.set_label()
            return super().place(**kwargs)
            
    return order_info_screen(master, info)