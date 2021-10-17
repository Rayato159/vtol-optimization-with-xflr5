from GeneticAlgorithm import GA

sizing = GA(
    chromosome_length=16*11, 
    bits=16,
    population_num=100, 
    generation=100, 
    crossover_prob=0.9, 
    mutation_prob=0.03, 
    k=3,
    rate=1.0,
    lower_bounds=[
        13.0,
        0.6,
        0,
        0.14,
        3,
        0.09,
        0,
        1.5,
        0.4,
        0.09,
        0
    ],
    upper_bounds=[
        13.0,
        0.6,
        0,
        0.14,
        3.5,
        0.12,
        0,
        2,
        0.6,
        0.12,
        15
    ]
)

solution = sizing.run()

print()
print(solution)