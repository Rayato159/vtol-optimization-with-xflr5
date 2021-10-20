from matplotlib import pyplot as plt
import numpy as np
from GeneticAlgorithm import GA

sizing = GA(
    chromosome_length=16*11, 
    bits=16,
    population_num=20, 
    generation=100, 
    crossover_prob=0.95, 
    mutation_prob=0.01, 
    k=3,
    # rate=1.0,
    lower_bounds=[
        5,
        0.6,
        0,
        0.08,
        3,
        0.09,
        0,
        1.5,
        0.4,
        0.09,
        0
    ],
    upper_bounds=[
        25,
        0.6,
        0,
        0.12,
        3.5,
        0.12,
        0,
        2,
        0.6,
        0.12,
        30
    ]
)

solution = sizing.run()

print()
print(solution)

# generation = 400
# population = [20, 40, 80, 160]
# solution = []

# for i in population:
#     sizing = GA(
#         chromosome_length=16*11, 
#         bits=16,
#         population_num=i, 
#         generation=generation, 
#         crossover_prob=0.95, 
#         mutation_prob=0.01, 
#         k=3,
#         # rate=1.0,
#         lower_bounds=[
#             5,
#             0.6,
#             0,
#             0.08,
#             3,
#             0.09,
#             0,
#             1.5,
#             0.4,
#             0.09,
#             0
#         ],
#         upper_bounds=[
#             25,
#             0.6,
#             0,
#             0.12,
#             3.5,
#             0.12,
#             0,
#             2,
#             0.6,
#             0.12,
#             30
#         ]
#     )

#     solution.append(sizing.run())

# x_plot = np.arange(0, generation, 1)

# p1 = solution[0]
# p2 = solution[1]
# p3 = solution[2]
# p4 = solution[3]

# plt.title(f'GA Generation: {generation}')
# plt.xlabel('Generation')
# plt.ylabel('CD')
# plt.plot(x_plot, p1, color='#F56FAD', label='population 20')
# plt.plot(x_plot, p2, color='#C32BAD', label='population 40')
# plt.plot(x_plot, p3, color='#7027A0', label='population 80')
# plt.plot(x_plot, p4, color='#1DB9C3', label='population 160')
# plt.legend()
# plt.show()