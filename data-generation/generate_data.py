import pandas as pd

from src.Teacher import Teacher
from src.Classroom import Classroom
from src.Student import Student
from src.Group import Group
from src.TimeSlot import TimeSlot
import random
import pandas as pd

from typing import List, Dict, Tuple

import random
from copy import deepcopy

students = [1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 3, 2, 1, 1, 1, 1]
limit = 3
duration = 4
classoom = [Classroom(), Classroom(), Classroom()]
teacher = [Teacher({1: [1, 2, 3, 4, 5, 6], 2: [2, 3, 4, 5], 4: [1, 2, 3, 4]}),
           Teacher({2: [1, 2, 3, 4], 3: [2, 3, 4, 5], 5: [1, 2, 3, 4, 5, 6, 7, 8]})]
working_hours = {1: [1, 2, 3, 4, 5, 6, 7, 8], 2: [1, 2, 3, 4, 5, 6, 7, 8], 3: [1, 2, 3, 4, 5, 6, 7, 8],
                 4: [1, 2, 3, 4, 5, 6, 7, 8], 5: [1, 2, 3, 4, 5, 6, 7, 8]}


def load_from_csv(path_to_file: str):
    return pd.read_csv(path_to_file)


def generate_classrooms(number_of_classrooms: int):
    return [Classroom() for _ in range(0, number_of_classrooms)]


def generate_working_hours(number_of_hours: int):
    return {day_id: [hour_id for hour_id in range(1, number_of_hours + 1)] for day_id in range(1, 6)}


def generate_students(number_of_students: int, students_range: int):
    return [random.randint(1, students_range) for _ in range(number_of_students)]


def generate_teachers(number_of_teachers: int, slots_per_day: int, slots_per_hour: int):
    return [Teacher(generate_teacher(slots_per_day, slots_per_hour)) for i in range(0, number_of_teachers)]


def generate_teacher(slots_per_day: int, slots_per_hour: int):
    # to be done, not sure what we actually want that dict to look like
    generated_dict = {
        1: [i + 1 for i in range(random.randrange(0, slots_per_day + 1, slots_per_hour))],
        2: [i + 1 for i in range(random.randrange(0, slots_per_day + 1, slots_per_hour))],
        3: [i + 1 for i in range(random.randrange(0, slots_per_day + 1, slots_per_hour))],
        4: [i + 1 for i in range(random.randrange(0, slots_per_day + 1, slots_per_hour))],
        5: [i + 1 for i in range(random.randrange(0, slots_per_day + 1, slots_per_hour))]
    }
    return generated_dict


def convert_teachers_to_dataframe(teachers_list: list[Teacher]):
    return {teacher.id: teacher.preferred_hours for teacher in teachers_list}


def convert_teachers_dataframe_to_list(teachers_dataframe):
    return [Teacher(teachers_dataframe[column].to_dict()) for column in teachers_dataframe]
    pass


# leftovers that can be used as inspiration during creation of other datasets


# students2 = generate_students(200, 3)
# teachers = generate_teachers(10, 8, 4)
# teachers_dataframe = pd.DataFrame(convert_teachers_to_dataframe(teachers))
# print(teachers_dataframe)
# print(convert_teachers_dataframe_to_list(teachers_dataframe))
# abc = pd.DataFrame(students2, columns=["student_id"])
# teachers_dataframe.to_csv("/Users/rafal/PycharmProjects/GlebokieUczenie/data-generation/teachers.csv")
