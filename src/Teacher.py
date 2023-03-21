# -*- coding: utf-8 -*-
from typing import List, Dict


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
