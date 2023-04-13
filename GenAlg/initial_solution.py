from GenAlg.Solution import Solution, connect_groups
from GenAlg.shared_types import *
from copy import deepcopy


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


def random_initial_solution(students: List[int], limit: int, duration: int, classroom: List[Classroom], teacher: List[Teacher], working_hours: Dict[Day, List[Slot]], connection_probability: float = 0.5):
    """
    Create one random solution
    """

    groups = create_groups(students, limit, list(set(students)), duration)
    groups = connect_groups(groups, limit, connection_probability)  # do zakomentowania jeśli nie chcemy łączenia grup przy generacji rozwiązań początkowych
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
        if not possible_first_slots:
            raise ValueError('Cannot create initial solution, too much students')
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