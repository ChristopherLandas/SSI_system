try:
    from tkinter import*
    import customtkinter as ctk
    import fitz
    from tkinter.ttk import Progressbar
    from threading import Thread
    import math
    from typing import Optional, Required
except Exception as e:
    print(f"This error occured while importing neccesary modules or library {e}")

class ShowPdf():

    img_object_li = []

    def pdf_view(self,master,width: Optional[int] = 600, height: Optional[int] = 600,
                 pdf_location: Optional[str] = "", bar=True, load="after",
                 zoomDPI: Optional[int] = 72):
        
        self.frame = ctk.CTkFrame(master,width= width,height= height, fg_color='white', corner_radius=5)

        self.scroll_y = ctk.CTkScrollbar(self.frame,orientation="vertical")
        self.scroll_x = ctk.CTkScrollbar(self.frame,orientation="horizontal")

        self.scroll_x.pack(fill="x",side="bottom",padx=(10),)
        self.scroll_y.pack(fill="y",side="right",pady=(10,15),)

        self.percentage_view = 0
        self.percentage_load = ctk.StringVar()

        if bar==True and load=="after":
            #self.display_msg = Label(textvariable=self.percentage_load)
            #self.display_msg.pack(pady=10)

            #self.loading = ctk.CTkProgressBar(self.frame,orientation= HORIZONTAL,mode='determinate')
            #self.loading.pack(side = ctk.TOP,fill='x')
            pass

        self.text = Text(self.frame,yscrollcommand=self.scroll_y.set,xscrollcommand= self.scroll_x.set,width= width,height= height,
                         highlightthickness =0, borderwidth=0, bd=0)
        self.text.pack(padx=(10,0), pady=(10))

        self.scroll_x.configure(command=self.text.xview)
        self.scroll_y.configure(command=self.text.yview)


        def add_img():
            precentage_dicide = 0
            open_pdf = fitz.open(pdf_location)

            for page in open_pdf:
                pix = page.get_pixmap(dpi=zoomDPI)
                pix1 = fitz.Pixmap(pix,0) if pix.alpha else pix
                img = pix1.tobytes("ppm")
                timg = PhotoImage(data = img)
                self.img_object_li.append(timg)
                if bar==True and load=="after":
                    precentage_dicide = precentage_dicide + 1
                    self.percentage_view = (float(precentage_dicide)/float(len(open_pdf))*float(100))
            if bar==True and load=="after":
                #self.loading.pack_forget()
                pass

            
            for i in self.img_object_li:
                self.text.image_create(END,image=i)
                self.text.tag_configure("center", justify='center')
                self.text.tag_add("center", "1.0", "end")
                self.text.configure(state=DISABLED)
             

        def start_pack():
            t1 = Thread(target=add_img)
            t1.start()

        if load=="after":
            master.after(100,start_pack)
            
        else:
            start_pack()

        return self.frame

    
