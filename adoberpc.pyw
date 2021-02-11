import os
import sys
import tkinter as tk
from datetime import datetime
from tkinter import messagebox

from PIL import ImageTk, Image

import main


def settoggle():
    if main.toggle:
        main.toggle = False
    elif not main.toggle:
        main.toggle = True


def configopen():
    os.startfile('config.txt')


class App:
    def __init__(self):
        with open("logging/log" + datetime.now().strftime("%m%d%Y%H%M%S") + ".txt", 'w+') as sys.stdout:
            print('booting up!')

            def restart():
                python = sys.executable
                os.execl(python, python, *sys.argv)

            self.top = tk.Tk(screenName='AdobeRPC')
            self.top.configure(background='#556066')

            self.refresh()
            self.top.title('AdobeRPC')

            self.top.geometry('310x500')
            self.top.resizable(width=0, height=0)

            self.status = tk.StringVar()
            self.status.set("Currently Active")

            canvas = tk.Canvas(bg="#556066", width=100, height=100)
            canvas.pack()
            img = Image.open("favicon.png")  # PIL solution
            img = img.resize((100, 100), Image.ANTIALIAS)  # The (250, 250) is (height, width)
            img = ImageTk.PhotoImage(img)  # convert to PhotoImage
            image = canvas.create_image(62, 62, anchor='center', image=img)
            # image.pack() # canvas objects do not use pack() or grid()

            txt1 = tk.Label(text='AdobeRPC', font="Arial 20", background='#fff', width=16)

            btn = tk.Button(self.top, text="Toggle on/off", command=self.tg, background='#a6d1ff', font="Arial",
                            width=28)

            txt2 = tk.Label(textvariable=self.status, background='#b2cad1', font="Arial", width=28)

            btn2 = tk.Button(self.top, text="Open Configuration", command=configopen, font="Arial", width=28)

            btn2 = tk.Button(self.top, text="Restart Program", command=restart, font="Arial", width=28)

            self.top.iconbitmap('favicon.ico')

            for child in self.top.winfo_children():
                child.grid_configure(padx=10, pady=10, ipadx='10', ipady='10')

            # self.top.protocol("WM_DELETE_WINDOW", self.top.iconify)

            self.top.mainloop()

    def tg(self):
        settoggle()
        if main.toggle:
            self.status.set('Currently active')
        if not main.toggle:
            self.status.set('Currently not updating')

        messagebox.showinfo("Attention", "Discord rich presence is now " + str(main.toggle))

    def refresh(self):
        main.update()
        self.top.after(15000, self.refresh)


app = App()
