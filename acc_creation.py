from typing import *
from typing import Optional, Tuple, Union
import customtkinter as ctk
import tkinter as tk;


class frame2(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.pack_propagate(0)

        self.upperframe = ctk.CTkFrame(self, self._current_width * .95, self._current_height * .85, 0, fg_color='transparent')
        self.upperframe.pack(padx = (self._current_width * .025, self._current_width * .025), pady = (self. _current_height * 0.025, 0))
        self.pack_propagate(0)

        self.left_frame = ctk.CTkFrame(self.upperframe, self._current_width * .475, self._current_height * .85, 12, fg_color='red');
        self.left_frame.pack(side = 'left', padx = (0, self._current_width * .0125));
        self.left_frame.grid_propagate(0)
        ctk.CTkLabel(self.left_frame, text= "Account", font=("Arial", 25)).grid(row = 0, column = 0, padx = (7, 0))

        '''ctk.CTkLabel(self.left_frame, text= "Full name", font=("Arial", 15)).grid(row = 1, column = 0, padx = (7, 0), pady = (24, 0), sticky = 'w')
        self.name_entry = ctk.CTkEntry(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8)
        self.name_entry.grid(row = 2, column = 0, padx = (7, 0))'''

        ctk.CTkLabel(self.left_frame, text= "Username", font=("Arial", 15)).grid(row = 3, column = 0, padx = (7, 0), pady = (12, 0), sticky = 'w')
        self.usn_option = ctk.CTkOptionMenu(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8)
        self.usn_option.grid(row = 4, column = 0, padx = (7, 0))

        '''ctk.CTkLabel(self.left_frame, text= "USN", font=("Arial", 15)).grid(row = 5, column = 0, padx = (7, 0), pady = (24, 0), sticky = 'w')
        self.usn_entry = ctk.CTkEntry(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8,
                                      state = 'readonly')
        self.usn_entry.grid(row = 6, column = 0, padx = (7, 0))

        ctk.CTkLabel(self.left_frame, text= "Password", font=("Arial", 15)).grid(row = 7, column = 0, padx = (7, 0), pady = (7, 0), sticky = 'w')
        self.pss_entry = ctk.CTkEntry(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8,
                                      state = 'readonly')
        self.pss_entry.grid(row = 8, column = 0, padx = (7, 0))'''

        self.right_frame = ctk.CTkFrame(self.upperframe, self._current_width * .475, self._current_height * .85, 12, fg_color='green');
        self.right_frame.pack(side = 'left', padx = (self._current_width * .0125, 0));
        self.right_frame.grid_propagate(0)
        ctk.CTkLabel(self.right_frame, text= "Access Level", font=("Arial", 25)).grid(row = 0, column = 0, padx = (7, 0))

        self.access_lvl_frame = ctk.CTkFrame(self.right_frame, self.right_frame._current_width * .91, self.right_frame._current_height * .91, fg_color='blue')
        self.access_lvl_frame.grid(row = 1, column = 0, sticky = 'we', padx = 7, pady = 7)
        self.access_lvl_frame.grid_propagate(0)

        self.access_lvls: List[str] = ['Dashboard', 'Transaction', 'Services', 'Sales', 'Inventory', 'Pet Information', 'Report', 'Users', 'Action Log']
        self.check_boxes: Dict[str, ctk.CTkCheckBox] = {}
        for i in range(len(self.access_lvls)):
            self.check_boxes[self.access_lvls[i]] = ctk.CTkCheckBox(self.access_lvl_frame, self.access_lvl_frame._current_width * .95, 24,
                                                                    text=self.access_lvls[i], state=ctk.DISABLED);
            self.check_boxes[self.access_lvls[i]].grid(row = i, column = 0, padx = 7, pady = 7);
            

        self.accept_button = ctk.CTkButton(self, 140, 50, 12, text="Proceed")
        self.accept_button.pack(anchor = 'e', padx = (0, self._current_width * .025), pady = (self._current_width * .0125))



class frame(ctk.CTkFrame):
    def __init__(self, master: any, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.pack_propagate(0)

        self.upperframe = ctk.CTkFrame(self, self._current_width * .95, self._current_height * .85, 0, fg_color='transparent')
        self.upperframe.pack(padx = (self._current_width * .025, self._current_width * .025), pady = (self. _current_height * 0.025, 0))
        self.pack_propagate(0)

        self.left_frame = ctk.CTkFrame(self.upperframe, self._current_width * .475, self._current_height * .85, 12, fg_color='red');
        self.left_frame.pack(side = 'left', padx = (0, self._current_width * .0125));
        self.left_frame.grid_propagate(0)
        ctk.CTkLabel(self.left_frame, text= "Account Credentials", font=("Arial", 25)).grid(row = 0, column = 0, padx = (7, 0))

        ctk.CTkLabel(self.left_frame, text= "Full name", font=("Arial", 15)).grid(row = 1, column = 0, padx = (7, 0), pady = (24, 0), sticky = 'w')
        self.name_entry = ctk.CTkEntry(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8)
        self.name_entry.grid(row = 2, column = 0, padx = (7, 0))

        ctk.CTkLabel(self.left_frame, text= "Position", font=("Arial", 15)).grid(row = 3, column = 0, padx = (7, 0), pady = (12, 0), sticky = 'w')
        self.position_option = ctk.CTkOptionMenu(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8)
        self.position_option.grid(row = 4, column = 0, padx = (7, 0))

        ctk.CTkLabel(self.left_frame, text= "USN", font=("Arial", 15)).grid(row = 5, column = 0, padx = (7, 0), pady = (24, 0), sticky = 'w')
        self.usn_entry = ctk.CTkEntry(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8,
                                      state = 'readonly')
        self.usn_entry.grid(row = 6, column = 0, padx = (7, 0))

        ctk.CTkLabel(self.left_frame, text= "Password", font=("Arial", 15)).grid(row = 7, column = 0, padx = (7, 0), pady = (7, 0), sticky = 'w')
        self.pss_entry = ctk.CTkEntry(self.left_frame, self.left_frame._current_width * .95, self.left_frame._current_height * .075, 8,
                                      state = 'readonly')
        self.pss_entry.grid(row = 8, column = 0, padx = (7, 0))

        self.right_frame = ctk.CTkFrame(self.upperframe, self._current_width * .475, self._current_height * .85, 12, fg_color='green');
        self.right_frame.pack(side = 'left', padx = (self._current_width * .0125, 0));
        self.right_frame.grid_propagate(0)
        ctk.CTkLabel(self.right_frame, text= "Access Level", font=("Arial", 25)).grid(row = 0, column = 0, padx = (7, 0))

        self.access_lvl_frame = ctk.CTkFrame(self.right_frame, self.right_frame._current_width * .91, self.right_frame._current_height * .91, fg_color='blue')
        self.access_lvl_frame.grid(row = 1, column = 0, sticky = 'we', padx = 7, pady = 7)
        self.access_lvl_frame.grid_propagate(0)

        self.access_lvls: List[str] = ['Dashboard', 'Transaction', 'Services', 'Sales', 'Inventory', 'Pet Information', 'Report', 'Users', 'Action Log']
        self.check_boxes: Dict[str, ctk.CTkCheckBox] = {}
        for i in range(len(self.access_lvls)):
            self.check_boxes[self.access_lvls[i]] = ctk.CTkCheckBox(self.access_lvl_frame, self.access_lvl_frame._current_width * .95, 24,
                                                                    text=self.access_lvls[i], state=ctk.DISABLED);
            self.check_boxes[self.access_lvls[i]].grid(row = i, column = 0, padx = 7, pady = 7);
            

        self.accept_button = ctk.CTkButton(self, 140, 50, 12, text="Proceed")
        self.accept_button.pack(anchor = 'e', padx = (0, self._current_width * .025), pady = (self._current_width * .0125))


class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)
        self.update()
        width = self.winfo_vrootwidth()
        height = self.winfo_vrootheight()

        self.frame = frame2(self, width * .4, height * .5, 12, fg_color= 'gray')
        self.frame.place(relx = .5, rely = .5, anchor = 'c')

        self.mainloop()

#body()