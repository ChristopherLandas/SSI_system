import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
import tkcalendar
from Theme import Color
from util import database
from tkinter import messagebox
from constants import action
from PIL import Image
import tkinter as tk
from tkinter import ttk



def show_sales_record_info(master, info:tuple, sales_info: tuple = None, sales_content: list = None) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple, sales_info: tuple = None, sales_content: list = None):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .835, height=height*0.925, corner_radius= 0, fg_color=Color.White_Platinum)
            
            self.grid_columnconfigure(0, weight=1)
            self.grid_rowconfigure(0, weight=1)
            self.grid_propagate(0)
            
            self.receipt_icon = ctk.CTkImage(light_image=Image.open("image/receipt_icon.png"), size=(28,28))
            
            #basic inforamtion needed; measurement

            """ lbltst = ctk.CTkLabel(self, text='OR#: %s\nCashier: %s\ndate of transaction: %s' % sales_info, text_color='white')
            lbltst._label.configure(justify=ctk.LEFT, )
            lbltst.pack(anchor = 'w')

            self.treeview = cctk.cctkTreeView(self, width= width * .7, height= height *.7, column_format='/No:45-#l/Name:x-tl/Price:150-tr!50!30')
            self.treeview.pack(pady =(12, 0)) """

            #the actual frame, modification on the frame itself goes here
            
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
            self.receipt_table_frame.grid_columnconfigure(0,weight=1)
            self.receipt_table_frame.grid_rowconfigure(0, weight=1)
            
            '''TABLE SETUP'''
            self.columns = ("rec_no", "particulars","qty","unit_price", "total")
            
            self.receipt_tree = ttk.Treeview(self.receipt_table_frame, columns=self.columns, show="headings",)
           
            self.receipt_tree.heading("rec_no", text="No")
            self.receipt_tree.heading("particulars", text="Particulars")
            self.receipt_tree.heading("qty", text="Qty")
            self.receipt_tree.heading("unit_price", text="UnitPrice")
            self.receipt_tree.heading("total", text="Total")

            self.receipt_tree.column("rec_no", width=int(width*0.001),anchor="e")
            self.receipt_tree.column("particulars", width=int(width*0.4), anchor="w")
            self.receipt_tree.column("qty", width=int(width*0.085), anchor="e")
            self.receipt_tree.column("unit_price", width=int(width*0.1), anchor="e")
            self.receipt_tree.column("total", width=int(width*0.1225), anchor="e")
            
            self.receipt_tree.tag_configure("odd",background=Color.White_AntiFlash)
            self.receipt_tree.tag_configure("even",background=Color.White_Ghost)
            
            self.receipt_tree.grid(row=0, column=0, sticky="nsew")
            
            self.y_scrollbar = ttk.Scrollbar(self.receipt_table_frame, orient=tk.VERTICAL, command=self.receipt_tree.yview)
            self.receipt_tree.configure(yscroll=self.y_scrollbar.set)
            self.y_scrollbar.grid(row=0, column=1, sticky="ns")
            '''END TABLE SETUP'''
            
            '''TOTAL'''
            self.bottom_frame = ctk.CTkFrame(self.client_info_frame, fg_color="transparent")
            self.bottom_frame.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=width*0.005, pady=(height*0.007))
            
            self.receipt_total_frame = ctk.CTkFrame(self.bottom_frame, height=height*0.05, width=width*0.2, fg_color=Color.White_Lotion)
            self.receipt_total_frame.pack(side='right')
            self.receipt_total_frame.pack_propagate(0)
        
            ctk.CTkLabel(self.receipt_total_frame, text="Total: ", font=("DM Sans Medium", 14)).pack(side="left", padx=(width*0.01,width*0.0165))
            self.receipt_total_amount = ctk.CTkLabel(self.receipt_total_frame, text="₱ ---,---.--",  font=("DM Sans Medium", 16))
            self.receipt_total_amount.pack(side="right", padx=(0,width*0.01))
    return instance(master, info, sales_info, sales_content)