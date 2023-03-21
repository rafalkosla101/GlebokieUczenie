# File with implemented class representing single solution

from typing import List, Dict, Tuple
from abc import ABC, abstractmethod


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


