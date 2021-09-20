from GeneticAlgorithm import GA

test =GA(chromosome_length=88, 
         bits=8,
         population_num=100, 
         generation=30, 
         crossover_prob=0.9, 
         mutation_prob=0.03, 
         k=3,
         rate=0.2)

solution = test.run()

print()
print(solution)