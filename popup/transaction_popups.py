import customtkinter as ctk
from customcustomtkinter import customcustomtkinter as cctk
import sql_commands
from util import *
from tkinter import messagebox
from constants import action
from customtkinter.windows.widgets.core_widget_classes import DropdownMenu

def show_list(master, obj, info:tuple):
    class instance(ctk.CTkFrame):
        def __init__(self, master, obj, info:tuple):
            self._master = master
            self.width = info[0]
            self.height = info[1]
            self._treeview: cctk.cctkTreeView = info[2]
            super().__init__(master, self.width * .8, self.height *.8, corner_radius= 0)

            self.columnconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.grid_propagate(0)

            self.upper_frame = ctk.CTkFrame(self, height= self.height * .075, corner_radius= 0, fg_color='#222222')
            self.upper_frame.pack_propagate(0)
            self.upper_frame.grid(row = 0, column = 0, sticky = 'we')
            ctk.CTkLabel(self.upper_frame, text='Add Item', font=('Arial', 24)).pack(side=ctk.LEFT, padx = (12, 0))
            self.data = database.fetch_data(sql_commands.get_item_and_their_total_stock, None)
            self.lower_frame = ctk.CTkFrame(self, corner_radius=0, fg_color='#111111')
            self.item_table = cctk.cctkTreeView(self.lower_frame, self.data, self.width * .75, self.height * .65,
                                                column_format='/name:x-tl/quantity:250-tl!50!30',
                                                double_click_command= self.get_item)
            self.item_table.pack(pady = (12, 0), fill='y')
            self.select_btn = ctk.CTkButton(self.lower_frame, 120, 30, text='select', command= self.get_item)
            self.select_btn.pack(pady = (0, 12))
            self.lower_frame.grid(row = 1, column = 0, sticky = 'nsew')
            #self.back_btn = ctk.CTkButton(self, width*.03, height * .4, text='back', command= reset).pack(pady = (12, 0))

        def reset(self):
            self.place_forget()

        def get_item(self, _: any = None):
            #if there's a selected item
            if self.item_table.data_grid_btn_mng.active is not None:
                item_name =  self.item_table.data_grid_btn_mng.active.winfo_children()[0]._text
                #getting the needed information for the item list
                transaction_data = database.fetch_data(sql_commands.get_item_data_for_transaction, (item_name, ))[0]
                #collects part of the data needed in the transaction
                items_in_treeview = [s.winfo_children()[2]._text if self._treeview.data_frames != [] else None for s in self._treeview.data_frames]
                #search the tree view if there's an already existing item

                #if there's an already existing item
                if(item_name in items_in_treeview):
                    print(transaction_data)
                    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[items_in_treeview.index(item_name)].winfo_children()[4].winfo_children()[0]
                    quantity_column.change_value()
                    price_column: ctk.CTkLabel = self._treeview.data_frames[items_in_treeview.index(item_name)].winfo_children()[6]
                    print(float(price_column._text), transaction_data[2])
                    price_column.configure(text = float(price_column._text) + transaction_data[2])
                    #modify the record's quantity
                else:
                    self._treeview.add_data(transaction_data+(0, transaction_data[2]))
                    quantity_column: cctk.cctkSpinnerCombo = self._treeview.data_frames[-1].winfo_children()[4].winfo_children()[0]
                    price_column: ctk.CTkLabel = self._treeview.data_frames[-1].winfo_children()[6]
                    self.item_table.data_grid_btn_mng.active.winfo_children()[1]

                    def spinner_command(mul: int = 1):
                        master.change_total_value(-float(price_column._text))
                        #before change

                        price_change = quantity_column._base_val * quantity_column.value
                        master.change_total_value(price_change)
                        price_column.configure(text = price_change)
                        #after change
                        if quantity_column._base_val * quantity_column.value >= quantity_column._base_val * quantity_column._val_range[1]:
                            messagebox.showinfo('NOTE!', 'Maximum stock reached')

                    quantity_column.configure(command = spinner_command, base_val = transaction_data[2], value = 1, val_range = (1
                    , 10))
                    #add a new record

                master.change_total_value(transaction_data[2])
                self.item_table.data_grid_btn_mng.deactivate_active()
                self.reset()
                #reset the state of this popup
    return instance(master, obj, info)
