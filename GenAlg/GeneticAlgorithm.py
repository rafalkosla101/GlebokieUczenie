# File with implemented universal class for solving genetic algorithm problem

from GenAlg.Population import Population, Solution
from GenAlg.shared_types import List


class GeneticAlgorithm:
    """
    Class implementing genetic algorithm.
    """
    def __init__(self, initial_population: Population, n_generations: int):
        self._initial_population = initial_population
        self._population_class = type(initial_population)
        self._n_generations = n_generations
        self._population_size = initial_population.get_population_size()

    def solve(self) -> List[Solution]:
        """
        Method for solving problem with genetic algorithm.
        """
        best_solutions: List[Solution] = []
        current_population: Population = self._initial_population

        for _ in range(self._n_generations):
            current_population.sort_by_fitness()
            best_solutions.append(current_population.get_best_solution())
            new_population = Population([])

            for _ in range(0, self._population_size, 2):

                # Selection
                selected_a, selected_b = current_population.selection()

                # Crossover
                crossovered_a, crossovered_b = selected_a.crossover(selected_b)

                # Mutation
                mutated_a = crossovered_a.mutate()
                mutated_b = crossovered_b.mutate()

                # Add to new population
                new_population.add(mutated_a)
                new_population.add(mutated_b)
            
            current_population = new_population.choose_best_including_other(current_population)
        
        return best_solutions
