# -*- coding: utf-8 -*-
SEATING_CAPACITY = 20


class Classroom:
    id_counter = 0

    # id sali nadawane automatycznie, seats - liczba miejsc
    def __init__(self, seating_capacity):
        self.id = Classroom.id_counter
        Classroom.id_counter += 1
        self.seating_capacity = seating_capacity

        # jeśli pojemność każdej sali jest taka sama można dać const
        # self.seating_capacity = SEATING_CAPACITY
