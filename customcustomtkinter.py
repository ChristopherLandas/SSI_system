from typing import Optional, Tuple, Union
import customtkinter as ctk
import tkinter as tk
from typing import *
from util import *
from functools import partial
from util import brighten_color
import re
from tkinter import messagebox;
from customtkinter.windows.widgets.font import CTkFont
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu
from tkcalendar import Calendar

class customcustomtkinter:
    class ctkButtonFrame(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, command: Union[Callable[[],None], None] = None,
                     hover: bool = True, hover_color: Union[str, Tuple[str, str]] = "transparent",
                     double_click_command: Union[Callable[[],None], None] = None, **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
                             background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            # sets the default properties of a frame

            self.og_color = self._fg_color
            self._hover_color = hover_color
            self._command = [] if isinstance(command, list) else [command]
            self._hover = hover
            self._doulbe_click_command = double_click_command
            #make a reference/encapsulation from extended arguments

            self.bind('<Button-1>', self.response)
            self.bind('<Double-Button-1>', None if self._doulbe_click_command == None else self._doulbe_click_command)
            self.pack_propagate(0)
            self.grid_propagate(0)
            self.update_button(hover)
            #set the property as a button

        def response(self, _):
                click_color = (brighten_color(self._hover_color[0], 1.25, brighten_color(self._hover_color[1], 1.25))) if isinstance(self._hover_color, tuple) else brighten_color(self._hover_color, 1.45)
                self.configure(fg_color = click_color)
                self.update()
                self.after(50)
                self.configure(fg_color = self._hover_color)
                for cmd in self._command:
                    if callable(cmd):
                        cmd()
        #click response of the button; includes the flash when clicked

        def update_button(self, is_hover: bool = True):
            if is_hover:
                self.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
                self.bind('<Leave>', lambda _: self.configure(fg_color = self.og_color))
            else:
                self.unbind('<Enter>', None)
                self.unbind('<Leave>', None)
        #update the frame's external properties

        def update_children(self):
            child = self.winfo_children()
            for i in child:
                i.unbind('<Button-1>', None)
                i.bind('<Button-1>', self.response)
                i.unbind('<Double-Button-1>', None)
                i.bind('<Double-Button-1>', None if self._doulbe_click_command == None else self._doulbe_click_command)
                if self._hover:
                    i.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
                    i.bind('<Leave>', lambda _: self.configure(fg_color = self.og_color))
                else:
                    i.unbind('<Enter>', None)
                    i.unbind('<Leave>', None)
        #update all the children properties to mimic the button properties

        def configure(self, require_redraw=False, command: Optional[Callable[[], None]] = None, hover: Optional[bool] = None,
                      hover_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
            if command is not None:
                self._command = [] if isinstance(command, list) else [command]
                self.unbind('<Button-1>', None)
                self.bind('<Button-1>', self.response)
                self.update_children()
            if hover_color is not None:
                self._hover_color = hover_color
                self.unbind('<Enter>', None)
                self.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
            if hover is not None:
                self._hover = hover
                self.update_button(hover)
                self.update_children()
            if 'double_click_command' in kwargs:
                self.unbind('<Double-Button-1>', None)
                self._doulbe_click_command = kwargs['double_click_command']
                self.bind('<Double-Button-1>', kwargs['double_click_command'])
                self.update_children()
                kwargs.pop('double_click_command')
            return super().configure(require_redraw, **kwargs)
        #override configure function of frame, allowing to add those external arguments
    #button frame: a frame with a properties of a buttons

    class menubar(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, position: tuple = (0, 0, 'c'), **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors,
                             overwrite_preferred_drawing_method, **kwargs)

            self._position = position
            self._shadow = ctk.CTkFrame(master, 0, 0)
            self.pack_propagate(0)
            self.grid_propagate(0)

        def place(self):
            #place shadow here
            return super().place(relx = self._position[0], rely = self._position[1], anchor = self._position[2])
        #override the place to place a shadow first

        def update_pos(self,  position: tuple = (0, 0, 'c')):
            self.deiconify()
            self._position = position
            self.place()
        #update the position, including the shadow

        def deiconify(self):
            self._shadow.place_forget()
            self.place_forget()
        #hide the menubar

    class cctkTreeView(ctk.CTkFrame):
        def __init__(self, master: any, data: Union [Union[tuple, list], None] = None, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, column_format: str = '/Title1:x-t/Title2:x-t/Title3:x-t!50!50',
                     header_color: Union[str, tuple] = '#006611', data_grid_color: Union[list, tuple] = ('#333333', '#444444'),
                     selected_color: Union [tuple, str] = brighten_color('#006611', 1.3),
                     conditional_colors: Union[dict, None] = {-1: {-1:None}}, navbar_font: tuple = ('Arial', 20),
                     row_font: tuple = ('Arial', 12), row_hover_color: Union [tuple, str] = '#2C74B3', content_color: Optional[Union[str, Tuple[str, str]]] = 'black',
                     double_click_command: Union[Callable[[],None], None] = None, record_text_color: Optional[Union[str, Tuple[str, str]]] = 'black',
                     bd_configs: Union[List[Tuple[int, Union[List[ctk.CTkLabel], ctk.CTkLabel]]], None] = None, **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors,
                             overwrite_preferred_drawing_method, **kwargs)

            if not re.fullmatch(r'(\/\w+:(x|\d+)-(\w+|\#\w+))+\!\d+\!\d+', column_format):
                ctk.CTkLabel(self, text='Wrong format\nCheck for errors').place(relx = .5, rely = .5, anchor = 'c')
                return;
            #check if the format follows the guideline, if it doesn't it will only pop a label
            self._column_format  = column_format
            self.column_titles = [s.replace('/', '') for s in re.findall(r'\/\w+', self._column_format)]
            self.column_types = [str(s) for s in re.findall(r'\-(\w+|\#\w+)', self._column_format)]
            total_fixed_width = sum([int(s) for s in re.findall(r'\:(x|\d+)', self._column_format) if str(s).isnumeric()])
            x_width = (self._current_width - (total_fixed_width + 14)) / len(re.findall(r'\:x', self._column_format))//1
            #set the measurements of the treeview according to the format given

            self.data_frames = []
            self._data = []
            self.data_grid_btn_mng = None
            self.column_widths = [x_width - 1 if s == 'x' else int(s) - 1 for s in re.findall(r'\:(x|\d+)', self._column_format)]
            self._header_heights = int(re.findall(r'\!(\d+)', column_format)[0])
            self._data_grid_heights = int(re.findall(r'\!(\d+)', column_format)[1])
            self._header_color = header_color
            self._data_grid_color = (data_grid_color[0], data_grid_color[1]) if isinstance(data_grid_color, tuple) else((data_grid_color[0][0], data_grid_color[1][0]), (data_grid_color[0][1], data_grid_color[1][1]))
            self._conditional_colors = conditional_colors
            self.navbar_font = navbar_font
            self.row_font = row_font
            self._selected_color =selected_color
            self._row_hover_color = row_hover_color
            self._double_click_command = double_click_command
            self.bd_configs = bd_configs
            self._record_text_color = record_text_color
            self._content_color = content_color
            #encapsulate other arguments

            self.pack_propagate(0)
            self.grid_propagate(0)
            self.grid_rowconfigure(1, weight=1)

            #make the root frame fixed in sizesz
            for i in range(len(self.column_titles)):
                btn = None
                if self.column_types[i] == 't' or self.column_types[i] == '#' or self.column_types[i] == 'q':
                    btn = customcustomtkinter.ctkButtonFrame(self, self.column_widths[i], self._header_heights, 0, fg_color= self._header_color,
                                                             hover_color= brighten_color(self._header_color, 1.75))
                    title = ctk.CTkLabel(btn, text=self.column_titles[i], font=self.navbar_font)
                    title.place(relx = .5, rely = .5, anchor = 'c',)
                    btn.update_children()
                else:
                    btn = ctk.CTkLabel(self, self.column_widths[i], self._header_heights, 0, fg_color= self._header_color,
                                       text=self.column_titles[i], font= self.navbar_font)
                btn.grid(row = 0, column = i, sticky='we', padx = (1,0))
                self.update()
            #generate the header bar

            self.scroll_bar_btn = customcustomtkinter.ctkButtonFrame(self, 14, self._header_heights, 0, fg_color=self._header_color,
                                                                     hover_color= brighten_color('#006611', 1.75),
                                                                     command = lambda: self.contents._parent_canvas.yview_moveto(0 if (self.contents._parent_canvas.yview()[1] > .5) else 1))
            self.scroll_bar_btn.grid(row = 0, column = len(self.column_titles), sticky='nsew')
            #additional button that will serve as go to top/down of a scroll bar

            self.contents = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color=self._content_color)
            self.contents.grid(row = 1, column = 0, columnspan = len(self.column_titles) + 1, sticky = 'news')
            #the data grid holder

            '''initial generation here'''
            if(data is not None):
                self.add_data(data)
            #generates data grid

            self.data_grid_btn_mng = customcustomtkinterutil.button_manager(self.data_frames, self._selected_color, True, None)
            #add a radio button like properties from each of the rows of the data grid

        def id_func(self, dlt_btn: ctk.CTkButton, val):
            lbl = dlt_btn.master.master.winfo_children()[self.column_types.index('q')]
            lbl.configure(text = str(int(lbl.cget('text')) + val))

        def bd_func(self, dlt_btn: ctk.CTkButton):
            confirmation = messagebox.askyesno('Warning', 'Are you sure you want to delete the data')
            if confirmation:
                data_mngr_index = self.data_grid_btn_mng._buttons.index(dlt_btn.master.master)
                self.data_grid_btn_mng._buttons.pop(data_mngr_index)
                self.data_grid_btn_mng._og_color.pop(data_mngr_index)
                #remove the row from the button manager

                if self.data_grid_btn_mng.active == dlt_btn.master.master:
                    self.data_grid_btn_mng.active = None
                #active button was set to none if it was destroyed
                if(self.bd_configs is not None):
                    self.bd_deduction(dlt_btn)

                dlt_btn.master.master.destroy()
                self._data.pop(data_mngr_index)
                for i in range(data_mngr_index, len(self.data_frames)):
                    color = self._data_grid_color[0] if i % 2 == 0 else self._data_grid_color[1]
                    self.data_grid_btn_mng._og_color[i] = color
                    self.data_frames[i].og_color = color
                    self.data_frames[i].configure(fg_color = color)
                    if '#' in str(self.column_types):
                        for j in range(len(self.column_types)):
                            if '#' in self.column_types[j]:
                                lbl: ctk.CTkLabel = self.data_frames[i].winfo_children()[j]
                                lbl.configure(text = int(lbl._text) - 1)
                    #update the number order of the frames
                #update the fg color of each of the frames, maintaining the alternating pattern

        def add_data(self, data: Union[tuple, list]):
            d = [data] if isinstance(data, tuple) else data
            for i in range(len(d)):
                tI = 0;
                frm = customcustomtkinter.ctkButtonFrame(self.contents, height=self._data_grid_heights, width=15,
                                                         fg_color=self._data_grid_color[0] if len(self.data_frames) % 2 == 0 else self._data_grid_color[1],
                                                         corner_radius= 0, hover_color= self._row_hover_color,
                                                         double_click_command= self._double_click_command)
                self.data_frames.append(frm)
                self._data.append(d[i])
                if self.data_grid_btn_mng is not None:
                    self.data_grid_btn_mng._og_color.append(frm._fg_color)
                for j in range(len(self.column_widths)):
                    #for label type column
                    if self.column_types[j][0] in ['t', '#']:
                        temp = ctk.CTkLabel(frm, text= d[i][tI] if self.column_types[j][0] == 't' else (len(self._data)), width = self.column_widths[j],
                                            justify = ctk.RIGHT, font= self.row_font, text_color = self._record_text_color)
                        txt_clr = self._record_text_color if j not in self._conditional_colors else self._conditional_colors[j].get(temp._text, self._record_text_color)
                        temp.configure(text_color = txt_clr)
                        temp._label.grid_forget()
                        temp._label.grid(row = 0, column=0, sticky='nsew', padx=(12, 12))
                        temp._label.configure(anchor= 'w' if self.column_types[j][1] == 'l' else 'e' if self.column_types[j][1] == 'r' else 'c')
                        temp.pack(side = tk.LEFT, fill = 'y', padx = (1,0))
                    #for info tab column
                    elif self.column_types[j] == 'iT':
                        temp:customcustomtkinter.info_tab = customcustomtkinter.info_tab(frm, width= self.column_widths[j], corner_radius= 0,
                                                                                         border_width=0, fg_color='transparent')
                        temp.pack(side = tk.LEFT, fill = 'y', padx = (1,0))
                        #modified_data = list(self._data[-1]).insert(j, temp.val)
                    #for special type column
                    else:
                        temp = ctk.CTkFrame(frm, width= self.column_widths[j], corner_radius= 0, border_width=0, fg_color='transparent')
                        temp.pack(side = tk.LEFT, fill = 'y', padx = (1,0))
                        if self.column_types[j] == 'bD':
                            dlt_btn = ctk.CTkButton(temp, self._data_grid_heights * .8, self._data_grid_heights * .8, fg_color='red' ,text='')
                            dlt_btn.configure(command = partial(self.bd_func, dlt_btn))
                            dlt_btn.place(relx = .5, rely = .5, anchor = 'c')
                            continue;
                        elif self.column_types[j] == 'id':
                            spinner = customcustomtkinter.cctkSpinnerCombo(temp ,step_count=1, entry_font=("Lucida", 20), bg_color='transparent', fg_color='transparent')
                            spinner.place(relx = .5, rely = .5, anchor = 'c')

                    if self.column_types[j][0] == 't':
                        tI += 1
                # generates the content from the frame

                frm.update_children()
                frm.pack(fill = 'x', pady = (1,0))
                self.contents.update()

        def update_table(self, data: Union[tuple, list]):
            for i in self.data_frames:
                i.destroy()
            self.data_frames = []
            self._data = []
            self.add_data(data)
            self.data_grid_btn_mng = customcustomtkinterutil.button_manager(self.data_frames, self._selected_color, True, None)

        def bd_deduction(self, btn: ctk.CTkButton):
            for tup in self.bd_configs:
                item = float(btn.master.master.winfo_children()[tup[0]]._text)
                if isinstance(tup[1], list):
                    for lbls in tup[1]:
                        lbls.configure(text = format_price(float(price_format_to_float(lbls._text)) - item))
                else:
                    tup[1].configure(text = format_price(float(price_format_to_float(tup[1]._text)) - item))

        def delete_all_data(self):
            for frm in self.data_frames:
                frm.destroy()
            self.data_grid_btn_mng._buttons.clear()
            self.data_grid_btn_mng._og_color.clear()
            self._data.clear()

        def configure(self, require_redraw=False, **kwargs):
            if 'double_click_command' in kwargs:
                for i in self.data_frames:
                    self._double_click_command = kwargs['double_click_command']
                    i.configure(double_click_command = kwargs['double_click_command'])
                kwargs.pop('double_click_command')
            return super().configure(require_redraw, **kwargs)

    class tk_calendar(ctk.CTkToplevel):
        def __init__(self, label,format, *args, fg_color: str or Tuple[str, str] or None = None, date_format: str ="numerical", **kwargs):
            super().__init__(*args, fg_color=fg_color, **kwargs)
            import datetime
            import util
            
            def set_date():
                date_text = None
                if "numerical" in date_format:
                    #label.configure(text= ( format % (self.cal.get_date())))
                    date_text = str(self.cal.get_date())
                elif "word" in date_format:
                    #label.configure(text= f"{util.date_to_words(str(self.cal.get_date()))}")
                    date_text = str(util.date_to_words(str(self.cal.get_date())))
                else:
                    date_text = "Invalid Format"
                
                label.configure(text=date_text)
                self.withdraw()
            
            position_X = (self.winfo_screenwidth()/2)
            position_Y = (self.winfo_screenheight()/2)-(400/2)


            self.title("Calendar")
            self.geometry("%dx%d+%d+%d"%(400,400,position_X,position_Y))
            self.resizable(0,0)

            self.cal = Calendar(self, year=2000, month=1, day=1, showweeknumbers=False, date_pattern="mm-dd-yyyy",
                                mindate=datetime.datetime.now(), normalbackground="#EAEAEA", weekendbackground="#F3EFE0")
            self.cal.pack(fill="both", expand=True, padx=5, pady=5)

            self.set_date = ctk.CTkButton(self, text="Set Date", font=("Robot", 16), command=set_date)
            self.set_date.pack(pady=10)

            self.attributes('-topmost',1)
        

    class cctkSpinnerCombo(ctk.CTkFrame):
        MAX_VAL = 2147483647
        MIN_VAL = -2147483648
        def __init__(self, master: any, width: int = 100, height: int = 30, corner_radius: Optional[Union[int, str]] = None,
                    border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                    fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                    background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                    overwrite_preferred_drawing_method: Union[str, None] = None,
                    #custom arguments
                    button_font: Optional[Tuple[str, int, str]] = ("Lucida", 20, "bold"), button_color: Optional[Union[str, Tuple[str, str]]] = ('#EB455F', '#2C74B3'),
                    button_hover_color:  Optional[Union[str, Tuple[str, str]]] = None, button_font_color: Optional[Union[str, Tuple[str, str]]] = ("black", "white"),
                    entry_font: Optional[Tuple[str, int, str]] = None, entry_text_color: Union[str, Tuple[str, str]] = 'black',
                    entry_fg_color:Optional[Tuple[str, int, str]] = None,
                    step_count: int = 1, val_range: Optional[Tuple[int, int]] = None, command:Callable = None,
                    base_val:int = 0, initial_val: int = 0, state: str = ctk.NORMAL, mode: Literal['num_only', 'click_only'] = 'num_only' ,**kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

            self._btn_font = button_font
            self._step_count = step_count
            self._command  = command
            self._fg_color = fg_color
            self._btn_color = (button_color, button_color) if isinstance(button_color, str) else button_color
            self._btn_hover_color = (button_hover_color, button_hover_color) if isinstance(button_hover_color, str) else button_hover_color
            self._val_range = val_range or (self.MIN_VAL, self.MAX_VAL)
            self._val_range = (self._val_range[1], self._val_range[0]) if self._val_range[0] > self._val_range[1] else self._val_range
            self.value = initial_val;
            self._base_val = base_val
            self._entry_text_color = entry_text_color
            self._state = state
            self._mode = mode

            self.grid_columnconfigure((0,2), weight=0)
            self.grid_columnconfigure(1, weight=1)

            '''events'''

            self.sub_button = ctk.CTkButton(self,text="-", command=partial(self.change_value, -1), text_color=button_font_color,
                                            font=button_font, height=height, width=width*.3, fg_color= self._btn_color[0], hover_color=button_hover_color,
                                            state= self._state)
            self.sub_button.grid(row=0, column=0, padx=(width*0.05,0), pady=(height*0.1))

            self.num_entry = ctk.CTkEntry(self, height=height, width=width*.7, border_width=0, font=entry_font, text_color=entry_text_color,
                                        justify="c", fg_color= entry_fg_color)
            self.num_entry.configure(state= self._state)

            self.num_entry.grid(row=0, column=1, padx=(width*0.05),pady=(height*0.15))

            self.add_button = ctk.CTkButton(self, command=self.change_value, text_color=button_font_color,
                                            text="+", font=button_font,height=height, width=width*.3, fg_color= self._btn_color[1], hover_color=button_hover_color,
                                            state= self._state)
            self.add_button.grid(row=0, column=2, padx=(0,width*0.05),pady=(height*0.1))

            self.num_entry.insert(0, initial_val)

            #setting up the button property
            if self._mode ==  'click_only':
                self.num_entry.configure(state = 'readonly')
                #entry is uneditable
            if self._mode == 'num_only':
                stringvar = ctk.StringVar()
                stringvar.set(initial_val)
                self.num_entry.bind('<Return>', self.return_entry_func)
                self.num_entry.bind('<Button-1>', lambda _: self.num_entry.configure(state = 'normal'))
                self.num_entry.configure(textvariable = stringvar)
                stringvar.trace_add('write', self.entry_check_on_text_change_callback)
                #entry is editable but only num can be enter

        def change_value(self, mul: int = 1):
            self.num_entry.configure(state = 'normal')
            try:
                val = self.value + (self._step_count * mul)
                val = self._val_range[0] if val < self._val_range[0] else self._val_range[1] if val > self._val_range[1] else val
                self.value = val;
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, val)
            except ValueError:
                return
            if self._command is not None:
                self._command(mul)
            self.num_entry.configure(state = 'readonly')

        def entry_check_on_text_change_callback(self, _ = None, *__):
            try:
                txt = self.num_entry.get()
                if (not str(txt[-1]).isnumeric()) or len(txt) > 15:
                    #if either the last input is either not a number or the quantity is more than 15
                    self.num_entry.delete(len(txt)-1, ctk.END)
                    return
                if int(txt) not in range(self._val_range[0], self._val_range[-1]):
                    self.num_entry.delete(0, ctk.END)
                    self.num_entry.insert(0, self._val_range[0] if int(txt) < self._val_range[0] else self._val_range[-1])
                self.value = int(self.num_entry.get())
                if self._command is not None:
                    self._command(0)
            except IndexError:
                pass

        def get(self) -> Union[int, None]:
            try:
                return int(self.num_entry.get())
            except ValueError:
                return None

        def set(self, value: int):
            self.num_entry.delete(0, "end")
            self.num_entry.insert(0, str(value))

        def configure(self, require_redraw=False, **kwargs):
            if "value" in kwargs:
                self.value = kwargs["value"]
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, kwargs["value"])
                kwargs.pop("value")
            if "base_val" in kwargs:
                self._base_val = kwargs["base_val"]
                kwargs.pop("base_val")
            if "command" in kwargs:
                self._command = kwargs["command"]
                kwargs.pop("command")
            if "val_range" in kwargs:
                if isinstance(kwargs['val_range'], tuple):
                    self._val_range = kwargs['val_range']
                    kwargs.pop('val_range')
            if "state" in kwargs:
                self.add_button.configure(state = kwargs["state"])
                self.sub_button.configure(state = kwargs["state"])
                self.num_entry.configure(state = kwargs["state"])
                kwargs.pop('state')
            return super().configure(require_redraw, **kwargs)

        def return_entry_func(self, _):
            txt:str = self.num_entry.get()
            if txt.replace('-', '').isnumeric():
                val = self._val_range[0] if int(txt) < self._val_range[0] else self._val_range[1] if int(txt) > self._val_range[1] else int(txt)
                self.value = val;
                self.num_entry.delete(0, "end")
                self.num_entry.insert(0, self.value)
                if self._command is not None:
                    self._command(0)
            else:
                self.num_entry.delete(0, ctk.END)
                self.num_entry.insert(0, self.value)
            self.num_entry.configure(state = 'readonly')

    class info_tab(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, tab: ctk.CTkFrame = None,
                     button_text: str = 'click to edit info', **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
                             background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            self._tab = tab
            self._button_text  = button_text
            self.value = None
            self.button = ctk.CTkButton(self, width * .8, height * .8, 12, text = self._button_text)
            self.button.place(relx = .5, rely = .5, anchor = 'c')

class customcustomtkinterutil:
    class button_manager:
        def __init__(self, buttons: list, hold_color: str = 'transparent', switch: bool = False,
                     default_active: Optional[int] = None, state: tuple = (lambda: None, lambda: None), children: Optional[list] = None):
            self.active = None
            self._state = state
            self._og_color =[]
            self._switch = switch
            self._hold_color = hold_color
            self._buttons = buttons
            self._default_active = default_active
            self._children = children
            #setup variables

            for i in range(len(buttons)):
                if isinstance(buttons[i], customcustomtkinter.ctkButtonFrame):
                    buttons[i]._command.append(partial(self.click, i))
                elif isinstance(buttons[i], ctk.CTkButton):
                    cmd = buttons[i]._command
                    buttons[i].configure(command = partial(self.click, i, cmd))
                self._og_color.append(buttons[i]._fg_color)
            #set the designated command for buttonframe and ctkbutton

        def click(self, i: int, button_command: callable = None, e: any = None):
            if button_command is not None:
                button_command()
            #actual command of a button

            if self.active == self._buttons[i] and self._switch:
                if self._children is not None:
                    self._children[i].deiconify()
                self.active.configure(hover = True)
                self.active.configure(fg_color = self._og_color[i])
                self._state[0]()
                self.active = None
                return
            #if the clicked button was the active button and the switch mode is on
            elif self.active is not None:
                if self._children is not None:
                    self._children[self._buttons.index(self.active)].deiconify()
                self.active.configure(fg_color = self._og_color[self._buttons.index(self.active)])
                self.active.configure(hover = True)
                self._state[0]()
            #if theres an existing active button
            if self._children is not None:
                self._children[i].place()
            self.active = self._buttons[i]
            self.active.configure(hover = False)
            self.active.configure(fg_color = self._hold_color)
            self._state[1]()
        #setup click variable

        def deactivate_active(self):
            if self._children is not None:
                self._children[self._buttons.index(self.active)].deiconify()
            self.active.configure(hover = True)
            self.active.configure(fg_color = self._og_color[self._buttons.index(self.active)])
            self._state[0]()
            self.active = None