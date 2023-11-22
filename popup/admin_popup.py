import customtkinter as ctk
import sql_commands
from Theme import Color
from util import database
from util import *
from tkinter import messagebox
from PIL import Image

def show_service_info(master, info:tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.service = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(25,25))
            self.edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(18,18))
            self.save_icon = ctk.CTkImage(light_image=Image.open("image/save.png"), size=(25,25))
            self.remove_icon = ctk.CTkImage(light_image=Image.open("image/trash.png"), size=(18,18))
            
            def edit_entries():
                self.edit_button.pack_forget()
                self.remove_button.pack_forget()
                self.set_entries('normal')
                
                self.cancel_button.pack(side=ctk.RIGHT, padx=(width*0.005,0))
                self.save_button.pack(side=ctk.RIGHT)
            
            def cancel_changes():
                self.set_entries('disabled')
                self.save_button.pack_forget()
                self.cancel_button.pack_forget()
                
                #self.remove_button.pack(side=ctk.RIGHT,padx=(width*0.005, 0))
                self.edit_button.pack(side=ctk.RIGHT)
                
            def save_changes():
                self.set_entries('disabled')
                self.save_button.pack_forget()
                self.cancel_button.pack_forget()

                if database.exec_nonquery([["UPDATE service_info_test SET service_name =?, category =?, price =? WHERE UID =?", (self.service_name_entry.get(), self.service_category_entry.get(), float(self.service_price_entry.get()), self.service_id_label._text)]]):
                    messagebox.showinfo("Success", "Service Updated\nRestart the system to apply changes", parent = self)
                    self.reload_service()
                else:
                    messagebox.showerror("Error", "An error occured\nfailed to change", parent = self)

                self.place_forget()
                #self.remove_button.pack(side=ctk.RIGHT,padx=(width*0.005, 0))
                self.edit_button.pack(side=ctk.RIGHT)
            
            self.main_frame = ctk.CTkFrame(self, width * 0.45, height=height*0.525, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=1, pady=1)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.service).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="SERVICE INFORMATION", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.content_frame.columnconfigure((1), weight=1)
            
            '''SERVICE ID'''
            self.service_id_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.065, width=width*0.185)
            self.service_id_frame.grid(row=0, column=0, sticky="nsw",padx=(width*0.005), pady=(height*0.01))
            self.service_id_frame.pack_propagate(0)
            ctk.CTkLabel(self.service_id_frame, text="Service ID: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.085, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.service_id_label = ctk.CTkLabel(self.service_id_frame, text="0000000", font=("DM Sans Medium", 14), corner_radius=5)
            self.service_id_label.pack(side=ctk.LEFT, fill='both', expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            '''BUTTONS'''
            self.event_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=height*0.055)
            self.event_frame.grid(row=0, column=1, sticky="nsew",padx=(0,width*0.005), pady=(height*0.01))
            self.event_frame.pack_propagate(0)
            
            self.remove_button = ctk.CTkButton(self.event_frame, text="Remove", height=height*0.055, width=width*0.065,image=self.remove_icon, fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14),)
            #self.remove_button.pack(side=ctk.RIGHT,padx=(width*0.005, 0))
            
            self.edit_button = ctk.CTkButton(self.event_frame, text="Edit", height=height*0.055, width=width*0.065,image=self.edit_icon, font=("DM Sans Medium", 14), command=edit_entries)
            self.edit_button.pack(side=ctk.RIGHT)
            
            self.save_button = ctk.CTkButton(self.event_frame, text="Save", height=height*0.055, width=width*0.065, image=self.save_icon, fg_color=Color.Green_Pistachio,
                                             hover_color=Color.Green_Aparagus, font=("DM Sans Medium", 14), command=save_changes)
            
            self.cancel_button = ctk.CTkButton(self.event_frame, text="Cancel", height=height*0.055, width=width*0.065, fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14),command=cancel_changes)
            
            
            '''SERVICE NAME'''
            self.service_name_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.service_name_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.005, height*0.01))
            self.service_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.service_name_frame, text="Service Name: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.085, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.service_name_entry = ctk.CTkEntry(self.service_name_frame, font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.service_name_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005)) 
        
            '''SERVICE CATEGORY'''
            self.service_category_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            #self.service_category_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.service_category_frame, text="Category: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.085, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.service_category_entry = ctk.CTkEntry(self.service_category_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.service_category_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            #self.service_category_option = ctk.CTkOptionMenu(self.service_category_frame, values=["Male","Female"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum,)
            
            '''SERVICE PRICE'''
            self.service_price_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.service_price_frame.grid(row=3, column=0, columnspan=1, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.service_price_frame, text="Price: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.085, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.service_price_entry = ctk.CTkEntry(self.service_price_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.service_price_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))

            '''SERVICE DATE'''
            self.service_date_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.service_date_frame.grid(row=3, column=1, columnspan=1, sticky="nsew", padx=(0,width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.service_date_frame, text="Date Added: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.085, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.service_date_label = ctk.CTkLabel(self.service_date_frame, text="0000000", font=("DM Sans Medium", 14), fg_color="transparent", corner_radius=5)
            self.service_date_label.pack(side=ctk.LEFT, fill='both', expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            self.entries=[self.service_name_entry, self.service_price_entry,self.service_category_entry]
            
            
        def reset(self):
            self.place_forget()
            self.set_entries('normal')
            self.reset_entries()
                
        def set_entries(self, state):
            for i in range(len(self.entries)):
                if 'normal' in state:
                    b_width= 2
                elif 'disabled' in state:
                    b_width = 0
                self.entries[i].configure(state=state,border_width=b_width )
            #self.service_item_txtbox.configure(state=state)
            
            
        def reset_entries(self):
            for i in range(len(self.entries)):
                self.entries[i].delete(0, ctk.END)
            #self.service_item_txtbox.delete("0.0", ctk.END)
        
        def load_data(self, raw_data):
            #print(raw_data)
            self.set_entries(state='normal')
            self.service_id_label.configure(text=f"{raw_data[0][0]}")
            self.service_name_entry.insert(0, f"{raw_data[0][1]}")
            self.service_price_entry.insert(0, f"{raw_data[0][2]}")
            self.service_category_entry.insert(0, f"{raw_data[0][3]}")
            self.service_date_label.configure(text=f"{raw_data[0][4]}")
            
            #self.service_item_txtbox.insert("0.0", f"{raw_data[0][2]}")
            self.set_entries(state='disabled')
        def place(self, service_info, service_reload_callback, **kwargs):
            self.reload_service = service_reload_callback
            self.raw_data = database.fetch_data(sql_commands.get_service_info, (f'{service_info[0]}',))
            self.load_data(self.raw_data)
            return super().place(**kwargs)
    return instance(master, info)

def show_item_info(master, info:tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            
            self.inventory = ctk.CTkImage(light_image=Image.open("image/inventory.png"), size=(22,25))
            self.edit_icon = ctk.CTkImage(light_image=Image.open("image/edit_icon.png"), size=(18,18))
            self.save_icon = ctk.CTkImage(light_image=Image.open("image/save.png"), size=(25,25))
            self.remove_icon = ctk.CTkImage(light_image=Image.open("image/trash.png"), size=(18,18))
            
            def edit_entries():
                self.edit_button.pack_forget()
                self.remove_button.pack_forget()
                self.set_entries('normal')
                
                #self.item_category_entry.pack_forget()
                #self.item_category_option.pack(side=ctk.LEFT, fill="x", expand=1, padx=(0,width*0.0025), pady=(height*0.005))
                
                self.cancel_button.pack(side=ctk.RIGHT, padx=(width*0.005,0))
                self.save_button.pack(side=ctk.RIGHT)
            
            def cancel_changes():
                self.set_entries('disabled')
                self.save_button.pack_forget()
                self.cancel_button.pack_forget()
                
                #self.item_category_option.pack_forget()
                #self.item_category_entry.pack(side=ctk.LEFT, fill="x", expand=1, padx=(0,width*0.0025), pady=(height*0.005))
                
                #self.remove_button.pack(side=ctk.RIGHT,padx=(width*0.005, 0))
                self.edit_button.pack(side=ctk.RIGHT)
                
            def save_changes():
                self.set_entries('disabled')
                self.save_button.pack_forget()
                self.cancel_button.pack_forget()

                #self.item_category_option.pack_forget()
                #self.item_category_entry.pack(side=ctk.LEFT, fill="x", expand=1, padx=(0,width*0.0025), pady=(height*0.005))

                if database.exec_nonquery([["UPDATE item_general_info SET name =?, Category =? WHERE UID =?", (self.item_name_entry.get(), self.item_category_entry.get(), self.item_id_label._text)],
                                           ["UPDATE item_settings SET Cost_price =?, Markup_Factor =?, Reorder_Factor =?, Crit_Factor =?, Safe_Stock =?, rate_mode = ? WHERE UID = ?", (float(self.item_unit_price_entry.get()), float(self.item_markup_entry.get())/float(self.item_unit_price_entry.get()), float(self.item_reorder_entry.get()), float(self.item_crit_entry.get()), int(self.item_safe_stock_entry.get()), int(self.item_rate_entry._values.index(self.item_rate_entry.get())), self.item_id_label._text)]]):
                    messagebox.showinfo("Success", "Item Updated\nRestart the system to apply changes", parent = self)
                    self.reload_item()
                    self.place_forget()
                    self.reset()
                else:
                    messagebox.showerror("Failed to Update", "An error occured", parent = self)
                
                #self.remove_button.pack(side=ctk.RIGHT,padx=(width*0.005, 0))
                self.edit_button.pack(side=ctk.RIGHT)
            
            self.main_frame = ctk.CTkFrame(self, width * 0.45, height=height*0.85, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew",padx=1, pady=1)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(1, weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.inventory).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="ITEM INFORMATION", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=self.reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            self.content_frame.columnconfigure((0,1), weight=1)
            
            '''SERVICE ID'''
            self.item_id_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.065, width=width*0.15)
            self.item_id_frame.grid(row=0, column=0, sticky="nsw",padx=(width*0.005), pady=(height*0.01))
            self.item_id_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_id_frame, text="Item ID: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.055, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_id_label = ctk.CTkLabel(self.item_id_frame, text="0000000", font=("DM Sans Medium", 14), corner_radius=5)
            self.item_id_label.pack(side=ctk.LEFT, fill='both', expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            '''BUTTONS'''
            self.event_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent", height=height*0.055)
            self.event_frame.grid(row=0, column=1, sticky="nsew",padx=(0,width*0.005), pady=(height*0.01))
            self.event_frame.pack_propagate(0)
            
            self.remove_button = ctk.CTkButton(self.event_frame, text="Remove", height=height*0.055, width=width*0.065,image=self.remove_icon, fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14),)
            #self.remove_button.pack(side=ctk.RIGHT,padx=(width*0.005, 0))
            
            self.edit_button = ctk.CTkButton(self.event_frame, text="Edit", height=height*0.055, width=width*0.065,image=self.edit_icon, font=("DM Sans Medium", 14), command=edit_entries)
            self.edit_button.pack(side=ctk.RIGHT)
            
            self.save_button = ctk.CTkButton(self.event_frame, text="Save", height=height*0.055, width=width*0.065, image=self.save_icon, fg_color=Color.Green_Pistachio,
                                             hover_color=Color.Green_Aparagus, font=("DM Sans Medium", 14), command=save_changes)
            
            self.cancel_button = ctk.CTkButton(self.event_frame, text="Cancel", height=height*0.055, width=width*0.065, fg_color=Color.Red_Pastel, font=("DM Sans Medium", 14),command=cancel_changes)
            
            '''ITEM NAME'''
            self.item_name_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_name_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(height*0.005, height*0.01))
            self.item_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_name_frame, text="Item Name: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.065, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_name_entry = ctk.CTkEntry(self.item_name_frame, font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_name_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005)) 
            
            '''ITEM UNIT'''
            self.item_unit_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_unit_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            self.item_unit_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_unit_frame, text="Item Unit: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.065, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_unit_entry = ctk.CTkEntry(self.item_unit_frame, font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_unit_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005)) 
        
            '''ITEM CATEGORY'''
            self.item_category_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_category_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.item_category_frame, text="Category: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.065, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_category_entry = ctk.CTkEntry(self.item_category_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_category_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            #self.service_category_option = ctk.CTkOptionMenu(self.service_category_frame, values=["Male","Female"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum,)
            
            '''ITEM PRICE'''
            ctk.CTkLabel(self.content_frame, text="Item Price", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w").grid(row=4, column=0, columnspan=1, sticky="nsew", padx=(width*0.01), pady=(0, height*0.01))
            
            #UNIT PRICE
            self.item_unit_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_unit_frame.grid(row=5, column=0, columnspan=1, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.item_unit_frame, text="Unit Price:  ₱  ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.075, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_unit_price_entry = ctk.CTkEntry(self.item_unit_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_unit_price_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            #MARKUP FACTOR
            self.item_markup_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06,width=width*0.15)
            self.item_markup_frame.grid(row=5, column=1, columnspan=1, sticky="nsw", padx=(0,width*0.005), pady=(0, height*0.01))
            self.item_markup_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_markup_frame, text="Markup Price: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.08, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_markup_entry = ctk.CTkEntry(self.item_markup_frame,  font=("DM Sans Medium",14), width=width*0.04, fg_color=Color.White_Lotion, state='disable', justify='right')
            self.item_markup_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            #ctk.CTkLabel(self.item_markup_frame, text="  %", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.015, anchor="w").pack(side=ctk.RIGHT, padx=(0,width*0.005),pady=(height*0.01))
            
            #SELLING PRICE
            self.item_selling_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_selling_frame.grid(row=6, column=0, columnspan=1, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.item_selling_frame, text="Selling Price:  ₱  ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.075, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_selling_price_entry = ctk.CTkEntry(self.item_selling_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_selling_price_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            '''ITEM INVENTORY'''
            ctk.CTkLabel(self.content_frame, text="Item Inventory", font=("DM Sans Medium", 14), fg_color="transparent", anchor="w").grid(row=7, column=0, columnspan=1, sticky="nsew", padx=(width*0.01), pady=(0, height*0.01))
            
            #REORDER FACTOR
            self.item_reorder_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_reorder_frame.grid(row=8, column=0, columnspan=1, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.item_reorder_frame, text="Reorder Factor: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.0825, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_reorder_entry = ctk.CTkEntry(self.item_reorder_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_reorder_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            #CRIT FACTOR
            self.item_crit_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06, width=width*0.15)
            self.item_crit_frame.grid(row=8, column=1, columnspan=1, sticky="nsw", padx=(0,width*0.005), pady=(0, height*0.01))
            self.item_crit_frame.pack_propagate(0)
            ctk.CTkLabel(self.item_crit_frame, text="Critical Factor: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.0775, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_crit_entry = ctk.CTkEntry(self.item_crit_frame,  font=("DM Sans Medium",14), width=width*0.05, fg_color=Color.White_Lotion, state='disable')
            self.item_crit_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
             
            #SAFE STOCK
            self.item_safe_stock_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_safe_stock_frame.grid(row=10, column=0, columnspan=1, sticky="nsew", padx=(width*0.005), pady=(0, height*0.01))
            ctk.CTkLabel(self.item_safe_stock_frame, text="Safe Stock: ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.0825, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_safe_stock_entry = ctk.CTkEntry(self.item_safe_stock_frame,  font=("DM Sans Medium",14), fg_color=Color.White_Lotion, state='disable')
            self.item_safe_stock_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            '''ITEM RATE'''
            
            self.item_rate_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.06)
            self.item_rate_frame.grid(row=11, column=0, columnspan=1, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            ctk.CTkLabel(self.item_rate_frame, text="Selling Rate:  ", font=("DM Sans Medium", 14), fg_color="transparent", width=width*0.0825, anchor="e").pack(side=ctk.LEFT, padx=(width*0.005,0),pady=(height*0.01))
            self.item_rate_entry = ctk.CTkOptionMenu(self.item_rate_frame, values=["Automatic", "Low", "High"], font=("DM Sans Medium",14), fg_color=Color.White_Lotion, anchor='w', text_color=Color.Blue_Maastricht)
            self.item_rate_entry.pack(side=ctk.LEFT, fill="both",expand=1, padx=(0,width*0.0025), pady=(height*0.005))
            
            #self.item_category_option = ctk.CTkOptionMenu(self.item_category_frame, values=["Male","Female"], font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Platinum,)
            
            self.entries = [self.item_name_entry, self.item_unit_entry, self.item_category_entry, self.item_unit_price_entry, self.item_markup_entry, self.item_selling_price_entry,
                            self.item_reorder_entry, self.item_crit_entry, self.item_safe_stock_entry]
            
        
        def reset(self):
            self.place_forget()
            self.set_entries('normal')
            self.reset_entries()
                
        def set_entries(self, state):
            for i in range(len(self.entries)):
                if 'disabled' in state or i in [1, 2, 5]:
                    b_width = 0
                if 'normal' in state and i not in [1, 2, 5]:
                    b_width= 2
                self.entries[i].configure(state=state,border_width=b_width)
            
        def reset_entries(self):
            for i in range(len(self.entries)):
                self.entries[i].delete(0, ctk.END)
            #self.service_item_txtbox.delete("0.0", ctk.END)
        
        def load_data(self, raw_data):
            self.set_entries('normal')

            self.item_id_label.configure(text=raw_data[0])
            #self.item_rate_entry.configure(text = raw_data[-1])
            for i in range(len(self.entries)):
                '''if i == 4:
                    self.entries[i].insert(0, f"{raw_data[i+1]*100}" )
                    continue'''
                
                self.entries[i].insert(0, raw_data[i+1])
            self.set_entries('disabled')
            
        def place(self, item_info, item_reload_callback, **kwargs):
            self.reload_item = item_reload_callback
            self.raw_data = database.fetch_data(sql_commands.get_inventory_info, (f'{item_info[0]}',))[0]
            temp=[]
            for i in range(len(self.raw_data)):
                print(self.raw_data[i])
                temp.append(self.raw_data[i])
                '''if i == 1 : 
                    temp.append('') 
                    continue'''
            self.load_data(raw_data=temp)
            del temp
            
            return super().place(**kwargs)
        
    return instance(master, info)