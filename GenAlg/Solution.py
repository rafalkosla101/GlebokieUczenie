# File with implemented class representing single solution

from typing import List, Dict, Tuple
from abc import ABC, abstractmethod

from src.Group import Group
from initial_solution import Day, Slot, Room, Lector

import random
import copy

class Solution(ABC):
    @abstractmethod
    def __init__(self):
        self.fitness_score = None
        self.solution = None

    @abstractmethod
    def calculate_fitness(self) -> float:
        """
        Calculates fitness and returns it.
        """
        pass

    @abstractmethod
    def is_feasible(self) -> bool:
        """
        Checks if solution is feasible.
        """
        pass

    @abstractmethod
    def mutate(self) -> 'Solution':
        """
        Copies solution and returns mutated copy.
        """
        pass

    @abstractmethod
    def crossover(self, other: 'Solution') -> List['Solution']:
        """
        Performs crossover with 'other' and returns a List of two solutions.
        """
        pass


class SolutionConcrete(Solution):
    def __init__(self, solution: Dict[Tuple[Day, Slot], List[Tuple[Group, int]]], possible_slots: Dict[Tuple[Day, Slot], Tuple[List[Room], List[Lector]]]):
        super().__init__()
        self.solution = solution
        self.possible_slots = possible_slots

    def calculate_fitness(self) -> float:
        return None

    def is_feasible(self) -> bool:
        return None

    def mutate(self) -> 'SolutionConcrete':
        return None

    def crossover(self, other: 'SolutionConcrete') -> List['SolutionConcrete']:
        return None

    def mutate_shift(self) -> 'SolutionConcrete':
        new_sol = copy.deepcopy(self.solution)
        new_poss_slots = copy.deepcopy(self.possible_slots)
        possible_slots_to_change = list(new_sol.keys())
        while possible_slots_to_change:
            slot_to_change = random.choice(possible_slots_to_change)
            possible_group_to_change = new_sol[slot_to_change]
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
                return SolutionConcrete(new_sol, new_poss_slots)
            possible_slots_to_change.remove(slot_to_change)
        return SolutionConcrete(new_sol, new_poss_slots)




