import csv


class GradeBook:
    def __init__(self):
        """Create an empty list of students."""
        self.students = []

    def add_student(self, name, student_id, number_of_scores, scores):
        """Add student to grade book"""
        if self.student_id_exists(student_id):
            raise ValueError(f"Student ID {student_id} already exists.")
        final_score = sum(scores) / number_of_scores
        student_data = {
            'Name': name,
            'Student ID': student_id,
            'Score 1': scores[0] if number_of_scores > 0 else 0,
            'Score 2': scores[1] if number_of_scores > 1 else 0,
            'Score 3': scores[2] if number_of_scores > 2 else 0,
            'Score 4': scores[3] if number_of_scores > 3 else 0,
            'Score 5': scores[4] if number_of_scores > 4 else 0,
            'Score 6': scores[5] if number_of_scores > 5 else 0,
            'Highest': max(scores) if scores else 0,
            'Lowest': min(scores) if scores else 0,
            'Final': final_score,
            'Grade': self.letter_grade(final_score)
        }
        self.students.append(student_data)

    def student_id_exists(self, student_id):
        """Check if student ID already exists"""
        return any(student['Student ID'] == student_id for student in self.students)

    def score_handling(self):
        """Compute the highest, lowest, and average scores for the class."""
        if not self.students:
            return None

        final_scores = [student['Final'] for student in self.students]
        highest = max(final_scores)
        lowest = min(final_scores)
        average = sum(final_scores) / len(final_scores)
        average_grade = self.letter_grade(average)

        return (f'Highest Score: {highest}, Lowest Score: {lowest}, '
                f'Class Average: {average:.2f}, Class Average Grade: {average_grade}')

    def export_csv(self, filename: str) -> None:
        """Export the data to a CSV file"""
        headers = ['Name', 'Student ID', 'Score 1', 'Score 2', 'Score 3', 'Score 4',
                   'Score 5', 'Score 6', 'Highest', 'Lowest', 'Final', 'Grade']
        data = self.score_handling()
        with open(filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=headers)
            writer.writeheader()
            writer.writerows(self.students)

            if data:
                stats = data.split(', ')
                for stat in stats:
                    file.write(f"{stat}\n")

    def letter_grade(self, score):
        """Calculate grades, numeric to letter"""
        if score >= 97:
            return 'A+'
        elif score >= 93:
            return 'A'
        elif score >= 90:
            return 'A-'
        elif score >= 87:
            return 'B+'
        elif score >= 83:
            return 'B'
        elif score >= 80:
            return 'B-'
        elif score >= 77:
            return 'C+'
        elif score >= 73:
            return 'C'
        elif score >= 70:
            return 'C-'
        elif score >= 67:
            return 'D+'
        elif score >= 63:
            return 'D'
        elif score >= 60:
            return 'D-'
        else:
            return 'F'
