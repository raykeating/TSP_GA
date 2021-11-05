from math import sqrt
from os import access
import random
from cities import Cities

class Population:
    def __init__(self, city_data: Cities, pop_size: int, seed: str):
        self.seed = seed
        self.pop_size = pop_size
        self.city_data = city_data
        self.population = []
        self.initialize_population()

    def get_assigned_random(x):
        return x[1]

    def initialize_population(self):
        random.seed(self.seed)
        for i in range(self.pop_size):
            allCities = []
            for city in self.city_data.cities:
                city_random_tuple = (city, random.uniform(0, 1))
                allCities.append(city_random_tuple)

            # shuffle the population.  Add the first city to the end to complete the chromosome.
            allCities = sorted(allCities, key=lambda x: x[1])

            chromosome = []

            for city in allCities:
                # just append the city to the new chromosome, 
                # not the random number used for shuffling
                chromosome.append(city[0])
            # add the starting city to complete the route
            chromosome.append(chromosome[0])
            
            # add the new chromosome to the population
            self.population.append(chromosome)

    def display_chromosome(self, chromosome):
        for city in chromosome:
            print(city["number"], end=' ')
        print("")

    def display_pop(self):
        # print the population
        for route in self.population:
            self.display_chromosome(route)

    def evaluate_fitness(self, chromosome):
        # calculate total euclidian distance of a route.
        total_distance = 0
        # initialize x1, y1 to starting position
        x1 = chromosome[0]["x_pos"]
        y1 = chromosome[0]["y_pos"]
        for i in range(len(chromosome)):
            # then, for each chromosome, iterate through and 
            # add distance between cities to total_distance
            x2 = chromosome[i]["x_pos"]
            y2 = chromosome[i]["y_pos"]
            total_distance += sqrt(((x1-x2)**2+(y1-y2)**2))
            x1 = y1
            x2 = y2
        return total_distance


            
    

        

    
            

