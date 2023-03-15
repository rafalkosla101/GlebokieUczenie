# File with implemented class representing single population

from typing import List
from Solution import Solution

class Population:
    """
    Default class for Population.
    """
    def __init__(self, population: List[Solution]):
        self._population = population
        self._population_size = len(population)

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
        Default selection method - selects 2 best solutions from population.
        """
        return self._population[:2]
