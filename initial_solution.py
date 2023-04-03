from src.Teacher import Teacher
from src.Classroom import Classroom
from src.Student import Student
from src.Group import Group
from src.TimeSlot import TimeSlot
from GenAlg.Solution import Solution


from typing import List, Dict, Tuple

import random
import matplotlib.pyplot as plt
import numpy as np

from matplotlib import patches
from copy import deepcopy

Day = int
Slot = int
Room = int
Lector = int
#Solution = Dict[Tuple[Day, Slot], List[Tuple[Group, int]]]


def create_groups(students: List[int], limit: int, possible_levels: List[int], duration: int) -> List[Group]:
    """
    Divide students into groups
    """
    students_by_levels: Dict[int, int] = {}
    possible_levels.sort()
    for level in possible_levels:
        count = students.count(level)
        students_by_levels[level] = count
    groups: List[Group] = []
    groupid: int = 0

    for level in possible_levels:
        while students_by_levels[level] >= limit:
            groups.append(Group(groupid, level, duration, {level: limit}, None, None))
            groupid += 1
            students_by_levels[level] -= limit
        if students_by_levels[level] > 0:
            groups.append(Group(groupid, level, duration, {level: students_by_levels[level]}, None, None))
            groupid += 1
    return groups


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


def random_initial_solution(students: List[int], limit: int, duration: int, classroom: List[Classroom], teacher: List[Teacher], working_hours: Dict[Day, List[Slot]]):
    """
    Create one random solution
    """

    groups = create_groups(students, limit, list(set(students)), duration)
    groups = connect_groups(groups, limit)  # do zakomentowania jeśli nie chcemy łączenia grup przy generacji rozwiązań początkowych
    possible_slots: Dict[Tuple[Day, Slot], Tuple[List[Room], List[Lector]]] = {}  # możliwe sloty do wybrania: dniu i id slotu przypisane są możliwe do wyboru sale i lektorzy
    possible_first_slots: Dict[Tuple[Day, Slot], Tuple[List[Room], List[Lector]]] = {}
    classroom_id: List[Room] = [c.id for c in classroom]
    teacher_id: List[Lector] = [t.id for t in teacher]
    for day in working_hours.keys():
        for slot in working_hours[day]:
            possible_slots[(day, slot)] = (deepcopy(classroom_id), deepcopy(teacher_id))
        for slot in working_hours[day][:-duration+1]:
            possible_first_slots[(day, slot)] = (deepcopy(classroom_id), deepcopy(teacher_id))

    solution: Dict[Tuple[Day, Slot], List[Tuple[Group, int]]] = {}

    for g in groups:
        first_slot = random.choice(list(possible_first_slots.keys()))
        chosen_room = random.choice(possible_first_slots[first_slot][0])
        chosen_teacher = random.choice(possible_first_slots[first_slot][1])
        g.teacher = chosen_teacher
        g.classroom = chosen_room
        for i in range(duration):
            key = (first_slot[0], first_slot[1] + i)
            if key in solution.keys():
                solution[key].append((g, i + 1))
            else:
                solution[key] = [(g, i + 1)]
            possible_slots[key][0].remove(chosen_room)
            possible_slots[key][1].remove(chosen_teacher)
            if not possible_slots[key][0] or not possible_slots[key][1]:
                possible_slots.pop(key)

            if key in possible_first_slots.keys():
                if chosen_room in possible_first_slots[key][0]:
                    possible_first_slots[key][0].remove(chosen_room)
                if chosen_teacher in possible_first_slots[key][1]:
                    possible_first_slots[key][1].remove(chosen_teacher)
                if not possible_first_slots[key][0] or not possible_first_slots[key][1]:
                    possible_first_slots.pop(key)

            key2 = (first_slot[0], first_slot[1] - i)
            if key2 in possible_first_slots.keys():
                if chosen_room in possible_first_slots[key2][0]:
                    possible_first_slots[key2][0].remove(chosen_room)
                if chosen_teacher in possible_first_slots[key2][1]:
                    possible_first_slots[key2][1].remove(chosen_teacher)
                if not possible_first_slots[key2][0] or not possible_first_slots[key2][1]:
                    possible_first_slots.pop(key2)

    return solution, possible_slots


