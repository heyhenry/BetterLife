import tkinter as tk
import json
import os
from userinfo import UserInfo
from PIL import Image, ImageTk

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

        # login 
        self.display_name = tk.StringVar()
        self.username = tk.StringVar()
        self.password = tk.StringVar()

        # intialise frames to an empty array
        self.frames = {}

        # iterate through the tuple that consists of frames (pages)
        for F in (SetupPage, LoginPage, ProfilePage, SettingsPage):
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
            self.show_frame(SettingsPage)
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
        self.display_name_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')

        username_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Username:', borderwidth=2)
        username_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.username_var)
        self.username_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')

        password_subtitle = tk.Label(form_wm, text='Password:', font=('helvetica', 12), borderwidth=2)
        password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.password_var)
        self.password_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')

        confirm_password_subtitle = tk.Label(form_wm, font=('helvetica', 12), text='Confirm Password:', borderwidth=2)
        confirm_password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.confirm_password_var)
        self.confirm_password_error = tk.Label(form_wm, font=('helvetica', 10), foreground='red')

        setup_submission = tk.Button(form_wm, font=('helvetica', 18), text='Setup', command=self.validate_setup_information)

        setup_title.place(x=160, y=50)
        
        display_name_subtitle.place(x=170, y=130)
        display_name_entry.place(x=170, y=150)
        self.display_name_error.place(x=170, y=180)

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
    def validate_setup_information(self):
        # clears error messages, so only latest form submission based errors are shown
        self.display_name_error.config(text='')
        self.username_error.config(text='')
        self.password_error.config(text='')
        self.confirm_password_error.config(text='')

        # check if name length is within 3 to 12 characters
        if len(self.display_name_var.get()) < 1 or len(self.display_name_var.get()) > 12:
            self.display_name_error.config(text='Invalid Name! Must be between 3 - 12 characters.')
        # check if username lengths is within 3 to 12 characters 
        elif len(self.username_var.get()) < 3 or len(self.username_var.get()) > 12:
            self.username_error.config(text='Invalid Username! Must be between 3 - 12 characters.')
        # check if password is atleast 6 characters long
        elif len(self.password_var.get()) < 6:
            self.password_error.config(text='Invalid Password! Must be 6 or more characters.')
        # check if password confirmation and password matched
        elif self.password_var.get() != self.confirm_password_var.get():
            self.confirm_password_error.config(text='Confirmation Failed! Password and Confirm Password must match.')
        # if successful, sets the username and password (aka 'creates' them)
        else:
            users['user'].display_name = self.display_name_var.get()
            users['user'].username = self.username_var.get()
            users['user'].password = self.password_var.get()

            json_object = json.dumps(users, indent=4, default=self.controller.custom_serializer)

            with open('user_save.json', 'w') as outfile:
                outfile.write(json_object)

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
        login_wm = tk.Frame(self, highlightbackground='black', highlightthickness=2)
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

        self.create_menu_bar()
        self.create_search_bar()
        self.create_user_section()
        self.create_something_section()
        self.create_badges_section()
        self.create_graph_section()

    # collection of widgets for the Profile Page
    # widgets contained in the menu bar
    def create_menu_bar(self):
        menu_bar = tk.Frame(self, background='blue', width=200, height=800)
        menu_bar.grid(row=0, rowspan=4, column=0, sticky='nswe')

        # get image from location
        app_icon_name_img = Image.open('./ui_assets/logo_white.png')
        # resize image
        app_icon_name_img.thumbnail((200,200))
        # convert image to be compatible in tkinter
        app_icon_name_img = ImageTk.PhotoImage(app_icon_name_img)
        
        app_icon = tk.Label(menu_bar, image=app_icon_name_img)
        # line of code below required to have a reference so the image doesn't get collected as garbage
        app_icon.image = app_icon_name_img
        app_icon.place(x=0, y=0)

        temp_settings_btn = tk.Button(menu_bar, text='Settings', command=lambda:self.controller.show_frame(SettingsPage))
        temp_settings_btn.place(x=50, y=300)

    # widgets contained in the search bar
    def create_search_bar(self):
        search_bar = tk.Frame(self, background='grey', width=1000, height=50)
        search_bar.grid(row=0, column=1, columnspan=2, sticky='nswe')
    
    # widgets contained in the user section
    def create_user_section(self):
        user_section = tk.Frame(self, background='red', width=1000, height=300)
        user_section.grid(row=1, column=1, columnspan=2, sticky='nswe')
    
    # widgets contained in the something section
    def create_something_section(self):
        something_section = tk.Frame(self, background='black', width=600, height=250)
        something_section.grid(row=2, column=1, sticky='nswe')
    
    # widgets contained in the badges section
    def create_badges_section(self):
        badges_section = tk.Frame(self, background='magenta', width=600, height=200)
        badges_section.grid(row=3, column=1, sticky='nswe')
    
    # widgets contained in the badges section
    def create_graph_section(self):
        graph_section = tk.Frame(self, background='brown', width=300, height=400)
        graph_section.grid(row=2, rowspan=2, column=2, sticky='nswe')

        # def boop(event):
        #     print('ya clicked me!')

        # # temp
        # welcome = tk.Label(self, text='Welcome to the Profile Page')
        # welcome.pack()

        # click_me = tk.Label(text='Click Me!', master=self)
        # click_me.pack()
        # click_me.bind("<Button-1>", boop)

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.display_name_var = tk.StringVar(value=users['user'].display_name)
        self.username_var = tk.StringVar(value=users['user'].username)
        self.password_var = tk.StringVar(value=users['user'].password)
        self.confirm_password_var = tk.StringVar(value=users['user'].password)

        self.create_widgets()

    def create_widgets(self):
        update_wm = tk.Frame(self, highlightbackground='black', highlightthickness=2)
        update_wm.place(relx=0.5, rely=0.5, anchor='center')
        update_wm.propagate(0)
        update_wm.config(width=800, height=600)

        settings_title = tk.Label(update_wm, font=('helvetiva', 32), text='Settings | Update Details')
         
        display_name_subtitle = tk.Label(update_wm, font=('helvetica', 12), text='Display Name:')
        display_entry = tk.Entry(update_wm, font=('helvetica', 18), textvariable=self.display_name_var)
        self.display_name_error = tk.Label(update_wm, font=('helvetica', 10), foreground='red')

        username_subtitle = tk.Label(update_wm, font=('helvetica', 12), text='Username:')
        username_entry = tk.Entry(update_wm, font=('helvetica', 18), textvariable=self.username_var)
        self.username_error = tk.Label(update_wm, font=('helvetica', 10), foreground='red')

        password_subtitle = tk.Label(update_wm, font=('helvetica', 12), text='Password:')
        password_entry = tk.Entry(update_wm, font=('helvetica', 18), textvariable=self.password_var)
        self.password_error = tk.Label(update_wm, font=('helvetica', 10), foreground='red')

        confirm_password_subtitle = tk.Label(update_wm, font=('helvetica', 12), text='Confirm Password:')
        confirm_password_entry = tk.Entry(update_wm, font=('helvetica', 18), textvariable=self.confirm_password_var)

        update_submission = tk.Button(update_wm, font=('helvetica', 18), text='Update Details', command=self.validate_update_information)

        settings_title.place(x=170, y=50)
    
        display_name_subtitle.place(x=270, y=130)
        display_entry.place(x=270, y=150)
        self.display_name_error.place(x=270, y=190)

        username_subtitle.place(x=270, y=230)
        username_entry.place(x=270, y=250)
        self.username_error.place(x=270, y=290)

        password_subtitle.place(x=100, y=330)
        password_entry.place(x=100, y=350)
        self.password_error.place(x=230, y=390)

        confirm_password_subtitle.place(x=450, y=330)
        confirm_password_entry.place(x=450, y=350)

        update_submission.place(x=300, y=450)

    # check to ensure all rules are met for user data entry *Refer to login page for indepth understanding
    def validate_update_information(self):
        self.display_name_error.config(text='')
        self.username_error.config(text='')
        self.password_error.config(text='')

        if len(self.display_name_var.get()) < 1 or len(self.display_name_var.get()) > 12:
            self.display_name_error.config(text='Invalid Name! Must be between 3 - 12 characters.')
        elif len(self.username_var.get()) < 3 or len(self.username_var.get()) > 12:
            self.username_error.config(text='Invalid Username! Must be between 3 - 12 characters.')
        elif len(self.password_var.get()) < 6:
            self.password_error.config(text='Invalid Password! Must be 6 or more characters.')
        elif self.password_var.get() != self.confirm_password_var.get():
            self.password_error.config(text='Confirmation Failed! Password and Confirm Password must match.')
        else:
            users['user'].display_name = self.display_name_var.get()
            users['user'].username = self.username_var.get()
            users['user'].password = self.password_var.get()

            json_object = json.dumps(users, indent=4, default=self.controller.custom_serializer)

            with open('user_save.json', 'w') as outfile:
                outfile.write(json_object)

            self.controller.show_frame(LoginPage)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()