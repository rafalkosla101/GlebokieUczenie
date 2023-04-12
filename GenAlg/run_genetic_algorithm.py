from GenAlg.GeneticAlgorithm import *
from GenAlg.initial_solution import *
from DataGeneration.generate_data import *


def run_genetic_algorithm(population_size: int,
                         n_generations: int, 
                         selection_type: Selection, 
                         mutation_type: Mutation,
                         crossover_type: Crossover) -> List[Solution]:
    """
    Runs genetic algorithm and returns a result.
    """

    # Read students and teachers information from CSV and school information from JSON file
    students: List = prepare_students_list()
    teachers: List = prepare_teachers_list()
    school_config: Dict = read_school_config()

    limit = school_config["limit"]
    duration = school_config["duration"]
    working_hours_temp = school_config["working_hours"]
    classrooms = [Classroom() for _ in range(school_config["number_of_classrooms"])]
    # Convert type of day in working_hours from str to int
    working_hours = {int(day): working_hours_temp[day] for day in working_hours_temp.keys()}
    # Prepare initial Population
    initial_population: Population = Population([], selection_type)

    for _ in range(population_size):
        sol, poss_slots = random_initial_solution(students, limit, duration, classrooms, teachers, working_hours)
        solution = Solution(sol, poss_slots, mutation_type, crossover_type)
        initial_population.add(solution)
    
    # Run genetic algorithm
    genetic_algorithm = GeneticAlgorithm(initial_population, n_generations)
    best_solutions = genetic_algorithm.solve()

    # Return list of best solutions from every generation
    return best_solutions
