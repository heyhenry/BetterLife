import tkinter as tk
import json
import os
from userinfo import UserInfo
from PIL import Image, ImageTk
from workout import Workout
from exercise import Exercise
from datetime import date

# note to self for next session: 
# maybe look towards simplifying the goals for the time being. 
# Then expand upon completion of a goal. I.e.in workouts, just track weight based workouts. forget about running, yoga, hiking for the time being.
# If you agree tomorrow, then update the readme document related to deliverables. Maybe even just make a more compact document detailing so.
# I.e. Brief Desc, Goal of App, Motivation of App, Deliverables, Future Expansion Deliverables.

users = {}
workouts = {}

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

        self.geometry('1200x800+350+100')

        self.load_users()
        self.load_workouts()

        # intialise frames to an empty array
        self.frames = {}

        # iterate through the tuple that consists of frames (pages)
        for F in (SetupPage, LoginPage, ProfilePage, SettingsPage, WorkoutPage, HabitsPage, NutritionPage):
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

    def load_workouts(self):
        global workouts
        if os.path.exists('workouts_save.json'):
            with open('workouts_save.json', 'r') as file:
                workouts_data = json.load(file)
                for workout, workout_info in workouts_data.items():
                    workouts[workout] = Workout(workout_info['date'], workout_info['time_spent'], workout_info['exercise_list'])

    # checks if the user already has already been verified (aka 'created')
    def check_user_exists(self):
        if users['user'].username:
            # if user exists, then...
            # if user has toggled on stay_logged status, then redirect to Profile page upon startup
            if users['user'].stay_logged == True:
                self.show_frame(ProfilePage)
            # else, redirect to the Login page upon startup
            else:
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
        elif isinstance(obj, Workout):
            return {
                "date": obj.date,
                "time_spent": obj.time_spent,
                "exercise_list": obj.exercise_list
            }
        elif isinstance(obj, Exercise):
            return {
                "exercise_name": obj.exercise_name,
                "set_count": obj.set_count,
                "rep_count": obj.rep_count,
                "weight_used": obj.weight_used
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
        
        self.password_privacy = False

        self.create_widgets()

    # a collection of widgets used to create the setup page
    def create_widgets(self):
        form_wm = tk.Frame(self, highlightbackground='black', highlightthickness=2)
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
        self.password_entry = tk.Entry(form_wm, font=('helvetica', 18), textvariable=self.password_var)
        password_mask_btn = tk.Button(form_wm, font=('helvetica', 12), text='Show Password', command=self.mask_password_toggle)
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
        self.password_entry.place(x=170, y=350)
        password_mask_btn.place(x=450, y=350)
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

            # create updated json data into json object
            json_object = json.dumps(users, indent=4, default=self.controller.custom_serializer)

            # open the json save file and rewrite with updated json data information via json object
            with open('user_save.json', 'w') as outfile:
                outfile.write(json_object)

            # redirect to the login page upon completion
            self.controller.show_frame(LoginPage)

    # mask password
    def mask_password_toggle(self):
        if self.password_privacy == False:
            self.password_entry.config(show='*')
            self.password_privacy = True
        else:
            self.password_entry.config(show='')
            self.password_privacy = False

class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.password_privacy = False

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
        self.password_entry = tk.Entry(login_wm, font=('helvetica', 18), textvariable=self.password_var)
        password_mask_btn = tk.Button(login_wm, font=('helvetica', 12), text='Show Password', command=self.mask_password_toggle)
        self.password_error = tk.Label(login_wm, font=('helvetica', 10), foreground='red')
        login_submission = tk.Button(login_wm, font=('helvetica', 18), text='Login', command=self.validate_login)

        login_title.place(x=130, y=50)
        username_subtitle.place(x=170, y=130)
        username_entry.place(x=170, y=150)
        self.username_error.place(x=170, y=180)
        password_subtitle.place(x=170, y=230)
        self.password_entry.place(x=170, y=250)
        password_mask_btn.place(x=450, y=250)
        self.password_error.place(x=170, y=280)
        login_submission.place(x=260, y=350)

    # process and validate login credentials
    def validate_login(self):
        self.username_error.config(text='')
        self.password_error.config(text='')

        if self.username_var.get() != users['user'].username:
            self.username_error.config(text='Incorrect Username! Try Again.')
        elif self.password_var.get() != users['user'].password:
            self.password_error.config(text='Invalid Password! Try Again.')
        else:
            self.controller.show_frame(ProfilePage)
    # mask password input field
    def mask_password_toggle(self):
        if self.password_privacy == False:
            self.password_entry.config(show="*")
            self.password_privacy = True
        else:
            self.password_entry.config(show="")
            self.password_privacy = False

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
    # menu bar for all pages
    def create_menu_bar(self):

        # redirects the page based on label clicked
        def redirect_page(mouse_event, page_choice):
            if page_choice == 'profile':
                self.controller.show_frame(ProfilePage)
            elif page_choice == 'workout':
                self.controller.show_frame(WorkoutPage)
            elif page_choice == 'habits':
                self.controller.show_frame(HabitsPage)
            elif page_choice == 'nutrition':
                self.controller.show_frame(NutritionPage)
            elif page_choice == 'settings':
                self.controller.show_frame(SettingsPage)

        # changes widget's text to a highlighted colour upon hovering over with mouse
        def on_hover(mouse_event, widget_name):
            widget_name.config(foreground='white', font=('helvetica', 18, 'underline'))
        
        # changes widget's text back to original colour upon hovering over with mouse
        def on_exit_hover(mouse_event, widget_name):
            widget_name.config(foreground='black', font=('helvetica', 18))

        # toggling the 'stay logged in' status
        def toggle_status(mouse_event, widget_label):
            if users['user'].stay_logged == False:
                widget_label.config(image=img_on)
                users['user'].stay_logged = True
            else:
                widget_label.config(image=img_off)
                users['user'].stay_logged = False

            json_object = json.dumps(users, indent=4, default=self.controller.custom_serializer)

            with open('user_save.json', 'w') as outfile:
                outfile.write(json_object)

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

        profile_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Profile', background='blue', activeforeground='white')
        workout_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Workout', background='blue')
        habits_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Habits', background='blue')
        nutrition_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Nutrition', background='blue')
        settings_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Settings', background='blue')        

        max_size = (60, 60)

        img_on = Image.open('ui_assets/switch-on.png')
        img_on.thumbnail(max_size)
        img_on = ImageTk.PhotoImage(img_on)

        img_off = Image.open('ui_assets/switch-off.png')
        img_off.thumbnail(max_size)
        img_off = ImageTk.PhotoImage(img_off)

        logged_status_text = tk.Label(menu_bar, font=('helvetica', 12, 'bold'), text='Stay logged in:', background='blue')
        logged_status = tk.Label(menu_bar, image=img_off, background='blue')
        logged_status.on_photo = img_on
        logged_status.off_photo = img_off

        app_icon.place(x=0, y=0)
        
        profile_btn.place(x=50, y=300)
        workout_btn.place(x=50, y=350)
        habits_btn.place(x=50, y=400)
        nutrition_btn.place(x=50, y=450)
        settings_btn.place(x=50, y=500)

        logged_status_text.place(x=40, y=650) #w=120
        logged_status.place(x=60, y=680)

        # bind actions
        profile_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'profile'))
        workout_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'workout'))
        habits_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'habits'))
        nutrition_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'nutrition'))
        settings_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'settings'))

        profile_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, profile_btn))
        profile_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, profile_btn))

        workout_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, workout_btn))
        workout_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, workout_btn))

        habits_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, habits_btn))
        habits_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, habits_btn))

        nutrition_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, nutrition_btn))
        nutrition_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, nutrition_btn))

        settings_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, settings_btn))
        settings_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, settings_btn))

        logged_status.bind('<Button-1>', lambda mouse_event: toggle_status(mouse_event, logged_status))

        # starts page with correct logged in status
        if users['user'].stay_logged == False:
            logged_status.config(image=img_off)
        else:
            logged_status.config(image=img_on)

    # widgets contained in the search bar
    def create_search_bar(self):
        search_bar = tk.Frame(self, background='grey', width=1000, height=50)
        search_bar.grid(row=0, column=1, columnspan=2, sticky='nswe')

        search_bar_entry = tk.Entry(search_bar, font=('helvetica', 18))
        logout_btn = tk.Button(search_bar, text='Logout', command=lambda:self.controller.show_frame(LoginPage))
        
        search_bar_entry.place(x=380, y=25, anchor='center', width=700)
        logout_btn.place(x=950, y=25, anchor='center')
    
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
        cancel_submission = tk.Button(update_wm, font=('helvetica', 18), text='Cancel', command=self.cancel)

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

        update_submission.place(x=250, y=450)
        cancel_submission.place(x=450, y=450)

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

    # resets input field values to original pre-redirect to profile page
    def cancel(self):
        self.display_name_var.set(users['user'].display_name)
        self.username_var.set(users['user'].username)
        self.password_var.set(users['user'].password)
        self.confirm_password_var.set(users['user'].password)

        self.controller.show_frame(ProfilePage)

class WorkoutPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.create_menu_bar()
        self.create_search_bar()
        self.create_title_bar()
        self.workout_form()
        self.weight_graph()
        self.time_graph()

    # menu bar for all pages
    def create_menu_bar(self):
        # redirects the page based on label clicked
        def redirect_page(mouse_event, page_choice):
            if page_choice == 'profile':
                self.controller.show_frame(ProfilePage)
            elif page_choice == 'workout':
                self.controller.show_frame(WorkoutPage)
            elif page_choice == 'habits':
                self.controller.show_frame(HabitsPage)
            elif page_choice == 'nutrition':
                self.controller.show_frame(NutritionPage)
            elif page_choice == 'settings':
                self.controller.show_frame(SettingsPage)

        # changes widget's text to a highlighted colour upon hovering over with mouse
        def on_hover(mouse_event, widget_name):
            widget_name.config(foreground='white', font=('helvetica', 18, 'underline'))
        
        # changes widget's text back to original colour upon hovering over with mouse
        def on_exit_hover(mouse_event, widget_name):
            widget_name.config(foreground='black', font=('helvetica', 18))

        # toggling the 'stay logged in' status
        def toggle_status(mouse_event, widget_label):
            if users['user'].stay_logged == False:
                widget_label.config(image=img_on)
                users['user'].stay_logged = True
            else:
                widget_label.config(image=img_off)
                users['user'].stay_logged = False

            json_object = json.dumps(users, indent=4, default=self.controller.custom_serializer)

            with open('user_save.json', 'w') as outfile:
                outfile.write(json_object)

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

        profile_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Profile', background='blue', activeforeground='white')
        workout_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Workout', background='blue')
        habits_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Habits', background='blue')
        nutrition_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Nutrition', background='blue')
        settings_btn = tk.Label(menu_bar, font=('helvetica', 18), text='Settings', background='blue')        

        max_size = (60, 60)

        img_on = Image.open('ui_assets/switch-on.png')
        img_on.thumbnail(max_size)
        img_on = ImageTk.PhotoImage(img_on)

        img_off = Image.open('ui_assets/switch-off.png')
        img_off.thumbnail(max_size)
        img_off = ImageTk.PhotoImage(img_off)

        logged_status_text = tk.Label(menu_bar, font=('helvetica', 12, 'bold'), text='Stay logged in:', background='blue')
        logged_status = tk.Label(menu_bar, image=img_off, background='blue')
        logged_status.on_photo = img_on
        logged_status.off_photo = img_off

        app_icon.place(x=0, y=0)
        
        profile_btn.place(x=50, y=300)
        workout_btn.place(x=50, y=350)
        habits_btn.place(x=50, y=400)
        nutrition_btn.place(x=50, y=450)
        settings_btn.place(x=50, y=500)

        logged_status_text.place(x=40, y=650) #w=120
        logged_status.place(x=60, y=680)

        # bind actions
        profile_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'profile'))
        workout_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'workout'))
        habits_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'habits'))
        nutrition_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'nutrition'))
        settings_btn.bind("<Button-1>", lambda mouse_event: redirect_page(mouse_event,'settings'))

        profile_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, profile_btn))
        profile_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, profile_btn))

        workout_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, workout_btn))
        workout_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, workout_btn))

        habits_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, habits_btn))
        habits_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, habits_btn))

        nutrition_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, nutrition_btn))
        nutrition_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, nutrition_btn))

        settings_btn.bind("<Enter>", lambda mouse_event: on_hover(mouse_event, settings_btn))
        settings_btn.bind("<Leave>", lambda mouse_event: on_exit_hover(mouse_event, settings_btn))

        logged_status.bind('<Button-1>', lambda mouse_event: toggle_status(mouse_event, logged_status))

        # starts page with correct logged in status
        if users['user'].stay_logged == False:
            logged_status.config(image=img_off)
        else:
            logged_status.config(image=img_on)

    # widgets contained in the search bar
    def create_search_bar(self):
        search_bar = tk.Frame(self, background='grey', width=1000, height=50)
        search_bar.grid(row=0, column=1, columnspan=2, sticky='nswe')

        search_bar_entry = tk.Entry(search_bar, font=('helvetica', 18))
        logout_btn = tk.Button(search_bar, text='Logout', command=lambda:self.controller.show_frame(LoginPage))

        search_bar_entry.place(x=380, y=25, anchor='center', width=700)
        logout_btn.place(x=950, y=25, anchor='center')

    def create_title_bar(self):
        title_bar = tk.Frame(self, background='orange', width=100, height=150)
        title_bar.grid(row=1, column=1, columnspan=2, sticky='nswe')

        workout_title = tk.Label(title_bar, font=('helvetica', 48, 'bold'), text='Workout Page', background='orange')
        workout_title.place(relx=0.5, rely=0.5, anchor='center')

    def workout_form(self):
        workout_wm = tk.Frame(self, background='red', width=500, height=600, highlightbackground='black', highlightthickness=2)
        workout_wm.grid(row=2, rowspan=2, column=1, sticky='nswe')

        exercise_name_var = tk.StringVar()
        set_count_var = tk.StringVar()
        rep_count_var = tk.StringVar()
        weight_used_var = tk.StringVar()

        time_spent_var = tk.StringVar()

        today_date = date.today()
        today_date = today_date.strftime('%d-%m-%Y')

        # add exercises to the workout entry for the day
        def add_exercise_entry():
            # check if workout entry for the day has been created, if not create one with today's date being the key
            if today_date not in workouts:
                workouts[today_date] = Workout(today_date, 0, [])

            # update the workout entry for the day with new exercises performed during the day
            new_exercise = Exercise(exercise_name_var.get(), set_count_var.get(), rep_count_var.get(), weight_used_var.get())
            # each new exercise will then be stored inside the exercise_list list as unique entries (still within the workout entry of the day)
            workouts[today_date].exercise_list.append(new_exercise)

            # updates the save file with the latest data
            json_object = json.dumps(workouts, indent=4, default=self.controller.custom_serializer)

            with open('workouts_save.json', 'w') as outfile:
                outfile.write(json_object)

            # displays notification message indicating that the exercise entry has been added
            exercise_added_notif.config(text='Exercise has been added!')
            # after a 1 second delay, it will erase the notificaiton display
            workout_wm.after(1000, erase_exercise_notification)

        # add the time spent during exercises in the workout entry for the day
        def add_time_entry():
            # check if workout entry for the day has been created, if not create one with today's date being the key
            if today_date not in workouts:
                workouts[today_date] = Workout(today_date, 0, [])

            # update the current time_spent with addition of new time spent
            workouts[today_date].time_spent += int(time_spent_var.get())

            # updates the save file with the latest data
            json_object = json.dumps(workouts, indent=4, default=self.controller.custom_serializer)

            with open('workouts_save.json', 'w') as outfile:
                outfile.write(json_object)

        # erases the exercise notification message
        def erase_exercise_notification():
            exercise_added_notif.config(text='')

        workout_form_title = tk.Label(workout_wm, font=('helvetica', 18), text='Workout Entry (Daily)', background='red')
        
        exercise_name = tk.Label(workout_wm, font=('helvetica', 12), text='Exercise Name:', background='red')
        exercise_name_entry = tk.Entry(workout_wm, font=('helvetica', 18), textvariable=exercise_name_var)

        set_count = tk.Label(workout_wm, font=('helvetica', 12), text='Set Count:', background='red')
        set_count_entry = tk.Entry(workout_wm, font=('helvetica', 18), textvariable=set_count_var)

        rep_count = tk.Label(workout_wm, font=('helvetica', 12), text='Rep Count:', background='red')
        rep_count_entry = tk.Entry(workout_wm, font=('helvetica', 18), textvariable=rep_count_var)

        weight_used = tk.Label(workout_wm, font=('helvetica', 12), text='Weight Used:', background='red')
        weight_used_entry = tk.Entry(workout_wm, font=('helvetica', 18), textvariable=weight_used_var)

        add_exercise = tk.Button(workout_wm, font=('helvetica', 12), text='Add Exercise', command=add_exercise_entry)
        exercise_added_notif = tk.Label(workout_wm, font=('helvetica', 12), background='red', foreground='green')

        time_spent = tk.Label(workout_wm, font=('helvetica', 12), text='Time Spent (in Mins):', background='red')
        time_spent_entry = tk.Entry(workout_wm, font=('helvetica', 18), textvariable=time_spent_var)

        add_time = tk.Button(workout_wm, font=('helvetica', 12), text='Add Time', command=add_time_entry)

        workout_form_title.place(x=130, y=10)

        exercise_name.place(x=120, y=60)
        exercise_name_entry.place(x=120, y=90)

        set_count.place(x=120, y=130)
        set_count_entry.place(x=120, y=160)

        rep_count.place(x=120, y=200)
        rep_count_entry.place(x=120, y=230)

        weight_used.place(x=120, y=270)
        weight_used_entry.place(x=120, y=300)

        add_exercise.place(x=200, y=340)
        exercise_added_notif.place(x=170, y=380)

        time_spent.place(x=120, y=420)
        time_spent_entry.place(x=120, y=450)

        add_time.place(x=200, y=490)

    def weight_graph(self):
        graph_one = tk.Frame(self, background='magenta', width=500, height=300)
        graph_one.grid(row=2, column=2, sticky='nswe')

    def time_graph(self):
        graph_two = tk.Frame(self, background='green', width=500, height=300)
        graph_two.grid(row=3, column=2, sticky='nswe')

class HabitsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        temp_lbl = tk.Label(self, text='Welcome to the Habits Page!')
        temp_lbl.pack()

class NutritionPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        temp_lbl = tk.Label(self, text='Welcome to the Nutrition Page!')
        temp_lbl.pack()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()