# genetic GC solver
def main():
    # get input
    with open('input.txt', 'r') as f:
        lines = f.readlines()
    # parse input
    dna = lines[0].strip()
    target = lines[1].strip()
    # run solver
    solver(dna, target)

def solver(dna, target):
    # create population
    population = []
    for i in range(0, 100):
        population.append(dna)
    # run solver
    while True:
        # get fitness
        fitness = []
        for i in range(0, len(population)):
            fitness.append(get_fitness(population[i], target))
        # get best
        best = population[fitness.index(min(fitness))]
        # print best
        print(best)
        # check if best is target
        if best == target:
            break
        # get next generation
        population = get_next_generation(population, fitness, target)

        
 