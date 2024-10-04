import tkinter as tk
import json
import os
from userinfo import UserInfo

users = {}

class MainApp(tk.Tk):
    # initialise main app class
    def __init__(self, *args, **kwargs):
        # initialise Tk class
        tk.Tk.__init__(self, *args, **kwargs)
        # create container
        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.geometry('1200x800')

        # login variables
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # intialise frames to an empty array
        self.frames = {}

        # iterate through the tuple that consists of frames (pages)
        for F in (SetupPage, LoginPage, ProfilePage):
            frame = F(container, self)
            # initialise frame of each page's object
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nswe')

        self.show_frame(SetupPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    def custom_serializer(self, obj):
        if isinstance(obj, UserInfo):
            return {
                "username": obj.username,
                "password": obj.password,
                "stay_logged": obj.stay_logged
            }
        return obj

class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        form_wm = tk.Frame(self)
        form_wm.place(relx=0.5, rely=0.5, anchor='center')
        form_wm.propagate(0)
        form_wm.config(width=600, height=600)

        setup_title = tk.Label(form_wm, text='Setup Account', font=('helvetica', 32))
        username_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Username:', borderwidth=2)
        username_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.username_var)
        password_subtitle = tk.Label(form_wm, text='Password:', font=('helvetica', 12), borderwidth=2)
        password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.password_var)
        confirm_password_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Confirm Password:', borderwidth=2)
        confirm_password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.confirm_password_var)
        setup_submission = tk.Button(form_wm, text='Proceed')

        setup_title.place(x=160, y=50)
        username_subtitle.place(x=170, y=130)
        username_entry.place(x=170, y=150)
        password_subtitle.place(x=170, y=230)
        password_entry.place(x=170, y=250)
        confirm_password_subtitle.place(x=170, y=330)
        confirm_password_entry.place(x=170, y=350)
        setup_submission.place(x=240, y=450)

    # check if user input is correct
    def validate_setup(self):
        # check if input lengths are within bounds
        if len(self.username_var.get()) < 3 or len(self.username_var.get()) > 12 or len(self.password_var.get()) < 6:
            print('Invalid inputs!')
        elif self.password_var.get() != self.confirm_password_var.get():
            print('passwords confirmation failed!')
        else:
            self.controller.username.set(self.username_var.get())
            self.controller.password.set(self.password_var.get())
            return True
        return False


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl1 = tk.Label(self, text='poop')
        lbl1.pack()

class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        lbl2 = tk.Label(self, text='wee')
        lbl2.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()