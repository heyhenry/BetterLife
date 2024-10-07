import tkinter as tk
from workout import Workout
from exercise import Exercise
import json

workouts = {'date_key' : Workout('test-date', '', {})}

root = tk.Tk()

def custom_serializer(obj):
    if isinstance(obj, Workout):
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


def add_exercise_entry():
    new_exercise = Exercise(exercise_name_var.get(), set_count_var.get(), rep_count_var.get(), weight_used_var.get())
    workouts['date_key'].exercise_list[new_exercise.exercise_name] = new_exercise

    # print(workouts['date_key'].exercise_list['bench press'])

    json_obj = json.dumps(workouts, indent=4, default=custom_serializer)

    with open('workout_save.json', 'w') as outfile:
        outfile.write(json_obj)

def add_time_entry():

    print(workouts['date_key'].time_spent)

exercise_name_var = tk.StringVar()
set_count_var = tk.StringVar()
rep_count_var = tk.StringVar()
weight_used_var = tk.StringVar()

time_spent_var = tk.StringVar()

form_wm = tk.Frame(root, width=600, height=600)
form_wm.propagate(0)
form_wm.pack(fill='both', expand=True, anchor='center')

# <----->

title = tk.Label(form_wm, text='Add Workout')

exercise_name = tk.Label(form_wm, text='Exercise Name:')
exercise_name_entry = tk.Entry(form_wm, textvariable=exercise_name_var)

set_count = tk.Label(form_wm, text='Set Count:')
set_count_entry = tk.Entry(form_wm, textvariable=set_count_var)

rep_count = tk.Label(form_wm, text='Rep Count:')
rep_count_entry = tk.Entry(form_wm, textvariable=rep_count_var)

weight_used = tk.Label(form_wm, text='Weight Used:')
weight_used_entry = tk.Entry(form_wm, textvariable=weight_used_var)

add_exercise = tk.Button(form_wm, text='Add Exercise', command=add_exercise_entry)

# <----->

time_spent = tk.Label(form_wm, text='Time Spent:')
time_spent_entry = tk.Entry(form_wm, textvariable=time_spent_var)

add_time = tk.Button(form_wm, text='Add Time', command=add_time_entry)

title.pack()

exercise_name.pack()
exercise_name_entry.pack()

set_count.pack()
set_count_entry.pack()

rep_count.pack()
rep_count_entry.pack()

weight_used.pack()
weight_used_entry.pack()

add_exercise.pack()

time_spent.pack()
time_spent_entry.pack()

add_time.pack()


root.mainloop()