def display_solutions(solution1: Solution, solution2: Solution, working_hours: Dict[int, List[int]]) -> None:
    """
    Function to display solutions
    :param sol1: First solution
    :param sol2: Second solution
    :param working_hours: Working hours
    """
    sol1 = solution1.solution
    sol2 = solution2.solution

    max_slot = max([slot for day in range(1, 5 + 1) for slot in working_hours[day]])
    groups1 = list(set([group.id for timeslot in sol1 for group, _ in sol1[timeslot]]))
    groups2 = list(set([group.id for timeslot in sol2 for group, _ in sol2[timeslot]]))

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    for day in range(1, 5 + 1):
        for slot in range(1, max_slot + 1):
            rect = patches.Rectangle((0, -30 * ((day - 1) * max_slot + slot - 1)), 30, -30, edgecolor="black", facecolor="blue", linewidth=1)
            ax.add_patch(rect)
            rx, ry = rect.get_xy()
            cx = rx + rect.get_width() / 2.0
            cy = ry + rect.get_height() / 2.0
            ax.annotate(f"({day}, {slot})", (cx, cy), color="black", fontsize=5, ha="center", va="center")

            if (day, slot) in sol1:
                for group, _ in sol1[(day, slot)]:
                    rect = patches.Rectangle((30 * (groups1.index(group.id) + 1), -30 * ((day - 1) * max_slot + slot)), 30, -30, edgecolor="black", facecolor="orange", linewidth=1)
                    ax.add_patch(rect)
                    rx, ry = rect.get_xy()
                    cx = rx + rect.get_width() / 2.0
                    cy = ry + rect.get_height() / 2.0
                    ax.annotate(str(group), (cx, cy), color="black", fontsize=5, ha="center", va="center")

            if (day, slot) in sol2:
                for group, _ in sol2[(day, slot)]:
                    rect = patches.Rectangle((30 * (groups2.index(group.id) + 1 + len(groups1)), -30 * ((day - 1) * max_slot + slot)), 30, -30, edgecolor="black", facecolor="green", linewidth=1)
                    ax.add_patch(rect)
                    rx, ry = rect.get_xy()
                    cx = rx + rect.get_width() / 2.0
                    cy = ry + rect.get_height() / 2.0
                    ax.annotate(str(group), (cx, cy), color="black", fontsize=5, ha="center", va="center")

    plt.axvline(x=30 * (1 + len(groups1)))
    plt.xlim([-5, 30 * (len(groups1) + len(groups2) + 1)])
    plt.ylim([-30 * (max_slot * 5 + 1), 5])
    plt.show()


if __name__ == '__main__':
    students = [1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 3, 2, 1, 1, 1, 1]
    limit = 3
    duration = 4
    classoom = [Classroom(), Classroom(), Classroom()]
    teacher = [Teacher({1: [1, 2, 3, 4, 5, 6], 2: [2, 3, 4, 5], 4: [1, 2, 3, 4]}), Teacher({2: [1, 2, 3, 4], 3: [2, 3, 4, 5], 5: [1, 2, 3, 4, 5, 6, 7, 8]})]
    working_hours = {1: [1, 2, 3, 4, 5, 6, 7, 8], 2: [1, 2, 3, 4, 5, 6, 7, 8], 3: [1, 2, 3, 4, 5, 6, 7, 8], 4: [1, 2, 3, 4, 5, 6, 7, 8], 5: [1, 2, 3, 4, 5, 6, 7, 8]}
    solution1, poss_slots1 = random_initial_solution(students, limit, duration, classoom, teacher, working_hours)
    solution2, poss_slots2 = random_initial_solution(students, limit, duration, classoom, teacher, working_hours)
    sol1 = Solution(solution1, poss_slots1)
    sol2 = Solution(solution2, poss_slots2)
    display_solutions(sol1, sol2, working_hours)
    new_sol1, new_sol2 = sol1.crossover(sol2)
    display_solutions(new_sol1, new_sol2, working_hours)
