import pandas as pd
import json

from GenAlg.shared_types import *
from GenAlg.GeneticAlgorithm import *
from GenAlg.initial_solution import *


def prepare_students_list() -> List:
    """
    Extracts data from CSV with students information.
    Gets only second value from tuples (group nr) and skips first element (it's column name). 
    Returns data in List.
    """
    csv_df = pd.read_csv("data-generation/students.csv", delimiter=',', index_col=0)
    students_list = list(csv_df["student_id"].values)
    
    return students_list


def prepare_teachers_list() -> List:
    """
    Extracts data from CSV with teachers information.

    """
    csv_df = pd.read_csv("data-generation/teachers.csv", delimiter=',', index_col=0)
    teachers_list = []
    for col in csv_df.columns:
        teacher_dict = {}
        for day_id in range(len(csv_df)):
            teacher_dict[day_id + 1] = csv_df[col].iloc[day_id]
        teachers_list.append(teacher_dict)
    
    return teachers_list


def read_school_config() -> List:
    with open("data-generation/school_config.json") as f:
        config_dict = json.load(f)

    return config_dict


def run_genetic_alorithm(population_size: int,
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
    working_hours = school_config["working_hours"]
    classrooms = [Classroom() for _ in range(school_config["number_of_classrooms"])]

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
