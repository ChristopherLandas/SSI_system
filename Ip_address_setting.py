from typing import Tuple
import customtkinter as ctk
from tkinter import messagebox
from tkextrafont import Font
from PIL import Image
from tkinter import _tkinter
from Theme import Color, Icons
import re, os, json
from typing import *

ctk.set_appearance_mode('light')

class ip_setup(ctk.CTk):
    def __init__(self, fg_color: str | Tuple[str, str] | None = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        
        try:
            #Transitioning to new font style
            Font(file="Font/DMSans-Bold.ttf")
            Font(file="Font/DMSans-Medium.ttf")
            Font(file='Font/DMSans-Regular.ttf')

            #Use DM Mono for numbers
            Font(file="Font/DMMono-Light.ttf")
            Font(file="Font/DMMono-Medium.ttf")
            Font(file="Font/DMMono-Regular.ttf")

        except _tkinter.TclError:
            pass
        
        title_name = "J.Z. Angeles Veterinary Clinic Network Setup"
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        
        root_w = 400
        root_h = 500
        pos_x = width/2 - root_w/2
        pos_y = height/2 - root_h/2
        
        
        def entry_checker(_ = None, *__):
            if re.search(r'[0-9\.]$', self.admin_entry.get() or "") is None and self.admin_entry._is_focused and self.admin_entry.get():
                        l = len(self.admin_entry.get())
                        self.admin_entry.delete(l-1, l)

            if re.search(r'[0-9\.]$', self.cashier_entry.get() or "") is None and self.cashier_entry._is_focused and self.cashier_entry.get():
                        l = len(self.cashier_entry.get())
                        self.cashier_entry.delete(l-1, l)
                        
            if re.search(r'[0-9\.]$', self.reception_entry.get() or "") is None and self.reception_entry._is_focused and self.reception_entry.get():
                        l = len(self.reception_entry.get())
                        self.reception_entry.delete(l-1, l) 
        
        
        self.title(title_name)
        self.geometry('%dx%d+%d+%d' % (root_w,root_h,pos_x,pos_y))
        self.minsize(root_w,root_h)
        self.resizable(0,0)
        self._fg_color = Color.White_Platinum
        self.ip_entries = {}
        self.default_gateway = self.get_default_gateway_ip()
        self.key_li = ["MY_NETWORK_IP", "RECEPTIONIST_IP", "CASHIER_IP", "ADMIN_IP"]
        
        self.main_frame = ctk.CTkFrame(self, fg_color=Color.White_Lotion)
        self.main_frame.pack(fill='both', expand=1, padx=(5,5), pady=(5,5))
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.title_frame.pack(fill='x', expand=0, padx=(5,5), pady=(5,5))
        self.title_frame.pack_propagate(1)
        
        ctk.CTkLabel(self.title_frame, text="",image=Icons.get_image('network_icon', (30,30)), fg_color='transparent', anchor='w', corner_radius=5, height=35).pack(side='left', padx=(5,0), pady=(5))
        ctk.CTkLabel(self.title_frame, text="Network Settings", font=("DM Sans Medium", 16), fg_color='transparent', anchor='w', corner_radius=5, padx=(10), height=35).pack(side='left', padx=(0), pady=(5))
        
        self.admin_frame = ctk.CTkFrame(self.main_frame, height=25, fg_color=Color.White_Platinum)
        self.admin_frame.pack(fill='x', expand=0, padx=(5,5), pady=(0,5))
        self.admin_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.admin_frame, text="",image=Icons.get_image('admin_user_icon', (45,45)), fg_color='transparent', anchor='w', corner_radius=5, height=35).grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(5,0), pady=(5))
        ctk.CTkLabel(self.admin_frame, text="Administrator IP", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', corner_radius=5).grid(row=0, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5,0))
        self.admin_entry = ctk.CTkEntry(self.admin_frame, font=("DM Sans Medium", 14), height=35, border_width=0, textvariable= ctk.StringVar())
        self.admin_entry._textvariable.trace_add('write', entry_checker)
        self.admin_entry.grid(row=1, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(0))
        self.admin_checkbox = ctk.CTkCheckBox(self.admin_frame, font=("DM Sans Medium", 14), text="Own IP")
        self.admin_checkbox.configure(command = lambda: self.set_ip(self.admin_checkbox))
        self.admin_checkbox.grid(row=2, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5))
        self.ip_entries[self.admin_checkbox] = self.admin_entry
        
        self.reception_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.reception_frame.pack(fill='x', expand=0, padx=(5,5), pady=(0,5))
        self.reception_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.reception_frame, text="",image=Icons.get_image('reception_icon', (45,45)), fg_color='transparent', anchor='w', corner_radius=5, height=35).grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(5,0), pady=(5))
        ctk.CTkLabel(self.reception_frame, text="Reception IP", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', corner_radius=5).grid(row=0, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5,0))
        self.reception_entry = ctk.CTkEntry(self.reception_frame, font=("DM Sans Medium", 14), height=35, border_width=0, textvariable= ctk.StringVar())
        self.reception_entry._textvariable.trace_add('write', entry_checker)
        self.reception_entry.grid(row=1, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(0))
        self.reception_checkbox = ctk.CTkCheckBox(self.reception_frame, font=("DM Sans Medium", 14), text="Own IP")
        self.reception_checkbox.configure(command = lambda: self.set_ip(self.reception_checkbox))
        self.reception_checkbox.grid(row=2, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5))
        self.ip_entries[self.reception_checkbox] = self.reception_entry
        self.reception_checkbox.grid(row=2, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5))

        self.cashier_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.cashier_frame.pack(fill='x', expand=0, padx=(5,5), pady=(0,5))
        self.cashier_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(self.cashier_frame, text="",image=Icons.get_image('cashier_icon', (45,45)), fg_color='transparent', anchor='w', corner_radius=5, height=35).grid(row=0, column=0, sticky='nsew', rowspan=3, padx=(5,0), pady=(5))
        ctk.CTkLabel(self.cashier_frame, text="Cashier IP", font=("DM Sans Medium", 14), fg_color='transparent', anchor='w', corner_radius=5).grid(row=0, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5,0))
        self.cashier_entry = ctk.CTkEntry(self.cashier_frame, font=("DM Sans Medium", 14), height=35, border_width=0, textvariable= ctk.StringVar())
        self.cashier_entry._textvariable.trace_add('write', entry_checker)
        self.cashier_entry.grid(row=1, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(0))
        self.cashier_checkbox = ctk.CTkCheckBox(self.cashier_frame, font=("DM Sans Medium", 14), text="Own IP")
        self.cashier_checkbox.configure(command = lambda: self.set_ip(self.cashier_checkbox))
        self.cashier_checkbox.grid(row=2, column=1, sticky='nsew', rowspan=1, padx=(5,5), pady=(5))
        self.ip_entries[self.cashier_checkbox] = self.cashier_entry
        
        self.default_frame = ctk.CTkFrame(self.main_frame, height= 50, fg_color=Color.White_Platinum)
        self.default_frame.pack(fill='x', expand=0, padx=(5,5), pady=(0,5))
        self.default_frame.grid_columnconfigure(1, weight=1)
        self.default_frame.pack_propagate(0)
        self.default_checkbox = ctk.CTkCheckBox(self.default_frame, font=("DM Sans Medium", 14), text="Use default IP", command= self.set_default_ip)
        self.default_checkbox.pack(side = ctk.LEFT, padx=(5,5), pady=(0,5))
        
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color=Color.White_Platinum)
        self.button_frame.pack(fill='x', expand=0, padx=(5,5), pady=(0,5))
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.pack_propagate(0)
        
        self.set_button = ctk.CTkButton(self.button_frame, text="Set IP", font=('DM Sans Medium', 14), fg_color=Color.Green_Pistachio, hover_color=Color.Green_Button_Hover_Color,
                                        command=self.set_command, text_color=Color.White_Lotion, height=35)
        self.set_button.pack(fill='y', expand=1, pady=5)
        
        self.entries = [self.admin_entry, self.cashier_entry, self.reception_entry]
        self.load_default()
        
        #default IP

    def load_default(self):
        with open('Resources\\network_settings.json', 'r') as file:
            temp_ = json.load(file)
        for i in range(len(self.entries)):
            self.entries[i].insert(0, temp_[self.key_li[i]])

    def set_default_ip(self):
        self.admin_checkbox.deselect()
        self.cashier_checkbox.deselect()
        self.reception_checkbox.deselect()
        if self.default_checkbox.get() == 1:
            self.admin_checkbox.configure(state = ctk.DISABLED)
            self.cashier_checkbox.configure(state = ctk.DISABLED)
            self.reception_checkbox.configure(state = ctk.DISABLED)
            if self.default_gateway is not None:
                for k in self.ip_entries.keys():
                    self.ip_entries[k].delete(0, ctk.END)
                    self.ip_entries[k].insert(0, '127.0.0.1')
                    self.ip_entries[k].configure(state = ctk.DISABLED)
        else:
            self.admin_checkbox.configure(state = ctk.NORMAL)
            self.cashier_checkbox.configure(state = ctk.NORMAL)
            self.reception_checkbox.configure(state = ctk.NORMAL)
            for k in self.ip_entries.keys():
                self.ip_entries[k].configure(state = ctk.NORMAL)
                self.ip_entries[k].delete(0, ctk.END)
            self.load_default()
    
    def set_command(self):
        st: List[str] = self.get_entries()
        temp = ['Admin IP', 'Cashier IP', 'Receptionist IP']
        for i in range(len(st)):
             if re.search(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$', st[i]) is None:
                  messagebox.showerror("Invalid Ip", f"Invalid Ip for {temp}")
                  return
             
        st = ['127.0.0.1' if self.default_checkbox.get() == 1 else self.default_gateway] + st

        for i in range(len(st)):
            self.modify_json(self.key_li[i], st[i])

        messagebox.showinfo("Success!", "Ip changed successfully", parent = self)
        self.destroy()
        
    def get_entries(self):
        return [entry.get() for entry in self.entries]

    def get_default_gateway_ip(self):
        file=os.popen("ipconfig")
        data=file.read()
        file.close()
        bits=[s.strip() for s in data.strip().split('\n')]
        
        for i in range(len(bits)):
            if 'Default' in bits[i]:
                li1 = re.search(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$', bits[i][bits[i].index(': ')+2:])
                li2 = re.search(r'^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$', bits[i+1])
                if li1 is not None:
                    return li1[0]
                if li2 is not None:
                    return bits[i+1]
        return None
    
    def set_ip(self, checkbox: ctk.CTkTextbox):
        if checkbox.get() == 1:
            if self.default_gateway is not None:
                self.ip_entries[checkbox].delete(0, ctk.END)
                self.ip_entries[checkbox].insert(0, self.default_gateway)
                self.ip_entries[checkbox].configure(state = ctk.DISABLED)
            else:
                 messagebox.showerror("Default gateway seems to be none,\nchange it on network settings", parent = self)
        else:
            self.ip_entries[checkbox].configure(state = ctk.NORMAL)
            self.ip_entries[checkbox].delete(0, ctk.END)

    def modify_json(self, key, new_value):
        try:
            with open('Resources\\network_settings.json', 'r') as file:
                data = json.load(file)

            data[key] = new_value

            with open('Resources\\network_settings.json', 'w') as file:
                json.dump(data, file, indent=2) 
        finally:
             pass
#son_file_path = 'example.json'
#modify_json(json_file_path, 'example_key', 'new_value')

if __name__ == '__main__':
    app = ip_setup()
    app.mainloop()