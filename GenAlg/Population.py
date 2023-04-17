# File with implemented class representing single population

from GenAlg.Solution import Solution
from GenAlg.shared_types import *


class Population:
    """
    Default class for Population.
    """

    def __init__(self, population: List[Solution], selection_type: Selection):
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
        Returns population list sorted descending by fitness.
        """
        return sorted(self._population, key=lambda s: s.calculate_fitness())
    
    def get_best_solution(self) -> Solution:
        """
        Returns best solution by calculating fitness (min value). 
        """
        return min(self._population, key=lambda s: s.calculate_fitness())
    
    def get_population_size(self) -> int:
        """
        Returns population size.
        """
        return self._population_size
    
    def choose_best_including_other(self, other: 'Population') -> List[Solution]:
        """
        Returns best _population_size solutions from self and other.
        """
        population_list = sorted(self._population + other._population, key=lambda s: s.calculate_fitness())[:self._population_size]
        return Population(population_list, self._selection_type)
    
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
            fitness_inv = [1 / sol.calculate_fitness() for sol in population]
            fitness_sum = sum(fitness_inv)
            random_point = random.uniform(0, fitness_sum)
            solution_idx = 0
            partial_sum = fitness_inv[solution_idx]

            while partial_sum < random_point:
                solution_idx += 1
                partial_sum += fitness_inv[solution_idx]
            
            return solution_idx
        
        first_solution_idx = choose_one_solution(self._population)
        second_solution_idx = choose_one_solution(self._population[:first_solution_idx] + self._population[first_solution_idx+1:])

        return [self._population[first_solution_idx], self._population[second_solution_idx]]


    def _selection_tournament(self, number_of_participants: int=3) -> List[Solution]:
        """
        Selects 2 solutions with tournament method
        """
        def choose_one_solution(population: List[Solution], number_of_participants: int) -> int:
            participants_idx_list = random.sample(range(len(population)), number_of_participants)
            return min([idx for idx in participants_idx_list], key=lambda s: population[s].calculate_fitness())
        
        first_solution_idx = choose_one_solution(self._population, number_of_participants)
        second_solution_idx = choose_one_solution(self._population[:first_solution_idx] + self._population[first_solution_idx+1:], number_of_participants)

        return [self._population[first_solution_idx], self._population[second_solution_idx]]
