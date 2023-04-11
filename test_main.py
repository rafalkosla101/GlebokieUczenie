from GenAlg.Solution import *
from GenAlg.GeneticAlgorithm import *
from GenAlg.Population import *
from GenAlg.initial_solution import *
from GenAlg.run_genetic_algorithm import run_genetic_algorithm_function


if __name__ == '__main__':
    students = [1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 3, 2, 1, 1, 1, 1]
    limit = 3
    duration = 4
    classoom = [Classroom(), Classroom(), Classroom()]
    teacher = [Teacher({1: [1, 2, 3, 4, 5, 6], 2: [2, 3, 4, 5], 4: [1, 2, 3, 4]}), Teacher({2: [1, 2, 3, 4], 3: [2, 3, 4, 5], 5: [1, 2, 3, 4, 5, 6, 7, 8]})]
    working_hours = {1: [1, 2, 3, 4, 5, 6, 7, 8], 2: [1, 2, 3, 4, 5, 6, 7, 8], 3: [1, 2, 3, 4, 5, 6, 7, 8], 4: [1, 2, 3, 4, 5, 6, 7, 8], 5: [1, 2, 3, 4, 5, 6, 7, 8]}
    solution1, poss_slots1 = random_initial_solution(students, limit, duration, classoom, teacher, working_hours)
    solution2, poss_slots2 = random_initial_solution(students, limit, duration, classoom, teacher, working_hours)
    sol1 = Solution(solution1, poss_slots1)
    sol2 = Solution(solution2, poss_slots2)
    display_solutions(sol1, sol2, working_hours)
    new_sol1, new_sol2 = sol1.crossover(sol2)
    display_solutions(new_sol1, new_sol2, working_hours)

