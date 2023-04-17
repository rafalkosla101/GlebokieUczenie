# File with implemented class representing single solution
# PROJECT PACKAGES
from GenAlg.utils import draw_rect
from GenAlg.shared_types import *
from DataGeneration.generate_data import *

# BUILT-IN PACKAGES
import matplotlib.pyplot as plt

from copy import deepcopy
from typing import Optional, Dict, List


class Solution:
    def __init__(self,
                 solution: Dict[Tuple[Day, Slot], List[Tuple[Group, int]]], 
                 possible_slots: Dict[Tuple[Day, Slot], Tuple[List[Room], List[Lector]]], limit: int, duration: int,
                 classrooms: List[Classroom], teachers: List[Teacher], working_hours: Dict[Day, List[Slot]],
                 mutation_method: Mutation,
                 crossover_method: Crossover):
        self.solution = solution
        self.possible_slots = possible_slots
        self.limit = limit
        self.duration = duration
        self.classrooms = classrooms
        self.teachers = teachers
        self.working_hours = working_hours
        self.mutation_method = mutation_method
        self.crossover_method = crossover_method

    def calculate_fitness(self) -> float:
        """
        Calculates fitness and returns it.
        """

        # Liczba slotów przydzielonych poza preferowanymi godzinami pracy lektora
        slots_beyond_preferred_hours: int = 0

        for (day, slot), group_info in self.solution.items():
            available_teachers = [t.id for t in self.teachers if day in t.preferred_hours and t.preferred_hours[day] and slot in t.preferred_hours[day]]
            slots_beyond_preferred_hours += sum([1 if group.teacher not in available_teachers else 0 for group, _ in group_info])

        # Zbiór okienek pomiędzy zajęciami
        total_breaks = 0
        teacher_working_hours: Dict[Lector, List[Tuple[Day, Slot]]] = {}
        for (day, slot), group_info in self.solution.items():
            for group, _ in group_info:
                if group.teacher not in teacher_working_hours.keys():
                    teacher_working_hours[group.teacher] = []
                teacher_working_hours[group.teacher].append((day, slot))
                teacher_working_hours[group.teacher].sort()

        for lector, slots in teacher_working_hours.items():
            for day in range(1, 6):
                current_slots = []
                for slot in slots:
                    if slot[0] == day:
                        current_slots.append(slot[1])
                if current_slots:
                    first_slot = min(current_slots)
                    last_slot = max(current_slots)
                    slots_spent_at_school = [i for i in range(first_slot, last_slot + 1)]
                    total_breaks += len(slots_spent_at_school) - len(current_slots)

        # Uczeń przypisany do grupy o innym poziomie niż preferowany
        improper_group = 0
        for _, group_info in self.solution.items():
            for group, _ in group_info:
                for student_level in group.number_of_students.keys():
                    if group.level != student_level:
                        improper_group += group.number_of_students[student_level]

        return BEYOND_HOURS_PENALTY * slots_beyond_preferred_hours + BREAKS_PENALTY * total_breaks + IMPROPER_LEVEL_PENALTY * improper_group

    def mutate(self) -> 'Solution':
        """
        Copies solution and returns mutated copy.
        """
        if self.mutation_method == Mutation.SHIFT:
            return self._mutate_shift()
        elif self.mutation_method == Mutation.CHANGE_TEACHER:
            return self._mutate_change_teacher()

    def crossover(self, other: 'Solution') -> Tuple['Solution', 'Solution']:
        """
        Performs crossover with 'other' and returns a Tuple of two solutions.
        """
        if self.crossover_method == Crossover.ALL_DAY:
            return self._crossover_all_day(other)
        elif self.crossover_method == Crossover.SINGLE_BLOCK:
            return self._crossover_single_block(other)

    def display(self, other: Optional['Solution']=None) -> None:
        """
        Method to display solution(s)
        :param other: Optional other solution
        """

        side = 30
        max_slot = max([slot for day in range(1, 5 + 1) for slot in self.working_hours[day]])
        groups1 = sorted(list(set([group.id for timeslot in self.solution for group, _ in self.solution[timeslot]])))
        groups2 = []

        if other is not None:
            groups2 = sorted(list(set([group.id for timeslot in other.solution for group, _ in other.solution[timeslot]])))

        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)

        _ = [draw_rect(side * i, 0, side, side, "red", ax, str(i)) for i, _ in enumerate(groups1)]
        _ = [draw_rect(side * (i + len(groups1)), 0, side, side, "red", ax, str(i)) for i, _ in enumerate(groups2)]

        for day in range(1, 5 + 1):
            day_y = (1 - day) * max_slot * side
            plt.axhline(y=day_y, color="blue")
            draw_rect(-2 * side, day_y, side, -max_slot * side, "blue", ax, str(day), to_fill=False)

            for slot in range(1, max_slot + 1):
                slot_y = -side * ((day - 1) * max_slot + slot - 1)
                draw_rect(-side, slot_y, side, -side, "blue", ax, str(slot), to_fill=False)

        for day, slot in self.solution:
            for group, _ in self.solution[(day, slot)]:
                x = side * groups1.index(group.id)
                y = -side * ((day - 1) * max_slot + slot - 1)
                draw_rect(x, y, side, -side, "orange", ax, str(group))

        if other is not None:
            for day, slot in other.solution:
                for group, _ in other.solution[(day, slot)]:
                    x = side * (groups2.index(group.id) + len(groups1))
                    y = -side * ((day - 1) * max_slot + slot - 1)
                    draw_rect(x, y, side, -side, "green", ax, str(group))

        plt.axvline(x=side * len(groups1), color="blue")

        if other is not None:
            plt.xlim([-2 * side, side * (len(groups1) + len(groups2))])

        else:
            plt.xlim([-2 * side, side * len(groups1)])

        plt.ylim([-side * (max_slot * 5), side])
        plt.axis('off')
        plt.show()

    def assign(self, students_by_levels: Dict[int, int], group_id: int) -> None:
        """
        Method to create new groups and assign students to them
        :param students_by_levels: Number of students assigned to each level
        :param group_id: Group ID
        """

        groups: List[Group] = []

        for level, num in students_by_levels.items():
            while num > 0:
                number_of_students = {level: self.limit} if num >= self.limit else {level: num}
                group = Group(group_id, level, self.duration, number_of_students, None, None)
                num -= self.limit
                groups.append(group)
                group_id += 1

        groups = connect_groups(groups, self.limit)
        possible_first_slots: Dict[Tuple[Day, Slot], Tuple[List[Room], List[Lector]]] = {}
        classroom_id = [c.id for c in self.classrooms]
        teacher_id = [t.id for t in self.teachers]

        for day in self.working_hours:
            for slot in self.working_hours[day][:-self.duration + 1]:
                classroom_id_, teacher_id_ = deepcopy(classroom_id), deepcopy(teacher_id)

                for i in range(self.duration):
                    timeslot = (day, slot + i)

                    if timeslot in self.solution:
                        for group, _ in self.solution[timeslot]:
                            if group.classroom in classroom_id_:
                                classroom_id_.remove(group.classroom)

                            if group.teacher in teacher_id_:
                                teacher_id_.remove(group.teacher)

                if classroom_id_ and teacher_id_:
                    possible_first_slots[(day, slot)] = (classroom_id_, teacher_id_)

        for g in groups:
            day, slot = random.choice(list(possible_first_slots.keys()))
            chosen_room = random.choice(possible_first_slots[(day, slot)][0])
            chosen_teacher = random.choice(possible_first_slots[(day, slot)][1])
            g.teacher = chosen_teacher
            g.classroom = chosen_room

            for i in range(self.duration):
                timeslot = (day, slot + i)

                if timeslot in self.solution:
                    for group, _ in self.solution[timeslot]:
                        if group.teacher == chosen_teacher or group.classroom == chosen_room:
                            break

                    else:
                        self.solution[timeslot].append((g, i + 1))

                else:
                    self.solution[timeslot] = [(g, i + 1)]

                if timeslot in possible_first_slots:
                    if chosen_room in possible_first_slots[timeslot][0]:
                        possible_first_slots[timeslot][0].remove(chosen_room)

                    if chosen_teacher in possible_first_slots[timeslot][1]:
                        possible_first_slots[timeslot][1].remove(chosen_teacher)

                    if not possible_first_slots[timeslot][0] or not possible_first_slots[timeslot][1]:
                        possible_first_slots.pop(timeslot)

                timeslot = (day, slot - i)

                if timeslot in possible_first_slots:
                    if chosen_room in possible_first_slots[timeslot][0]:
                        possible_first_slots[timeslot][0].remove(chosen_room)

                    if chosen_teacher in possible_first_slots[timeslot][1]:
                        possible_first_slots[timeslot][1].remove(chosen_teacher)

                    if not possible_first_slots[timeslot][0] or not possible_first_slots[timeslot][1]:
                        possible_first_slots.pop(timeslot)
        
    def _mutate_shift(self) -> 'Solution':
        new_sol = copy.deepcopy(self.solution)
        new_poss_slots = copy.deepcopy(self.possible_slots)
        possible_slots_to_change = list(new_sol.keys())
        while possible_slots_to_change:
            slot_to_change = random.choice(possible_slots_to_change)
            possible_group_to_change = copy.copy(new_sol[slot_to_change])
            while possible_group_to_change:
                group_to_change, slot_number = random.choice(possible_group_to_change)
                slot_before_group = (slot_to_change[0], slot_to_change[1] - slot_number)
                slot_after_group = (slot_before_group[0], slot_before_group[1] + 1 + group_to_change.duration)
                shift_possibilities = []
                if slot_before_group in new_poss_slots.keys() and group_to_change.teacher in new_poss_slots[slot_before_group][1] and group_to_change.classroom in new_poss_slots[slot_before_group][0]:
                    shift_possibilities.append(slot_before_group)
                if slot_after_group in new_poss_slots.keys() and group_to_change.teacher in new_poss_slots[slot_after_group][1] and group_to_change.classroom in new_poss_slots[slot_after_group][0]:
                    shift_possibilities.append(slot_after_group)
                if not shift_possibilities:
                    possible_group_to_change.remove((group_to_change, slot_number))
                    continue
                new_slot = random.choice(shift_possibilities)
                if new_slot == slot_before_group:
                    if new_slot in new_sol.keys():
                        new_sol[new_slot].append((group_to_change, 1))
                    else:
                        new_sol[new_slot] = [(group_to_change, 1)]
                    for i in range(1, group_to_change.duration):
                        indx = new_sol[(new_slot[0], new_slot[1] + i)].index((group_to_change, i))
                        new_sol[(new_slot[0], new_slot[1] + i)][indx] = (group_to_change, i + 1)
                    new_sol[(new_slot[0], new_slot[1] + group_to_change.duration)].remove((group_to_change, group_to_change.duration))
                    if not new_sol[(new_slot[0], new_slot[1] + group_to_change.duration)]:
                        new_sol.pop((new_slot[0], new_slot[1] + group_to_change.duration))
                    if (new_slot[0], new_slot[1] + group_to_change.duration) in new_poss_slots.keys():
                        new_poss_slots[(new_slot[0], new_slot[1] + group_to_change.duration)][0].append(group_to_change.classroom)
                        new_poss_slots[(new_slot[0], new_slot[1] + group_to_change.duration)][1].append(group_to_change.teacher)
                    else:
                        new_poss_slots[(new_slot[0], new_slot[1] + group_to_change.duration)] = ([group_to_change.classroom], [group_to_change.teacher])
                elif new_slot == slot_after_group:
                    if new_slot in new_sol.keys():
                        new_sol[new_slot].append((group_to_change, group_to_change.duration))
                    else:
                        new_sol[new_slot] = [(group_to_change, group_to_change.duration)]
                    for i in range(group_to_change.duration - 1, 0, -1):
                        indx = new_sol[(new_slot[0], new_slot[1] - i)].index((group_to_change, group_to_change.duration - i + 1))
                        new_sol[(new_slot[0], new_slot[1] - i)][indx] = (group_to_change, group_to_change.duration - i)
                    new_sol[(new_slot[0], new_slot[1] - group_to_change.duration)].remove((group_to_change, 1))
                    if not new_sol[(new_slot[0], new_slot[1] - group_to_change.duration)]:
                        new_sol.pop((new_slot[0], new_slot[1] - group_to_change.duration))
                    if (new_slot[0], new_slot[1] - group_to_change.duration) in new_poss_slots.keys():
                        new_poss_slots[(new_slot[0], new_slot[1] - group_to_change.duration)][0].append(group_to_change.classroom)
                        new_poss_slots[(new_slot[0], new_slot[1] - group_to_change.duration)][1].append(group_to_change.teacher)
                    else:
                        new_poss_slots[(new_slot[0], new_slot[1] - group_to_change.duration)] = ([group_to_change.classroom], [group_to_change.teacher])
                new_poss_slots[new_slot][0].remove(group_to_change.classroom)
                new_poss_slots[new_slot][1].remove(group_to_change.teacher)
                if not new_poss_slots[new_slot][0] or not new_poss_slots[new_slot][1]:
                    new_poss_slots.pop(new_slot)
                return Solution(new_sol, new_poss_slots, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)
            possible_slots_to_change.remove(slot_to_change)
        return Solution(new_sol, new_poss_slots, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)
    
    def _mutate_change_teacher(self) -> 'Solution':
        new_sol = copy.deepcopy(self.solution)
        new_poss_slot = copy.deepcopy(self.possible_slots)
        possible_slots_to_change = list(new_sol.keys())
        while possible_slots_to_change:
            slot_to_change = random.choice(possible_slots_to_change)
            possible_group_to_change = copy.copy(new_sol[slot_to_change])
            while possible_group_to_change:
                group_to_change, slot_number = random.choice(possible_group_to_change)
                first_slot = (slot_to_change[0], slot_to_change[1] - slot_number + 1)
                last_slot = (first_slot[0], first_slot[1] + group_to_change.duration - 1)
                first_slot_poss_teacher = []
                if first_slot in new_poss_slot.keys():
                    first_slot_poss_teacher = new_poss_slot[first_slot][1]
                poss_teachers = []
                for teacher in first_slot_poss_teacher:
                    if last_slot in new_poss_slot.keys() and teacher in new_poss_slot[last_slot][1]:
                        poss_teachers.append(teacher)
                if not poss_teachers:
                    possible_group_to_change.remove((group_to_change, slot_number))
                    continue
                chosen_teacher = random.choice(poss_teachers)
                prev_teacher = group_to_change.teacher
                group_to_change.teacher = chosen_teacher
                for i in range(group_to_change.duration):
                    new_poss_slot[(first_slot[0], first_slot[1] + i)][1].append(prev_teacher)
                    new_poss_slot[(first_slot[0], first_slot[1] + i)][1].remove(chosen_teacher)
                return Solution(new_sol, new_poss_slot, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)
            possible_slots_to_change.remove(slot_to_change)
        return Solution(new_sol, new_poss_slot, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)

    def _crossover_all_day(self, other: 'Solution') -> Tuple['Solution', 'Solution']:
        """
        Function to perform the crossover of two solutions day-wise
        :param other: Other solution
        """

        new_sol1, new_sol2 = {}, {}
        day1, day2 = random.randrange(1, 5 + 1), random.randrange(1, 5 + 1)
        n_groups1 = len([group for day, slot in self.solution
                         for group, i in self.solution[(day, slot)] if day == day1 and i == 1])
        n_groups2 = len([group for day, slot in other.solution
                         for group, i in other.solution[(day, slot)] if day == day2 and i == 1])
        n_groups = min([n_groups1, n_groups2])
        idx1 = max([group.id for timeslot in other.solution for group, _ in other.solution[timeslot]])
        idx2 = max([group.id for timeslot in self.solution for group, _ in self.solution[timeslot]])
        n_students1 = [group.number_of_students for day, slot in self.solution
                       for group, i in self.solution[(day, slot)] if day == day1 and i == 1]
        n_students2 = [group.number_of_students for day, slot in other.solution
                       for group, i in other.solution[(day, slot)] if day == day2 and i == 1]
        levels1, levels2 = {i: 0 for i in range(1, 3 + 1)}, {i: 0 for i in range(1, 3 + 1)}
        n1, n2 = 0, 0

        for (day, slot), group_info in self.solution.items():
            if day != day1:
                new_sol1[(day, slot)] = group_info
                continue

            for group, i in group_info:
                if i != 1:
                    continue

                n1 += 1

                if n1 > n_groups:
                    for level, num in group.number_of_students.items():
                        levels1[level] += num

                else:
                    idx1 += 1
                    group_ = deepcopy(group)
                    group_.id = idx1
                    group_.number_of_students = n_students2[n1 - 1]

                    for j in range(group.duration):
                        if (day2, slot + j) in new_sol2:
                            new_sol2[(day2, slot + j)].append((group_, j + 1))

                        else:
                            new_sol2[(day2, slot + j)] = [(group_, j + 1)]

        for (day, slot), group_info in other.solution.items():
            if day != day2:
                new_sol2[(day, slot)] = group_info
                continue

            for group, i in group_info:
                if i != 1:
                    continue

                n2 += 1

                if n2 > n_groups:
                    for level, num in group.number_of_students.items():
                        levels2[level] += num

                else:
                    idx2 += 1
                    group_ = deepcopy(group)
                    group_.id = idx2
                    group_.number_of_students = n_students1[n2 - 1]

                    for j in range(group.duration):
                        if (day1, slot + j) in new_sol1:
                            new_sol1[(day1, slot + j)].append((group_, j + 1))

                        else:
                            new_sol1[(day1, slot + j)] = [(group_, j + 1)]

        new_sol1 = Solution(new_sol1, self.possible_slots, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)
        new_sol2 = Solution(new_sol2, self.possible_slots, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)

        if n_groups1 > n_groups2:
            new_sol1.assign(levels1, idx1 + 1)

        elif n_groups1 < n_groups2:
            new_sol2.assign(levels2, idx2 + 1)

        return new_sol1, new_sol2

    def _crossover_single_block(self, other: 'Solution') -> Tuple['Solution', 'Solution']:
        """
        Function to perform the crossover of two solutions block-wise
        :param other: Other solution
        """

        new_sol1, new_sol2 = {}, {}
        day1, slot1, group_id1 = random.choice([(day, slot, group.id) for day, slot in self.solution for group, i in self.solution[(day, slot)] if i == 1])
        day2, slot2, group_id2 = random.choice([(day, slot, group.id) for day, slot in other.solution for group, i in other.solution[(day, slot)] if i == 1])
        idx1 = max([group.id for timeslot in other.solution for group, _ in other.solution[timeslot]])
        idx2 = max([group.id for timeslot in self.solution for group, _ in self.solution[timeslot]])
        n_students1 = [group.number_of_students for day, slot in self.solution
                       for group, i in self.solution[(day, slot)] if day == day1 and group.id == group_id1 and i == 1][0]
        n_students2 = [group.number_of_students for day, slot in other.solution
                       for group, i in other.solution[(day, slot)] if day == day2 and group.id == group_id2 and i == 1][0]
        levels1, levels2 = {i: 0 for i in range(1, 3 + 1)}, {i: 0 for i in range(1, 3 + 1)}
        group1, group2 = None, None

        print(day1, day2)
        print(slot1, slot2)

        for (day, slot), group_info in self.solution.items():
            if day != day1:
                new_sol1[(day, slot)] = group_info
                continue

            for group, i in group_info:
                if i != 1:
                    continue

                if group.id == group_id1:
                    # for level, num in group.number_of_students.items():
                    #     levels1[level] += num

                    group1 = deepcopy(group)
                    group1.id = idx1 + 1
                    group1.number_of_students = n_students2

                else:
                    for j in range(group.duration):
                        if (day1, slot + j) in new_sol1:
                            new_sol1[(day1, slot + j)].append((group, j + 1))

                        else:
                            new_sol1[(day1, slot + j)] = [(group, j + 1)]

        for (day, slot), group_info in other.solution.items():
            if day != day2:
                new_sol2[(day, slot)] = group_info
                continue

            for group, i in group_info:
                if i != 1:
                    continue

                if group.id == group_id2:
                    # for level, num in group.number_of_students.items():
                    #     levels2[level] += num

                    group2 = deepcopy(group)
                    group2.id = idx2 + 1
                    group2.number_of_students = n_students1

                else:
                    for j in range(group.duration):
                        if (day2, slot + j) in new_sol2:
                            new_sol2[(day2, slot + j)].append((group, j + 1))

                        else:
                            new_sol2[(day2, slot + j)] = [(group, j + 1)]


        to_delete2 = []

        for j in range(self.duration):
            if (day1, slot1 + j) in new_sol2:
                for group, i in new_sol2[(day1, slot1 + j)]:
                    if group.classroom == group1.classroom or group.teacher == group1.teacher:
                        to_delete2.append((day1, slot1 + j - i + 1, group.id))

                        for level, num in group.number_of_students.items():
                            levels2[level] += num

        to_delete2 = list(set(to_delete2))

        for day, slot, group_id in to_delete2:
            for j in range(self.duration):
                if (day, slot + j) in new_sol2:
                    group_info = []

                    for group, i in new_sol2[(day, slot + j)]:
                        if group.id != group_id:
                            group_info.append((group, i))

                    if group_info:
                        new_sol2[(day, slot + j)] = group_info

                    else:
                        del new_sol2[(day, slot + j)]

        for j in range(self.duration):
            if (day1, slot1 + j) in new_sol2:
                new_sol2[(day1, slot1 + j)].append((group1, j + 1))

            else:
                new_sol2[(day1, slot1 + j)] = [(group1, j + 1)]

        to_delete1 = []

        for j in range(self.duration):
            if (day2, slot2 + j) in new_sol1:
                for group, i in new_sol1[(day2, slot2 + j)]:
                    if group.classroom == group2.classroom or group.teacher == group2.teacher:
                        to_delete1.append((day2, slot2 + j - i + 1, group.id))

                        for level, num in group.number_of_students.items():
                            levels1[level] += num

        to_delete1 = list(set(to_delete2))

        for day, slot, group_id in to_delete1:
            for j in range(self.duration):
                if (day, slot + j) in new_sol1:
                    group_info = []

                    for group, i in new_sol1[(day, slot + j)]:
                        if group.id != group_id:
                            group_info.append((group, i))

                    if group_info:
                        new_sol1[(day, slot + j)] = group_info

                    else:
                        del new_sol1[(day, slot + j)]

        for j in range(self.duration):
            if (day2, slot2 + j) in new_sol1:
                new_sol1[(day2, slot2 + j)].append((group2, j + 1))

            else:
                new_sol1[(day2, slot2 + j)] = [(group2, j + 1)]

        new_sol1 = Solution(new_sol1, self.possible_slots, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)
        new_sol2 = Solution(new_sol2, self.possible_slots, self.limit, self.duration, self.classrooms, self.teachers,
                            self.working_hours, self.mutation_method, self.crossover_method)

        for i in range(len(to_delete2)):
            new_sol2.assign(levels2, idx1 + i + 1)

        for i in range(len(to_delete1)):
            new_sol1.assign(levels1, idx2 + i + 1)

        print(levels1)
        print(levels2)

        return new_sol1, new_sol2


