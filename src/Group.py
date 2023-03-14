# -*- coding: utf-8 -*-


class Group:
    def __init__(self, group_id: int, level, duration: int, number_of_students: int, teacher: int, classroom: int):
        self.id = group_id
        self.level = level
        self.duration = duration
        self.number_of_students = number_of_students
        self.teacher = teacher
        self.classroom = classroom


