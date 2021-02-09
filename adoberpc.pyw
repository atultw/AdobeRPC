import tkinter as Tkinter
from tkinter import messagebox

import main


def settoggle():
    if main.toggle:
        main.toggle = False
    elif not main.toggle:
        main.toggle = True


class App:
    def __init__(self):
        self.top = Tkinter.Tk(screenName='AdobeRPC')
        self.refresh()
        self.top.title('AdobeRPC')

        self.top.geometry('400x200')
        self.top.resizable(width=0, height=0)

        self.status = Tkinter.StringVar()
        self.status.set(str(main.toggle))

        txt1 = Tkinter.Label(text='AdobeRPC by a2lya', padx='20', pady='20')
        txt1.pack()

        btn = Tkinter.Button(self.top, text="Toggle on/off", command=self.tg, padx='20', pady='20', background='#29d1e3')
        btn.pack()

        txt2 = Tkinter.Label(textvariable=self.status, background='#00ffff', padx='20', pady='20')
        txt2.pack()

        self.top.mainloop()

    def tg(self):
        settoggle()
        self.status.set(str(main.toggle))
        messagebox.showinfo("Info", "Discord rich presence is now " + str(main.toggle))

    def refresh(self):
        main.update()
        self.top.after(15000, self.refresh)


app = App()
