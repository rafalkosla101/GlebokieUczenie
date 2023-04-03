# File with implemented class representing single solution

from typing import List, Dict, Tuple

from src.Group import Group
from initial_solution import Day, Slot, Room, Lector
from enum import Enum

import random
import copy


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


class Solution():
    def __init__(self,
                 solution: Dict[Tuple[Day, Slot], List[Tuple[Group, int]]], 
                 possible_slots: Dict[Tuple[Day, Slot], Tuple[List[Room], List[Lector]]],
                 mutation_method: Mutation=Mutation.SHIFT,
                 crossover_method: Crossover=Crossover.ALL_DAY):
        self.solution = solution
        self.possible_slots = possible_slots
        self.mutation_method = mutation_method
        self.crossover_method = crossover_method

    def calculate_fitness(self) -> float:
        """
        Calculates fitness and returns it.
        """
        pass

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
            return self._crossover_all_day()
        elif self.crossover_method == Crossover.SINGLE_BLOCK:
            return self._crossover_single_block()
        
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
                return Solution(new_sol, new_poss_slots)
            possible_slots_to_change.remove(slot_to_change)
        return Solution(new_sol, new_poss_slots)
    
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
                return Solution(new_sol, new_poss_slot)
            possible_slots_to_change.remove(slot_to_change)
        return Solution(new_sol, new_poss_slot)
    
    def _crossover_all_day(self, sol2: 'Solution') -> Tuple['Solution', 'Solution']:
        """
        Function to perform the crossover of two solutions
        :param self: First solution
        :param sol2: Second solution
        """

        new_sol1 = {}
        new_sol2 = {}

        day1, day2 = random.randrange(1, 6), random.randrange(1, 6)

        for (day, slot), group_info in self.solution.items():
            if day == day1:
                new_sol2[(day, slot)] = group_info

            else:
                new_sol1[(day, slot)] = group_info

        for (day, slot), group_info in sol2.solution.items():
            if day == day2:
                new_sol1[(day, slot)] = group_info

            else:
                new_sol2[(day, slot)] = group_info

        new_sol1 = Solution(new_sol1, self.possible_slots, self.mutation_method, self.crossover_method)
        new_sol2 = Solution(new_sol2, self.possible_slots, self.mutation_method, self.crossover_method)
        
        return new_sol1, new_sol2
