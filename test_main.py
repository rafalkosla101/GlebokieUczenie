from GenAlg.Solution import *
from GenAlg.GeneticAlgorithm import *
from GenAlg.Population import *
from GenAlg.initial_solution import *
from GenAlg.run_genetic_algorithm import run_genetic_algorithm, plot_fitness


if __name__ == '__main__':
    students = [1, 1, 2, 3, 1, 2, 3, 1, 2, 3, 3, 3, 2, 1, 1, 1, 1]
    limit = 3
    duration = 4
    classoom = [Classroom(), Classroom(), Classroom()]
    teacher = [Teacher({1: [1, 2, 3, 4, 5, 6], 2: [2, 3, 4, 5], 4: [1, 2, 3, 4]}), Teacher({2: [1, 2, 3, 4], 3: [2, 3, 4, 5], 5: [1, 2, 3, 4, 5, 6, 7, 8]})]
    working_hours = {1: [1, 2, 3, 4, 5, 6, 7, 8], 2: [1, 2, 3, 4, 5, 6, 7, 8], 3: [1, 2, 3, 4, 5, 6, 7, 8], 4: [1, 2, 3, 4, 5, 6, 7, 8], 5: [1, 2, 3, 4, 5, 6, 7, 8]}
    #solution1, poss_slots1 = random_initial_solution(students, limit, duration, classoom, teacher, working_hours)
    # solution2, poss_slots2 = random_initial_solution(students, limit, duration, classoom, teacher, working_hours)
    # sol1 = Solution(solution1, poss_slots1)
    # sol2 = Solution(solution2, poss_slots2)
    # display_solutions(sol1, sol2, working_hours)
    # new_sol1, new_sol2 = sol1.crossover(sol2)
    # display_solutions(new_sol1, new_sol2, working_hours)

    results = run_genetic_algorithm(10, 10, Selection.BEST, Mutation.SHIFT, Crossover.ALL_DAY)
    '''
    for slot in results[0].solution:
        print(slot)
        for group in results[0].solution[slot]:
            print(group[0])
    '''
    display_solutions(results[0], results[1], working_hours)

