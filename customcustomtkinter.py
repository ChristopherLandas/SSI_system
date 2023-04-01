import customtkinter as ctk
import tkinter as tk
from typing import *
from functools import partial
from functools import wraps
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
            self._command = command
            self._commands = [command]
            self._hover = hover
            #make a reference/encapsulation from extended arguents

            self.bind('<Button-1>', command)
            self.pack_propagate(0)
            self.grid_propagate(0)
            self.update_button()
            #set the sequence events of 3rd party properties

        def update_button(self, is_hover = True):
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
                for c in self._commands:
                    i.bind('<Button-1>', c)
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
                self._command = command
                self._commands.append(command)
                self.unbind('<Button-1>', None)
                for c in self._commands:
                    self.bind('<Button-1>', c)
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

    class button_manager:
        def __init__(self, buttons: list = None, hold_color: str = 'transparent', og_color: str = 'green',
                     default_active: Optional[int] = None, commands: tuple = (lambda: print('disable'), lambda: print('enable'))):
            self.active = None
            self._command = commands
            self._og_color = og_color
            self._hold_color = hold_color
            self._buttons = buttons
            self._default_active = default_active
            #setup variables

            for i in range(len(buttons)):
                buttons[i].bind('<Button-1>', partial(self.click, i))
                if(isinstance(buttons[i], customcustomtkinter.ctkButtonFrame)):
                    buttons[i].configure(command = partial(self.click, i))

        def click(self, i: int, _):
            if(isinstance(self._buttons[i], customcustomtkinter.ctkButtonFrame)):
                og = self._buttons[i]._fg_color
                click_color = brighten_color(og, 1.25) if isinstance(og, tuple) else (brighten_color(og, 1.25), brighten_color(og, .75))
                self._buttons[i].configure(fg_color = click_color)
                self._buttons[i].update()
                self._buttons[i].after(50, None)

            if(self.active is not None):
                self.active.configure(fg_color = self._og_color)
                self.active.configure(hover = True)
                self._command[0]()
            self.active = self._buttons[i]
            self.active.configure(hover = False)
            self.active.configure(fg_color = self._hold_color)
            self._command[1]()
        #setup click variable