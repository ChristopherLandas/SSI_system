from typing import *
from tkinter import*
import tkinter as tk
from tkinter import messagebox
from typing import Optional, Tuple, Union
import customtkinter as ctk
from os.path import exists
from tkinter import filedialog
import datetime
from PIL import Image
#from util import *
#import sql_commands
import ctypes
from Theme import Color, Icons
from functools import partial

import ctypes
from Theme import Color, Icons
from functools import partial

from datetime import datetime
import customTkPDFViewer as cpdf
scaling = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

    
def generate_report(or_number: str, cashier_name: str, client_name: str, pet_name: str, item_particulars, service_particulars, total_amount, amount_paid):
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics.charts.piecharts import Pie
    from reportlab.pdfgen.canvas import Canvas
    from datetime import datetime as datetime_temp
    from reportlab.lib import colors
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.graphics import renderPDF
    from reportlab.platypus import SimpleDocTemplate
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import Table
    from reportlab.platypus import TableStyle
    from PyPDF2 import PdfWriter, PdfReader
    import math
    import os
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw


    ttfFile = os.path.join('C:\Windows\Fonts', 'Times.ttf')
    pdfmetrics.registerFont(TTFont("Times-New-Roman", ttfFile))
    ttfFile = os.path.join('C:\Windows\Fonts', 'Timesbd.ttf')
    pdfmetrics.registerFont(TTFont("Times-New-Roman-Bold", ttfFile))
    #pdfmetrics.registerFont(TTFont('Times New Roman', 'TimesNewRoman.ttf'))
    today = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    #newpath = f'Resources\\receipt\\{current_month}'
    temp_filename = f'Resources\\receipt\\temp_receipt.pdf'
    
    pdf = SimpleDocTemplate(
        filename=temp_filename,
        pagesize=letter
    )
    #header
    receipt_header_temp = [['JOSEPH Z. ANGELES VETERINARY CLINIC'],
                    ['LIVESTOCK CONSULTANCY']]
    receipt_header = Table(receipt_header_temp)
    header_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 18),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (0, 0), -30),
        ('BOTTOMPADDING', (0, 0), (0, 1), 10),
        ('TOPPADDING', (0, 1), (0, 1), -5),
        ]
    )

    second_header_temp = [['SJDM City, Bulacan Hardware 2000 Bldg.'],
                    ['Brgy. Graceville, SJDM City, Bulacan'],
                    ['Tel.: 8994-9043'],
                    ['Cel.: 0922-976-9287 / 0927-887-0270 /'],
                    [' 0922-408-7709']]
    receipt_header2 = Table(second_header_temp)
    header2_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
        ('BOTTOMPADDING', (0, 4), (-1, 4), 15),
        ]
    )
    receipt_header.setStyle(header_style)
    receipt_header2.setStyle(header2_style)
    current_pets = []
    pet_name = None
    ctr = 0
    if not service_particulars is None:
        for p in service_particulars:
            if not p[1] in current_pets:
                current_pets.append(p[1])
        '''
        for p in service_particulars:
            if ctr > 0:
                pet_name += ', '
                pet_name += p[1]
            else:
                pet_name = p[1]
                ctr += 1
        '''
        for p in current_pets:
            if ctr > 0:
                pet_name += ', '
                pet_name += p
            else:
                pet_name = p
                ctr += 1
            
    
    receipt_content = [
        ['Statement of Account', '', f'Date: {today}', ''], 
        [f'OR#: {or_number}', '', f'Cashier: {cashier_name}', ''],
        [f'Name of Client: {client_name}', '', '', ''],
        [f'Pet Name: {pet_name}', '', '', ''],
        ['Particulars', 'Quantity', 'Unit Price', 'Amount']]
    ''',
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        ['Total:', '', '', f'{total_amount}'],
        ['Amount Paid:', '', '', f'{amount_paid}']]
    '''
    if not service_particulars is None:
        for p in service_particulars:
            receipt_content.append([f'{p[0]} - {p[1]}', '1', f'P{p[6]}', f'P{p[6]}'])
    if not item_particulars is None:
        for p in item_particulars:
            item_prc = "P{:,.2f}".format(float(p[4]))
            item_total = "P{:,.2f}".format(float(p[4])*float(p[3]))
            #receipt_content.append([p[2], p[3], p[4], float(p[4])*float(p[3])])
            receipt_content.append([p[2], p[3], item_prc, item_total])

    total_amount_price = "P{:,.2f}".format(float(total_amount))
    amount_paid_price = "P{:,.2f}".format(float(amount_paid))
    change_price = "P{:,.2f}".format(float(amount_paid)-float(total_amount))
    #receipt_content.append(['Total:', '', '', f'{total_amount}'])
    #receipt_content.append(['Amount Paid:', '', '', f'{amount_paid}'])
    #receipt_content.append(['Change:', '', '', f'{float(amount_paid)}-{float(total_amount)}'])
    receipt_content.append(['Total:', '', '', f'{total_amount_price}'])
    receipt_content.append(['Amount Paid:', '', '', f'{amount_paid_price}'])
    receipt_content.append(['Change:', '', '', f'{change_price}'])

    #add data for table
    
    table_content = Table(receipt_content)
    bc = colors.lightgrey
    #add table style
    tbl_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (2, 0), (-1, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (2, 1), (-1, 1)),
        ('SPAN', (0, 2), (-1, 2)),
        ('SPAN', (0, 3), (-1, 3)),
        ('SPAN', (0, len(receipt_content)-3), (2, len(receipt_content)-3)),
        ('SPAN', (0, len(receipt_content)-2), (2, len(receipt_content)-2)),
        ('SPAN', (0, len(receipt_content)-1), (2, len(receipt_content)-1)),
        ('BACKGROUND', (0, 4), (-1, 4), bc),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (0, len(receipt_content)-1), (0, len(receipt_content)-1), 'RIGHT'),
        ('ALIGN', (0, len(receipt_content)-2), (0, len(receipt_content)-2), 'RIGHT'),
        ('ALIGN', (0, len(receipt_content)-3), (0, len(receipt_content)-3), 'RIGHT'),
        ('ALIGN', (1, 5), (3, len(receipt_content)-1), 'RIGHT'),
        #font style
        ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
    )

    table_content.setStyle(tbl_style)
    #alternate background color
    rowNumb = len(receipt_content)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.lightgrey

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        #table_content.setStyle(ts)

    rowNumb = len(receipt_content)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.lightgrey

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )

    #add borders
    ts = TableStyle([
        ('GRID', (0, 0), (-1, 4), 0.5, colors.black),
        ('GRID', (0, len(receipt_content)-3), (-1, len(receipt_content)-1), 0.5, colors.black),
        ('BOX', (0, 5), (0, len(receipt_content)-4), 0.5, colors.black),
        ('BOX', (1, 5), (1, len(receipt_content)-4), 0.5, colors.black),
        ('BOX', (2, 5), (2, len(receipt_content)-4), 0.5, colors.black),
        ('BOX', (3, 5), (3, len(receipt_content)-4), 0.5, colors.black),
    ])
    table_content.setStyle(ts)
    
    elems = []
    elems.append(receipt_header)
    elems.append(receipt_header2)
    elems.append(table_content)

    pdf.build(elems)
    #pdf compilation
    merger = PdfWriter()
    input2 = open(temp_filename, "rb")
    
    # add the first 3 pages of input1 document to output
    merger.append(input2)
    # Write to an output PDF document
    output = open(temp_filename, "wb")
    merger.write(output)
    # Close File Descriptors
    merger.close()
    output.close()
    #add footer
    p1 = pdfrw1(temp_filename)

    writer = pdfrw2()
    writer.write(temp_filename, p1)

    #region none sample
    
    current_month = datetime.now().strftime("%m-%Y-receipts")
    current_day = datetime.now().strftime("%Y_%m_%d")
    
    newpath = f'Resources\\receipt\\{current_month}' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    new_filename = f'{newpath}\\{current_day}_{client_name}_{or_number}_receipt.pdf'
    
    pdf = SimpleDocTemplate(
        filename=new_filename,
        pagesize=letter
    )
    #header
    receipt_header_temp = [['JOSEPH Z. ANGELES VETERINARY CLINIC'],
                    ['LIVESTOCK CONSULTANCY']]
    receipt_header = Table(receipt_header_temp)
    header_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 18),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (0, 0), -30),
        ('BOTTOMPADDING', (0, 0), (0, 1), 10),
        ('TOPPADDING', (0, 1), (0, 1), -5),
        ]
    )

    second_header_temp = [['SJDM City, Bulacan Hardware 2000 Bldg.'],
                    ['Brgy. Graceville, SJDM City, Bulacan'],
                    ['Tel.: 8994-9043'],
                    ['Cel.: 0922-976-9287 / 0927-887-0270 /'],
                    [' 0922-408-7709']]
    receipt_header2 = Table(second_header_temp)
    header2_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),
        ('BOTTOMPADDING', (0, 4), (-1, 4), 15),
        ]
    )
    receipt_header.setStyle(header_style)
    receipt_header2.setStyle(header2_style)

    pet_name = None
    ctr = 0
    if not service_particulars is None:
        for p in service_particulars:
            if ctr > 0:
                pet_name += ', '
                pet_name += p[1]
            else:
                pet_name = p[1]
                ctr += 1
            
    
    receipt_content = [
        ['Statement of Account', '', f'Date: {today}', ''], 
        [f'TransactionID: {or_number}', '', f'Cashier: {cashier_name}', ''],
        [f'Client: {client_name}', '', '', ''],
        [f'Pet Name: {pet_name}', '', '', ''],
        ['Particulars', 'Quantity', 'Unit Price', 'Amount']]
    ''',
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        [' ', '', '', ''],
        ['Total:', '', '', f'{total_amount}'],
        ['Amount Paid:', '', '', f'{amount_paid}']]
    '''
    
    if not service_particulars is None:
        for p in service_particulars:
            receipt_content.append([f'{p[0]} - {p[1]}', '1', f'P{p[6]}', f'P{p[6]}'])
    if not item_particulars is None:
        for p in item_particulars:
            item_prc = "P{:,.2f}".format(float(p[4]))
            item_total = "P{:,.2f}".format(float(p[4])*float(p[3]))
            receipt_content.append([p[2], p[3], item_prc, item_total])

    total_amount_price = "P{:,.2f}".format(float(total_amount))
    amount_paid_price = "P{:,.2f}".format(float(amount_paid))
    change_price = "P{:,.2f}".format(float(amount_paid)-float(total_amount))
    receipt_content.append(['Total:', '', '', f'{total_amount_price}'])
    receipt_content.append(['Amount Paid:', '', '', f'{amount_paid_price}'])
    receipt_content.append(['Change:', '', '', f'{change_price}'])

    #add data for table
    
    table_content = Table(receipt_content)
    bc = colors.lightgrey
    #add table style
    tbl_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('SPAN', (0, 0), (1, 0)),
        ('SPAN', (2, 0), (-1, 0)),
        ('SPAN', (0, 1), (1, 1)),
        ('SPAN', (2, 1), (-1, 1)),
        ('SPAN', (0, 2), (-1, 2)),
        ('SPAN', (0, 3), (-1, 3)),
        ('SPAN', (0, len(receipt_content)-3), (2, len(receipt_content)-3)),
        ('SPAN', (0, len(receipt_content)-2), (2, len(receipt_content)-2)),
        ('SPAN', (0, len(receipt_content)-1), (2, len(receipt_content)-1)),
        ('BACKGROUND', (0, 4), (-1, 4), bc),
        ('ALIGN', (0, 1), (0, -1), 'LEFT'),
        ('ALIGN', (0, len(receipt_content)-1), (0, len(receipt_content)-1), 'RIGHT'),
        ('ALIGN', (0, len(receipt_content)-2), (0, len(receipt_content)-2), 'RIGHT'),
        ('ALIGN', (0, len(receipt_content)-3), (0, len(receipt_content)-3), 'RIGHT'),
        ('ALIGN', (1, 5), (3, len(receipt_content)-1), 'RIGHT'),
        #font style
        ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ]
    )

    table_content.setStyle(tbl_style)
    #alternate background color
    rowNumb = len(receipt_content)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.lightgrey

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        #table_content.setStyle(ts)

    rowNumb = len(receipt_content)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.lightgrey

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )

    #add borders
    ts = TableStyle([
        ('GRID', (0, 0), (-1, 4), 0.5, colors.black),
        ('GRID', (0, len(receipt_content)-3), (-1, len(receipt_content)-1), 0.5, colors.black),
        ('BOX', (0, 5), (0, len(receipt_content)-4), 0.5, colors.black),
        ('BOX', (1, 5), (1, len(receipt_content)-4), 0.5, colors.black),
        ('BOX', (2, 5), (2, len(receipt_content)-4), 0.5, colors.black),
        ('BOX', (3, 5), (3, len(receipt_content)-4), 0.5, colors.black),
    ])
    table_content.setStyle(ts)
    
    elems = []
    elems.append(receipt_header)
    elems.append(receipt_header2)
    elems.append(table_content)
    #print(elems)
    pdf.build(elems)
    #pdf compilation
    merger = PdfWriter()
    input2 = open(new_filename, "rb")
    
    # add the first 3 pages of input1 document to output
    merger.append(input2)
    # Write to an output PDF document
    output = open(new_filename, "wb")
    merger.write(output)
    # Close File Descriptors
    merger.close()
    output.close()
    #add footer
    p1 = pdfrw1(new_filename)

    writer = pdfrw2()
    writer.write(new_filename, p1)

    #endregion

