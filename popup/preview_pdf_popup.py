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
import calendar
#from constants import *
#from customcustomtkinter import customcustomtkinter as cctk
from datetime import datetime

from tkPDFViewer import tkPDFViewer as pdf
#region README
r'''
goto
C:\Users\username\AppData\Local\Programs\Python\Python311\Lib\site-packages\tkPDFViewer\tkPDFViewer.py
change def ShowPdf() to this - >

class ShowPdf():

    img_object_li = []

    def pdf_view(self,master,width=1200,height=600,pdf_location="",bar=True,load="after",zoomDPI=72):

        self.frame = Frame(master,width= width,height= height,bg="white")

        scroll_y = Scrollbar(self.frame,orient="vertical")
        scroll_x = Scrollbar(self.frame,orient="horizontal")

        scroll_x.pack(fill="x",side="bottom")
        scroll_y.pack(fill="y",side="right")

        percentage_view = 0
        percentage_load = StringVar()

        if bar==True and load=="after":
            self.display_msg = Label(textvariable=percentage_load)
            self.display_msg.pack(pady=10)

            loading = Progressbar(self.frame,orient= HORIZONTAL,length=100,mode='determinate')
            loading.pack(side = TOP,fill=X)

        self.text = Text(self.frame,yscrollcommand=scroll_y.set,xscrollcommand= scroll_x.set,width= width,height= height)
        self.text.pack(side="left")

        scroll_x.config(command=self.text.xview)
        scroll_y.config(command=self.text.yview)


        def add_img():
            precentage_dicide = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                pix = page.get_pixmap(dpi=zoomDPI)
                pix1 = fitz.Pixmap(pix,0) if pix.alpha else pix
                img = pix1.tobytes("ppm")
                timg = PhotoImage(data = img)
                self.img_object_li.append(timg)
                if bar==True and load=="after":
                    precentage_dicide = precentage_dicide + 1
                    percentage_view = (float(precentage_dicide)/float(len(open_pdf))*float(100))
                    loading['value'] = percentage_view
                    percentage_load.set(f"Please wait!, your pdf is loading {int(math.floor(percentage_view))}%")
            if bar==True and load=="after":
                loading.pack_forget()
                self.display_msg.pack_forget()

            for i in self.img_object_li:
                self.text.image_create(END,image=i)
                self.text.insert(END,"\n\n")
            self.text.configure(state="disabled")

for functioning 'zoom' level and preview
'''

