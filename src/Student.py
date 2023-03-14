# -*- coding: utf-8 -*-


class Student:
    id_counter = 0

    # id nadawane automatycznie, level - grupa językowa (jako A,B,C, czy typu int?)
    def __init__(self,  level):
        self.id = Student.id_counter
        Student.id_counter += 1
        self.level = level
        self.group = None

    def add_to_group(self, group_id):
        self.group = group_id
