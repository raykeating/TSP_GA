from cities import Cities
from population import Population

map = Cities("/home/ray/Code/A2_3P71/city_data.txt")
pop = Population(map, 50, "oogabooga")

def main():
    min_distance = 100000000000000
    for i in range(len(pop.population)):
        min_distance = min(min_distance, pop.evaluate_fitness(pop.population[i]))

    print(min_distance)

if __name__ == "__main__":
    main()