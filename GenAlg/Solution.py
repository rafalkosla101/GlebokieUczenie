# File with implemented class representing single solution

from typing import List, Type
from abc import ABC, abstractmethod

class Solution(ABC):
    @abstractmethod
    def __init__(self):
        self.fitness_score = None
        self.solution = None

    @abstractmethod
    def calculate_fitness(self) -> int:
        pass

    @abstractmethod
    def is_feasible(self) -> bool:
        pass

    @abstractmethod
    def mutate(self) -> 'Solution':
        pass

    @abstractmethod
    def crossover(self, other: 'Solution') -> List['Solution']:
        pass