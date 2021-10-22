#Create by HashTable159
#Edit before use.

import numpy as np
import time

from Objective import Aerodynamics
from matplotlib import pyplot as plt

class GA:
    def __init__(self,
                chromosome_length=16*11, 
                bits=16,
                population_num=400, 
                generation=1600, 
                crossover_prob=0.9, 
                mutation_prob=0.03, 
                k=3,
                lower_bounds=[],
                upper_bounds=[]
                ):

        self.bits = bits
        self.chromosome_length = chromosome_length
        self.population_num = population_num
        self.generation = generation
        self.crossover_prob = crossover_prob
        self.mutation_prob = mutation_prob
        self.k = int(k)
        self.obj_func = Aerodynamics()
        self.lower_bounds = lower_bounds
        self.upper_bounds = upper_bounds
        self.camera = 0.153
        self.motors = 1.9
        self.battery = 6.3
    
    def getPopulation(self):
        population = np.empty((0, self.chromosome_length))
        for _ in range(self.population_num):
            while True:
                rand_chromosome = np.random.randint(2, size=(self.chromosome_length))
                rand_param = self.obj_func.result(self.decode(rand_chromosome)[0])

                w_wing = rand_param[30]
                w_h_tail = rand_param[31]
                w_v_tail = rand_param[32]

                print(rand_param)
                if(
                    w_wing + w_h_tail + w_v_tail + self.camera + self.motors + self.battery <= rand_param[0]
                ):
                    break
            population = np.vstack([population, rand_chromosome])
        return population

    def decimal(self, binary):
        decimal_result = 0

        for index, bit in enumerate(binary):
            decimal_result += bit*2**(len(binary)-index-1)

        return decimal_result
    
    def objtive_function(self, parameters):
        return round(self.obj_func.function(parameters), 6)

    def decode(self, binary):

        decode = []
        for i in range(len(self.lower_bounds)):
            decode.append(round(self.lower_bounds[i] + self.decimal(binary[self.bits*i:self.bits*(i+1)])*((self.upper_bounds[i] - self.lower_bounds[i])/(2**self.bits - 1)), 6))

        return decode, self.objtive_function(decode)

    def binary_swap(self, bit):
        if bit == 0:
            return 1
        else:
            return 0

    def select_parents(self, population):
        winner_parents = np.empty((2, self.chromosome_length))
        
        for i in range(2):
            selected_parents = np.empty((self.k, self.chromosome_length))

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
            section_1 = np.random.randint(self.chromosome_length)
            while section_1 == self.chromosome_length-1:
                section_1 = np.random.randint(self.chromosome_length)

            section_2 = np.random.randint(self.chromosome_length)
            while section_2 <= section_1:
                section_2 = np.random.randint(self.chromosome_length)

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
        count = 0
        pool_of_generation = self.getPopulation()
        best_of_generation = np.empty((0, 2))
        best_of_all_stack = np.empty((0, 2))
        best_of_all = np.empty((0, 2))
        start_time = time.time()
        stack_plot = []

        print("First generation")
        for index, element in enumerate(pool_of_generation):
            print(f"LINE\t{index+1}\tf={self.decode(element)[1]}")

        for gen in range(self.generation):
            new_population = np.empty((0, self.chromosome_length))

            for _ in range(int(self.population_num/2)):
                #constraints
                while True:
                    parents = self.select_parents(pool_of_generation)
                    childs = self.crossover(parents)
                    mutated_childs = self.mutation(childs)

                    decode_1 = self.obj_func.result(self.decode(mutated_childs[0])[0])
                    decode_2 = self.obj_func.result(self.decode(mutated_childs[1])[0])

                    w_wing_1 = decode_1[30]
                    w_h_tail_1 = decode_1[31]
                    w_v_tail_1 = decode_1[32]

                    w_wing_2 = decode_2[30]
                    w_h_tail_2 = decode_2[31]
                    w_v_tail_2 = decode_2[32]
                    
                    if(
                        w_wing_1 + w_h_tail_1 + w_v_tail_1 + self.camera + self.motors + self.battery <= decode_1[0]
                        and w_wing_2 + w_h_tail_2 + w_v_tail_2 + self.camera + self.motors + self.battery <= decode_2[0]
                    ):
                        break

                new_population = np.vstack([new_population, mutated_childs])
            
            pool_of_generation = new_population
            count = gen+1

            print()
            print(f"Generation #{gen+1}")
            for index, element in enumerate(new_population):
                print(f"LINE\t{index+1}\tf={self.decode(element)[1]}")
                best_of_all_stack = np.vstack([best_of_all_stack, self.decode(element)])

            best_of_generation_stack = np.empty((0, 1))
            for index, element in enumerate(new_population):
                best_of_generation_stack = np.vstack([best_of_generation_stack, self.decode(element)[1]])
            
            best_of_generation = self.decode(new_population[np.argmin(best_of_generation_stack)])
            stack_plot.append(best_of_generation[1])

        best_of_all_find = np.empty((0, 1))
        for item in best_of_all_stack:
            best_of_all_find = np.vstack([best_of_all_find, item[1]])
        best_of_all = best_of_all_stack[np.argmin(best_of_all_find)]

        end_time = time.time()
        execution_time = end_time - start_time

        # x_plot = np.arange(0, self.generation, 1)
        # plt.title(f'Generation: {self.generation}, Population: {self.population_num}')
        # plt.plot(x_plot, stack_plot, color='#FF0075')
        # plt.show()

        print()
        print('best_of_generation')
        result_generation = self.obj_func.result(best_of_generation[0])

        w_wing = self.obj_func.wing_weight(result_generation[0], result_generation[7], result_generation[4], result_generation[1])
        # w_h_tail = self.obj_func.h_tail_weight(result_generation[0], result_generation[28], result_generation[15], result_generation[4], result_generation[6])
        # w_v_tail = self.obj_func.v_tail_weight(result_generation[0], result_generation[29], result_generation[7], result_generation[22], result_generation[21])
        w_h_tail = self.obj_func.wing_weight(result_generation[0], result_generation[28], result_generation[15], 0.09)
        w_v_tail = self.obj_func.wing_weight(result_generation[0], result_generation[29], result_generation[22], 0.09)

        print(f'MTOW:\t{round(result_generation[0], 2)}')
        print(f'cr:\t{round(result_generation[1], 2)}')
        print(f'ct:\t{round(result_generation[2], 2)}')
        print(f'taper_ratio:\t{round(result_generation[3], 2)}')
        print(f'swept:\t{round(result_generation[4], 2)}')
        print(f'b:\t{round(result_generation[5], 2)}')
        print(f'mac:\t{round(result_generation[6], 2)}')
        print(f'S:\t{round(result_generation[7], 2)}')
        print(f'AR:\t{round(result_generation[8], 1)}')
        print(f'e:\t{round(result_generation[9], 2)}')
        print(f'Cl:\t{round(result_generation[10], 6)}')
        print(f'Cdi:\t{round(result_generation[11], 6)}')
        print(f'Cd0_w:\t{round(result_generation[12], 6)}')
        print(f't_c_h:\t{round(result_generation[13], 2)}')
        print(f'swept_h:\t{round(result_generation[14], 2)}')
        print(f'b_h:\t{round(result_generation[15], 2)}')
        print(f'c_h:\t{round(result_generation[16], 2)}')
        print(f'Cd0_h:\t{round(result_generation[17], 6)}')
        print(f'AR_v:\t{round(result_generation[18], 1)}')
        print(f'taper_ratio_v:\t{round(result_generation[19], 2)}')
        print(f't_c_v:\t{round(result_generation[20], 2)}')
        print(f'swept_v:\t{round(result_generation[21], 2)}')
        print(f'b_v:\t{round(result_generation[22], 2)}')
        print(f'cr_v:\t{round(result_generation[23], 2)}')
        print(f'ct_v:\t{round(result_generation[24], 2)}')
        print(f'mac_v:\t{round(result_generation[25], 2)}')
        print(f'lv:\t{round(result_generation[33], 2)}')
        print(f'Cd0_v:\t{round(result_generation[26], 6)}')
        print(f'CD:\t{round(result_generation[27], 6)}')
        print('weight_of_component')
        print(f'w_wing:\t{round(w_wing, 2)}')
        print(f'w_h_tail:\t{round(w_h_tail, 2)}')
        print(f'w_v_tail:\t{round(w_v_tail, 2)}')
        
        print()
        print('best_of_all')
        result_all = self.obj_func.result(best_of_all[0])

        w_wing = self.obj_func.wing_weight(result_all[0], result_all[7], result_all[4], result_all[1])
        w_h_tail = self.obj_func.wing_weight(result_all[0], result_all[28], result_all[15], 0.09)
        w_v_tail = self.obj_func.wing_weight(result_all[0], result_all[29], result_all[22], 0.09)
        # w_h_tail = self.obj_func.h_tail_weight(result_all[0], result_all[28], result_all[15], result_all[4], result_all[6])
        # w_v_tail = self.obj_func.v_tail_weight(result_all[0], result_all[29], result_all[7], result_all[22], result_all[21])

        print(f'MTOW:\t{round(result_all[0], 2)}')
        print(f'cr:\t{round(result_all[1], 2)}')
        print(f'ct:\t{round(result_all[2], 2)}')
        print(f'taper_ratio:\t{round(result_all[3], 2)}')
        print(f'swept:\t{round(result_all[4], 2)}')
        print(f'b:\t{round(result_all[5], 2)}')
        print(f'mac:\t{round(result_all[6], 2)}')
        print(f'S:\t{round(result_all[7], 2)}')
        print(f'AR:\t{round(result_all[8], 1)}')
        print(f'e:\t{round(result_all[9], 2)}')
        print(f'Cl:\t{round(result_all[10], 6)}')
        print(f'Cdi:\t{round(result_all[11], 6)}')
        print(f'Cd0_w:\t{round(result_all[12], 6)}')
        print(f't_c_h:\t{round(result_all[13], 2)}')
        print(f'swept_h:\t{round(result_all[14], 2)}')
        print(f'b_h:\t{round(result_all[15], 2)}')
        print(f'c_h:\t{round(result_all[16], 2)}')
        print(f'Cd0_h:\t{round(result_all[17], 6)}')
        print(f'AR_v:\t{round(result_all[18], 1)}')
        print(f'taper_ratio_v:\t{round(result_all[19], 2)}')
        print(f't_c_v:\t{round(result_all[20], 2)}')
        print(f'swept_v:\t{round(result_all[21], 2)}')
        print(f'b_v:\t{round(result_all[22], 2)}')
        print(f'cr_v:\t{round(result_all[23], 2)}')
        print(f'ct_v:\t{round(result_all[24], 2)}')
        print(f'mac_v:\t{round(result_all[25], 2)}')
        print(f'lv:\t{round(result_all[33], 2)}')
        print(f'Cd0_v:\t{round(result_all[26], 6)}')
        print(f'CD:\t{round(result_all[27], 6)}')
        print('weight_of_component')
        print(f'w_wing:\t{round(w_wing, 2)}')
        print(f'w_h_tail:\t{round(w_h_tail, 2)}')
        print(f'w_v_tail:\t{round(w_v_tail, 2)}')

        print()
        print(f"Execution_time:\t{round(execution_time, 2)} sec, @Generation: {count}")
        print(f"BEST_OF:\t\tPARAMETERS:\t\t\tOBJ_VALUE:")
        print(f"Generation\t\t{best_of_generation[0]}\t\t{best_of_generation[1]}")
        print(f"All_time\t\t{best_of_all[0]}\t\t{best_of_all[1]}")
        print()
        print(f"Generation\t\t{best_of_generation[0]}: {result_generation}")
        print()
        print(f"All_time\t\t{best_of_all[0]}: {result_all}")

        # return best_of_generation[0], result_generation, best_of_all[0], result_all
        return stack_plot