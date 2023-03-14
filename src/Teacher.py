# -*- coding: utf-8 -*-
from typing import List


class Teacher:
    id_counter = 0

    # id nadawane automatycznie, preferowane godziny jako lista slotów (chyba że ma być jakoś inaczej)
    def __init__(self, preferred_hours: List[int]):
        self.id = Teacher.id_counter
        Teacher.id_counter += 1
        self.preferred_hours = preferred_hours

    # dodawanie slotu do preferowanych godzin
    def add_slot(self, slot_id: int):
        self.preferred_hours.append(slot_id)
