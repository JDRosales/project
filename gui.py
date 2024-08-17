from tkinter import *
from logic import GradeBook


class Gui:
    def __init__(self, window):
        """Create gui"""
        self.window = window
        self.gradebook = GradeBook()
        self.validation_delay = None

        """input student info"""
        self.label_name = Label(self.window, text='Student Name:')
        self.input_name = Entry(self.window, width=20)

        self.label_id = Label(self.window, text='Student ID:')
        self.input_id = Entry(self.window, width=20)

        self.label_attempts = Label(self.window, text='Number of Scores:')
        self.attempts_var = StringVar(value='1')
        self.attempts_var.trace_add('write', self.schedule_update_score_entries)
        self.input_attempts = Entry(self.window, textvariable=self.attempts_var, width=20)

        """score entry"""
        self.score_labels = []
        self.score_entries = []
        for i in range(6):  # Allows up to 6 scores
            self.score_labels.append(Label(self.window, text=f"Score {i+1}:"))
            self.score_entries.append(Entry(self.window, width=20))

        button_frame = Frame(self.window)
        button_frame.grid(row=9, column=0, columnspan=2, pady=10, padx=5)

        self.button_save = Button(button_frame, text='Enter Grade', fg='blue', command=self.submit_and_export)
        self.button_save.pack(expand=True)  # Center within the frame

        self.status_message = Label(self.window, text="", fg='red')

        """widget placement"""
        self.label_name.grid(row=0, column=0, padx=5, pady=5)
        self.input_name.grid(row=0, column=1, padx=5, pady=5)
        self.label_id.grid(row=1, column=0, padx=5, pady=5)
        self.input_id.grid(row=1, column=1, padx=5, pady=5)
        self.label_attempts.grid(row=2, column=0, padx=5, pady=5)
        self.input_attempts.grid(row=2, column=1, padx=5, pady=5)

        """initialize scores"""
        self.update_scores()
        self.status_message.grid(row=10, column=0, columnspan=2)

    def schedule_update_score_entries(self, *args):
        """Schedules score entry updates"""
        if self.validation_delay:
            self.window.after_cancel(self.validation_delay)
        self.validation_delay = self.window.after(500, self.update_scores)

    def update_scores(self):
        """Updates score entries based on number of scores"""
        try:
            attempts = int(self.attempts_var.get() or 1)
            if attempts < 1 or attempts > 6:
                raise ValueError("Number of scores must be a number between 1 and 6")
        except ValueError:
            self.status_message.config(text="Number of scores must be a number between 1 and 6", fg='red')
            return

        self.status_message.config(text="")

        # Continue with updating the score entries only if the input is valid
        for i in range(6):
            self.score_labels[i].grid_remove()
            self.score_entries[i].grid_remove()

        for i in range(attempts):
            self.score_labels[i].grid(row=i + 3, column=0, padx=5, pady=5)
            self.score_entries[i].grid(row=i + 3, column=1, padx=5, pady=5)

        for i in range(attempts):
            self.score_labels[i].grid(row=i + 3, column=0, padx=5, pady=5)
            self.score_entries[i].grid(row=i + 3, column=1, padx=5, pady=5)

    def submit_and_export(self):
        """Validates and submits the student data and scores, handling exceptions."""
        name = self.input_name.get().strip()
        student_id = self.input_id.get().strip()
        attempts = self.input_attempts.get().strip()
        '''Exception handling'''
        try:
            """Valid Name"""
            if not name.replace(' ', '').isalpha():
                raise ValueError("Name must not be empty, and only contain letters and spaces")
            """Valid ID"""
            if not student_id.isdigit():
                raise ValueError("Student ID must be a number and contain no letters")
            student_id = int(student_id)
            """Valid Scores"""
            attempts = int(attempts)
            if attempts < 1 or attempts > 6:  # Updated range check
                raise ValueError("Number of scores must be between 1 and 6")

            scores = []
            for i in range(attempts):
                score_str = self.score_entries[i].get().strip()
                if score_str == '':
                    raise ValueError("Scores cannot be empty")
                if not score_str.isdigit() or not 0 <= int(score_str) <= 100:
                    raise ValueError("Scores must be between 0 and 100")
                scores.append(int(score_str))

            if not name:
                raise ValueError("Student name cannot be empty")

            self.gradebook.add_student(name, student_id, attempts, scores)
            self.gradebook.export_csv('grades.csv')
            self.status_message.config(text=f"Successfully Entered: {name}'s grade", fg='green')
            self.reset()
        except ValueError as e:
            self.status_message.config(text=str(e), fg='red')

    def reset(self):
        """Resets the application for a new student entry"""
        self.input_name.delete(0, END)
        self.input_id.delete(0, END)
        self.attempts_var.set('1')
        for entry in self.score_entries:
            entry.delete(0, END)
