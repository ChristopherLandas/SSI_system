import customtkinter as ctk
import datetime
from tkextrafont import Font
from tkcalendar import Calendar
from PIL import Image
import mariadb
import tkinter
from Constants import db_constants
import hashlib
import re

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class login_GUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        dbKey = db_constants.login_credential_columns
        def signin():
            '''steps:
            get salt
            generate the initial pass
            loop the password
            check the db for credentials
            login
            '''

            #get salt
            try:
                db_con = mariadb.connect(user="root", password="test123", host="127.0.0.1", port=3306, database='test')
                db_cur = db_con.cursor()
                db_cur.execute(f'SELECT {dbKey.SALT} FROM {dbKey.TABLE} WHERE {dbKey.USERNAME} = ?', (self.email_entry.get(), ))
                salt = str(db_cur.fetchall()[0][0]).encode('utf-8')
            except mariadb.Error:
                tkinter.messagebox.showinfo('db error', 'db error')
                return
            except IndexError:
                tkinter.messagebox.showinfo('incorrect', 'incorrect')
            else:
                db_cur.close()
                db_con.close()

            #generate the initial pass
            hash_encryptor = hashlib.sha256()
            hash_encryptor.update(self.password_entry.get().encode('utf-8')+salt)
            initial_pass = hash_encryptor.hexdigest()

            #loop the password
            for _ in range(len(self.email_entry.get()) + int(re.findall('\d{2}', initial_pass)[0])):
                hash_encryptor.update(initial_pass.encode('utf-8') + salt)
                initial_pass = hash_encryptor.hexdigest()

            #check the db for credentials
            try:
                db_con = mariadb.connect(user="root", password="test123", host="127.0.0.1", port=3306, database='test')
                db_cur = db_con.cursor()
                db_cur.execute(f'SELECT COUNT(*) AS len FROM {dbKey.TABLE} WHERE {dbKey.USERNAME} = ? AND {dbKey.PASSWORD} = ?', (self.email_entry.get(), initial_pass))
                does_have = db_cur.fetchall()[0][0] > 0
            except mariadb.Error:
                tkinter.messagebox.showinfo('db error', 'db error')
                return
            else:
                db_cur.close()
                db_con.close()

            if(does_have):
                #main_page.main_page(self, withdraw_root=True)
                tkinter.messagebox.showinfo('', 'login')
            else:
                tkinter.messagebox.showinfo('', 'incorrect')


        self.title("Application Development")

        win_width=900
        win_height=600

        logo_image = ctk.CTkImage(light_image=Image.open("image/survey_logo.png"), size=(100,100))

        self.geometry(f"{win_width}x{win_height}")
        self.minsize(win_width,win_height)
        self.state('zoomed')
        self.configure(fg_color="#FEFEFE")

        self.frame = ctk.CTkFrame(self, width=800, height=500,fg_color="#EEEEEE", border_color="#222831", corner_radius=10, border_width=3)
        self.frame.place(relx=0.5, rely=0.5, anchor="c")

        self.frame.grid_columnconfigure(0, weight=2)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_propagate(False)

        self.frame_title = ctk.CTkFrame(self.frame)
        self.frame_title.grid(row=0, column=0, sticky="nsew", padx=(10,5), pady=10)

        self.title_container = ctk.CTkFrame(self.frame_title,fg_color="transparent")
        self.title_container.place(relx=0.5,rely=0.45, anchor="c")

        self.logo_label = ctk.CTkLabel(self.title_container, image=logo_image, text="")
        self.logo_label.pack(pady=5)

        self.title_label = ctk.CTkLabel(self.title_container, text="FILIPINO SURVEY SALARY RECORDS", font=("Lucida Console",35), text_color="#222831", wraplength=400)
        self.title_label.pack(pady=10)

        self.frame_entry = ctk.CTkFrame(self.frame)
        self.frame_entry.grid(row=0, column=1, sticky="nsew", padx=(5,10), pady=10)

        self.entry_containter = ctk.CTkFrame(self.frame_entry, fg_color="transparent")
        self.entry_containter.place(relx=0.5, rely=0.55, anchor="c")

        self.email_entry = ctk.CTkEntry(self.entry_containter, width=280, height=40,placeholder_text="Enter Email")
        self.email_entry.pack(fill="x", pady=10, padx=10)

        self.password_entry = ctk.CTkEntry(self.entry_containter, width=280, height=40,show="*", placeholder_text="Enter Password")
        self.password_entry.pack(fill="x", pady=10, padx=10)

        self.invalid_label = ctk.CTkLabel(self.entry_containter, text="Invalid entry email or password", font=("Lucida Console",12), text_color="red")
        self.invalid_label.pack()
        self.invalid_label.pack_forget()

        self.create_account_btn = ctk.CTkButton(self.entry_containter,command=self.create_event, width=150, height=30,  text="Create Account", font=("Lucida Console", 14),fg_color="#00ADB5", border_color="#393E46")
        self.create_account_btn.pack(side="bottom",pady=(5,30))

        self.or_text = ctk.CTkLabel(self.entry_containter, text="OR", font=("Lucida Console",14))
        self.or_text.pack(side="bottom")

        self.login_btn = ctk.CTkButton(self.entry_containter, width=180, height=40,  text="LOGIN", font=("Lucida Console", 20),fg_color="#00ADB5", border_color="#393E46", command=signin)
        self.login_btn.pack(side="bottom",pady=(40,5))



    def login_event(self):
        print("login")

    def create_event(self):

        def close_create():
            self.create_acc.destroy()
            self.create_account_btn.configure(state="normal")

        def check_entry():
            if self.fname_entry.get() and self.lname_entry.get():
                if self.bday_textlabel.cget("text") != "yyyy/mm/dd":
                    if self.emailCreate_entry.get():
                        if self.passCreate_entry.get() and self.confirmPassCreate_entry.get():
                            if self.passCreate_entry.get() == self.confirmPassCreate_entry.get():
                                self.error_msg.place_forget()
                                self.create_acc.destroy()
                                self.create_account_btn.configure(state="normal")
                                print("proceed")
                            else:
                                self.error_msg.configure(text="Password do not match")
                                self.error_msg.place(relx=0.5, rely=0.87, anchor="c")
                            pass
                        else:
                            self.error_msg.configure(text="Enter Password")
                            self.error_msg.place(relx=0.5, rely=0.87, anchor="c")
                        pass
                    else:
                        self.error_msg.configure(text="Enter Email")
                        self.error_msg.place(relx=0.5, rely=0.87, anchor="c")
                    pass
                else:
                    self.error_msg.configure(text="Enter birthday")
                    self.error_msg.place(relx=0.5, rely=0.87, anchor="c")
                pass
            else:
                self.error_msg.configure(text="Complete name fields")
                self.error_msg.place(relx=0.5, rely=0.87, anchor="c")

        self.create_account_btn.configure(state="disabled")
        win_width = 450
        win_height = 600

        position_X = (self.winfo_screenwidth()/2)
        position_Y = (self.winfo_screenheight()/2)-(win_height/2)

        self.create_acc = ctk.CTkToplevel(self)
        self.create_acc.title("Create Account")
        self.create_acc.geometry("%dx%d+%d+%d" % (win_width, win_height, position_X, position_Y))
        self.create_acc.minsize(win_width, win_height)
        self.create_acc.resizable(0,0)

        self.create_frame =ctk.CTkFrame(self.create_acc, width=win_width, height=win_height)
        self.create_frame.pack(padx=10, pady=10, fill="both")

        self.create_frame.grid_columnconfigure((0,1), weight=1)
        self.create_frame.grid_rowconfigure(13, weight=1)
        self.create_frame.grid_propagate(False)

        self.create_label = ctk.CTkLabel(self.create_frame, text="CREATE YOUR ACCOUNT",font=("Roboto",24))
        self.create_label.grid(row=0, columnspan=2, pady=(30,20))

        self.fname_label = ctk.CTkLabel(self.create_frame, text="First Name: ", font=("Roboto",18))
        self.fname_label.grid(row=1, column=0, sticky="nw",padx=(50,0))

        self.fname_entry = ctk.CTkEntry(self.create_frame, width=100, height=40, placeholder_text="Enter your First Name")
        self.fname_entry.grid(row=2, column=0, sticky="we", padx=(50,5), pady=(0,10))

        self.lname_label = ctk.CTkLabel(self.create_frame, text="Last Name: ", font=("Roboto",18))
        self.lname_label.grid(row=1, column=1, sticky="nw",padx=(5,50))

        self.lname_entry = ctk.CTkEntry(self.create_frame, width=100,height=40, placeholder_text="Enter your Last Name")
        self.lname_entry.grid(row=2, column=1, sticky="we", padx=(0,50), pady=(0,10))

        self.bday_label = ctk.CTkLabel(self.create_frame, text="Birthday: (yyyy/mm/dd)", font=("Roboto",16))
        self.bday_label.grid(row=3, columnspan=2, sticky="nw",padx=50)

        self.bday_textlabel = ctk.CTkLabel(self.create_frame, height=40, text="yyyy/mm/dd", font=("Roboto",18))
        self.bday_textlabel.grid(row=4, columnspan=2, sticky="nsew", padx=50)

        self.select_bday = ctk.CTkButton(self.create_frame,text="Select Date", command=self.show_cal,height=40)
        self.select_bday.grid(row=5, columnspan=2)

        self.emailCreate_label = ctk.CTkLabel(self.create_frame, text="Email: ", font=("Roboto",18))
        self.emailCreate_label.grid(row=6, columnspan=2, sticky="nw", padx=50, pady=(20,0))

        self.emailCreate_entry = ctk.CTkEntry(self.create_frame, height=40, placeholder_text="Enter your email",)
        self.emailCreate_entry.grid(row=7, columnspan=2, sticky="nsew", padx=50, pady=(0,10))

        self.passCreate_label = ctk.CTkLabel(self.create_frame, text="Password: ",font=("Roboto",18))
        self.passCreate_label.grid(row=8, columnspan=2, sticky="nw",padx=50)

        self.passCreate_entry = ctk.CTkEntry(self.create_frame, height=40, placeholder_text="Enter Password", show="*")
        self.passCreate_entry.grid(row=9, columnspan=2, sticky="nsew", padx=50, pady=(0,5))

        self.confirmPassCreate_entry = ctk.CTkEntry(self.create_frame, height=40, placeholder_text="Confirm Password", show="*")
        self.confirmPassCreate_entry.grid(row=10, columnspan=2, sticky="nsew", padx=50, pady=(5,20))

        self.cancel_create = ctk.CTkButton(self.create_frame,text="Cancel", height=40, command=close_create)
        self.cancel_create.grid(row=11, column=0,sticky="w", padx=(50,0), pady=(30,0))

        self.submit_create = ctk.CTkButton(self.create_frame,text="Submit", height=40, command=check_entry)
        self.submit_create.grid(row=11, column=1, sticky="e", padx=(0,50), pady=(30,0))

        self.error_msg = ctk.CTkLabel(self.create_frame, text="Please fill all requirements", font=("Roboto", 18))
        self.error_msg.place(relx=0.5, rely=0.85, anchor="c")
        self.error_msg.place_forget()



    def show_cal(self):
        def get_date():
            print(self.cal.selection_get())
            self.bday_textlabel.configure(text=f"{self.cal.selection_get()}")
            self.cal_frame.destroy()
            self.select_bday.configure(state="normal")
            self.cancel_create.configure(state="normal")


        self.select_bday.configure(state="disabled")
        self.cancel_create.configure(state="disabled")
        import datetime

        mindate= datetime.date(year=1900, day=1, month=1)

        position_X = (self.winfo_screenwidth()/2)
        position_Y = (self.winfo_screenheight()/2)-(400/2)

        self.cal_frame = ctk.CTkToplevel(self)
        self.cal_frame.title("Calendar")
        self.cal_frame.geometry("%dx%d+%d+%d"%(400,400,position_X,position_Y))
        self.cal_frame.resizable(0,0)

        self.cal = Calendar(self.cal_frame, font="Roboto 16", year=2000, month=1, day=1, firstweekday="sunday",
                            mindate=mindate, normalbackground="#EAEAEA", weekendbackground="#F3EFE0")
        self.cal.pack(fill="both", expand=True, padx=5, pady=5)

        self.set_date = ctk.CTkButton(self.cal_frame, text="Set Date", font=("Robot", 16),
                                      command=get_date)
        self.set_date.pack(pady=10)



if __name__ == "__main__":
    app = login_GUI()
    app.mainloop()