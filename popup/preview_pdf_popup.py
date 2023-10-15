from typing import *
from tkinter import*
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
import os
from tkinter import filedialog
import datetime
import re
from PIL import Image
#from util import *
#import sql_commands
import calendar
#from constants import *
#from customcustomtkinter import customcustomtkinter as cctk
from datetime import datetime

from tkPDFViewer import tkPDFViewer as pdf

#initializing tk


#main part of the program
'''
def browseFiles():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title="Select PDF file",
                                          filetype=(('PDF File','.pdf'),
                                                    ('PDF File','.PDF'),
                                                    ('ALL file','.txt')))
    
    print(filename)
    v1=pdf.ShowPdf()
    v2=v1.pdf_view(root,pdf_location=open(filename,'r'),width=77,height=100)
    v2.pack()
'''
    



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

def preview_pdf_popup(receipt: int, ornum = None, cashier = None, client = None, pet = None, item = None, service = None, total = None, paid = None):
    previewpopup = ctk.CTkToplevel()
    previewpopup.attributes('-topmost', 1)
    previewpopup.geometry('630x700+400+100')
    previewpopup.title('PDF Viewer')
    previewpopup.configure(bg='white')

    pdfviewer = ShowPdf()
    if receipt:
        generate_report(or_number = ornum, cashier_name = cashier, client_name = client, pet_name = pet, item_particulars = item, service_particulars = service, total_amount = total, amount_paid = paid)
    filename='image/sample.pdf'
    vaas2 = NONE
    vaas1=pdf.ShowPdf()
    vaas1.img_object_li.clear()
    vaas2=pdfviewer.pdf_view(previewpopup,
                   pdf_location=r"image/sample.pdf",
                   width=77,height=100)
    vaas2.pack()
    previewpopup.mainloop()
'''
    #header
    report_header_temp = [
        ['Dr. Joseph Z. Angeles Veterinary Clinic'],
        
                    ['Gov F. Halili Ave, Brgy. Gaya-gaya, San Jose Del Monte City, Bulacan'],
                    ['+ 02 774 6090']]
    report_header = Table(report_header_temp)
    tbl_header_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        #font style
        ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
        ('FONTNAME', (0, 1), (0, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (0, 0), 18),
        ('FONTSIZE', (0, 1), (0, 2), 12),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (0, 0), 20),
        ('BOTTOMPADDING', (0, 2), (0, 2), 25),
        ]
        )

    report_header.setStyle(tbl_header_style)
        #filename = f'{desktop}\\{y_temp}_yearly_report.pdf'
        

    #add table style
    tbl_style = TableStyle(
        [
        #text alignment, starting axis, -1 = end
        ('SPAN', (0, 0), (-1, 0)),
        #('SPAN', (0, 1), (1, 1)),
        #('SPAN', (2, 1), (3, 1)),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
        ('ALIGN', (0, 2), (0, -1), 'LEFT'),
        ('ALIGN', (0, 2), (0, -1), 'LEFT'),
        ('ALIGN', (1, 2), (-1, -1), 'RIGHT'),
        #font style
        ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
        ('FONTSIZE', (0, 0), (-1, -1), 16),
        #space at the bottom
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LEFTPADDING', (0, 3), (-1, -1), 10),
        ]
    )

    table_content.setStyle(tbl_style)

    #alternate background color
    rowNumb = len(yearly_report_content_temp)
    for i in range(1, rowNumb):
        if i % 2 == 0:
            bc = colors.white
        else:
            bc = colors.lightgrey

        ts = TableStyle(
            [('BACKGROUND', (0, i), (-1, i), bc)]
        )
        table_content.setStyle(ts)

    #add borders
    ts = TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])
    table_content.setStyle(ts)
    elems = []
    elems.append(report_header)
    elems.append(table_content)
    pdf.build(elems)
    #pdf compilation
    
    writer = pdfrw2()
    writer.write(f"{desktop}\{file_name}.pdf", p1)
    messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Yearly Report.")
'''

'''
def show_popup(master, info:tuple, user: str, full_name: str, position: str) -> ctk.CTkFrame:
    class add_item(ctk.CTkFrame):
        def __init__(self, master, info:tuple, user: str):
            self.DEFAULT_PATH = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Documents')
            self.CURRENT_DAY = datetime.datetime.now()
            self.DEFAULT_YEAR = [str(self.CURRENT_DAY.year)]
            self.user = user
            self.full_name = full_name
            self.position = position
            width = info[0]
            height = info[1]
            #basic inforamtion needed; measurement

            super().__init__(master,  corner_radius= 0, fg_color="#B3B3B3")
            #the actual frame, modification on the frame itself goes here
            
            '''