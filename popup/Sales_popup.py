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
from popup import preview_pdf_popup as ppdfp
from util import *

def show_sales_record_info(master, info:tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            acc_cred = info[3]
            super().__init__(master, width * .835, height=height*0.925, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            
            def reset():
                self.place_forget()
            
            def show_receipt():
                global raw_items, raw_service_info, raw_transaction_info
                #print(show_receipt)
                if self.client_name._text in r'N/A':
                    or_num = f"{self.date_label._text.replace('-', '_')}_noname_{self.or_label._text}_receipt"
                else:
                    or_num = f"{self.date_label._text.replace('-', '_')}_{self.client_name._text}_{self.or_label._text}_receipt"
                formatted_items = []
                for i in raw_items:
                    temp_items = [0, 1]
                    for it in i:
                        temp_items.append(it)
                    formatted_items.append(temp_items)
                #print(or_num)
                #ppdfp.preview_pdf_popup(receipt=0, view_receipt_by_or=f"{or_num}", title="Receipt Viewer", is_receipt=1)
                ppdfp.preview_pdf_popup(receipt=0, view_receipt_by_or=or_num, ornum=raw_transaction_info[0], cashier=raw_transaction_info[4], client=raw_transaction_info[1], pet='s[1]', item=formatted_items, service=raw_service_info, total=raw_transaction_info[2], paid=raw_transaction_info[2], title="Transaction Receipt Viewer", is_receipt=1)
            
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
            self.content_frame.grid(row=1, column=0, sticky="nsew", padx=(width*0.005), pady=(width*0.005))
            
            #CASHIER
            self.cashier_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.235)
            self.cashier_frame.pack(side="left", padx=(width*0.0045), pady=(width*0.005))
            self.cashier_frame.pack_propagate(0)
            
            ctk.CTkLabel(self.cashier_frame, text="Cashier: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.055, anchor="e").pack(side="left", padx=(width*0.0045,0))
            self.cashier_name_label = ctk.CTkLabel(self.cashier_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.cashier_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
        
            #DATE
            self.date_frame = ctk.CTkFrame(self.content_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.2)
            self.date_frame.pack(side="right", padx=(0, width*0.005), pady=(width*0.005))
            self.date_frame.pack_propagate(0)
            ctk.CTkLabel(self.date_frame, text="Transaction Date: ", fg_color="transparent", font=("DM Sans Medium", 14), width=width*0.035, anchor="e").pack(side="left", padx=(width*0.01,0))
            self.date_label = ctk.CTkLabel(self.date_frame, text="Date", font=("DM Sans Medium", 14))
            self.date_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''TRANSACTION INFO'''
            
            self.client_info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
            self.client_info_frame.grid(row=2, column=0,sticky="nsew", padx=width*0.005, pady=(0,width*0.005))
            self.client_info_frame.grid_columnconfigure(2, weight=1)
            self.client_info_frame.grid_rowconfigure(1, weight=1)
            
            #OR NUMBER 
            self.or_label = ctk.CTkLabel(self.client_info_frame, text="OR#001", fg_color=Color.White_Lotion, font=("DM Sans Medium", 14), corner_radius=5, height=height*0.05, width=width*0.115)
            self.or_label.grid(row=0, column=0, padx=(width*0.005), pady= width*0.005)
            
            #CLIENT 
            self.client_frame = ctk.CTkFrame(self.client_info_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.25)
            self.client_frame.grid(row=0, column=1, padx=(0,width*0.005), pady= width*0.005)
            self.client_frame.pack_propagate(0)
            
            self.view_receipt = ctk.CTkButton(self.client_info_frame, text="View Receipt", font=("DM Sans Medium", 14), command=show_receipt)
            self.view_receipt.grid(row=0, column=2, sticky="nse",padx=(0,width*0.005), pady= width*0.005)
            
            self.change_order_btn = ctk.CTkButton(self.client_info_frame, text="Change Order", font=("DM Sans Medium", 14), command=lambda:self.change_order.place(relx=0.5, rely=0.5, anchor='c'))
            self.change_order_btn.grid(row=0, column=3, sticky="nse",padx=(0,width*0.005), pady= width*0.005)
            
            ctk.CTkLabel(self.client_frame, text="Client: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,0))
            self.client_name = ctk.CTkLabel(self.client_frame, text="Jane Doe",  font=("DM Sans Medium", 14), fg_color="transparent")
            self.client_name.pack(side="left", fill='x', expand=1)
            
            #TABLE
            self.receipt_table_frame = ctk.CTkFrame(self.client_info_frame)
            self.receipt_table_frame.grid(row=1, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(0,width*0.005) )
           
            self.receipt_treeview = cctk.cctkTreeView(self.receipt_table_frame, width= width * .795, height= height * .7, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/Particulars:x-tl/UnitPrice:{int(width*.125)}-tr/QuantityPcs:{int(width*.115)}-tr/Total:{int(width*.125)}-tr!30!30')
            
            self.receipt_treeview.pack()
            '''TOTAL'''
            self.bottom_frame = ctk.CTkFrame(self.client_info_frame, fg_color="transparent")
            self.bottom_frame.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=width*0.005, pady=(width*0.005))
            
            self.receipt_total_frame = ctk.CTkFrame(self.bottom_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.pack(side='right')
            self.receipt_total_frame.pack_propagate(0)
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ ---,---.--",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
          
            self.labels = [self.or_label, self.client_name, self.receipt_total_amount, self.date_label, self.cashier_name_label]
        
            self.change_order = change_order(self,(width, height, acc_info, acc_cred))
            
        def set_values(self):
            [self.labels[i].configure(text=f"{self.transact_info[i]}") for i in range(len(self.labels))]     
        
        
        def place(self, sales_info, **kwargs):
            try:
                return super().place(**kwargs)
            finally:
                global raw_items, raw_service_info, raw_transaction_info
                raw_items = database.fetch_data(sql_commands.get_item_record, (sales_info[0],))
                raw_service = database.fetch_data(sql_commands.get_service_record, (sales_info[0],))
                self.transact_info = database.fetch_data(sql_commands.get_sales_record_info, (sales_info[0],))[0]  
                raw_service_info = database.fetch_data(sql_commands.get_service_record_temp, (sales_info[0],))
                raw_transaction_info = database.fetch_data(sql_commands.get_sales_record_info, (sales_info[0],))[0]      
                self.set_values()
                
                temp = [split_unit(item[0])+(item[1:]) for item in raw_items]
                items = [((f'{database.fetch_data(sql_commands.get_item_brand, database.fetch_data(sql_commands.get_uid, (temp[0], temp[1]))[0])[0][0]} {temp[0]} ({temp[1]})'),) +  temp[2:] if len(temp)==5 else 
                            ((f'{database.fetch_data(sql_commands.get_item_brand, database.fetch_data(sql_commands.get_uid_null_unit, (temp[0],))[0])[0][0]} {temp[0]}'),) +  temp[1:] for temp in temp]
                
                raw_data =  raw_service + items
                self.tree_data = [(data[0],  f"₱ {format_price(data[2])}", data[1], f"₱ {format_price(data[3])}") for data in raw_data]
                self.receipt_treeview.update_table(self.tree_data) 
            
            
    return instance(master, info)


def change_order(master, info:tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple):
            width = info[0]
            height = info[1]
            acc_info = info[2]
            super().__init__(master, width * .835, height=height*0.925, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            
            def reset():
                self.place_forget()
            
           
            self.main_frame = ctk.CTkFrame(self, corner_radius= 0, fg_color=Color.White_Lotion)
            self.main_frame.grid(row=0, column=0, sticky="nsew", padx=width*0.01, pady=height*0.0225)
            self.main_frame.grid_columnconfigure((0), weight=1)
            self.main_frame.grid_rowconfigure((1), weight=1)
            self.main_frame.grid_propagate(0)
    
            self.top_frame = ctk.CTkFrame(self.main_frame, corner_radius=0, fg_color=Color.Blue_Yale, height=height*0.05)
            self.top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
            self.top_frame.pack_propagate(0)

            ctk.CTkLabel(self.top_frame, text="", fg_color="transparent", image=self.receipt_icon).pack(side="left",padx=(width*0.01,0))
            ctk.CTkLabel(self.top_frame, text="CHANGE ORDER", text_color="white", font=("DM Sans Medium", 14)).pack(side="left",padx=width*0.005)
            self.close_btn= ctk.CTkButton(self.top_frame, text="X", height=height*0.04, width=width*0.025, command=reset)
            self.close_btn.pack(side="right", padx=width*0.005)
            
            #region Sales Table
            
            self.sales_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Test_Color_Green, corner_radius=5,)
            self.sales_frame.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=width*0.005, pady=width*0.005)
            self.sales_frame.grid_propagate(0)
            
            '''Client Frame'''
            self.client_frame = ctk.CTkFrame(self.sales_frame, fg_color=Color.Test_Color_Blue,height=height*0.055)
            self.client_frame.pack(fill='x', expand=0 ,padx=(width*0.005), pady=(width*0.005))
            
            self.or_label = ctk.CTkLabel(self.client_frame, text='', font=('DM Sans Medium', 14), fg_color=Color.White_Lotion, width=width*0.125, height=height*0.05, corner_radius=5)
            self.or_label.pack(side='left')
            
            '''Client Name Frame'''
            self.client_name_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.215)
            self.client_name_frame.pack(side="left", padx=(width*0.005), pady=(0))
            self.client_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.client_name_frame, text="Client: ", fg_color="red", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.cleint_name_label = ctk.CTkLabel(self.client_name_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.cleint_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''Date Frame'''
            self.date_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.185)
            self.date_frame.pack(side="right", expand=0, padx=(0), pady=(0))
            self.date_frame.pack_propagate(0)
            ctk.CTkLabel(self.date_frame, text="Date: ", fg_color="red", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.date_label = ctk.CTkLabel(self.date_frame, text="2023-11-01", font=("DM Sans Medium", 14))
            self.date_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''Cashier Name Frame'''
            self.cashier_name_frame = ctk.CTkFrame(self.client_frame, fg_color=Color.White_Lotion, height=height*0.05, width=width*0.215)
            self.cashier_name_frame.pack(side="right", padx=(width*0.005), pady=(0))
            self.cashier_name_frame.pack_propagate(0)
            ctk.CTkLabel(self.cashier_name_frame, text="Client: ", fg_color="red", font=("DM Sans Medium", 14), width=width*0.05, anchor="e").pack(side="left", padx=(width*0.005,0))
            self.cashier_name_label = ctk.CTkLabel(self.cashier_name_frame, text="Juan Dela Cruz", font=("DM Sans Medium", 14))
            self.cashier_name_label.pack(side="left",  fill='x', expand=1, padx=(0, width*0.005))
            
            '''Button Frame'''
            self.button_frame = ctk.CTkFrame(self.sales_frame, fg_color=Color.Test_Color_Blue,height=height*0.055)
            self.button_frame.pack(fill='x', expand=0 ,padx=(width*0.005), pady=(0,width*0.005))
            
            self.add_item_btn = ctk.CTkButton(self.button_frame, width=width*0.115, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 14), text='Add Item',
                                         )
            self.add_item_btn.pack(side="left",padx=(0,width*0.005), pady=(0))
            
            self.replace_item_btn = ctk.CTkButton(self.button_frame, width=width*0.125, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 14), text='Replaced Items(#)')
            self.replace_item_btn.pack(side="right", padx=(width*0.005,0), pady=(0))
            
            '''Treeview'''
            self.client_treeview_frame = ctk.CTkFrame(self.sales_frame, corner_radius=0,fg_color=Color.Test_Color_Red)
            self.client_treeview_frame.pack(fill='both', expand=0, padx=(width*0.005), pady=(0,width*0.005))
            
            self.client_treeview = cctk.cctkTreeView(self.client_treeview_frame, width= width*0.795, height= height*0.6, corner_radius=0,
                                           column_format=f'/No:{int(width*.035)}-#r/ItemBrand:{int(width*0.125)}-tl/ItemDescription:x-tl/UnitPrice:{int(width*.125)}-tr/QuantityPcs:{int(width*.115)}-tr/Total:{int(width*.115)}-tr!30!30')
            self.client_treeview.pack()
            
            #endregion 
    
            #region Financial Additionals
            
            self.finance_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Test_Color_Yellow, corner_radius=5, height=height*0.065)
            self.finance_frame.grid(row=3, column=0, columnspan=1, rowspan=1, sticky='nsew', padx=(width*0.005), pady=(0,width*0.005))
            
          
            
            #endregion
            
            #region Action
            
            self.action_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Test_Color_Blue, corner_radius=5, width=width*0.215, height=height*0.065)
            self.action_frame.grid(row=3, column=1, columnspan=1, sticky='nsew', padx=(0, width*0.005), pady=(0,width*0.005))
            
            self.cancel_btn = ctk.CTkButton(self.action_frame, width=width*0.085, height=height*0.05,corner_radius=5,  fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,
                                            font=("DM Sans Medium", 16), text='Cancel')
            self.cancel_btn.pack(side="left", padx=(width*0.005,0), pady=(width*0.005)) 
            
            self.add_btn = ctk.CTkButton(self.action_frame, width=width*0.115, height=height*0.05,corner_radius=5, font=("DM Sans Medium", 16), text='Change Order',
                                         )
            self.add_btn.pack(side="left",fill='x', expand=1,padx=(width*0.005), pady=(width*0.005))
            
            #endregion
        def place(self, **kwargs):
            try:
                return super().place(**kwargs)
            finally:
                pass 
                   
    return instance(master, info)