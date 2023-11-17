from typing import *
import datetime
from typing import Callable, Optional, Tuple, Union
from customcustomtkinter import customcustomtkinter as cctk
import customtkinter as ctk
from util import text_overflow_ellipsis as fit_to_trim
from Theme import Color, Icons

from util import Callable, Optional, Tuple, Union

class notif_entity(cctk.ctkButtonFrame):
    def __init__(self,
                 master: any,
                 notif_title: str,
                 notif_desc: str,
                 #notif_date: datetime.datetime, 
                 width: int = 100,
                 height: int = 200,
                 fg_color: str| tuple[str, str]= None,
                 command: Callable[[], None] | None = None,
                 hover: bool = False,
                 hover_color: str | Tuple[str, str] = Color.White_Platinum,
                 text_colors: Optional[Tuple[str, str, str] | Tuple[Tuple[str, str, str], Tuple[str, str, str]]] = None,
                 fonts: Optional[Tuple[Tuple[str, int], Tuple[str, int], Tuple[str, int]]] = None,
                 font_sizes: Optional[Tuple[float, float, float]] = None,
                 info_cnt: tuple | str | int = None,
                 **kwargs):
        "notif entity object"
        super().__init__(master, width= width, height = height, corner_radius = 5, border_width = 0, bg_color = 'transparent', fg_color = fg_color,
                         border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, command = command, hover = hover,
                         hover_color = hover_color, double_click_command = None, **kwargs)
        
        self.info_cnt = info_cnt
        self._notif_title = notif_title
        self._notif_desc = notif_desc
        #self._notif_date = notif_date
        self._font_sizes = font_sizes or (16, 14, 12) #In 150 scaling it is good
        self._fonts: ctk.CTkFont = fonts or (('DM Sans Medium', self._font_sizes[0]), ('DM Sans Medium', self._font_sizes[1]), ('DM Sans Medium', self._font_sizes[2]))
        self._text_colors = text_colors or (Color.Blue_Maastricht, Color.Blue_Maastricht, Color.Blue_Maastricht)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        
        icon_dict = {   'Out of stock':     Icons.get_image('inventory_out_icon', (35,35)),
                        'Item low stock':   Icons.get_image('inventory_low_icon', (35,35)),
                        'About to Expire':  Icons.get_image('inventory_nxp_icon', (35,35)),
                        'Expired stock':    Icons.get_image('inventory_exp_icon', (35,35)),
                        
                        'Near scheduled':   Icons.get_image('sched_near_icon', (35,35)),
                        'Schedule Overdue': Icons.get_image('sched_warning_icon', (35,35)),
                        'Scheduled Today':  Icons.get_image('sched_today_icon', (35,35)),
                    }
        self.icon = ctk.CTkLabel(self, fg_color= 'transparent', text='', image=icon_dict.get(notif_title), anchor='n')
        self.icon.grid(row = 0, column = 0, rowspan=2,sticky = 'nsew', padx=(10), pady=(8,0))

        self.Notif_title = ctk.CTkLabel(self, text= notif_title, fg_color='transparent', anchor='w',
                                        text_color= self._text_colors[0], font = self._fonts[0])
        self.Notif_title.grid(row = 0, column = 1, sticky = 'we', padx = (0,3), pady = (5, 0))
        
        self.Notif_description = ctk.CTkLabel(self, text= notif_desc, fg_color='transparent', anchor='w',
                                              text_color= self._text_colors[1], font= self._fonts[1])
        self.Notif_description._label.configure(justify= 'left')
        self.Notif_description.grid(row = 1, column = 1, sticky = 'we', padx = (10,5), pady = (2, 0))
        
        '''self.Notif_date_diff = ctk.CTkLabel(self, text= calculate_day(notif_date), fg_color='transparent', anchor= 'w',
                                            text_color= self._text_colors[2], font= self._fonts[2])
        self.Notif_date_diff.grid(row = 2, column = 1, sticky = 'we', padx = (3, 0), pady = (2, 0))'''

    def pack(self, **kwargs):
        return super().pack(**kwargs)

def create_entity(master: any,
                 notif_title: str,
                 notif_desc: str,
                 #notif_date: datetime.datetime, 
                 width: int = 200,
                 height: int = 200,
                 fg_color: str| tuple[str, str]= Color.White_Lotion,
                 font_sizes: Optional[Tuple[float, float, float]] = None,
                 Desc_lines: int = 2,
                 offset: float = .85,
                 info_cnt: tuple | str | int = None) -> notif_entity:
    "Creates the Notif and automatically place it to the master"

    #command = lambda: notif_info_popup(info_cnt[0], (info_cnt[1], info_cnt[2])).place(text_info = info_cnt[3])
    command = None
    instance: notif_entity = notif_entity(master, notif_title, notif_desc, width, height, fg_color, command= command, font_sizes= font_sizes, info_cnt = info_cnt)
    instance.pack(fill = 'x', pady=(3,0), padx=(3,0))
    instance.update()
    fit_to_trim(instance.Notif_description, width - height * offset, Desc_lines)
    instance.update_children()
    return instance

def notif_info_popup(master: any, info: tuple) -> ctk.CTkFrame:
    class instance(ctk.CTkFrame):
        def __init__(self, master, info:tuple,):
            width = info[0]
            height = info[1]
            super().__init__(master, width * .8, height * .8)
            self.pack_propagate(0)
            self.grid_propagate(0)

            self.label = ctk.CTkLabel(self, text = '')
            self.label.place(relx = .5, rely = .5, anchor = 'c')

            self.close_btn = ctk.CTkButton(self, text= 'close', command= self.destroy)
            self.close_btn.pack(anchor = 'ne')

        def place(self, **kwargs):
            kwargs['relx'] = .5
            kwargs['rely'] = .5
            kwargs['anchor'] = 'c'
            if 'text_info' in kwargs:
                self.label.configure(text = kwargs['text_info'])
                kwargs.pop('text_info')
            return super().place(**kwargs)
        
    return instance(master= master, info=info)

'''def calculate_day(date_time: datetime.datetime, return_type: Literal['datetime', 'strform'] = 'strform') -> datetime.timedelta | str:
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
#CURRENTLY OBSOLETE'''