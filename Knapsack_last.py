
import random as r

# hyper parameters
population_size = 5
num_generations = 3
mutation_probability = 0.1
crossover_probability = 0.6


def convertToInt(f):  # Converting the entire file to array of integers
    arr = []
    for line in f:
        s = 0
        for x in line:
            if (not x.isdigit()):
                s /= 10
                if (s != 0):
                    arr.append(int(s))
                    s = 0
            if (x.isdigit()):
                s += int(x)
                s *= 10
    return arr


def evaluate_solution(total_weight, weights, values, bits_arr):  # Evaluate every solution
    t_w = 0
    fitness = 0
    for i in range(len(values)):
        if (bits_arr[i] == 1):
            t_w += weights[i]

    if (t_w > total_weight):
        return -1

    for i in range(len(values)):
        if (bits_arr[i] == 1):
            fitness += values[i]

    return fitness


def initialize_population(test_case):  # Generate a random array that consists only of 0s and 1s
    sol = []
    for i in range(test_case):
        sol.append(r.randint(0, 1))
    return sol

def mutation(sol):
    for i in range(len(sol)):
        rand = r.random()
        if rand <= mutation_probability:
            if (sol[i]):
                sol[i] = 0
            else:
                sol[i] = 1
    return sol


def selection(fitness_values):
    cummulative_fitness_sols = []
    # cumulative_fitness = 0
    selected = []
    for i in range(len(fitness_values)):
        if i == 0:
            cummulative_fitness_sols.append(fitness_values[0])
        else:
            cummulative_fitness_sols.append(fitness_values[i] + cummulative_fitness_sols[i - 1])

    cumulative_fitness = cummulative_fitness_sols[-1]

    for i in range(len(cummulative_fitness_sols)):
        rand = r.uniform(0, cumulative_fitness)
        # print(r)
        for n in range(len(cummulative_fitness_sols) - 1):
            if 0 <= rand < cummulative_fitness_sols[0]:
                selected.append(0)
                break
            if cummulative_fitness_sols[n] <= rand < cummulative_fitness_sols[n + 1]:
                selected.append(n + 1)
                break

    return selected




def cross_over(parent1, parent2):
    cut_point = r.randint(1, len(parent1) - 1)
    # print(f"cut point= {cut_point}")
    prob = r.uniform(0, 1)
    # print(f"prob= {prob}")
    temp1 = parent1
    temp2 = parent2
    child1 = [0] * len(parent1)
    child2 = [0] * len(parent2)

    if prob <= crossover_probability:
        child1[0:cut_point] = parent1[0:cut_point]
        child1[cut_point:] = parent2[cut_point:]
        child2[0:cut_point] = temp2[0:cut_point]
        child2[cut_point:] = temp1[cut_point:]
    else:
        return parent1, parent2

    return child1, child2


def replacement2(arr_of_sol, new_generation):
    tmp = arr_of_sol + new_generation
    fit1 = []
    fit2 = []
    res = []
    for i in range(len(arr_of_sol)):
        fit1.append(evaluate_solution(total_weight, weights, values, arr_of_sol[i]))
        fit2.append(evaluate_solution(total_weight, weights, values, new_generation[i]))
    tmp_fit = fit1 + fit2

    for i in range(len(arr_of_sol)):
        MAX = -1e6
        max_index = -1
        for j in range(len(tmp)):
            if tmp_fit[j] > MAX:
                MAX = tmp_fit[j]
                max_index = j
        tmp_fit[max_index] = -2
        res.append(tmp[max_index])
    return res


f = open('knapsack_input(1).txt', 'r')
arr = convertToInt(f)
total_test_cases = arr[0]

index = 1
j = 1
while (total_test_cases):
    test_case = arr[index]
    index += 1
    total_weight = arr[index]
    index += 1
    weights = []
    values  = []
    arr_of_sol = []
    fitness_vals = []
    for item in range(test_case):
        weights.append(arr[index])
        values.append(arr[index+1])
        index += 2

    for i in range(len(weights)):
        arr_of_sol.append(initialize_population(len(weights)))

    for i in range(test_case):
        fitness_vals.append(evaluate_solution(total_weight, weights, values, arr_of_sol[i]))


    for generation in range(250):
        new_generation = []
        new_fitness = []
        arr_of_soll =[]
        for sol in range(0, len(weights) - 1, 2):
            x, y = cross_over(arr_of_sol[sol], arr_of_sol[sol + 1])
            x = mutation(x)
            y = mutation(y)
            new_generation.append(x)
            new_generation.append(y)
        if len(weights) % 2 != 0:
            arr_of_sol[-1] = mutation(arr_of_sol[-1])
            new_generation.append(arr_of_sol[-1])
        arr_of_sol = replacement2(arr_of_sol, new_generation)
        for i in range(len(arr_of_sol)):
            score = evaluate_solution(total_weight, weights, values, arr_of_sol[i])
            new_fitness.append(score)
        arr_of_soll = selection(new_fitness)


    MAX = -1e6
    MAX_index = -1
    c = 0

    for i in range(test_case):
        if new_fitness[i] > MAX:
            MAX = new_fitness[i]
            MAX_index = i

    for i in arr_of_sol[MAX_index]:
        if i == 1:
            c += 1
    l = arr_of_sol[MAX_index]
    print(f"For test case number {j}:")
    print(f"{c} items got selected, with total value of = {MAX}")
    print("The weight and value of each item is:")
    for i in range(test_case):
        if l[i] == 1:
            print(f"weight= {weights[i]:5d}, value={values[i]:5d} ")

    print("_______________________________________________")
    total_test_cases -= 1
    j+=1
