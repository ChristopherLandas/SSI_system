import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
import tkcalendar
from Theme import Color
from util import database
from util import *
from tkinter import messagebox
from constants import action
from PIL import Image
import tkinter as tk
from tkinter import ttk



def show_sales_record_info(master, info:tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.925, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            
            def reset():
                self.place_forget()
                
            
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.0225)
            self.main_frame.grid_columnconfigure(0, weight=1)
            self.main_frame.grid_rowconfigure(2, weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.receipt_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="SALES RECORD", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            '''INFO PART'''
            self.content_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(height*0.01))
            
            #CASHIER
            self.cashier_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.225)
            self.cashier_frame.pack(side="left", padx=(width*0.0045), pady=(height*0.008))
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.055, anchor="e").pack(side="left", padx=(width*0.0045,0))
            self.cashier_name_label = ctk.CTkLabel(self.cashier_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.cashier_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.0045))
            
            #DATE
            self.date_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.15)
            self.date_frame.pack(side="right", padx=(0, width*0.0045), pady=(height*0.008))
            self.date_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.date_frame, text="Date: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.035, anchor="e").pack(side="left", padx=(width*0.0045,0))
            self.date_label = ctk.CTkLabel(self.date_frame, text="Date", font=("DM Sans Medium", 14))
            self.date_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.0045))
            
            '''TRANSACTION INFO'''
            
            self.client_info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=2, column=0,sticky="nsew", padx=width*0.005, pady=(0,height*0.01))
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            self.client_info_frame.grid_rowconfigure(1, weight=1)
            
            #OR NUMBER 
            self.or_label = ctk.CTkLabel(self.client_info_frame, text="OR#001", fg_color=Color.White_Lotion, font=("DM Sans Medium", 14), corner_radius=5, height=height*0.05, width=width*0.115)
            self.or_label.grid(row=0, column=0, padx=(width*0.005), pady= height*0.007)
            
            #CLIENT 
            self.client_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= height*0.007)
            self.client_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,0))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14), fg_color="transparent")
            self.client_name.pack(side="left", fill='x', expand=1)
            
            #TABLE
            self.receipt_table_frame = ctk.CTkFrame(self.client_info_frame)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(0,height*0.007) )
           
            self.receipt_treeview = cctk.cctkTreeView(self.receipt_table_frame, width= width * .795, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.025)}-#r/Particulars:x-tl/Quantity:{int(width*.1)}-tr/UnitPrice:{int(width*.125)}-tr/Total:{int(width*.125)}-tr!30!30')
            
            self.receipt_treeview.pack()
            '''TOTAL'''
            self.bottom_frame = ctk.CTkFrame(self.client_info_frame, fg_color="transparent")
            self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(height*0.007))
            
            self.receipt_total_frame = ctk.CTkFrame(self.bottom_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.pack(side='right')
            self.receipt_total_frame.pack_propagate(0)
        
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ ---,---.--",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
          
            self.labels = [self.or_label, self.client_name, self.receipt_total_amount, self.date_label, self.cashier_name_label]
        
        def set_values(self):
            [self.labels[i].configure(text=f"{self.transact_info[i]}") for i in range(len(self.labels))]     
        
        
        def place(self, sales_info, **kwargs):
            raw_items = database.fetch_data(sql_commands.get_item_record, (sales_info,))
            raw_service = database.fetch_data(sql_commands.get_service_record, (sales_info,))
            self.transact_info = database.fetch_data(sql_commands.get_sales_record_info, (sales_info,))[0]         
            self.set_values()
             
            temp =  raw_service + raw_items
            self.tree_data = [(data[0], data[1], f"₱ {format_price(data[2])}", f"₱ {format_price(data[3])}") for data in temp]
            
            self.receipt_treeview.update_table(self.tree_data) 
            
            return super().place(**kwargs)
    return instance(master, info)