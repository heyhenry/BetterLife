# Current Logic the Workout Forms & Graphs will be based on

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