# Current Logic the Workout Forms & Graphs will be based on

# (Planning Pre-Creation)
Usage of DateTime to identify the day, so as to record all workouts done for that day.

Currently, will ask user to manually input each exercise and its relevant data, it will automatically be attached to the day of entry.

We will go on the basis that the user, in order to uplift his life, should practice this habit of data entry every day they work out, rather than delaying this task. To help build a good habit and sense of rythm in their lives.

With that logic: 

Each Workout Data Entry will include the following fields:

- Execise Name
- Set Count
- Rep Count
- Weight Used
- Time Spent


---

Repeatably clickable and data entryable function of Exercise Name, Set Count, Rep Count, Weight Used then overall clickable button on time spent.

What will be required:

Usage of DateTime to Record Date
Creation of Workout Entry Object which will include the following attributes:
    - date
    - time_spent
        - Exercise
            - exercise_name
            - set_count
            - rep_count
            - weight_used

This object has the ability to keep creating new exercise entries therefore... we need an exercise object too..

class Exercise:
    - exercise_name
    - set_count
    - rep_count
    - weight_used

# Post-Creation Notes and Details:

There is 2 object classes, Workout and Exercise.

Workout Object Class contains the following attributes:
- date <--- The date of the workout entry, also used as a key and is automatically created based on the date upon creation via datetime library
- time_spent <--- Manually user inputted data that is measured in minutes, to detail how long the exercises took and is accumulative for the day
- exercise_list <--- A list of Exercise objects that details the various activities completed and is accumulative for the day, albeit separated in their own Exercise object entries

Exercise Object Class contains the following attributes:
- exercise_name <--- The name of the exercise about to be detailed
- set_count <--- The quantity of sets worked in the exercise
- rep_count <--- The quantity of repetitive action of said exercised done per set
- weight_used <--- The weight used in the exercise

Currently 'workouts' is similar to the 'users' dictionary, in the sense that there is only 1 user in the users dictionary, and all the workouts are in relation to said user.

In the form section of the workout, named 'Workout Entry (Daily)', exercises and time spent can be separately updated. This allows the user to input a multitude of exercises they have completed, and ideally they will use the time spent field to input the total time spent based on all the exercises they have done so far. They are able to keep increasing the time spent throughout the day, when they come back to enter more workout data, same as the exercises performed as only 1 workout entry is created per day, and all its contents for that day (exercises and timespent) are stored within.

An Example for Visual Understanding:
I have completed a 45 minutes gym session that consists of the following:
3 x 10 Flat Bench Press @ 100kg Barbell
3 x 15 Triceps Pressdowns @ 12.4kg Banded
3 x 10 Incline Bench Press @ 20kg Dumbbells

I would enter into the workout entry each exercise individually:
exercise_name: Flat Bench Press
set_count: 3
rep_count: 10
weight_used: 100kg
[Add Exercise]

After entering the other exercises or before, I can also input the time spent:
time_spent: 45
[Add Time]