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

        self.load_users()

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

        self.check_user_exists()

    # showcases/displays the frame of choice
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    # loads up the users data
    def load_users(self):
        global users
        # checks if the save file can be located
        if os.path.exists('user_save.json'):
            # opens the save file and reads its data
            with open('user_save.json', 'r') as file:
                users_data = json.load(file)
                # store the user data as an object into the users dictionary
                for user, user_info in users_data.items():
                    users[user] = UserInfo(user_info['display_name'], user_info['username'], user_info['password'], user_info['stay_logged'])

    # checks if the user already has already been verified (aka 'created')
    def check_user_exists(self):
        if users['user'].username:
            self.username.set(users['user'].username)
            self.password.set(users['user'].password)
            
            # if so, program startup displays the login page
            self.show_frame(LoginPage)
        else:
            # if not, program startup displays the setup page
            self.show_frame(SetupPage)

    # custom serialization of user data to save file
    def custom_serializer(self, obj):
        if isinstance(obj, UserInfo):
            return {
                "display_name": obj.display_name,
                "username": obj.username,
                "password": obj.password,
                "stay_logged": obj.stay_logged
            }
        return obj

class SetupPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.display_name_var = tk.StringVar()
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.confirm_password_var = tk.StringVar()

        self.create_widgets()

    # a collection of widgets used to create the setup page
    def create_widgets(self):
        form_wm = tk.Frame(self)
        form_wm.place(relx=0.5, rely=0.5, anchor='center')
        form_wm.propagate(0)
        form_wm.config(width=600, height=600)

        setup_title = tk.Label(form_wm, font=('helvetica', 32), text='Setup Account')
        display_name_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Display Name:')
        display_name_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.display_name_var)
        display_name_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')
        username_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Username:', borderwidth=2)
        username_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.username_var)
        self.username_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')
        password_subtitle = tk.Label(form_wm, text='Password:', font=('helvetica', 12), borderwidth=2)
        password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.password_var)
        self.password_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')
        confirm_password_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Confirm Password:', borderwidth=2)
        confirm_password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.confirm_password_var)
        self.confirm_password_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')
        setup_submission = tk.Button(form_wm, font=('helvetica', 18), text='Setup', command=self.setup_procedure)

        setup_title.place(x=160, y=50)
        
        display_name_subtitle.place(x=170, y=130)
        display_name_entry.place(x=170, y=150)
        display_name_error.place(x=170, y=180)

        username_subtitle.place(x=170, y=230)
        username_entry.place(x=170, y=250)
        self.username_error.place(x=170, y=280)
        
        password_subtitle.place(x=170, y=330)
        password_entry.place(x=170, y=350)
        self.password_error.place(x=170, y=380)
        
        confirm_password_subtitle.place(x=170, y=430)
        confirm_password_entry.place(x=170, y=450)
        self.confirm_password_error.place(x=170, y=480)
        
        setup_submission.place(x=240, y=550)

    # check if user input is correct
    def validate_setup(self):
        # clears error messages, so only latest form submission based errors are shown
        self.username_error.config(text='')
        self.password_error.config(text='')
        self.confirm_password_error.config(text='')

        # check if username lengths are within 3 to 12 characters long
        if len(self.username_var.get()) < 3 or len(self.username_var.get()) > 12:
            self.username_error.config(text='Invalid Username! Must be between 3 - 12 characters.')
        # check if password is atleast 6 characters long
        elif len(self.password_var.get()) < 6:
            self.password_error.config(text='Invalid Password! Must be 6 or more characters.')
        # check if password confirmation and password matched
        elif self.password_var.get() != self.confirm_password_var.get():
            self.confirm_password_error.config(text='Confirmation Failed! Password and Confirm Password must match.')
        # if successful, sets the username and password (aka 'creates' them)
        else:
            self.controller.username.set(self.username_var.get())
            self.controller.password.set(self.password_var.get())
            return True
        return False
    
    # process the login information
    def setup_procedure(self):
        # if validation goes through, stores login details to save file
        if self.validate_setup():
            users['user'].username = self.controller.username.get()
            users['user'].password = self.controller.password.get()

            json_object = json.dumps(users, indent=4, default=self.controller.custom_serializer)

            with open('user_save.json', 'w') as outfile:
                outfile.write(json_object)

            # afterwards, redirects to login page
            self.controller.show_frame(LoginPage)

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.create_widgets()

    # collection of widgets for the login page
    def create_widgets(self):
        login_wm = tk.Frame(self)
        login_wm.place(relx=0.5, rely=0.5, anchor='center')
        login_wm.propagate(0)
        login_wm.config(width=600, height=600)

        login_title = tk.Label(login_wm, font=('helvetica', 32), text='Login to BetterLife')
        username_subtitle = tk.Label(login_wm, font=('helvetica', 12), text='Username:', borderwidth=2)
        username_entry = tk.Entry(login_wm, font=('helvetica', 18), textvariable=self.username_var)
        self.username_error = tk.Label(login_wm, font=('helvetica', 10), foreground='red')
        password_subtitle = tk.Label(login_wm, font=('helvetica', 12), text='Password:', borderwidth=2)
        password_entry = tk.Entry(login_wm, font=('helvetica', 18), textvariable=self.password_var)
        self.password_error = tk.Label(login_wm, font=('helvetica', 10), foreground='red')
        login_submission = tk.Button(login_wm, font=('helvetica', 18), text='Login', command=self.validate_login)

        login_title.place(x=130, y=50)
        username_subtitle.place(x=170, y=130)
        username_entry.place(x=170, y=150)
        self.username_error.place(x=170, y=180)
        password_subtitle.place(x=170, y=230)
        password_entry.place(x=170, y=250)
        self.password_error.place(x=170, y=280)
        login_submission.place(x=260, y=350)

    # process and validate login credentials
    def validate_login(self):
        self.username_error.config(text='')
        self.password_error.config(text='')

        if self.username_var.get() != self.controller.username.get():
            self.username_error.config(text='Incorrect Username! Try Again.')
        elif self.password_var.get() != self.controller.password.get():
            self.password_error.config(text='Invalid Password! Try Again.')
        else:
            self.controller.show_frame(ProfilePage)

class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.create_widgets()

    # collection of widgets for the Profile Page
    def create_widgets(self):

        menu_bar = tk.Frame(self, background='blue', width=200, height=800)
        search_bar = tk.Frame(self, background='grey', width=1000, height=50)
        user_section = tk.Frame(self, background='red', width=1000, height=300)
        something_section = tk.Frame(self, background='black', width=600, height=250)
        badges_section = tk.Frame(self, background='magenta', width=600, height=200)
        graph_section = tk.Frame(self, background='brown', width=300, height=400)

        menu_bar.grid(row=0, rowspan=4, column=0, sticky='nswe')
        search_bar.grid(row=0, column=1, columnspan=2, sticky='nswe')
        user_section.grid(row=1, column=1, columnspan=2, sticky='nswe')
        something_section.grid(row=2, column=1, sticky='nswe')
        badges_section.grid(row=3, column=1, sticky='nswe')
        graph_section.grid(row=2, rowspan=2, column=2, sticky='nswe')

        # def boop(event):
        #     print('ya clicked me!')

        # # temp
        # welcome = tk.Label(self, text='Welcome to the Profile Page')
        # welcome.pack()

        # click_me = tk.Label(text='Click Me!', master=self)
        # click_me.pack()
        # click_me.bind("<Button-1>", boop)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()