import customtkinter as ctk
import tkinter as tk
from typing import *
from functools import partial
from util import brighten_color
import re
from tkinter import messagebox;

class customcustomtkinter:
    class ctkButtonFrame(ctk.CTkFrame):
        def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, command: Union[Callable[[],None], None] = None,
                     hover: bool = True, hover_color: Union[str, Tuple[str, str]] = "transparent",
                     **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color,
                             background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
            # sets the default properties of a frame

            self.og_color = self._fg_color
            self._hover_color = hover_color
            self._command = [] if isinstance(command, list) else [command]
            self._hover = hover
            #make a reference/encapsulation from extended arguments

            self.bind('<Button-1>', self.response)
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
                    if(callable(cmd)):
                        cmd()
        #click response of the button; includes the flash when clicked

        def update_button(self, is_hover: bool = True):
            if(is_hover):
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
                if(self._hover):
                    i.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
                    i.bind('<Leave>', lambda _: self.configure(fg_color = self.og_color))
                else:
                    i.unbind('<Enter>', None)
                    i.unbind('<Leave>', None)
        #update all the children properties to mimic the button properties

        def configure(self, require_redraw=False, command: Optional[Callable[[], None]] = None, hover: Optional[bool] = None,
                      hover_color: Optional[Union[str, Tuple[str, str]]] = None, **kwargs):
            if(command is not None):
                self._command = [] if isinstance(command, list) else [command]
                self.unbind('<Button-1>', None)
                self.bind('<Button-1>', self.response)
                self.update_children()
            if(hover_color is not None):
                self._hover_color = hover_color
                self.unbind('<Enter>', None)
                self.bind('<Enter>', lambda _: self.configure(fg_color = self._hover_color))
            if(hover is not None):
                self._hover = hover
                self.update_button(hover)
                self.update_children()
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

        def __init__(self, master: any, data: Union[tuple, list], width: int = 200, height: int = 200, corner_radius: Optional[Union[int, str]] = None,
                     border_width: Optional[Union[int, str]] = None, bg_color: Union[str, Tuple[str, str]] = "transparent",
                     fg_color: Optional[Union[str, Tuple[str, str]]] = None, border_color: Optional[Union[str, Tuple[str, str]]] = None,
                     background_corner_colors: Union[Tuple[Union[str, Tuple[str, str]]], None] = None,
                     overwrite_preferred_drawing_method: Union[str, None] = None, column_format: str = '/Title1:x-t/Title2:x-t/Title3:x-t!50!50',
                     header_color: Union[str, tuple] = '#006611', data_grid_color: Union[list, tuple] = ('#333333', '#444444'),
                     selected_color: str = brighten_color('#006611', 1.3), **kwargs):
            super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors,
                             overwrite_preferred_drawing_method, **kwargs)


            if not re.fullmatch(r'(\/\w+:(x|\d+)-(\w+|\#))+\!\d+\!\d+', column_format):
                ctk.CTkLabel(self, text='Wrong format\nCheck for errors').place(relx = .5, rely = .5, anchor = 'c')
                return;
            #check if the format follows the guideline, if it doesn't it will only pop a label

            self._column_format  = column_format
            self.column_titles = [s.replace('/', '') for s in re.findall(r'\/\w+', self._column_format)]
            self.column_types = [str(s) for s in re.findall(r'\-(\w+|\#)', self._column_format)]
            total_fixed_width = sum([int(s) for s in re.findall(r'\:(x|\d+)', self._column_format) if str(s).isnumeric()])
            x_width = (self._current_width - (total_fixed_width + 14)) / len(re.findall(r'\:x', self._column_format))
            #set the measurements of the treeview according to the format given

            self.data_frames = []
            self._data = []
            self.data_grid_btn_mng = None
            self.column_widths = [x_width if s == 'x' else int(s) for s in re.findall(r'\:(x|\d+)', self._column_format)]
            self._header_heights = int(re.findall(r'\!(\d+)', column_format)[0])
            self._data_grid_heights = int(re.findall(r'\!(\d+)', column_format)[1])
            self._header_color = header_color
            self._data_grid_color = (data_grid_color[0], data_grid_color[1]) if isinstance(data_grid_color, tuple) else((data_grid_color[0][0], data_grid_color[1][0]), (data_grid_color[0][1], data_grid_color[1][1]))
            #encapsulate other arguments

            self.pack_propagate(0)
            self.grid_propagate(0)
            self.grid_rowconfigure(1, weight=1)
            #make the root frame fixed in sizesz

            for i in range(len(self.column_titles)):
                btn = None
                if self.column_types[i] == 't' or self.column_types[i] == '#' or self.column_types[i] == 'q':
                    btn = customcustomtkinter.ctkButtonFrame(self, self.column_widths[i], self._header_heights, 0,
                                                            fg_color= self._header_color, hover_color= brighten_color(self._header_color, 1.75),)
                    title = ctk.CTkLabel(btn, text=self.column_titles[i])
                    title.place(relx = .5, rely = .5, anchor = 'c')
                    btn.update_children()
                else:
                    btn = ctk.CTkLabel(self, self.column_widths[i], self._header_heights, 0, fg_color= self._header_color,
                                       text=self.column_titles[i])
                btn.grid(row = 0, column = i, sticky='we')
            #generate the header bar

            self.contents = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color='#333333')
            self.contents.grid(row = 1, column = 0, columnspan = len(self.column_titles) + 1, sticky = 'news')
            #the data grid holder

            self.scroll_bar_btn = customcustomtkinter.ctkButtonFrame(self, 14, self._header_heights, 0, fg_color='#006611',
                                                                     hover_color= brighten_color('#006611', 1.75),
                                                                     command = lambda: self.contents._parent_canvas.yview_moveto(0 if (self.contents._parent_canvas.yview()[1] > .5) else 1))
            self.scroll_bar_btn.grid(row = 0, column = len(self.column_titles), sticky='nsew')
            #additional button that will serve as go to top/down of a scroll bar

            '''initial generation here'''
            customcustomtkinterutil.add_data(self, data)
            #self.add_data(data)
            #generates data grid

            self.data_grid_btn_mng = customcustomtkinterutil.button_manager(self.data_frames, brighten_color('#006611', 2), True, None)
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

                dlt_btn.master.master.destroy()
                for i in range(data_mngr_index, len(self.data_frames)):
                    color = self._data_grid_color[0] if i % 2 == 0 else self._data_grid_color[1]
                    self.data_grid_btn_mng._og_color[i] = color
                    self.data_frames[i].og_color = color
                    self.data_frames[i].configure(fg_color = color)
                #update the fg color of each of the frames, maintaining the alternating pattern

        def add_data(self, data: Union[tuple, list]):
            d = [data] if isinstance(data, tuple) else data
            for i in range(len(d)):
                tI = 0;
                frm = customcustomtkinter.ctkButtonFrame(self.contents._parent_canvas, height=self._data_grid_heights, width=15,
                                                         fg_color=self._data_grid_color[0] if len(self.data_frames) % 2 == 0 else self._data_grid_color[1],
                                                         corner_radius= 0, hover_color= brighten_color('#006611', 1.25))
                self.data_frames.append(frm)
                self._data.append(d[i])
                if self.data_grid_btn_mng is not None:
                    self.data_grid_btn_mng._og_color.append(frm._fg_color)

                for j in range(len(self.column_widths)):
                    if self.column_types[j] in ['t', '#']:
                        temp = ctk.CTkLabel(frm, text= d[i][tI] if self.column_types[j] in ['t'] else (i + 1), width = self.column_widths[j])
                        temp.pack(side = tk.LEFT, fill = 'y')
                    else:
                        temp = ctk.CTkFrame(self.data_frames[i], width= self.column_widths[j], corner_radius= 0, border_width=0, fg_color='transparent')
                        temp.pack(side = tk.LEFT, fill = 'y')
                        if self.column_types[j] == 'bD':
                            dlt_btn = ctk.CTkButton(temp, self._data_grid_heights * .8, self._data_grid_heights * .8, fg_color='red' ,text='')
                            dlt_btn.configure(command = partial(self.bd_func, dlt_btn))
                            dlt_btn.place(relx = .5, rely = .5, anchor = 'c')
                            continue;
                        elif self.column_types[j] == 'id':
                            self.spinner = customcustomtkinter.cctkSpinnerCombo(self.data_frames[i],step_count=1, fg_color=("green", "blue"), button_color=("red", "yellow"),entry_fg_color=("red", "yellow"),
                                   button_hover_color=("yellow", "red"), entry_font=("Lucida", 20), entry_text_color=("white", "black"))
                            self.spinner.place(relx = .5, rely = .5, anchor = 'c')
                    if self.column_types[j] == 't':
                        tI += 1
                # generates the content from the frame

                self.data_frames[i].update_children()
                self.data_frames[i].pack(fill = 'x', pady = (1,0))

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
                if(isinstance(buttons[i], customcustomtkinter.ctkButtonFrame)):
                    buttons[i]._command.append(partial(self.click, i))
                elif(isinstance(buttons[i], ctk.CTkButton)):
                    cmd = buttons[i]._command
                    buttons[i].configure(command = partial(self.click, i, cmd))
                self._og_color.append(buttons[i]._fg_color)
            #set the designated command for buttonframe and ctkbutton

        def click(self, i: int, button_command: callable = None, e: any = None):
            if(button_command is not None):
                button_command()
            #actual command of a button

            if(self.active == self._buttons[i] and self._switch):
                if(self._children is not None):
                    self._children[i].deiconify()
                self.active.configure(hover = True)
                self.active.configure(fg_color = self._og_color[i])
                self._state[0]()
                self.active = None
                return
            #if the clicked button was the active button and the switch mode is on
            elif(self.active is not None):
                if(self._children is not None):
                    self._children[self._buttons.index(self.active)].deiconify()
                self.active.configure(fg_color = self._og_color[self._buttons.index(self.active)])
                self.active.configure(hover = True)
                self._state[0]()
            #if theres an existing active button
            if(self._children is not None):
                self._children[i].place()
            self.active = self._buttons[i]
            self.active.configure(hover = False)
            self.active.configure(fg_color = self._hold_color)
            self._state[1]()
        #setup click variable