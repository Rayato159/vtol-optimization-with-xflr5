#Create by HashTable159
#Edit this function before used

import numpy as np
import time
from ObjectiveFunction import Obj_Func

class GA:
    def __init__(self, 
                chorosome_length=16, 
                bits=8,
                population_num=100, 
                generation=30, 
                crossover_prob=0.9, 
                mutation_prob=0.03, 
                k=3):

        self.bits = bits
        self.chorosome_length= chorosome_length
        self.population_num = population_num
        self.generation = generation
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.k = int(k)
        self.obj_func = Obj_Func()
    
    def getPopulation(self):
        return np.random.randint(2, size=(self.population_num, self.chorosome_length))

    def decimal(self, binary):
        decimal_result = 0

        for index, bit in enumerate(binary):
            decimal_result += bit*2**(len(binary)-index-1)

        return decimal_result
    
    def objtive_function(self, parameters):
        return round(self.obj_func.function(parameters), 6)

    def decode(self, 
               binary, 
               lower_bounds=[-5, -5], 
               upper_bounds=[5, 5]
               ):

        decode = []
        for i in range(len(lower_bounds)):
            decode.append(round(lower_bounds[i] + self.decimal(binary[self.bits*i:self.bits*(i+1)])*((upper_bounds[i] - lower_bounds[i])/(2**self.bits - 1)), 6))

        return decode, self.objtive_function(decode)

    def binary_swap(self, bit):
        if bit == 0:
            return 1
        else:
            return 0

    def select_parents(self, population):
        winner_parents = np.empty((2, self.chorosome_length))
        
        for i in range(2):
            selected_parents = np.empty((self.k, self.chorosome_length))

            for j in range(self.k):
                rand_num = np.random.randint(len(population))
                selected_parents[j] = population[rand_num]
            
            obj_value = np.empty((self.k, 1))
            for index, element in enumerate(selected_parents):
                obj_value[index] = self.decode(element)[1]

            winner_parents[i] = selected_parents[np.argmin(obj_value)]

        return winner_parents

    def crossover(self, parents):
        rand_crossover_prob = np.random.rand()

        if rand_crossover_prob < self.crossover_prob:
            section_1 = np.random.randint(self.chorosome_length)
            while section_1 == self.chorosome_length-1:
                section_1 = np.random.randint(self.chorosome_length)

            section_2 = np.random.randint(self.chorosome_length)
            while section_2 <= section_1:
                section_2 = np.random.randint(self.chorosome_length)

            for index, _ in enumerate(parents[0]):
                if section_1 <= index <= section_2:
                    parents[0][index], parents[1][index] = parents[1][index], parents[0][index]

            return parents

        return parents

    def mutation(self, childs):
        for index, _ in enumerate(childs[0]):
            rand_mutation_prob = np.random.rand()

            if rand_mutation_prob < self.mutation_prob:
                childs[0][index] = self.binary_swap(childs[0][index])

        for index, _ in enumerate(childs[1]):
            rand_mutation_prob = np.random.rand()

            if rand_mutation_prob < self.mutation_prob:
                childs[1][index] = self.binary_swap(childs[1][index])    
        
        return childs
    
    def run(self):
        pool_of_solution = self.getPopulation()
        start_time = time.time()
        
        for index, element in enumerate(pool_of_solution):
            print(f"LINE\t{index+1}\tf={self.decode(element)[1]}")

        for gen in range(self.generation):
            new_population = np.empty((0, self.chorosome_length))

            for popula in range(int(self.population_num/2)):
                parents = self.select_parents(pool_of_solution)
                childs = self.crossover(parents)
                mutated_childs = self.mutation(childs)
                new_population = np.vstack([new_population, mutated_childs])

                print()
                print(f"Obj_value_for_mutated_chlid #1 at generation #{gen+1} : {mutated_childs[0]}, {self.decode(mutated_childs[0])[1]}")
                print(f"Obj_value_for_mutated_chlid #2 at generation #{gen+1} : {mutated_childs[1]}, {self.decode(mutated_childs[0])[1]}")
            
            pool_of_solution = new_population

            print()
            for index, element in enumerate(new_population):
                print(f"LINE\t{index+1}\tf={self.decode(element)[1]}")

        end_time = time.time()
        execution_time = end_time - start_time

model = GA()
model.run() 