class ShowPdf(cpdf.ShowPdf):
    def goto(self, page):
        try:
            self.text.see(self.img_object_li[page - 1])
        except IndexError:
            if self.img_object_li:
                self.text.see(self.img_object_li[-1])
  
class preview_pdf_popup(ctk.CTkToplevel):
    
    
    def __init__(self, *args, fg_color: str | Tuple[str, str] | None = None,
                 #Custom Arguments
                 
                 receipt: int, ornum = None, cashier = None, client = None, pet = None, item = None, service = None, total = None, paid = None,
                 title: Optional[str] = 'Viewer', view_receipt_by_or: Optional[str] = None, is_receipt: Optional[bool] = False,
                  **kwargs,
                 ):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        
        
        self.attributes('-topmost',1)
        self.view_by_reciept = view_receipt_by_or
        self.zoom_step = 10
        self.zoom_limit = 10
        self.default_dpi=100
        self.zoom_counter = 0
        window_height, window_width = self.winfo_screenheight()/scaling, (self.winfo_screenwidth()/scaling)
        self.window_width = window_width

        toplvl_width = 600
        toplvl_height = 650
        position_X = (self.winfo_screenwidth()/2) - (toplvl_width/2)
        position_Y = (window_height/2) - (toplvl_height/2)

        self.title(title)
        self.geometry("%dx%d+%d+%d"%(toplvl_width,toplvl_height,position_X,position_Y))
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Platinum, width=window_width*0.5)
        self.main_frame.pack(pady=window_width*0.005, padx=window_width*0.005)
        
        
        self.zoom_frame = ctk.CTkFrame(self.main_frame, fg_color='transparent')
        self.zoom_frame.pack()
        self.zoom_out_btn = ctk.CTkButton(self.zoom_frame, text='', image=Icons.zoom_out_icon, font = ("DM Sans Medium", 14), width=window_width*0.03, height=window_width*0.03,
                                          command=partial(self.zoom_function, -1))
        self.zoom_out_btn.pack(side = 'left', padx = (window_width*0.005), pady = (window_width*0.005, 0))
        
        self.zoom_in_btn = ctk.CTkButton(self.zoom_frame, text='', image=Icons.zoom_in_icon, font=("DM Sans Medium", 14), width=window_width*0.03, height=window_width*0.03,
                                         command=partial(self.zoom_function, 1))
        self.zoom_in_btn.pack(side = 'left', padx = (0,window_width*0.005), pady = (window_width*0.005, 0))
        
        self.zoom_reset = ctk.CTkButton(self.zoom_frame, text='', image=Icons.zoom_reset_icon,font=("DM Sans Medium", 14), width=window_width*0.03, height=window_width*0.03,
                                         command=partial(self.zoom_function, 0))
        self.zoom_reset.pack(side = 'left', padx = (0,window_width*0.005),pady = (window_width*0.005, 0))
        self.zoom_entry = ctk.CTkLabel(self.zoom_frame, fg_color=Color.White_Lotion, text = '---%',font=("DM Sans Medium", 14), height=40,
                                       width=toplvl_width*0.175, corner_radius=window_width*0.005)
        self.zoom_entry.pack(side = 'left', padx = (0,window_width*0.005), pady = (window_width*0.005, 0))
        
        
        self.pdf_viewer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.pdf_viewer_frame.pack(pady=(0, window_width*0.005), )

        self.pdfviewer = ShowPdf()
        
        self.zoom_entry.configure(text=f"{self.default_dpi}%")
        if receipt:
            generate_report(or_number = ornum, cashier_name = cashier, client_name = client, pet_name = pet, item_particulars = item, service_particulars = service, total_amount = total, amount_paid = paid)
        
        self.vaas2 = NONE
        self.vaas1=cpdf.ShowPdf()
        self.vaas1.img_object_li.clear()
        self.current_folder = datetime.now().strftime("%m-%Y-receipts")
        
        if self.view_by_reciept and is_receipt:
            if exists(f"Resources/receipt/{self.current_folder}/{self.view_by_reciept}.pdf"):
                self.vaas2= self.pdfviewer.pdf_view(self.pdf_viewer_frame, pdf_location=f"Resources/receipt/{self.current_folder}/{self.view_by_reciept}.pdf",
                                      width=80,height=100,zoomDPI=self.default_dpi)
                self.vaas2.pack(pady=window_width*0.005, padx=(window_width*0.005))
            else:
                self.destroy()
                messagebox.showerror("File Missing", "The file you are trying to access is missing.")
                
        elif not self.view_by_reciept and is_receipt:
            self.vaas2= self.pdfviewer.pdf_view(self.pdf_viewer_frame, pdf_location=r"Resources/receipt/temp_receipt.pdf",
                        width=80,height=100,zoomDPI=self.default_dpi)
            self.vaas2.pack(pady=window_width*0.005, padx=(window_width*0.005))
        else:
            self.vaas2= self.pdfviewer.pdf_view(self.pdf_viewer_frame, pdf_location=r"image/sample.pdf",
                        width=80,height=100,zoomDPI=self.default_dpi)
            self.vaas2.pack(pady=window_width*0.005, padx=(window_width*0.005))
            
    def zoom_function(self, value):
        self.zoom_counter += value
        if value == 0: self.zoom_counter = 0 
        self.zoom_state_check(zoom_dpi=max(50, ((self.zoom_counter * self.zoom_step) + self.default_dpi)))
    
    def zoom_state_check(self, zoom_dpi):
        #self.zoom_in_btn.configure(state=)
        
        self.zoom_in_btn.configure(state = 'disabled' if self.zoom_counter == self.zoom_limit else 'normal') 
        self.zoom_out_btn.configure(state = 'disabled' if self.zoom_counter == -self.zoom_limit else 'normal')
        self.zoom_entry.configure(text=f"{zoom_dpi}%")
        
        if self.vaas2: # if old instance exists, destroy it first
            self.vaas2.destroy()
         # creating object of ShowPdf from tkPDFViewer. 
        self.vaas1 = cpdf.ShowPdf() 
        # clear the image list # this corrects the bug inside tkPDFViewer module
        self.vaas1.img_object_li.clear()
        # Adding pdf location and width and height. 
        if self.view_by_reciept:
            self.vaas2= self.pdfviewer.pdf_view(self.pdf_viewer_frame, pdf_location=f"Resources/receipt/{self.current_folder}/{self.view_by_reciept}.pdf",
                                      width=80,height=100,zoomDPI=zoom_dpi)
            self.vaas2.pack(pady=self.window_width*0.005, padx=(self.window_width*0.005))
        else:
            self.vaas2=self.vaas1.pdf_view(self.pdf_viewer_frame,pdf_location = r"image\sample.pdf", zoomDPI=zoom_dpi, width=80,height=100 ) # default value for zoomDPI=72. Set higher dpi for zoom in, lower dpi for zoom out
            # Placing Pdf inside gui
            self.vaas2.pack(pady=self.window_width*0.005, padx=(self.window_width*0.005))
    
    