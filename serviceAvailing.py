from typing import Optional, Tuple, Union
import customtkinter as ctk
from typing import *
import datetime
from Theme import Color

class pet_info_frame(ctk.CTkFrame):
    def __init__(self, master: any, title:str, name_select_callback: callable, name_selection:list = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        #self.pack_propagate(0)
        self._title = title
        self._corner_radius = 0

        ctk.CTkLabel(self, text = title.title(), font=('Arial', 20), anchor='w').pack(fill = 'x', padx=6, pady=(6,0))
        
        ctk.CTkLabel(self, text = f'Name', font=('Arial', 15), anchor='w').pack(fill = 'x',padx=6)
        self.name = ctk.CTkOptionMenu(self, height=28, values= name_selection or None)
        self.name.configure(command = lambda _: name_select_callback(self, self.name.get()))
        self.name.set('')
        self.name.pack(fill = 'x',padx=6)

        ctk.CTkLabel(self, text = f'Date', font=('Arial', 15), anchor='w').pack(fill = 'x',padx=6)
        self.date = ctk.CTkOptionMenu(self, height=28)
        self.date.pack(fill = 'x',padx=6, pady=(0,6))


    '''functions'''
    def get_data(self, data_format: Literal['metadata', 'tuple']) -> dict | list:
        if data_format == 'metadata':
            return {'name': self.name.get(), 'schedule': self.date.get()}
        elif data_format == 'tuple':
            return (self.name.get(), datetime.datetime.now().strftime('%Y-%m-%d'))

class pets(ctk.CTkFrame):
    def __init__(self, master: any, length:int, title: str, pets_name: List[str], proceed_command:callable, cancel_command:callable = None, width: int = 200, height: int = 200, corner_radius: int | str | None = None, border_width: int | str | None = None, bg_color: str | Tuple[str, str] = "transparent", fg_color: str | Tuple[str, str] | None = None, border_color: str | Tuple[str, str] | None = None, background_corner_colors: Tuple[str | Tuple[str, str]] | None = None, overwrite_preferred_drawing_method: str | None = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)
        self.grid_propagate(0)
        self.frames: List[pet_info_frame] = []
        self.columnconfigure(0, weight=1)
        self._title = title

        def cancel_sequence():
            if cancel_command:
                cancel_command()
            self.destroy()

        def proceed_sequence():
            proceed_command(self.get_data())
            self.destroy()

        def update_frames_selection(sender: ctk.CTkOptionMenu, to_remove: str) -> None:
            for i in self.frames:
                if i is not sender:
                    temp = pets_name.copy()
                    temp.pop(temp.index(to_remove))
                    i.name.configure(values = temp)
        #manage the selection of each patient frames to prevent duplicate pets 

        ctk.CTkLabel(self, text = f"   {self._title}", font = ('Arial', 20), anchor='w', fg_color=Color.Blue_Yale).grid(row = 0, column = 0, sticky = 'nsew', columnspan=3)

        self.main_frame = ctk.CTkScrollableFrame(self, self._current_width * .95, self._current_height * .8, fg_color = 'transparent')
        self.main_frame.grid(row = 1, column = 0, sticky = 'ns', padx = (self._current_width * .0075 ,0), columnspan = 3)
        #content frame
        
        for _ in range(length):
            self.frames.append(pet_info_frame(self.main_frame, f'pet {_ + 1}', name_selection=pets_name, height=180, name_select_callback= update_frames_selection))
            self.frames[-1].pack(fill = 'x', side = 'top', pady = (0, 5))
        #generate the patient info catalogs, length varies to the given length

        self.cancel_btn = ctk.CTkButton(self, self._current_width * .15, self._current_height * .08, text='Cancel', command=cancel_sequence)
        self.cancel_btn.grid(row = 2, column = 1, sticky = 'nsew')
        self.proceed_btn = ctk.CTkButton(self, self._current_width * .15, self._current_height * .08, text='Proceed', command= proceed_sequence)
        self.proceed_btn.grid(row = 2, column = 2, sticky = 'nsew', padx=(12,20))

       

    '''functions'''
    def get_data(self) -> list:
        data = []
        for i in self.frames:
            data.append(i.get_data(data_format='tuple'))
        return data
    
class body(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.state("zoomed")
        self.update()
        self.attributes("-fullscreen", True)

        #pets1 = pets(self, 2, 'test', self.winfo_screenwidth() * .65, self.winfo_screenheight() * .65, fg_color= 'red')
        pets1 = pets(self, 2, 'grooming', ['hello', 'world'], None, None, self.winfo_screenwidth() * .65, self.winfo_screenheight() * .65, fg_color= 'red')
        pets1.place(relx = .5, rely = .5, anchor = 'c')
        
        self.mainloop()

#body()