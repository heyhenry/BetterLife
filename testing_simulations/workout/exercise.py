class Exercise:
    def __init__(self, exercise_name, set_count, rep_count, weight_used):
        self.exercise_name = exercise_name
        self.set_count = set_count
        self.rep_count = rep_count
        self.weight_used = weight_used

    def __str__(self):
        return (f"Exercise Name: {self.exercise_name}, Sets: {self.set_count}, Reps: {self.rep_count}, Weight Used: {self.weight_used}")