def connect_groups(groups: List[Group], limit: int, connection_probability: float = 0.5) -> List[Group]:
    """
    Connect groups with students on similar level
    """
    to_connect: List[Tuple[Group, int]] = []  # groups that can be connected
    for g in groups:
        if sum(g.number_of_students.values()) < limit:
            to_connect.append((g, sum(g.number_of_students.values())))
    to_connect.sort(key=lambda x: x[0].level)
    iterator = 0
    while iterator < len(to_connect) - 1:
        connected = False
        if to_connect[iterator][1] + to_connect[iterator + 1][1] <= limit:
            if random.random() < connection_probability:
                g1 = to_connect[iterator][0]
                g2 = to_connect[iterator + 1][0]
                levels = g1.number_of_students
                for l in g2.number_of_students.keys():
                    if l in levels.keys():
                        levels[l] += g2.number_of_students[l]
                    else:
                        levels[l] = g2.number_of_students[l]
                keys_list = list(levels.keys())
                keys_list.sort()
                if len(keys_list) == 2 and keys_list[1] - keys_list[0] == 1:
                    connected = True
                    lev = keys_list[0] if levels[keys_list[0]] > levels[keys_list[1]] else keys_list[1]
                    new_group = Group(g1.id, lev, g1.duration, levels, g1.teacher, g1.classroom)
                    groups.remove(g1)
                    groups.remove(g2)
                    groups.append(new_group)
                elif len(keys_list) == 3 and keys_list[1] - keys_list[0] == 1 and keys_list[2] - keys_list[1] == 1:
                    connected = True
                    new_group = Group(g1.id, keys_list[1], g1.duration, levels, g1.teacher, g1.classroom)
                    groups.remove(g1)
                    groups.remove(g2)
                    groups.append(new_group)
        iterator += 2 if connected else 1
    return groups