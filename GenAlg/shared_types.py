from typing import List, Dict, Tuple, Optional
from enum import Enum
import random
import copy


SEATING_CAPACITY = 20

# Fitness parameters
BEYOND_HOURS_PENALTY = 1
BREAKS_PENALTY = 1
IMPROPER_LEVEL_PENALTY = 1

Day = int
Slot = int
Room = int
Lector = int


class Selection(Enum):
    """
    Enum of selection types
    """
    BEST = 0
    ROULETTE = 1
    TOURNAMENT = 2


class Mutation(Enum):
    """
    Enum of mutation methods
    """
    SHIFT = 0
    CHANGE_TEACHER = 1


class Crossover(Enum):
    """
    Enum of crossover methods
    """
    ALL_DAY = 0
    SINGLE_BLOCK = 1


class Group:
    def __init__(self, group_id: int, level: int, duration: int, number_of_students: Dict[int, int],
                 teacher: Optional[int], classroom: Optional[int]):
        self.id = group_id
        self.level = level
        self.duration = duration
        self.number_of_students = number_of_students
        self.teacher = teacher
        self.classroom = classroom

    def __str__(self):
        return f"({self.teacher}, {self.classroom})"
        # return f"L: {self.level}, S: {self.number_of_students}, T: {self.teacher}, C: {self.classroom}"
        # return f'Group ID: {self.id}, Level: {self.level}, Students: {self.number_of_students}, Teacher: {self.teacher}, Classroom: {self.classroom}'


class Classroom:
    id_counter = 0

    # id sali nadawane automatycznie, seats - liczba miejsc
    # def __init__(self, seating_capacity):
    def __init__(self):
        self.id = Classroom.id_counter
        Classroom.id_counter += 1
        # self.seating_capacity = seating_capacity

        # jeśli pojemność każdej sali jest taka sama można dać const
        self.seating_capacity = SEATING_CAPACITY


class Teacher:
    id_counter = 0

    # id nadawane automatycznie, preferowane godziny jako lista slotów (chyba że ma być jakoś inaczej) - dodałam że to słownik, bo grupa nie może mieć np. 15min w poniedziałek i 45 min we wtorek
    def __init__(self, preferred_hours: Dict[int, List[int]]):
        self.id = Teacher.id_counter
        Teacher.id_counter += 1
        self.preferred_hours = preferred_hours

    # dodawanie slotu do preferowanych godzin
    def add_slot(self, day: int, slot_id: int):
        if day in self.preferred_hours.keys():
            self.preferred_hours[day].append(slot_id)
        else:
            self.preferred_hours[day] = [slot_id]

    def delete_empty_lists(self):
        new_dict = {key: val for key, val in self.preferred_hours.items() if val != '[]'}
        self.preferred_hours = new_dict

    def convert_slots_to_int(self):
        for key, val in self.preferred_hours.items():
            int_slots = [int(slot) for slot in val[1:-1].split(", ")]
            self.preferred_hours[key] = int_slots
