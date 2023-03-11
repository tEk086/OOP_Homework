
def average_grade(self):
    if self.grades:
        average = round((sum(map(sum, self.grades.values()))) / sum(map(len, self.grades.values())), 1)
        return average
    else:
        return 'Невозможно посчитать среднее значение'


def course_stats(course):
    try:
        summary_grades = []
        for student in Student.students_list:
            if course not in student.grades.keys():
                continue
            else:
                summary_grades.append(student.grades[course])
        average = round((sum(map(sum, summary_grades))) / sum(map(len, summary_grades)), 1)
        return f'Средняя оценка ДЗ по курсу {course} составляет: {average}'
    except ZeroDivisionError:
        return 'Списки пусты. Оценки по курсу отсутствуют'


def lecturers_stats(course):
    try:
        summary_grades = []
        for lecturer in Lecturer.lecturers_list:
            if course not in lecturer.grades.keys():
                continue
            else:
                summary_grades.append(lecturer.grades[course])
        average = round((sum(map(sum, summary_grades))) / sum(map(len, summary_grades)), 1)
        return f'Средняя оценка лекторов по курсу {course} составляет: {average}'
    except ZeroDivisionError:
        return 'Списки пусты'


class Student:
    students_list = []

    def __init__(self, name, surname, gender):
        self.students_list.append(self)
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}
        average_grade(self)

    def __str__(self):
        result = f'\nИмя: {self.name} \nФамилия: {self.surname}' \
                 f'\nСредняя оценка за домашние задания: {average_grade(self)}' \
                 f'\nКурсы в процессе изучения: {", ".join(self.courses_in_progress)}' \
                 f'\nЗавершенные курсы: {", ".join(self.finished_courses)}'
        return result

    def __gt__(self, other):
        if isinstance(other, Student) and average_grade(self) > average_grade(other):
            return True
        else:
            return False

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) \
                and course in lecturer.courses_attached \
                and course in self.courses_in_progress:
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка 1'


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        if isinstance(self, Lecturer):
            result = f'\nИмя: {self.name} \nФамилия: {self.surname} \nСредняя оценка за лекции: {average_grade(self)}'
            return result
        elif isinstance(self, Reviewer):
            result = f'\nИмя: {self.name} \nФамилия: {self.surname}'
            return result
        else:
            return 'Ошибка 2'


class Lecturer(Mentor):
    lecturers_list = []

    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.lecturers_list.append(self)
        self.grades = {}
        average_grade(self)

    def __gt__(self, other):
        if isinstance(other, Lecturer) and average_grade(self) > average_grade(other):
            return True
        else:
            return False


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка 3'


reviewer1 = Reviewer('Some', 'Buddy')
reviewer1.courses_attached += ['Python']
reviewer2 = Reviewer('Джейсон', 'Степлер')

lecturer1 = Lecturer('Some', 'Buddy')
lecturer1.courses_attached += ['Python']

lecturer2 = Lecturer('Elena', 'Nikitina')
lecturer2.courses_attached += ['Python']

student1 = Student('Ruoy', 'Eman', 'your_gender')
student1.courses_in_progress += ['Python']
student1.courses_in_progress += ['Git']
student1.finished_courses += ['Введение в программирование']

student2 = Student('Self', 'Myself', 'Student')
student2.courses_in_progress += ['Python']

reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 10)
reviewer1.rate_hw(student1, 'Python', 10)

reviewer1.rate_hw(student2, 'Python', 10)
reviewer1.rate_hw(student2, 'Python', 9)
reviewer1.rate_hw(student2, 'Python', 10)

student1.rate_lecturer(lecturer1, 'Python', 10)
student1.rate_lecturer(lecturer1, 'Python', 9)
student1.rate_lecturer(lecturer1, 'Python', 10)

student2.rate_lecturer(lecturer2, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 10)
student2.rate_lecturer(lecturer2, 'Python', 10)

print(reviewer1)
print(lecturer1)
print(student1)

print(reviewer2)
print(lecturer2)
print(student2)

print(lecturer1 < lecturer2)
print(student1 > student2)

print(course_stats('Python'))
print(lecturers_stats('Python'))
print(lecturers_stats('Git'))
