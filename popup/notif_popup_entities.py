from typing import *
import datetime
from typing import Callable, Optional, Tuple, Union
from customcustomtkinter import customcustomtkinter as cctk
import customtkinter as ctk
import re

from util import Callable, Optional, Tuple, Union
def create_entity(master: any,
                 notif_title: str,
                 notif_desc: str,
                 notif_date: datetime.datetime,
                 width: int = 200,
                 height: int = 200,
                 fg_color: str| tuple[str, str]= None,
                 font_sizes: Optional[Tuple[float, float, float]] = None):
    "Creates the Notif and automatically place it to the master"
    instance: notif_entity = notif_entity(master, notif_title, notif_desc, notif_date, 100, height, fg_color, font_sizes= font_sizes)
    instance.pack(fill = 'x')
    instance.update()
    text_overflow_elipsis(instance.Notif_description, width, 2)
    instance.update_children()
    return instance



class notif_entity(cctk.ctkButtonFrame):
    def __init__(self,
                 master: any,
                 notif_title: str,
                 notif_desc: str,
                 notif_date: datetime.datetime,
                 width: int = 100,
                 height: int = 200,
                 fg_color: str| tuple[str, str]= None,
                 command: Callable[[], None] | None = None,
                 hover: bool = True,
                 hover_color: str | Tuple[str, str] = "transparent",
                 text_colors: Optional[Tuple[str, str, str] | Tuple[Tuple[str, str, str], Tuple[str, str, str]]] = None,
                 fonts: Optional[Tuple[Tuple[str, int], Tuple[str, int], Tuple[str, int]]] = None,
                 font_sizes: Optional[Tuple[float, float, float]] = None,
                 **kwargs):
        "notif entity object"
        super().__init__(master, width=100, height = height, corner_radius = 0, border_width = 0, bg_color = 'transparent', fg_color = fg_color,
                         border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, command = command, hover = hover,
                         hover_color = hover_color, double_click_command = None, **kwargs)
        self._notif_title = notif_title
        self._notif_desc = notif_desc
        self._notif_date = notif_date
        self._font_sizes = font_sizes or (24, 16, 13)
        self._fonts: ctk.CTkFont = fonts or (('Arial', self._font_sizes[0]), ('Arial', self._font_sizes[1]), ('Arial', self._font_sizes[2]))
        self._text_colors = text_colors or ('black', 'black', '#777777')

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)


        #region: appearance
        self.Notif_title = ctk.CTkLabel(self, text= notif_title, fg_color='transparent', anchor='w',
                                        text_color= self._text_colors[0], font = self._fonts[0])
        self.Notif_title.grid(row = 0, column = 0, sticky = 'we', padx = (3, 0), pady = (2, 0))
        
        self.Notif_description = ctk.CTkLabel(self, text= notif_desc, fg_color='transparent', anchor='nw',
                                              text_color= self._text_colors[1], font= self._fonts[1],)
        self.Notif_description._label.configure(justify= 'left')
        self.Notif_description.grid(row = 1, column = 0, sticky = 'nsew', padx = 3, pady = 2)
        
        
        self.Notif_date_diff = ctk.CTkLabel(self, text= calculate_day(notif_date), fg_color='transparent', anchor= 'w',
                                            text_color= self._text_colors[2], font= self._fonts[2])
        self.Notif_date_diff.grid(row = 2, column = 0, sticky = 'news', padx = (3, 0))
        #endregion
    
    def pack(self, **kwargs):
        return super().pack(**kwargs)


def calculate_day(date_time: datetime.datetime, return_type: Literal['datetime', 'strform'] = 'strform') -> datetime.timedelta | str:
    time_difference = datetime.datetime.now() - date_time
    if(return_type == 'datetime'):
        return time_difference

    if time_difference >= datetime.timedelta(days=365):
        years = time_difference.days // 365
        return f'{f"{years} years" if years > 1 else "A year"} ago'
    elif time_difference >= datetime.timedelta(days=30):
        months = time_difference.days // 30
        return f'{f"{months} months" if months > 1 else "A month"} ago'
    elif time_difference >= datetime.timedelta(days=1):
        days = time_difference.days
        if(days / 7 >= 1):
            weeks = days // 7
            return(f'{f"{weeks} weeks" if weeks > 1 else "A week"} ago')
        return f'{f"{days} days" if days > 1 else "a day"} ago'
    else:
        hours = time_difference.seconds // 3600
        return f'{f"{hours} hours" if hours > 1 else "an hour"} ago'
        
def text_overflow_elipsis(lbl: ctk.CTkLabel, width: int = None, lines: int = 1, width_padding: int = 0):
    font_tool = ctk.CTkFont(lbl._font[0], lbl._font[1]) if isinstance(lbl._font, tuple) else lbl._font

    ellipsis_length:int = (font_tool.measure("..."))
    txt_dvd: list = []
    index_holder: int = 0
    for i in range(lines):
        txt: str = ""
        if i == lines - 1:
            for _ in range(index_holder, len(lbl._text)):
                if font_tool.measure(txt + lbl._text[i]) < ((lbl._current_width if width is None else width) - ellipsis_length - width_padding):
                    txt += lbl._text[index_holder]
                    index_holder += 1
                else:
                    txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}...")
                    break
        else:
            for _ in range(index_holder, len(lbl._text)):
                if font_tool.measure(txt + lbl._text[i]) < ((lbl._current_width if width is None else width) - width_padding):
                    try:    
                        if lbl._text[index_holder] == " ":
                            temp: str = re.findall(r'(\w+) ', lbl._text[index_holder:])[0]
                            if(font_tool.measure(" " + txt + temp) > ((lbl._current_width if width is None else width) - width_padding)):
                                txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                                break
                        if lbl._text[index_holder] == "\n":
                            txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                        txt += lbl._text[index_holder]
                        index_holder += 1
                    except:
                        txt_dvd.append(f"{lbl._text[index_holder + 1:] if lbl._text[index_holder:].startswith(' ') else lbl._text[index_holder:]}\n")
                        break
                else:
                    txt_dvd.append(f"{txt[1:] if txt.startswith(' ') else txt}\n")
                    break
                
    lbl.configure(text = ''.join(txt_dvd))


