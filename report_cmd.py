from util import *
import sql_commands
import calendar
from tkinter import messagebox
from constants import *
import datetime

def generate_report(report_type: str, acc_name_preparator: str, date_creation: str, monthly_month: str|int, monthly_year: str|int, daily_full_date: str, file_path: str, yearly_year: str|int, master: any):
            from reportlab.graphics.shapes import Drawing, Rect, String
            from reportlab.graphics.charts.piecharts import Pie
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
            ttfFile = os.path.join('C:\Windows\Fonts', 'Times.ttf')
            pdfmetrics.registerFont(TTFont("Times-New-Roman", ttfFile))
            ttfFile = os.path.join('C:\Windows\Fonts', 'Timesbd.ttf')
            pdfmetrics.registerFont(TTFont("Times-New-Roman-Bold", ttfFile))
            #pdfmetrics.registerFont(TTFont('Times New Roman', 'TimesNewRoman.ttf'))
            months_Text = ["January", "February", "March","April","May", "June", "July", "August","September","October", "November", "December"]
            #desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
            desktop = file_path

            def round_up_to_nearest_100000(num):
                return math.ceil(num / 10000) * 10000
            
            def calculate_step_count(i: int, len_count: int = 1):
                count = round(i/len_count)
                len_div = len(str(count)[1:])
                return math.ceil(count/10 ** len_div) * 10 ** len_div
            #yearly

            if 'Yearly' == report_type:
                #start of data collection
                #get monthly_year
                y_temp = yearly_year
                months_temp = [*range(1, 13, 1)]
                monthly_data_items_temp = [database.fetch_data(sql_commands.get_items_monthly_sales_sp_temp, (s, y_temp))[0][0] or 0 for s in months_temp]
                monthly_data_service_temp = [database.fetch_data(sql_commands.get_services_monthly_sales_sp_temp, (s, y_temp))[0][0] or 0 for s in months_temp]
                #end of data collection
                #path for charts
                my_path = f'image\charts.pdf'
                #create page with letter size
                d = Drawing(612, 792)
                #get ceiling amount for bar chart
                step_val = 0
                data_max_val= 0
                for x in monthly_data_items_temp:
                    if x > data_max_val:
                        data_max_val= x
                for x in monthly_data_service_temp:
                    if x > data_max_val:
                        data_max_val= x

                data_max_val = math.ceil(data_max_val/1000) * 1000
                step_val = calculate_step_count(data_max_val, 10)

                #create bar chart
                bc = VerticalBarChart()
                bc.x = 86
                bc.y = 405
                bc.height = 270
                bc.width = 480
                bc.data = [monthly_data_items_temp , monthly_data_service_temp]
                bc.strokeColor = colors.black
                bc.groupSpacing = 10
                bc.barSpacing = 1
                #change bar color
                bc.bars[0].fillColor = colors.lightgreen
                bc.bars[1].fillColor = colors.pink
                bc.valueAxis.valueMin = 0
                bc.valueAxis.valueMax = data_max_val
                bc.valueAxis.valueStep = step_val or 1
                bc.categoryAxis.labels.fontSize = 12
                bc.categoryAxis.labels.fontName = 'Times-New-Roman'
                bc.categoryAxis.labels.boxAnchor = 'ne'
                bc.categoryAxis.labels.dx = 5
                bc.categoryAxis.labels.dy = -2
                bc.categoryAxis.labels.angle = 30
                bc.categoryAxis.categoryNames = months_Text
                #legends
                d.add(String(225,700, f'Yearly Sales Graph as of {y_temp}', fontName = 'Times-New-Roman', fontSize=16))
                d.add(String(265,280, 'Yearly Sales', fontName = 'Times-New-Roman', fontSize=16))
                d.add(Rect(120, 75, 380, 240, fillColor=colors.transparent, strokeColor=colors.gray))
                d.add(Rect(350, 350, 15, 15, fillColor=colors.pink))
                d.add(Rect(250, 350, 15, 15, fillColor=colors.lightgreen))
                d.add(String(370,350, 'Services', fontName = 'Times-New-Roman', fontSize=12))
                d.add(String(270,350, 'Items', fontName = 'Times-New-Roman', fontSize=12))
                #add barchart to drawing
                d.add(bc, '')
                #get total amount for service and items income
                total_item_income_temp = 0
                for income in monthly_data_items_temp:
                    total_item_income_temp += income
                total_service_income_temp = 0
                for income in monthly_data_service_temp:
                    total_service_income_temp += income
                total_income_temp = total_item_income_temp + total_service_income_temp
                
                #create piechart
                pc = Pie()
                pc.x = 231
                pc.y = 100
                pc.height = 150
                pc.width = 150
                pc.slices.strokeWidth=0
                pc.slices.fontSize = 16
                pc.slices.fontName = 'Times-New-Roman'
                pc.simpleLabels = 0
                pc.slices.label_simple_pointer = 1
                pc.data = [total_item_income_temp, total_service_income_temp]
                pc.labels = ['Items', 'Services']
                pc.slices[0].fillColor = colors.lightgreen
                pc.slices[1].fillColor = colors.pink
                pc.slices[1].popout = 10
                #add piechart on drawing
                d.add(pc, '')
                #create pdf
                renderPDF.drawToFile(d, my_path, '')

                #footer
                filename = f'image/footer.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter,
                )
                pdf.bottomMargin = 20
                pdf.leftMargin = 20
                pdf.rightMargin = 20
                footer_content = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 1 of 2']]
                footer_content2 = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 2 of 2']]
                table_footer = Table(footer_content)
                table_footer2 = Table(footer_content2)
                tbl_footer_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
                    #font style
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
                    ('FONTSIZE', (0, 0), (0, -1), 14),
                    ('FONTSIZE', (0, 0), (0, 0), 10),
                    #space at the bottom
                    ('TOPPADDING', (0, 0), (0, -1), 670),
                    ('RIGHTPADDING', (0, 0), (0, 0), 300),
                    ]
                )
                table_footer.setStyle(tbl_footer_style)
                table_footer2.setStyle(tbl_footer_style)
                elems = []
                elems.append(table_footer)
                elems.append(table_footer2)
                pdf.build(elems)

                #content
                filename = f'{desktop}\\{y_temp}_yearly_report.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter
                )
                #header
                report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
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

                total_item_income_temp = 0
                for income in monthly_data_items_temp:
                    total_item_income_temp += income
                total_service_income_temp = 0
                for income in monthly_data_service_temp:
                    total_service_income_temp += income
                total_income_temp = total_item_income_temp + total_service_income_temp
                #header for table columns
                yearly_report_content_temp = [[f'Yearly Sales Report as of {y_temp}'], [f'Prepared by: {acc_name_preparator}', '', f'Date: {date_creation}', ''], ['Month', 'Items', 'Services', 'Total Income']]
                #add data for table
                yearly_report_total_items_temp = 0
                yearly_report_total_services_temp = 0
                monthlength = len(monthly_data_items_temp)
                for i in range(0, monthlength):
                    yearly_report_temp_data = []
                    yearly_report_temp_data.append(months_Text[i])
                    yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i])}')
                    yearly_report_temp_data.append(f'P{format_price(monthly_data_service_temp[i])}')
                    yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i] + monthly_data_service_temp[i])}')
                    yearly_report_content_temp.append(yearly_report_temp_data)
                    yearly_report_total_items_temp += monthly_data_items_temp[i]
                    yearly_report_total_services_temp += monthly_data_service_temp[i]
                
                yearly_report_total_all_temp = yearly_report_total_items_temp + yearly_report_total_services_temp
                yearly_report_content_temp.append(["Total: ", f'P{format_price(yearly_report_total_items_temp)}', f'P{format_price(yearly_report_total_services_temp)}', f'P{format_price(yearly_report_total_all_temp)}'])
                table_content = Table(yearly_report_content_temp)

                #add table style
                tbl_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('SPAN', (0, 0), (-1, 0)),
                    ('SPAN', (0, 1), (1, 1)),
                    ('SPAN', (2, 1), (3, 1)),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
                    ('ALIGN', (0, 2), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 3), (-1, -1), 'RIGHT'),
                    ('ALIGN', (0, 2), (3, 2), 'CENTER'),
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
                merger = PdfWriter()
                input1 = open(f"image/charts.pdf", "rb")
                input2 = open(f"{desktop}\{y_temp}_yearly_report.pdf", "rb")
                # add the first 3 pages of input1 document to output

                merger.append(input2)
                merger.append(input1)
                # Write to an output PDF document
                output = open(f"{desktop}\{y_temp}_yearly_report.pdf", "wb")
                merger.write(output)
                # Close File Descriptors
                merger.close()
                output.close()
                #add footer
                from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw
                p1 = pdfrw1(f"{desktop}\{y_temp}_yearly_report.pdf")
                p2 = pdfrw1("image/footer.pdf")

                for page in range(len(p1.pages)):
                    merger = pdfrw(p1.pages[page])
                    merger.add(p2.pages[page]).render()

                writer = pdfrw2()
                writer.write(f"{desktop}\{y_temp}_yearly_report.pdf", p1)
                messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Yearly Report.", parent = master)
            
            #monthly
            if 'Monthly' == report_type:
                #start of data collection
                m_temp = months_Text.index(monthly_month)+1
                y_temp = monthly_year

                monthly_label_temp = [*range(1, calendar.monthrange(datetime.datetime.now().year, datetime.datetime.now().month)[-1]+1, 1)]
                monthly_data_items_temp2 = [database.fetch_data(sql_commands.get_items_daily_sales_sp_temp, (f'{monthly_year}-{m_temp}-{s}',))[0][0] for s in monthly_label_temp]
                monthly_data_service_temp2 = [database.fetch_data(sql_commands.get_services_daily_sales_sp_temp, (f'{monthly_year}-{m_temp}-{s}',))[0][0] for s in monthly_label_temp]

                monthly_data_items_temp = []
                monthly_data_service_temp = []

                for monthly_month in monthly_data_items_temp2:
                    if monthly_month == None:
                        monthly_data_items_temp.append(0)
                    else:
                        monthly_data_items_temp.append(monthly_month)

                for monthly_month in monthly_data_service_temp2:
                    if monthly_month == None:
                        monthly_data_service_temp.append(0)
                    else:
                        monthly_data_service_temp.append(monthly_month)

                
                monthly_label_temp = [*range(1, calendar.monthrange(datetime.datetime.now().monthly_year, int(m_temp))[-1]+1, 1)]
                monthly_label_temp2 = []
                for monthly_month in monthly_label_temp:
                    monthly_label_temp2.append(str(monthly_month))

                #full_date_temp = datetime.datetime.strptime((m_temp), '%m').strftime('%B')
                full_date_temp = months_Text[m_temp-1]

                #endstep_val
                #Charts
                my_path = f'image\charts.pdf'
                d = Drawing(612, 792)

                step_val = 1
                data_max_val = 1
                
                for x in monthly_data_items_temp:
                    if x > data_max_val:
                        data_max_val = x
                for x in monthly_data_service_temp:
                    if x > data_max_val:
                        data_max_val = x
                
                data_max_val = math.ceil(data_max_val/1000) * 1000
                step_val = calculate_step_count(data_max_val, 10)
                #calculate the step value, and the max y-axis of graph

                data5 = [monthly_data_items_temp , monthly_data_service_temp]
                bc = VerticalBarChart()
                bc.x = 86
                bc.y = 405
                bc.height = 270
                bc.width = 480
                bc.data = data5
                bc.strokeColor = colors.black
                bc.groupSpacing = 10
                bc.barSpacing = 1
                #change bar color
                bc.bars[0].fillColor = colors.lightgreen
                bc.bars[1].fillColor = colors.pink
                bc.valueAxis.valueMin = 0
                bc.valueAxis.valueMax = data_max_val
                bc.valueAxis.valueStep = step_val or 1
                bc.categoryAxis.labels.fontSize = 12
                bc.categoryAxis.labels.fontName = 'Times-New-Roman'
                bc.categoryAxis.labels.boxAnchor = 'ne'
                bc.categoryAxis.labels.dx = 5
                bc.categoryAxis.labels.dy = -2
                bc.categoryAxis.labels.angle = 0
                bc.categoryAxis.categoryNames = monthly_label_temp2
                #legends
                d.add(String(195,700, f'Monthly Sales Graph as of {full_date_temp} {y_temp}',  fontName = 'Times-New-Roman', fontSize=16))
                d.add(String(255,280, 'Monthly Sales', fontName = 'Times-New-Roman', fontSize=16))
                d.add(Rect(120, 75, 380, 240, fillColor=colors.transparent, strokeColor=colors.gray))
                d.add(Rect(350, 350, 15, 15, fillColor=colors.pink))
                d.add(Rect(250, 350, 15, 15, fillColor=colors.lightgreen))
                d.add(String(370,350, 'Services', fontName = 'Times-New-Roman', fontSize=12))
                d.add(String(270,350, 'Items', fontName = 'Times-New-Roman', fontSize=12))

                d.add(bc, '')
                
                pc = Pie()

                total_item_income_temp = 0
                for income in monthly_data_items_temp:
                    total_item_income_temp += income
                total_service_income_temp = 0
                for income in monthly_data_service_temp:
                    total_service_income_temp += income
                total_income_temp = total_item_income_temp + total_service_income_temp
                
                pc.x = 231
                pc.y = 100
                pc.height = 150
                pc.width = 150
                pc.slices.strokeWidth=0
                pc.slices.fontSize = 16
                pc.slices.fontName = 'Times-New-Roman'
                pc.simpleLabels = 0
                pc.slices.label_simple_pointer = 1
                pc.data = [total_item_income_temp, total_service_income_temp]
                pc.labels = ['Items', 'Services']
                pc.slices[0].fillColor = colors.lightgreen
                pc.slices[1].fillColor = colors.pink
                pc.slices[1].popout = 10
                d.add(pc, '')
                renderPDF.drawToFile(d, my_path, '')

                #footer
                filename = f'image/footer.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter,
                )
                pdf.bottomMargin = 20
                pdf.leftMargin = 20
                pdf.rightMargin = 20
                footer_content = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 1 of 3']]
                table_footer = Table(footer_content)
                footer_content2 = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 2 of 3']]
                table_footer2 = Table(footer_content2)
                footer_content3 = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 3 of 3']]
                table_footer3 = Table(footer_content3)
                tbl_footer_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
                    #font style
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
                    ('FONTSIZE', (0, 0), (0, -1), 14),
                    ('FONTSIZE', (0, 0), (0, 0), 10),
                    #space at the bottom
                    ('TOPPADDING', (0, 0), (0, -1), 670),
                    ('RIGHTPADDING', (0, 0), (0, 0), 300),
                    ]
                )
                table_footer.setStyle(tbl_footer_style)
                table_footer2.setStyle(tbl_footer_style)
                table_footer3.setStyle(tbl_footer_style)
                elems = []
                elems.append(table_footer)
                elems.append(table_footer2)
                elems.append(table_footer3)
                pdf.build(elems)

                #content
                filename = f'{desktop}\\{full_date_temp}_{y_temp}_monthly_report.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter
                )
                #header
                report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
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
                #header for table columns
                yearly_report_content_temp = [
                    [f'Monthly Sales Report as of {full_date_temp} {y_temp}'], [f'Prepared by: {acc_name_preparator}', '', f'Date: {date_creation}', ''], ['Day', 'Items', 'Services', 'Total Income']
                ]
                #add data for table
                yearly_report_total_items_temp = 0
                yearly_report_total_services_temp = 0
                monthlength = len(monthly_data_items_temp)
                for i in range(0, monthlength):
                    yearly_report_temp_data = []
                    yearly_report_temp_data.append(monthly_label_temp[i])
                    yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i])}')
                    yearly_report_temp_data.append(f'P{format_price(monthly_data_service_temp[i])}')
                    yearly_report_temp_data.append(f'P{format_price(monthly_data_items_temp[i] + monthly_data_service_temp[i])}')
                    yearly_report_content_temp.append(yearly_report_temp_data)
                    yearly_report_total_items_temp += monthly_data_items_temp[i]
                    yearly_report_total_services_temp += monthly_data_service_temp[i]
                
                yearly_report_total_all_temp = yearly_report_total_items_temp + yearly_report_total_services_temp
                yearly_report_content_temp.append(["Total: ", f'P{format_price(yearly_report_total_items_temp)}', f'P{format_price(yearly_report_total_services_temp)}', f'P{format_price(yearly_report_total_all_temp)}'])
                table_content = Table(yearly_report_content_temp)

                #add table style
                tbl_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('SPAN', (0, 0), (-1, 0)),
                    ('SPAN', (0, 1), (1, 1)),
                    ('SPAN', (2, 1), (3, 1)),
                    ('ALIGN', (0, 0), (0, -1), 'CENTER'),
                    ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
                    ('ALIGN', (0, 2), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 3), (-1, -1), 'RIGHT'),
                    ('ALIGN', (0, 2), (3, 2), 'CENTER'),
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
                merger = PdfWriter()
                input1 = open(f"image/charts.pdf", "rb")
                input2 = open(f"{desktop}\{full_date_temp}_{y_temp}_monthly_report.pdf", "rb")
                # add the first 3 pages of input1 document to output
                merger.append(input2)
                merger.append(input1)
                # Write to an output PDF document
                output = open(f"{desktop}\{full_date_temp}_{y_temp}_monthly_report.pdf", "wb")
                merger.write(output)
                # Close File Descriptors
                merger.close()
                output.close()
                #add footer
                from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw
                p1 = pdfrw1(f"{desktop}\{full_date_temp}_{y_temp}_monthly_report.pdf")
                p2 = pdfrw1("image/footer.pdf")

                for page in range(len(p1.pages)):
                    merger = pdfrw(p1.pages[page])
                    merger.add(p2.pages[page]).render()

                writer = pdfrw2()
                writer.write(f"{desktop}\{full_date_temp}_{y_temp}_monthly_report.pdf", p1)
                messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Monthly Report.", parent = master)

            #daily
            if 'Daily' == report_type:
                #start of data collection
                '''date_temp = 1
                if self.date_selected_label._text.startswith(self.year_option.get()):
                    date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%Y-%m-%d').strftime('%Y-%m-%d')
                else:
                    date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%Y-%m-%d')'''
                date_temp = datetime.datetime.strptime(daily_full_date, '%B %d, %Y').strftime('%Y-%m-%d')

                '''full_date_temp = 1
                if self.date_selected_label._text.startswith(self.year_option.get()):
                    full_date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%Y-%m-%d').strftime('%B %d, %Y')
                else:
                    full_date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%B %d, %Y')'''
                full_date_temp = daily_full_date

                day_date_temp = datetime.datetime.strptime(full_date_temp, '%B %d, %Y').strftime('%d')
                month_date_temp = datetime.datetime.strptime(full_date_temp, '%B %d, %Y').strftime('%B')

                data_temp = [float(database.fetch_data(sql_commands.get_items_daily_sales_sp_temp, (date_temp,))[0][0] or 0),
                             float(database.fetch_data(sql_commands.get_services_daily_sales_sp_temp, (date_temp,))[0][0] or 0)]

                m_temp = monthly_month
                y_temp = monthly_year
                #end
                #Charts
                my_path = f'image\charts.pdf'
                d = Drawing(612, 792)

                step_val = 1
                service_max = 1

                if data_temp[0] > service_max:
                    service_max = data_temp[0]
                if data_temp[1] > service_max:
                    service_max = data_temp[1]

                service_max = round_up_to_nearest_100000(service_max)
                step_val = service_max * 0.1
                step_val = round(step_val, -3)
                d.add(String(265,380, 'Daily Sales', fontName = 'Times-New-Roman', fontSize=16))
                d.add(Rect(120, 175, 380, 240, fillColor=colors.transparent, strokeColor=colors.gray))
                
                pc = Pie()
                pc.x = 231
                pc.y = 200
                pc.height = 150
                pc.width = 150
                pc.slices.strokeWidth=0
                pc.slices.fontSize = 16
                pc.slices.fontName = 'Times-New-Roman'
                pc.simpleLabels = 0
                pc.slices.label_simple_pointer = 1
                pc.data = data_temp
                pc.labels = ['Items', 'Services']
                pc.slices[0].fillColor = colors.lightgreen
                pc.slices[1].fillColor = colors.pink
                pc.slices[1].popout = 10
                d.add(pc, '')
                renderPDF.drawToFile(d, my_path, '')

                #footer
                filename = f'image/footer.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter,
                )
                pdf.bottomMargin = 20
                pdf.leftMargin = 20
                pdf.rightMargin = 20
                footer_content = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 1 of 1']]
                table_footer = Table(footer_content)
                tbl_footer_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
                    #font style
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
                    ('FONTSIZE', (0, 0), (0, -1), 14),
                    ('FONTSIZE', (0, 0), (0, 0), 10),
                    #space at the bottom
                    ('TOPPADDING', (0, 0), (0, -1), 670),
                    ('RIGHTPADDING', (0, 0), (0, 0), 300),
                    ]
                )
                table_footer.setStyle(tbl_footer_style)
                elems = []
                elems.append(table_footer)
                pdf.build(elems)

                #content
                filename = f'{desktop}\\{month_date_temp}_{day_date_temp}_{y_temp}_daily_report.pdf'
                #filename = f'{desktop}\\report_Test.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter
                )
                #header
                report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
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

                yearly_report_content_temp = [[f'Daily Sales Report as of {month_date_temp} {day_date_temp}, {y_temp}'], [f'Prepared by: {acc_name_preparator}', f'Date: {date_creation}'], ['Items', f'P{format_price(data_temp[0])}'], 
                                              ['Services', f'P{format_price(data_temp[1])}'],
                                              ['Total Income', f'P{format_price(data_temp[0] + data_temp[1])}']]
                
                inventory_report_temp = [['']]

                inventory_report_data_temp = [[f'Inventory Report as of {y_temp}'], ['Item', 'Stock', 'Status']]
                #add data for table
                for x in database.fetch_data(sql_commands.get_inventory_by_group):
                    temp_data = []
                    temp_data.append(x[0])
                    temp_data.append(x[1])
                    temp_data.append(x[4])
                    inventory_report_data_temp.append(temp_data)
                
                table_content = Table(yearly_report_content_temp)
                table_content2 = Table(inventory_report_temp)
                table_content3 = Table(inventory_report_data_temp)
                
                #add table style
                from reportlab.platypus import TableStyle
                tbl_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('SPAN', (0, 0), (-1, 0)),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                    ('ALIGN', (2, 1), (2, -2), 'LEFT'),
                    #font style
                    ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 16),
                    #space at the bottom
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('LEFTPADDING', (1, 0), (1, -1), 10),
                    ]
                )

                tbl_style2 = TableStyle(
                    [
                    #font style
                    ('FONTSIZE', (0, 0), (-1, -1), 18),
                    #space at the bottom
                    ('TOPPADDING', (0, 0), (-1, -1), 60),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 45),
                    ]
                )

                table_content.setStyle(tbl_style)
                table_content2.setStyle(tbl_style2)
                table_content3.setStyle(tbl_style)
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

                rowNumb = len(inventory_report_data_temp)
                for i in range(1, rowNumb):
                    if i % 2 == 0:
                        bc = colors.white
                    else:
                        bc = colors.lightgrey

                    ts = TableStyle(
                        [('BACKGROUND', (0, i), (-1, i), bc)]
                    )
                    table_content3.setStyle(ts)

                #add borders
                ts = TableStyle([
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ])
                table_content.setStyle(ts)
                table_content3.setStyle(ts)
                
                ts = TableStyle([
                    ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
                ])
                table_content.setStyle(ts)
                elems = []
                elems.append(report_header)
                elems.append(table_content)
                #elems.append(table_content2)
                #elems.append(table_content3)

                pdf.build(elems)
                #pdf compilation
                merger = PdfWriter()
                input1 = open(f"image\charts.pdf", "rb")
                #input2 = open(f"{desktop}\{month_date_temp}_{day_date_temp}_{y_temp}_daily_report.pdf", "rb")
                input2 = open(filename, "rb")
                
                # add the first 3 pages of input1 document to output
                merger.append(input2)
                #merger.append(input1)
                # Write to an output PDF document
                #output = open(f"{desktop}\{month_date_temp}_{day_date_temp}_{y_temp}_daily_report.pdf", "wb")
                output = open(filename, "wb")
                merger.write(output)
                # Close File Descriptors
                merger.close()
                output.close()
                #add footer
                from pdfrw import PdfReader as pdfrw1, PdfWriter as pdfrw2, PageMerge as pdfrw
                #p1 = pdfrw1(f"{desktop}\{month_date_temp}_{day_date_temp}_{y_temp}_monthly_report.pdf")
                p1 = pdfrw1(filename)
                p2 = pdfrw1("image/footer.pdf")
                p3 = pdfrw1("image/charts.pdf")

                for page in range(len(p1.pages)):
                    merger = pdfrw(p1.pages[page])
                    merger.add(p2.pages[page]).render()

                merger = pdfrw(p1.pages[0])
                merger.add(p3.pages[0]).render()

                writer = pdfrw2()
                #writer.write(f"{desktop}\{month_date_temp}_{day_date_temp}_{y_temp}_daily_report.pdf", p1)
                writer.write(filename, p1)
                messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Daily Report.", parent = master)

                #Inventory Report
                '''
                #start of data collection
                date_temp = 1
                if self.date_selected_label._text.startswith(self.year_option.get()):
                    date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%Y-%m-%d').strftime('%Y-%m-%d')
                else:
                    date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%Y-%m-%d')

                full_date_temp = 1
                if self.date_selected_label._text.startswith(self.year_option.get()):
                    full_date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%Y-%m-%d').strftime('%B %d, %Y')
                else:
                    full_date_temp = datetime.datetime.strptime(self.date_selected_label._text, '%B %d, %Y').strftime('%B %d, %Y')

                day_date_temp = datetime.datetime.strptime(full_date_temp, '%B %d, %Y').strftime('%d')
                month_date_temp = datetime.datetime.strptime(full_date_temp, '%B %d, %Y').strftime('%B')

                data_temp = [float(database.fetch_data(sql_commands.get_items_daily_sales_sp_temp, (date_temp,))[0][0] or 0),
                             float(database.fetch_data(sql_commands.get_services_daily_sales_sp_temp, (date_temp,))[0][0] or 0)]

                m_temp = self.month_option.get()
                y_temp = self.year_option.get()
                #end
                
                #footer
                filename = f'image/footer.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter,
                )
                pdf.bottomMargin = 20
                pdf.leftMargin = 20
                pdf.rightMargin = 20
                footer_content = [['Dr. Joseph Z. Angeles Veterinary Clinic', 'Page 1 of 1']]
                table_footer = Table(footer_content)
                tbl_footer_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('ALIGN', (0, 1), (0, 1), 'RIGHT'),
                    #font style
                    ('FONTNAME', (0, 0), (-1, -1), 'Times-New-Roman'),
                    ('FONTSIZE', (0, 0), (0, -1), 14),
                    ('FONTSIZE', (0, 0), (0, 0), 10),
                    #space at the bottom
                    ('TOPPADDING', (0, 0), (0, -1), 670),
                    ('RIGHTPADDING', (0, 0), (0, 0), 300),
                    ]
                )
                table_footer.setStyle(tbl_footer_style)
                elems = []
                elems.append(table_footer)
                pdf.build(elems)

                #content
                filename = f'{desktop}/{month_date_temp}_{day_date_temp}_{y_temp}_inventory_report.pdf'
                pdf = SimpleDocTemplate(
                    filename=filename,
                    pagesize=letter
                )
                #header
                report_header_temp = [['Dr. Joseph Z. Angeles Veterinary Clinic'],
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

                inventory_report_data_temp = [[f'Inventory Report as of {month_date_temp} {day_date_temp}, {y_temp}'], [f'Prepared by: {acc_name_preparator}', f'Date: {date_creation}'], ['Item', 'Stock', 'Status']]
                #add data for table
                for x in database.fetch_data(sql_commands.get_inventory_by_group):
                    temp_data = []
                    temp_data.append(x[0])
                    temp_data.append(x[1])
                    temp_data.append(x[4])
                    inventory_report_data_temp.append(temp_data)
                table_content = Table(inventory_report_data_temp)
                
                #add table style
                tbl_style = TableStyle(
                    [
                    #text alignment, starting axis, -1 = end
                    ('SPAN', (0, 0), (-1, 0)),
                    ('SPAN', (1, 1), (2, 1)),
                    ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                    ('ALIGN', (0, 1), (0, -1), 'LEFT'),
                    ('ALIGN', (1, 1), (1, -1), 'RIGHT'),
                    ('ALIGN', (2, 1), (2, -2), 'LEFT'),
                    #font style
                    ('FONTNAME', (0, 0), (0, 0), 'Times-New-Roman-Bold'),
                    ('FONTNAME', (0, 1), (-1, -1), 'Times-New-Roman'),
                    ('FONTSIZE', (0, 0), (-1, -1), 16),
                    #space at the bottom
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
                    ('LEFTPADDING', (1, 0), (1, -1), 10),
                    ]
                )

                tbl_style2 = TableStyle(
                    [
                    #font style
                    ('FONTSIZE', (0, 0), (-1, -1), 18),
                    #space at the bottom
                    ('TOPPADDING', (0, 0), (-1, -1), 60),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 45),
                    ]
                )

                table_content.setStyle(tbl_style)
                #alternate background color

                rowNumb = len(inventory_report_data_temp)
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
                
                ts = TableStyle([
                    ('ALIGN', (0, 1), (-1, 1), 'LEFT'),
                ])
                table_content.setStyle(ts)
                elems = []
                elems.append(report_header)
                elems.append(table_content)
                pdf.build(elems)
                #pdf compilation
                
                #add footer
                p1 = pdfrw1(f"{desktop}/{month_date_temp}_{day_date_temp}_{y_temp}_inventory_report.pdf")
                p2 = pdfrw1("image/footer.pdf")

                for page in range(len(p1.pages)):
                    merger = pdfrw(p1.pages[page])
                    merger.add(p2.pages[page]).render()

                writer = pdfrw2()
                writer.write(f"{desktop}/{month_date_temp}_{day_date_temp}_{y_temp}_inventory_report.pdf", p1)
                messagebox.showinfo(title="Generate PDF Report", message="Succesfully Generated Inventory Report.")
                '''
# the file itself is currently in no use and obsolete