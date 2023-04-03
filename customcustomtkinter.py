import customtkinter as ctk
import tkinter as tk
from typing import *
from functools import partial
from util import brighten_color

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