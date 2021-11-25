import math
from math import floor, sqrt, ceil
from os import access
import random
from cities import Cities
import copy

class Population:
    def __init__(self, city_data: Cities, pop_size: int, seed: str, population=[]):
        self.seed = seed
        self.pop_size = pop_size
        self.city_data = city_data
        self.population = population
        self.initialize_population()
        # route_length assumes all routes are the same length
        self.route_length = len(self.population[0])

    def initialize_population(self):
        # initialize a population of size self.pop_size

        random.seed(self.seed)
        for i in range(self.pop_size):
            all_cities = []
            for city in self.city_data.cities:
                city_random_tuple = (city, random.uniform(0, 1))
                all_cities.append(city_random_tuple)

            # shuffle the population.  Add the first city to the end to complete the chromosome.
            all_cities = sorted(all_cities, key=lambda x: x[1])

            chromosome = []

            for city in all_cities:
                # just append the city to the new chromosome, 
                # not the random number used for shuffling
                chromosome.append(city[0])
            # add the starting city to complete the route
            chromosome.append(chromosome[0])
            
            # add the new chromosome to the population
            self.population.append(chromosome)

    def display_chromosome(self, chromosome):
        # print a single chromosome
        for city in chromosome:
            if city:
                print(city["number"], end=' ')
            else:
                print("*", end=" ")
        print('| len: ', self.evaluate_fitness(chromosome), end="")
        print("")

    def get_route_as_string(self, route):
        # get route as a string
        route_string = ""
        for city in route:
            if city:
                route_string += (city["number"]+" ")
            else:
                route_string += ("*" + " ")
        
        return route_string

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
            x1 = x2
            y1 = y2
        return total_distance

    def get_most_fit(self):
        # get the most fit chromosome from the population

        most_fit = None
        lowest_distance = math.inf
        for route in self.population:
            if self.evaluate_fitness(route) < lowest_distance:
                most_fit = route
                lowest_distance = self.evaluate_fitness(route)
        
        return most_fit

    def apply_pmx_crossover(self, p1, p2, rate):
        # only do crossover if it is within the correct success rate (float between 0 and 1).  defaults to 100%
        if (random.uniform(0, 1) < rate):
            # apply partially mapped crossover (PMX) to parent 1 (p1) and parent 2 (p2) to get children.
            # since the children must be a permutation of the parents, there must be no repeated cities

            # fill c1 and c2 with empty values
            c1 = [None for x in p1]
            c2 = [None for x in p2]

            # step 1: identify arbitrary cut points (without changing starting/ending city)
            point1 = round(random.uniform(1, self.route_length-2))
            point2 = round(random.uniform(1, self.route_length-2))

            # rearrange point 1 and 2 so that point 1 is the min, and point 2 is the max
            temp_min = min(point1, point2)
            temp_max = max(point1, point2)
            point1 = temp_min
            point2 = temp_max

            # step 2: copy & swap the "genetic material" between point 1 and 2 between the parents
            x = slice(point1, point2)
            c1[x] = p2[x] 
            c2[x] = p1[x]

            # print("step 2 - a")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)

            # The last city WILL be a duplicate (same as starting city), so add it manually here
            c1[self.route_length-1] = p1[0]
            c1[0] = p1[0]
            c2[self.route_length-1] = p2[0]
            c2[0] = p2[0]

            # print("step 2 - b")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)

            # check if the swapped "genetic material" creates a duplicate (same as first city)
            for i in range(point1, point2):
                if c1[i] and c1[i] == c1[0]:
                    c1[i] = None

            for i in range(point1, point2):
                if c2[i] and c2[i] == c2[0]:
                    c2[i] = None

            # print("step 2 - c")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)

            # step 3: fill in cities where no conflicts arise (no duplicates)

            # for each "spot" in the chromosome
            # if it can be added without creating a duplicate city, add it to the child chromosome in the correct spot.
            for i in range(self.route_length):
                if not p1[i] in c1 and not c1[i]: # if it is not already in c1 and c1[i] is not already assigned a city
                    c1[i] = p1[i]

                if not p2[i] in c2 and not c2[i]:
                    c2[i] = p2[i]

            # print("step 3")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)
            
            # step 4: fill the remaining cities (at random)

            # find the cities that are not in the child chromosome
            # store in these lists
            not_in_c1 = []
            not_in_c2 = []

            # check which cities are not in the route
            for city in p1: # use p1 as the check since it has (should have) all the cities
                if not city in c1: 
                    not_in_c1.append(city)

            for city in p2:    
                if not city in c2:
                    not_in_c2.append(city)

            # print("step 4")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)
            # print("--")
            # print("not in")
            # self.display_chromosome(not_in_c1)
            # self.display_chromosome(not_in_c2)
            
            

            # add the cities which have been left out (not_in_c1/c2)
            counter = 0
            for i, city in enumerate(c1):
                if not city:
                    c1[i] = not_in_c1[counter]
                    counter += 1
            
            counter = 0
            for i, city in enumerate(c2):
                if not city:
                    c2[i] = not_in_c2[counter]
                    counter += 1
            
            return c1, c2
        else:
            return p1, p2

    def apply_uox_crossover(self, p1, p2, rate):
        # only do crossover if it is within the correct success rate (float between 0 and 1).  defaults to 100%
        if (random.uniform(0, 1) < rate):
            # print("parents")
            # self.display_chromosome(p1)
            # self.display_chromosome(p2)
            # apply uniform order crossover (UOX) to parent 1 (p1) and parent 2 (p2) to get children.
            # since the children must be a permutation of the parents, there must be no repeated cities

            # works exactly the same as pmx crossover, but a bitmask is used for swapping bits 
            # rather than a random slice of the array, like in apply_pmx_crossover

            # fill c1 and c2 with empty values
            c1 = [None for x in p1]
            c2 = [None for x in p2]

            # step 1: create arbitrary bitmask of length route_length
            bitmask = [bool(random.getrandbits(1)) for x in range(self.route_length)]

            # step 2: copy & swap the "genetic material" according to the bitmask
            # (don't swap the 1st city or last city)
            for i in range(1, self.route_length-1):
                if bitmask[i]:
                    c1[i] = p2[i] 
                    c2[i] = p1[i]

            # print("step 2 - a")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)

            # The last city WILL be a duplicate (same as starting city), so add it manually here
            c1[self.route_length-1] = p1[0]
            c1[0] = p1[0]
            c2[self.route_length-1] = p2[0]
            c2[0] = p2[0]

            # print("step 2 - b")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)

            # eliminate duplicates (resulting from swapped elements being the same as the starting city)
            for i in range(1, self.route_length-1):
                if c1[i] == c1[0]:
                    c1[i] = None
            
            for i in range(1, self.route_length-1):
                if c2[i] == c2[0]:
                    c2[i] = None

            # print("step 2 - c")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)

            # step 3: fill in cities where no conflicts arise (no duplicates)

            # for each "spot" in the chromosome
            # if it can be added without creating a duplicate city, add it to the child chromosome in the correct spot.
            for i in range(self.route_length):
                if not p1[i] in c1 and not c1[i]: # if it is not already in c1 and c1[i] is not already assigned a city
                    c1[i] = p1[i]

                if not p2[i] in c2 and not c2[i]:
                    c2[i] = p2[i]

            # print("step 3")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)
            
            # step 4: fill the remaining cities (at random)

            # find the cities that are not in the child chromosome
            # store in these lists
            not_in_c1 = []
            not_in_c2 = []

            # check which cities are not in the route
            for city in p1: # use p1 as the check since it has (should have) all the cities
                if not city in c1: 
                    not_in_c1.append(city)

            for city in p2:    
                if not city in c2:
                    not_in_c2.append(city)

            # print("step 4")
            # self.display_chromosome(c1)
            # self.display_chromosome(c2)
            # print("--")
            # print("not in")
            # self.display_chromosome(not_in_c1)
            # self.display_chromosome(not_in_c2)
            
            

            # add the cities which have been left out (not_in_c1/c2)
            counter = 0
            for i, city in enumerate(c1):
                if not city:
                    c1[i] = not_in_c1[counter]
                    counter += 1
            
            counter = 0
            for i, city in enumerate(c2):
                if not city:
                    c2[i] = not_in_c2[counter]
                    counter += 1
            
            return c1, c2
        else:
            return p1, p2
        # only do crossover if it is within the correct success rate (float between 0 and 1).  defaults to 100%
        if (random.uniform(0, 1) < rate):
            # apply uniform order crossover (UOX) to parent 1 (p1) and parent 2 (p2) to get children.
            # since the children must be a permutation of the parents, there must be no repeated cities

            # works exactly the same as pmx crossover, but a bitmask is used for swapping bits 
            # rather than a random slice of the array, like in apply_pmx_crossover

            # fill c1 and c2 with empty values
            c1 = [None for x in p1]
            c2 = [None for x in p2]

            # step 1: create arbitrary bitmask of length route_length
            bitmask = [bool(random.getrandbits(1)) for x in range(self.route_length)]

            # step 2: copy & swap the "genetic material" according to the bitmask
            for i in range(1, self.route_length-1):
                if bitmask[i]:
                    c1[i] = p2[i] 
                    c2[i] = p1[i]

            # step 3: fill in cities where no conflicts arise (no duplicates)

            # The last city WILL be a duplicate (same as starting city), so add it manually here
            c1[self.route_length-1] = p1[0]
            c1[0] = p1[0]
            c2[self.route_length-1] = p2[0]
            c2[0] = p2[0]


            # for each "spot" in the parent chromosome
            # if it can be added without creating a duplicate city, add it to the child chromosome in the correct spot.
            for i in range(self.route_length):
                if not p1[i] in c1 and not c1[i]: # if it is not already in c1 and c1[i] has not been assigned a city yet
                    c1[i] = p1[i]

                if not p2[i] in c2 and not c2[i]:
                    c2[i] = p2[i]

            # # step 4: fill the remaining cities (at random)

            # find the cities that are not in the child chromosome
            # store in these lists
            not_in_c1 = []
            not_in_c2 = []

            # check which cities are not in the route
            for city in p1: # use p1 as the check since it has (should have) all the cities
                if not city in c1: 
                    not_in_c1.append(city)

            for city in p2:    
                if not city in c2:
                    not_in_c2.append(city)

            # add to child (in the same order they appear in their parent chromosomes).
            counter = 0
            for i, city in enumerate(c1):
                if not city:
                    c1[i] = not_in_c1[counter]
                    counter += 1
            
            counter = 0
            for i, city in enumerate(c2):
                if not city:
                    c2[i] = not_in_c2[counter]
                    counter += 1

            return c1, c2
        else:
            return p1, p2

    def mutate(self, route:list, mutation_rate):
        if random.uniform(0, 1) < mutation_rate:

            # a mutation will randomly change a city in a route to some other city, and the other city will be replaced by the changed city
            # if the mutation changes the first city, that city will also be changed
            random_city1 = random.choice(route)
            random_city2 = random.choice(route)
            route[route.index(random_city1)], route[route.index(random_city2)] = route[route.index(random_city2)], route[route.index(random_city1)]
            # if the mutation changes the starting/ending city, update the route so the starting city stays the same
            if (random_city1 == route[0] or random_city1 == route[-1]):
                route[0] = random_city1
                route[-1] = random_city1
            if (random_city2 == route[0] or random_city2 == route[-1]):
                route[0] = random_city2
                route[-1] = random_city2
        
            return route
        else:
            return route

    # evolve: given the evolution parameters and the current population, return a new population 
    # (list of routes) that has undergone a single generation of evolution
    def evolve(self, tournament_size, crossover_rate, mutation_rate, elite_size):
        # evolve the population one generation via tournament selection, crossover, and mutation.
        # Uses elitism, meaning a percentage (should be <10%) of the population are allowed to replicate 
        # into the next generation (not steady-state)

        new_population = []
        mating_pool = []

        # STEP 0: REPLICATION
        # ensure that the most fit chromosome replicates.  Select it from the 
        # population and add to the new population. It will also be added to 
        # the mating pool through tournament selection
        best_routes = sorted(self.population, key=lambda x: self.evaluate_fitness(x))
        for i in range(elite_size):
            new_population.append(best_routes[i])

        # STEP 1: SELECTION (TOURNAMENT)
        # create the new population with same size as previous population 
        # (-1 since the most fit has already been replicated from the previous generation)
        for i in range(self.pop_size - elite_size):
            tournament = []
            for j in range(tournament_size):
                tournament.append(random.choice(self.population))

            winner = None
            best_score = math.inf
            for j in range(tournament_size):
                if (self.evaluate_fitness(tournament[j]) < best_score):
                    winner = tournament[j]
            
            mating_pool.append(winner)

        # STEP 2: CROSSOVER (PMX) + MUTATION
        # apply crossover to randomly selected chromosomes in the gene pool
        # new population should have the same size as previous population
        # 
        # then, apply mutation to the children if the probability is set to a value > 0
        counter = 0
        while len(new_population) < self.pop_size:
            parent1 = mating_pool[counter]
            parent2 = mating_pool[counter-1]
            counter += 1
            try:
                # change uox to pmx if you want to use pmx crossover
                child1, child2 = self.apply_uox_crossover(parent1, parent2, crossover_rate)
            except IndexError:
                # handle weird error in the crossover method.  If it occurs, just try again with new parents (it is rare)
                print("an error in crossover occurred")
                continue

            # MUTATION
            child1 = self.mutate(child1, mutation_rate)
            child2 = self.mutate(child2, mutation_rate)
            
            new_population.append(child1)
            if len(new_population) < self.pop_size:
                new_population.append(child2)
        
        return new_population

    def check_chromosome_validity(self, route):
        # check that there are no duplicates in the route

        # convert route to a set of numbers
        route_as_ints = []
        for city in route:
            if city:
                route_as_ints.append(city["number"])

        if len(route) == len(set(route_as_ints)):
            return False
        else:
            return True
            
    def check_population_validity(self):
        for route in self.population:
            if not self.check_chromosome_validity(route):
                raise ValueError("Invalid Route Detected")

    def get_average_fitness(self):
        population_total_distance = 0
        for route in self.population:
            population_total_distance += self.evaluate_fitness(route)
        
        return (population_total_distance/self.pop_size)
            
    

        

    
            

