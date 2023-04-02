# -*- coding: utf-8 -*-
from typing import Dict


class Group:
    def __init__(self, group_id: int, level: int, duration: int, number_of_students: Dict[int, int], teacher: int, classroom: int):
        self.id = group_id
        self.level = level
        self.duration = duration
        self.number_of_students = number_of_students
        self.teacher = teacher
        self.classroom = classroom

    def __str__(self):
        return f"G: {self.id}, L: {self.level}, S: {self.number_of_students}, T: {self.teacher}, C: {self.classroom}"
        # return f'Group ID: {self.id}, Level: {self.level}, Students: {self.number_of_students}, Teacher: {self.teacher}, Classroom: {self.classroom}'


