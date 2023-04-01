# File with implemented class representing single population

from typing import List
from GenAlg.Solution import Solution
from enum import Enum
import random


class Selection(Enum):
    """
    Enum of selection types
    """
    BEST = 0
    ROULETTE = 1
    TOURNAMENT = 2


class Population:
    """
    Default class for Population.
    """

    def __init__(self, population: List[Solution], selection_type: Selection=Selection.ROULETTE):
        self._population = population
        self._population_size = len(population)
        self._selection_type = selection_type

    def add(self, other: Solution) -> None:
        """
        Adds solution to population.
        """
        self._population.append(other)
        self._population_size += 1

    def sort_by_fitness(self) -> List[Solution]:
        """
        Returns population list sorted ascending by fitness.
        """
        return sorted(self._population, key=lambda s: s.calculate_fitness())
    
    def get_best_solution(self) -> Solution:
        """
        Returns best solution by calculating fitness. 
        """
        return max(self._population, key=lambda s: s.calculate_fitness())
    
    def get_population_size(self) -> int:
        """
        Returns population size.
        """
        return self._population_size
    
    def choose_best_including_other(self, other: 'Population') -> List[Solution]:
        """
        Returns best _population_size solutions from self and other.
        """
        return sorted(self._population + other._population, key=lambda s: s.calculate_fitness())[:self._population_size]
    
    def selection(self) -> List[Solution]:
        """
        Selects 2 solutions with different methods
        """
        if self._selection_type == Selection.BEST:
            return self._selection_best()
        elif self._selection_type == Selection.ROULETTE:
            return self._selection_roulette()
        elif self._selection_type == Selection.TOURNAMENT:
            return self._selection_tournament()

    def _selection_best(self) -> List[Solution]:
        """
        Selects 2 best solutions
        """
        return self.sort_by_fitness()[:2]
    
    def _selection_roulette(self) -> List[Solution]:
        """
        Selects 2 solutions with roulette method
        """
        def choose_one_solution(population: List[Solution]) -> int:
            fitness_sum = sum([sol.calculate_fitness() for sol in population])
            random_point = random.uniform(0, fitness_sum)
            partial_sum = 0
            solution_idx = 0

            while partial_sum < random_point:
                partial_sum += population[solution_idx].calculate_fitness()
                solution_idx += 1
            
            return solution_idx + 1
        
        first_solution_idx = choose_one_solution(self._population)
        second_solution_idx = choose_one_solution(self._population[:first_solution_idx] + self._population[first_solution_idx+1])

        return [self._population[first_solution_idx], self._population[second_solution_idx]]


    def _selection_tournament(self, number_of_participants: int=3) -> List[Solution]:
        """
        Selects 2 solutions with tournament method
        """
        def choose_one_solution(population: List[Solution], number_of_participants: int) -> int:
            participants_idx_list = random.sample(range(len(population)), number_of_participants)
            return max([idx for idx in participants_idx_list], key=lambda s: population[s].calculate_fitness())
        
        first_solution_idx = choose_one_solution(self._population, number_of_participants)
        second_solution_idx = choose_one_solution(self._population[:first_solution_idx] + self._population[first_solution_idx+1], number_of_participants)

        return [self._population[first_solution_idx], self._population[second_solution_idx]]
