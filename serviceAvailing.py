from typing import Tuple
import customtkinter as ctk
from typing import *
import datetime
from Theme import Color
from PIL import Image
from customcustomtkinter import customcustomtkinter as cctk
from tkinter import messagebox
from util import database
from util import *
from popup import service_popup


class pet_info_frame(ctk.CTkFrame):
    def __init__(self, master: any, title:str, name_select_callback: callable, name_selection:list = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        #self.pack_propagate(0)
        self._master = master
        self._title = title
        self._corner_radius = 0
        self._fg_color= Color.White_Lotion
        self.grid_columnconfigure(0, weight=1)
        self.name_select_callback = name_select_callback
        
        self.pholder = ctk.CTkImage(light_image=Image.open("image/pholder.png"), size=(100,100))
        self.calendar= ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(18,18))
        
        ctk.CTkFrame(self, height=height*0.0085, fg_color=Color.Blue_Yale, corner_radius=0).grid(row=0, column=0, sticky="nsew")
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,)
        self.main_frame.grid(row =1, column=0, sticky ="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.main_frame, text = title.title(), font=('DM Sans Medium', 14), fg_color=Color.White_Platinum, corner_radius=5, 
                     width=width*0.085, height=height*0.055).grid(row=0, column=0, padx=(width*0.005), pady=(width*0.005), sticky="n")
        
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.info_frame.grid(row = 0, column=1, padx=(0, width*0.005), pady=(width*0.005), sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure((1), weight=1)
        
        #ctk.CTkLabel(self.info_frame, text="", image="").grid(row=0,column=0, rowspan=2, sticky="nsew",padx=(width*0.05,width*0.0015), pady=(height*0.05))
        self.sub_frame =ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.sub_frame.grid(row=0, column=1, sticky="nsew", padx=width*0.005, pady=(width*0.005))
        self.sub_frame.grid_columnconfigure((1), weight=1)
        ctk.CTkLabel(self.sub_frame, text =f'Name: ', font=("DM Sans Medium",14), anchor='e', width=width*0.025).grid(row=0, column=0,sticky="nsew", padx=(width*0.005,0))
        self.name = ctk.CTkOptionMenu(self.sub_frame, values= name_selection or None, font=("DM Sans Medium", 14), width=width*0.185, height=height*0.055, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Lotion,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts,)
        self.name.configure(command = lambda _: name_select_callback(self, self.name.get()))
        self.name.grid(row=0, column=1, columnspan=2, sticky="nsew", pady=(0))
        self.name.set('')
        
        ctk.CTkLabel(self.sub_frame, text =f'Date: ', font=("DM Sans Medium",14), anchor='e', width=width*0.025).grid(row=1, column=0,sticky="nsew", padx=(width*0.005,0))
        self.first_date_entry = ctk.CTkLabel(self.sub_frame, width=width*0.185,  height=height*0.055, text="Set Date", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5)
        self.first_date_entry.grid(row=1, column=1, sticky="nsew", pady=(width*0.005,0)) 
        
        self.first_date_scheduler = service_popup.calendar_with_scheduling(master.master.master.master.master.master, (width, height), self.first_date_entry, date_format= 'word')

        self.first_date_btn = ctk.CTkButton(self.sub_frame, text="", image=self.calendar, height=height*0.055, width=height*0.055,
                                            command= lambda: self.first_date_scheduler.place(relx = .5, rely = .5, anchor = 'c'))
        #                                    command=lambda:cctk.tk_calendar(self.first_date_entry, "%s", date_format="word", min_date=datetime.datetime.now()))
        self.first_date_btn.grid(row=1,column=2, sticky="w", pady=(width*0.005,0))
        #enable this part when service requires multiple days
        
    '''functions'''
    def get_data(self, data_format: Literal['metadata', 'tuple']) -> dict | list:
        if data_format == 'metadata':
            return {'name': self.name.get(), 'schedule': self.date.get()}
        elif data_format == 'tuple':
            #d_temp = None if self.first_date_entry._text == "Set Date" else datetime.datetime.strptime(self.first_date_entry._text, "%B %d, %Y").strftime('%Y-%m-%d')
            d_temp = None if self.first_date_entry._text == "Set Date" else datetime.datetime.strptime(self.first_date_entry._text, "%B %d, %Y").strftime('%Y-%m-%d')
            return (self.name.get(), d_temp)
        
class pet_period_info_frame(ctk.CTkFrame):
    def __init__(self, master: any, title:str, name_select_callback: callable, name_selection:list = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self._title = title
        self._corner_radius = 0
        self._fg_color= Color.White_Lotion
        self.grid_columnconfigure(0, weight=1)
        self.name_select_callback = name_select_callback
        
        self.pholder = ctk.CTkImage(light_image=Image.open("image/pholder.png"), size=(100,100))
        self.calendar= ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(18,18))
        
        ctk.CTkFrame(self, height=height*0.0085, fg_color=Color.Blue_Yale, corner_radius=0).grid(row=0, column=0, sticky="nsew")
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,)
        self.main_frame.grid(row =1, column=0, sticky ="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.main_frame, text = title.title(), font=('DM Sans Medium', 14), fg_color=Color.White_Platinum, corner_radius=5, 
                     width=width*0.085, height=height*0.055).grid(row=0, column=0, padx=(width*0.005), pady=(width*0.005), sticky="n")
        
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.info_frame.grid(row = 0, column=1, padx=(0, width*0.005), pady=(width*0.005), sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure((1), weight=1)
        
        #ctk.CTkLabel(self.info_frame, text="", image="").grid(row=0,column=0, rowspan=2, sticky="nsew",padx=(width*0.05,width*0.0015), pady=(height*0.05))
        self.sub_frame =ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.sub_frame.grid(row=0, column=1, sticky="nsew", padx=width*0.005, pady=(width*0.005))
        self.sub_frame.grid_columnconfigure((1), weight=1)
        ctk.CTkLabel(self.sub_frame, text =f'Name: ', font=("DM Sans Medium",14), anchor='e', width=width*0.025).grid(row=0, column=0,sticky="nsew", padx=(width*0.005,0))
        self.name = ctk.CTkOptionMenu(self.sub_frame, values= name_selection or None, font=("DM Sans Medium", 14), width=width*0.185, height=height*0.055, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Lotion,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts,)
        self.name.configure(command = lambda _: name_select_callback(self, self.name.get()))
        self.name.grid(row=0, column=1, columnspan=2, sticky="nsew", pady=(0))
        self.name.set('')
        
        ctk.CTkLabel(self.sub_frame, text =f'Date: ', font=("DM Sans Medium",14), anchor='e', width=width*0.025).grid(row=1, column=0,sticky="nsew", padx=(width*0.005,0))
        self.first_date_entry = ctk.CTkLabel(self.sub_frame, width=width*0.185,  height=height*0.055, text="Set Date", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5)
        self.first_date_entry.grid(row=1, column=1, sticky="nsew", pady=(width*0.005,0)) 
        
        self.first_date_scheduler = service_popup.calendar_with_scheduling(master.master.master.master.master.master, (width, height), self.first_date_entry, date_format= 'word' ,command = self.reset_second_date)

        self.first_date_btn = ctk.CTkButton(self.sub_frame, text="", image=self.calendar, height=height*0.055, width=height*0.055,
                                            command= lambda: self.first_date_scheduler.place(relx = .5, rely = .5, anchor = 'c'))
                                            #command=lambda:cctk.tk_calendar(self.first_date_entry, "%s", date_format="numerical", min_date=datetime.datetime.now()))
        self.first_date_btn.grid(row=1,column=2, sticky="w", pady=(width*0.005,0))
        #enable this part when service requires multiple days
        ctk.CTkLabel(self.sub_frame, text ="up to", font=("DM Sans Medium",14), width=width*0.015).grid(row=2, column=1,sticky="nsew")
        self.second_date_entry = ctk.CTkLabel(self.sub_frame, width=width*.185,  height=height*0.055, text="Set Date", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5)
        self.second_date_entry.grid(row=3, column=1, sticky="nsew", pady=(width*0.005,0)) 
        self.second_date_scheduler = service_popup.calendar_with_scheduling(master.master.master.master.master.master, (width, height), self.second_date_entry, date_format= 'word')
        
        self.second_date_btn = ctk.CTkButton(self.sub_frame, text="", image=self.calendar, height=height*0.055, width=height*0.055,
                                            command= lambda: self.second_date_scheduler.place(relx = .5, rely = .5, anchor = 'c', date = self.first_date_scheduler.cal.get_date()))
                                            #command=lambda:cctk.tk_calendar(self.second_date_entry, "%s", date_format="numerical", min_date=datetime.datetime.strptime(self.first_date_entry._text, '%m-%d-%Y') if not self.first_date_entry._text.startswith("Set") else datetime.datetime.now()))
        self.second_date_btn.grid(row=3,column=2, sticky="w", pady=(width*0.005,0))
        
    '''functions'''
    def get_data(self, data_format: Literal['metadata', 'tuple']) -> dict | list:
        if data_format == 'metadata':
            return {'name': self.name.get(), 'schedule': self.date.get()}
        elif data_format == 'tuple':
            d_temp = None if self.first_date_entry._text == "Set Date" else datetime.datetime.strptime(self.first_date_entry._text, "%B %d, %Y").strftime('%Y-%m-%d')
            dt_temp = None if self.second_date_entry._text == "Set Date" else datetime.datetime.strptime(self.second_date_entry._text, "%B %d, %Y").strftime('%Y-%m-%d')
            return (self.name.get(), d_temp, dt_temp)
    
    def reset_second_date(self):
        self.second_date_entry.configure(Text = "Set Date")
        
class pet_multiple_period_info_frame(ctk.CTkFrame):
    def __init__(self, master: any, title:str, name_select_callback: callable, name_selection:list = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self._title = title
        self._corner_radius = 0
        self._fg_color= Color.White_Platinum
        self.grid_columnconfigure(0, weight=1)
        self.name_select_callback = name_select_callback
        
        self.pholder = ctk.CTkImage(light_image=Image.open("image/pholder.png"), size=(100,100))
        self.calendar= ctk.CTkImage(light_image=Image.open("image/calendar.png"), size=(18,18))
        
        ctk.CTkFrame(self, height=height*0.0085, fg_color=Color.Blue_Yale, corner_radius=0).grid(row=0, column=0, sticky="nsew")
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion,)
        self.main_frame.grid(row =1, column=0, sticky ="nsew")
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.main_frame, text = title.title(), font=('DM Sans Medium', 14), fg_color=Color.White_Platinum, corner_radius=5, 
                     width=width*0.085, height=height*0.055).grid(row=0, column=0, padx=(width*0.005), pady=(width*0.005), sticky="n")
        
        self.info_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.info_frame.grid(row = 0, column=1, padx=(0, width*0.005), pady=(width*0.005), sticky="nsew")
        self.info_frame.grid_rowconfigure(0, weight=1)
        self.info_frame.grid_columnconfigure((1), weight=1)
        
        #ctk.CTkLabel(self.info_frame, text="", image="").grid(row=0,column=0, rowspan=2, sticky="nsew",padx=(width*0.05,width*0.0015), pady=(height*0.05))
        self.sub_frame =ctk.CTkFrame(self.info_frame, fg_color="transparent")
        self.sub_frame.grid(row=0, column=1, sticky="nsew", padx=width*0.005, pady=(width*0.005))
        self.sub_frame.grid_columnconfigure((2), weight=1)
        ctk.CTkLabel(self.sub_frame, text =f'Name: ', font=("DM Sans Medium",14), anchor='e', width=width*0.025).grid(row=0, column=0,sticky="nsew", padx=(width*0.005,0))
        self.name = ctk.CTkOptionMenu(self.sub_frame, values= name_selection or None, font=("DM Sans Medium", 14), width=width*0.185, height=height*0.055, dropdown_fg_color=Color.White_AntiFlash,  fg_color=Color.White_Lotion,
                                                 text_color=Color.Blue_Maastricht, button_color=Color.Blue_Tufts,)
        self.name.configure(command = lambda _: name_select_callback(self, self.name.get()))
        self.name.grid(row=0, column=1, columnspan=5, sticky="nsew", pady=(0))
        self.name.set('')
        
        ctk.CTkLabel(self.sub_frame, text =f'Date: ', font=("DM Sans Medium",14), anchor='e', width=width*0.025).grid(row=1, column=0,sticky="nsew", padx=(width*0.005,0))
        self.first_date_entry = ctk.CTkLabel(self.sub_frame, width=width*0.185,  height=height*0.055, text="Set Date", font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, corner_radius=5)
        self.first_date_entry.grid(row=1, column=1, sticky="nsew", columnspan=4, pady=(width*0.005,0)) 
        
        self.first_date_scheduler = service_popup.calendar_with_scheduling(master.master.master.master.master.master, (width, height), self.first_date_entry, date_format= 'word')

        self.first_date_btn = ctk.CTkButton(self.sub_frame, text="", image=self.calendar, height=height*0.055, width=height*0.055,
                                            command= lambda: self.first_date_scheduler.place(relx = .5, rely = .5, anchor = 'c'))
                                            #command=lambda:cctk.tk_calendar(self.first_date_entry, "%s", date_format="numerical", min_date=datetime.datetime.now()))
        self.first_date_btn.grid(row=1,column=5, sticky="e", pady=(width*0.005,0))
        #enable this part when service requires multiple days
        ctk.CTkLabel(self.sub_frame, text ="Scheduled every", font=("DM Sans Medium",14)).grid(row=2, column=1, columnspan=5,sticky="nsew")
        
        self.date_config_frame = ctk.CTkFrame(self.sub_frame, fg_color='transparent', height=height*0.055, corner_radius=0)
        self.date_config_frame.grid(row=3, column=1, columnspan=5)
        
        period_sv = ctk.StringVar()
        insct_sv = ctk.StringVar()
        
        period_sv.trace_add('write', self.period_days_callback)
        insct_sv.trace_add('write', self.instance_count_callback)
        
        
        self.period_days = ctk.CTkEntry(self.date_config_frame, width=width*0.05,  height=height*0.055, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, 
                                        corner_radius=5, textvariable= period_sv, justify='right')
        self.period_days.pack(side='left',  pady=(0))
        
        ctk.CTkLabel(self.date_config_frame, text ="Days", font=("DM Sans Medium",14)).pack(side='left', pady=(0), padx = (width*0.005,0))
        
        ctk.CTkLabel(self.date_config_frame, text ="Times", font=("DM Sans Medium",14)).pack(side='right', pady=(0), padx = (0)) 
        self.instance_count_days = ctk.CTkEntry(self.date_config_frame, width=width*0.05,  height=height*0.055, font=("DM Sans Medium", 14), text_color=Color.Blue_Maastricht, fg_color=Color.White_Lotion, 
                                                corner_radius=5, textvariable= insct_sv, justify='right')
        self.instance_count_days.pack(side='right', pady=(0), padx=(0,width*0.005))
        ctk.CTkLabel(self.date_config_frame, text ="For", font=("DM Sans Medium",14), anchor='e').pack(side='right', fill='x', pady=(0),  padx = (width*0.025,width*0.005))

    '''functions'''
    def get_data(self, data_format: Literal['metadata', 'tuple']) -> dict | list:
        if data_format == 'metadata':
            return {'name': self.name.get(), 'schedule': self.date.get()}
        elif data_format == 'tuple':
            d_temp = None if self.first_date_entry._text == "Set Date" else datetime.datetime.strptime(self.first_date_entry._text, "%B %d, %Y").strftime('%Y-%m-%d')
            prd_temp = self.period_days.get()
            ins_ct = self.instance_count_days.get()
            return (self.name.get(), d_temp, prd_temp, ins_ct)
        
    def period_days_callback(self, _ = None, *__):
        txt = self.period_days.get()
        try:
            if (not str(txt[-1]).isnumeric()) or len(txt) > 15:
                self.period_days.delete(len(txt)-1, ctk.END)
        except IndexError:
            pass
    def instance_count_callback(self, _ = None, *__):
        txt = self.instance_count_days.get()
        try:
            if (not str(txt[-1]).isnumeric()) or len(txt) > 15:
                self.instance_count_days.delete(len(txt)-1, ctk.END)
        except IndexError:
            pass