#endregion
    
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

    filename = f'image\\sample.pdf'
    
    pdf = SimpleDocTemplate(
        filename=filename,
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
    input2 = open(filename, "rb")
    
    # add the first 3 pages of input1 document to output
    merger.append(input2)
    # Write to an output PDF document
    output = open(filename, "wb")
    merger.write(output)
    # Close File Descriptors
    merger.close()
    output.close()
    #add footer
    p1 = pdfrw1(filename)

    writer = pdfrw2()
    writer.write(filename, p1)

    #region none sample
    
    current_month = datetime.now().strftime("%m-%Y-receipts")
    current_day = datetime.now().strftime("%Y_%m_%d_")
    #region change for default path
    '''
    document_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
    newpath = f'{document_path}\\receipt\\{current_month}' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    '''
    #endregion
    newpath = f'receipt\\{current_month}' 
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    filename = f'{newpath}\\{current_day}{client_name}_{or_number}_receipt.pdf'
    
    pdf = SimpleDocTemplate(
        filename=filename,
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

    pdf.build(elems)
    #pdf compilation
    merger = PdfWriter()
    input2 = open(filename, "rb")
    
    # add the first 3 pages of input1 document to output
    merger.append(input2)
    # Write to an output PDF document
    output = open(filename, "wb")
    merger.write(output)
    # Close File Descriptors
    merger.close()
    output.close()
    #add footer
    p1 = pdfrw1(filename)

    writer = pdfrw2()
    writer.write(filename, p1)

    #endregion

class ShowPdf(pdf.ShowPdf):
    def goto(self, page):
        try:
            self.text.see(self.img_object_li[page - 1])
        except IndexError:
            if self.img_object_li:
                self.text.see(self.img_object_li[-1])
    
#region Zoom Functions
def zoom_in():
    #global variables for the widgets
    global vaas2, ctr, zoom_in_btn, zoom_out_btn, zoom_label, pdf_viewer_frame
    #count how many times zoom in, if reached endpoint disable button
    ctr += 1
    if ctr == 5:
        zoom_in_btn.configure(state = 'disabled')
    if ctr == 2:
        zoom_out_btn.configure(state = 'normal')
    #if pdf viewer exists, destroy it
    if vaas2:
        vaas2.destroy()
    zoomValue = 50 * ctr
    if zoomValue > 250:
        zoomValue = 250
    # creating object of ShowPdf from tkPDFViewer. 
    vaas1 = pdf.ShowPdf() 
    # clear the image list # this corrects the bug inside tkPDFViewer module
    vaas1.img_object_li.clear()
    # Adding pdf location and width and height. 
    zoom_label.configure(text = f'{zoomValue}%')
    vaas2=vaas1.pdf_view(pdf_viewer_frame,pdf_location = r"image\sample.pdf",zoomDPI=zoomValue) # default value for zoomDPI=72. Set higher dpi for zoom in, lower dpi for zoom out
    # Placing Pdf inside gui
    vaas2.pack()

def zoom_out():
    #global variables for the widgets
    global vaas2, ctr, zoom_label, zoom_in_btn, zoom_out_btn, pdf_viewer_frame
    #count how many times zoom in, if reached endpoint disable button
    ctr -= 1
    if ctr == 1:
        zoom_out_btn.configure(state = 'disabled')
    if ctr == 4:
        zoom_in_btn.configure(state = 'normal')
    if vaas2: # if old instance exists, destroy it first
        vaas2.destroy()
    zoomValue = 50 * ctr
    if zoomValue < 50:
        zoomValue = 50
    zoom_label.configure(text = f'{zoomValue}%')
    # creating object of ShowPdf from tkPDFViewer. 
    vaas1 = pdf.ShowPdf() 
    # clear the image list # this corrects the bug inside tkPDFViewer module
    vaas1.img_object_li.clear()
    # Adding pdf location and width and height. 
    vaas2=vaas1.pdf_view(pdf_viewer_frame,pdf_location = r"image\sample.pdf",zoomDPI=zoomValue) # default value for zoomDPI=72. Set higher dpi for zoom in, lower dpi for zoom out
    # Placing Pdf inside gui
    vaas2.pack()
#endregion

class preview_pdf_popup(ctk.CTkToplevel):
    def __init__(self, *args, fg_color: str | Tuple[str, str] | None = None,
                 #Custom Arguments
                 
                 receipt: int, ornum = None, cashier = None, client = None, pet = None, item = None, service = None, total = None, paid = None,
                 title: Optional[str] = 'Viewer', view_receipt_by_or: Optional[str] = None,
                  **kwargs,
                 ):
        super().__init__(*args, fg_color=fg_color, **kwargs)

        self.attributes('-topmost',1)
        toplvl_width = 800
        toplvl_height = 600
        position_X = (self.winfo_screenwidth()/2) - (toplvl_width/2)
        position_Y = (self.winfo_screenheight()/2) - (toplvl_height/2)


        self.title(title)
        self.geometry("%dx%d+%d+%d"%(toplvl_width,toplvl_height,position_X,position_Y))
        print(position_X)
        print(position_Y)
        self.configure(bg='white')
        global zoom_out_btn, zoom_in_btn, zoom_label, vaas2, ctr, pdf_viewer_frame
        ctr = 2
        #region add zooming function widgets
        zoom_frame = ctk.CTkFrame(self)
        zoom_frame.pack()
        zoom_out_btn = ctk.CTkButton(zoom_frame, text='-', command=zoom_out, font = ("DM Sans Medium", 14), width=30)
        zoom_out_btn.pack(side = 'left')
        zoom_label = ctk.CTkLabel(zoom_frame, fg_color='#ffffff', text = '100%', corner_radius=5)
        zoom_label.pack(side = 'left', padx = 5)
        zoom_in_btn = ctk.CTkButton(zoom_frame, text='+', command=zoom_in, font=("DM Sans Medium", 14), width=30)
        zoom_in_btn.pack(side = 'left')
        #endregion
        
        pdf_viewer_frame = ctk.CTkFrame(self)
        pdf_viewer_frame.pack()

        pdfviewer = ShowPdf()
        if receipt:
            generate_report(or_number = ornum, cashier_name = cashier, client_name = client, pet_name = pet, item_particulars = item, service_particulars = service, total_amount = total, amount_paid = paid)
        #filename='image/sample.pdf'
        vaas2 = NONE
        vaas1=pdf.ShowPdf()
        vaas1.img_object_li.clear()
        current_folder = datetime.now().strftime("%m-%Y-receipts")
        
        if view_receipt_by_or:
            
            if exists(f"receipt/{current_folder}/{view_receipt_by_or}.pdf"):
                vaas2=pdfviewer.pdf_view(pdf_viewer_frame, pdf_location=f"receipt/{current_folder}/{view_receipt_by_or}.pdf",
                                      width=100,height=50, zoomDPI=100)
                vaas2.pack()
            else:
                self.destroy()
                messagebox.showerror("File Missing", "The file you are trying to access is missing.")
                
        else:
            vaas2=pdfviewer.pdf_view(pdf_viewer_frame, pdf_location=r"image/sample.pdf",
                        width=100,height=50, zoomDPI=100)
            vaas2.pack()
        