import pandas as pd
import json
import random
# from src.Teacher import Teacher
# from src.Classroom import Classroom
# from src.Student import Student
# from src.Group import Group
# from src.TimeSlot import TimeSlot
from GenAlg.shared_types import *
from typing import List, Dict, Tuple


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


def convert_teachers_to_dataframe(teachers_list: List[Teacher]):
    return {teacher.id: teacher.preferred_hours for teacher in teachers_list}


def convert_teachers_dataframe_to_list(teachers_dataframe):
    return [Teacher(teachers_dataframe[column].to_dict()) for column in teachers_dataframe]
    # days = teachers_dataframe['0']
    # teachers_dataframe = teachers_dataframe.drop(columns=['0'])
    # t_list = [Teacher(teachers_dataframe[column].to_dict()) for column in teachers_dataframe]
    # for teacher in t_list:
    #     new_dict = {}
    #     for k in teacher.preferred_hours.keys():
    #         new_dict[days[k]] = teacher.preferred_hours[k]
    #     teacher.preferred_hours = new_dict
    # return t_list


def prepare_students_list() -> List:
    """
    Extracts data from CSV with students information.
    Gets only second value from tuples (group nr) and skips first element (it's column name).
    Returns data in List.
    """
    csv_df = pd.read_csv(MY_PATH + "data_generation/students.csv", delimiter=',', index_col=0)
    students_list = list(csv_df["student_id"].values)

    return students_list


def prepare_teachers_list() -> List:
    """
    Extracts data from CSV with teachers information.
    Returns list of dictionaries
    """
    csv_df = pd.read_csv(MY_PATH + "data_generation/teachers.csv", delimiter=',', index_col=0)
    teachers_list = [Teacher({day_id + 1: csv_df[col].iloc[day_id] for day_id in range(len(csv_df))}) for col in
                     csv_df.columns]
    for teacher in teachers_list:
        teacher.delete_empty_lists()
    return teachers_list


def read_school_config() -> List:
    with open(MY_PATH + "data_generation/school_config.json") as f:
        config_dict = json.load(f)

    return config_dict


# leftovers that can be used as inspiration during creation of other datasets


# students2 = generate_students(200, 3)
# teachers = generate_teachers(10, 8, 4)
# teachers_dataframe = pd.DataFrame(convert_teachers_to_dataframe(teachers))
# print(teachers_dataframe)
# print(convert_teachers_dataframe_to_list(teachers_dataframe))
# abc = pd.DataFrame(students2, columns=["student_id"])
# teachers_dataframe.to_csv("/Users/rafal/PycharmProjects/GlebokieUczenie/data-generation/teachers.csv")
