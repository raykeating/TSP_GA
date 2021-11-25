import math
import os
from cities import Cities
# from graphics import * # used for show_path (disabled)
from population import Population
import copy

# # NOTE: I had to disable this function because I couldn't get it to properly compile from the command line if it was here
# # show_path: displays a route on the screen.  Click anywhere on the window to close the screen.
# # this works best with the eil51 data.
# def show_path(route):
#         path = []
#         win = GraphWin("Path", 600, 600)
#         win.setCoords(0,0, 70,70)
#         for i, city in enumerate(route):
#             x = city["x_pos"]
#             y = city["y_pos"]
#             pnt = Point(x, y)
#             path.append(pnt)
#             point = Circle(pnt,0.3)
#             if i == 0 or i == len(route)-1:
#                 point = Circle(pnt,0.5)
#                 point.setFill("red")
#             else:
#                 point.setFill("black")
#             point.draw(win)

#         for i in range(1,len(path)):
#             line = Line(path[i], path[i-1])
#             line.draw(win)
#         win.getMouse()
#         win.close()

# test_run: does a single run and outputs the info to console.
def test_run(tournament_size, crossover_rate, mutation_rate, elite_size, generations, pop_size, seed, datafile):
    run_best_route = None
    run_best_distance = math.inf
    map = Cities(datafile)
    pop = Population(map, pop_size, seed)
    for i in range(generations):
        newPop = pop.evolve(tournament_size, crossover_rate, mutation_rate, elite_size)
        pop.population = newPop
        generation_best_distance = pop.evaluate_fitness(pop.get_most_fit())
        generation_average_distance = pop.get_average_fitness()
        print(f'generation {i} best distance: {generation_best_distance}')
        print(f'generation {i} average distance: {generation_average_distance}')
        if generation_best_distance < run_best_distance:
            run_best_distance = generation_best_distance
            run_best_route = copy.deepcopy(pop.get_most_fit())
    

    print("\nDistance of Best Route Found")
    print(run_best_distance)
    print("\nBest Route Found")
    pop.display_chromosome(run_best_route)
    print("")

    return run_best_route

# generate_report: generates a report in CSV-style format (but saved as txt) detailing the info from 5 runs
def generate_report(datafile, outputfile, pop_size, generations, tournament_size, crossover_rate, mutation_rate, elite_size):
    # initialize the city data
    map = Cities(outputfile)

    # generate the run data and store in run_data
    run_data = []
    best_fitness_data = []
    alltime_best_distance = math.inf
    for i in range(5):
        run_best_route = None
        run_best_distance = math.inf
        seed = "run"+str(i+1)
        pop = Population(map, pop_size, seed)
        for j in range(generations):
            run_data.append([j])
        for j in range(generations):
            newPop = pop.evolve(tournament_size, crossover_rate, mutation_rate, elite_size)
            pop.population = newPop
            generation_best_distance = pop.evaluate_fitness(pop.get_most_fit())
            generation_average_distance = pop.get_average_fitness()
            run_data[j].append(generation_best_distance)
            run_data[j].append(generation_average_distance)
            if generation_best_distance < run_best_distance:
                run_best_distance = generation_best_distance
                run_best_route = pop.get_most_fit()
                if generation_best_distance < alltime_best_distance:
                    alltime_best_distance = pop.evaluate_fitness(pop.get_most_fit())
        best_fitness_data.append(str(run_best_distance))
        best_fitness_data.append(pop.get_route_as_string(run_best_route))

    report = open(f'{outputfile}', "x")

    report.write("Shortest distance over all runs\n")
    report.write(str(alltime_best_distance)+"\n")
    report.write("\n")

    report.write("K-value,Crossover Rate,Mutation Rate,Elite Size,Population Size,Generations\n")
    report.write(f'{tournament_size},{crossover_rate},{mutation_rate},{elite_size},{pop_size},{generations}\n')
    report.write("\n")
    report.write("Run 1 Seed,Run 2 Seed,Run 3 Seed,Run 4 Seed,Run 5 Seed\n")
    report.write("run1,run2,run3,run4,run5\n")
    report.write("\n")
    
    report.write(",Run 1 Best Overall Distance, Run 1 Best Overall Path,Run 2 Best Overall Distance, Run 2 Best Overall Path,Run 3 Best Overall Distance, Run 3 Best Overall Path,Run 4 Best Overall Distance, Run 4 Best Overall Path,Run 5 Best Overall Distance, Run 5 Best Overall Path\n")
    for item in best_fitness_data:
        report.write(",")
        report.write(item)
    report.write("\n\n")

    report.write("Generation,Run 1 Best Fitness,Run 1 Average Fitness,Run 2 Best Fitness,Run 2 Average Fitness,Run 3 Best Fitness,Run 3 Average Fitness,Run 4 Best Fitness,Run 4 Average Fitness,Run 5 Best Fitness,Run 5 Average Fitness\n")
    # for each run
    for i in range(generations):
        # for each item in run_data[i]
        for item in run_data[i]:
            report.write(str(item)+",")
        report.write("\n")


    report.close()

def main():
    
    # this code will run a single GA with the specified parameters and output the results
    # returns the best route to be displayed on screen
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'eil51.txt')
    best_route = test_run(tournament_size=4, crossover_rate=0.9, mutation_rate=0.3, elite_size=15, generations=300, pop_size=75, seed="hello", datafile=filename)

    # this would display the best route found in a simple GUI.  
    # I have disabled it because tkinter has some issues running from the command line.
    # I have included a screenshot of the GUI working in the "ignore" folder, if you're interested.
    # show_path(best_route)



    # code I used to generate a single report (pmx/uox can be changed in population.py in the evolve function)
    # generate_report(datafile=filename, outputfile=os.path.join(dirname, 'experiment1_data.txt'), pop_size=75, generations=1000, tournament_size=3, crossover_rate=1, mutation_rate=0, elite_size=5)
    # generate_report(datafile=filename, outputfile=os.path.join(dirname, 'experiment2_data.txt'), pop_size=75, generations=1000, tournament_size=3, crossover_rate=1, mutation_rate=0.1, elite_size=5)
    # generate_report(datafile=filename, outputfile=os.path.join(dirname, 'experiment3_data.txt'), pop_size=75, generations=1000, tournament_size=3, crossover_rate=0.9, mutation_rate=0, elite_size=5)
    # generate_report(datafile=filename, outputfile=os.path.join(dirname, 'experiment4_data.txt'), pop_size=75, generations=1000, tournament_size=3, crossover_rate=0.9, mutation_rate=0.1, elite_size=5)
    # generate_report(datafile=filename, outputfile=os.path.join(dirname, 'experiment5_data.txt'), pop_size=75, generations=1000, tournament_size=4, crossover_rate=0.9, mutation_rate=0.3, elite_size=15)
if __name__ == "__main__":
    main()
