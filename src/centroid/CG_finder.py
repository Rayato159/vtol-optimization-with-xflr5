from GA_CG import GA

cg = GA(
    chromosome_length=16*3, 
    bits=16,
    population_num=100, 
    generation=100, 
    crossover_prob=0.95, 
    mutation_prob=0.01, 
    k=3,
    # rate=1.0,
    lower_bounds=[
        0,
        0,
        -0.6
    ],
    upper_bounds=[
        2,
        2,
        0
    ]
)

solution = cg.run()