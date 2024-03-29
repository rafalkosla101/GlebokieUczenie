# -*- coding: utf-8 -*-


# slot czasowy jako id oraz godzinowo w bardziej czytelnej formie
class TimeSlot:
    def __init__(self, slot_id: int, time: str):
        self.id = slot_id
        self.time = time        # czas w czytelnej formie np. "15:00 - 15:15" (najwyżej można to usunąć)

    def __str__(self):
        return self.time