class pets(ctk.CTkFrame):
    def __init__(self, master: any, length:int, title: str, pets_name: List[str], proceed_command:callable, cancel_command:callable = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.frames: List[pet_info_frame | pet_period_info_frame | pet_multiple_period_info_frame] = []
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.parent_frame_tab = None
        self._root_treeview: cctk.cctkTreeView = None
        self.parent_service_dict: dict = {}
        self._title = title
        self.service_icon = ctk.CTkImage(light_image=Image.open("image/services.png"), size=(20,20))
        #print(self._title)
        self._type = database.fetch_data("Select duration_type from service_info_test WHERE service_name = ?", (self._title, ))[0][0]
        self.change_total_val_serv_callback = None
        
        def cancel_sequence():
            if cancel_command:
                cancel_command()
            self.place_forget()

        def proceed_sequence():
            for fr in self.frames:
                if fr.name.get() == "" or fr.first_date_entry._text == "Set Date":
                    messagebox.showerror("Fail to proceed", "Fill all the required info", parent = self)
                    return
                if isinstance(fr, pet_period_info_frame):
                    temp: pet_period_info_frame = fr
                    if temp.second_date_entry._text == "Set Date":
                        messagebox.showerror("Fail to proceed", "Fill all the required info", parent = self)
                        return
                elif isinstance(fr, pet_multiple_period_info_frame):
                    temp: pet_multiple_period_info_frame = fr
                    if temp.period_days.get() == "" or temp.instance_count_days.get() == "":
                        messagebox.showerror("Fail to proceed", "Fill all the required info", parent = self)
                        return
            #for checking the missing informattion like patient, date, etc.

            original_price = price_format_to_float(self.parent_frame_tab.winfo_children()[1]._text[1:])
            previous_price = price_format_to_float(self.parent_frame_tab.winfo_children()[3]._text[1:])
            total_price_lbl = self.parent_frame_tab.winfo_children()[3]
            #referring to the intialprice of the system
            
            quan_list: list = []
            for temp_data in self.get_data():
                if self._type == 1:
                    print(temp_data)
                    d2 = datetime.datetime.strptime(temp_data[2], '%Y-%m-%d')
                    d1 = datetime.datetime.strptime(temp_data[1], '%Y-%m-%d')
                    quan_list.append(((d2-d1).days + 1))
                elif self._type == 2:
                    count_intsc = temp_data[-1]
                    quan_list.append(count_intsc)

            if self._type != 0:
                frame_spinner: cctk.cctkSpinnerCombo = self.parent_frame_tab.winfo_children()[2].winfo_children()[0]
                modified_price = sum([int(s) for s in quan_list])

                def new_frame_spn_cmd():
                    if self._title in self.parent_service_dict:
                        self.parent_service_dict[self._title] = self.parent_service_dict[self._title][0: frame_spinner.value]
                
                def decrease_callback():
                    self.change_total_val_serv_callback(-(float(quan_list[-1]) * original_price))
                    quan_list.pop()
                    total_price_lbl.configure(text = f"₱{format_price(float(original_price) * sum([float(s) for s in quan_list]))}")
                    data = self._root_treeview._data[self._root_treeview.data_frames.index(self.parent_frame_tab)]
                    self._root_treeview._data[self._root_treeview.data_frames.index(self.parent_frame_tab)] = (data[0], data[1], data[2], total_price_lbl._text)


                def increase_callback():
                    quan_list.append(0)

                frame_spinner.configure(command = new_frame_spn_cmd, decrease_callback = decrease_callback, increase_callback = increase_callback)
                        
                total_price_lbl.configure(text = f"₱{format_price(float(original_price) * modified_price)}", fg_color = 'yellow')
                data = self._root_treeview._data[self._root_treeview.data_frames.index(self.parent_frame_tab)]
                self._root_treeview._data[self._root_treeview.data_frames.index(self.parent_frame_tab)] = (data[0], data[1], data[2], total_price_lbl._text)
                self.change_total_val_serv_callback(-previous_price)
                self.change_total_val_serv_callback(price_format_to_float(total_price_lbl._text[1:]))

            proceed_command(self.get_data())
            self.place_forget()
            
        def update_frames_selection(sender: ctk.CTkOptionMenu, to_remove: str) -> None:
            pet_copy = pets_name.copy()

            for fr in self.frames:
                pet_name = fr.get_data('tuple')
                if pet_name[0] in pet_copy:
                    pet_copy.pop(pet_copy.index(pet_name[0]))

            for fr in self.frames:
                fr.name.configure(values = pet_copy)
        #manage the selection of each patient frames to prevent duplicate pets 

        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color=Color.White_Lotion, width=width*0.45,  height=height*0.85, border_color=Color.White_Platinum, border_width=1)
        self.main_frame.grid(row=0, column=0)
        self.main_frame.grid_propagate(0)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        self.top_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.Blue_Yale, corner_radius=0, height=height*0.085)
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=(1), pady=(1,0))
        
        ctk.CTkLabel(self.top_frame,text="", image=self.service_icon,).pack(side="left", padx=(self._current_width*0.015,0))
        ctk.CTkLabel(self.top_frame, text = f"{self._title}", font = ("DM Sans Medium", 16), anchor='w', text_color="white").pack(side="left", padx=self._current_width * 0.005)
        ctk.CTkButton(self.top_frame, text="X",width=width*0.0225, command=cancel_sequence).pack(side="right", padx=(0,width*0.01),pady=height*0.005)
        
        self.content_frame = ctk.CTkScrollableFrame(self.main_frame, width=width*0.425,  height=height*0.675, fg_color=Color.White_Platinum)
        self.content_frame.grid(row = 1, column = 0, sticky="nsew", padx=(width*0.005), pady=(width*0.005))
        
        #content frame
        
        for _ in range(length):
            if self._type == 2:
                self.frames.append(pet_multiple_period_info_frame(self.content_frame, f'pet {_ + 1}', name_selection=pets_name, width=width, height=height, name_select_callback= update_frames_selection))
            elif self._type == 1:
                self.frames.append(pet_period_info_frame(self.content_frame, f'pet {_ + 1}', name_selection=pets_name, width=width, height=height, name_select_callback= update_frames_selection))
            elif self._type == 0:
                self.frames.append(pet_info_frame(self.content_frame, f'pet {_ + 1}', name_selection=pets_name, width=width, height=height,name_select_callback= update_frames_selection))

            self.frames[-1].pack(fill='x',side='top', pady = (0, width*0.005))
        #generate the patient info catalogs, length varies to the given length

        self.bot_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.bot_frame.grid(row = 2, column=0, sticky="nsew", padx=(width*0.005), pady=(0,width*0.005))
        
        self.cancel_btn = ctk.CTkButton(self.bot_frame, width=width*0.125, height=height*0.055, text='Cancel', command=cancel_sequence,
                                         fg_color=Color.Red_Pastel, hover_color=Color.Red_Pastel_Hover,font=("DM Sans Medium", 16))
        self.cancel_btn.pack(side="left",  padx=(width*0.005), pady=width*0.005)
        self.proceed_btn = ctk.CTkButton(self.bot_frame, width=width*0.125, height=height*0.055, text='Proceed', command= proceed_sequence, font=("DM Sans Medium", 16),)
        self.proceed_btn.pack(side="right", padx=(width*0.005), pady=width*0.005)


    '''functions'''
    def get_data(self) -> list:
        data = []
        for i in self.frames:
            data.append(i.get_data(data_format='tuple'))
        return data
    
    def place(self, service_dict: dict, root_treeview: tuple, change_total_val_serv_callback: callable, master_frame: any, master_btn: ctk.CTkButton, **kwargs):
        self.parent_frame_tab = master_frame
        self._root_treeview = root_treeview
        self.parent_service_dict = service_dict
        self.change_total_val_serv_callback = change_total_val_serv_callback
        self.master_btn = master_btn
        frame_spinner: cctk.cctkSpinnerCombo = self.parent_frame_tab.winfo_children()[2].winfo_children()[0]
        temp_cmd = frame_spinner._command

        if self._type == 0:
            def new_frame_spn_cmd():
                if self._title in service_dict:
                    service_dict[self._title] = [] if frame_spinner.value < 1 else service_dict[self._title][0: frame_spinner.value]
                temp_cmd()
            frame_spinner.configure(command = new_frame_spn_cmd)
        #for modifying the spinnercombo of the table

        if(self._title in service_dict):
            for i in range(len(service_dict[self._title])):
                self.frames[i].name.set(service_dict[self._title][i][0])
                self.frames[i].name_select_callback(self.frames[i], self.frames[i].name.get())
                d_temp = "Set Date" if service_dict[self._title][i][1] is None else datetime.datetime.strptime(service_dict[self._title][i][1], "%Y-%m-%d").strftime('%B %d, %Y')
                self.frames[i].first_date_entry.configure(text =  d_temp)

                if self._type == 1:
                    temp: pet_period_info_frame = self.frames[i]
                    snd_temp = "Set Date" if service_dict[self._title][i][2] is None else datetime.datetime.strptime(service_dict[self._title][i][2], "%Y-%m-%d").strftime('%B %d, %Y')
                    temp.second_date_entry.configure(text = snd_temp)
                elif self._type == 2:
                    temp: pet_multiple_period_info_frame = self.frames[i]
                    temp.period_days.delete(0, ctk.END)
                    temp.period_days.insert(0, service_dict[self._title][i][2])
                    temp.instance_count_days.delete(0, ctk.END)
                    temp.instance_count_days.insert(0, service_dict[self._title][i][3])
        #for reentring the elements based on the type of service
        return super().place(**kwargs)
    
    def place_forget(self):
        self.master_btn.configure(state = ctk.NORMAL)
        return super().place_forget()
    
""" class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)

        #pets1 = pets(self, 2, 'test', self.winfo_screenwidth() * .65, self.winfo_screenheight() * .65, fg_color= 'red')
        pets1 = pets(self, 2, 'grooming', ['hello', 'world'], None, None, self.winfo_screenwidth() * .65, self.winfo_screenheight() * .65, fg_color= 'red')
        pets1.place(relx = .5, rely = .5, anchor = 'c')
        
        self.mainloop() """

#body()