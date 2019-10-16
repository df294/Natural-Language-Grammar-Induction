import sys
from ruleset import *
from genetic import *
import time
import datetime
import sys
import signal
import json
from collections import namedtuple
import fitness

START_TIME = datetime.datetime.now()

current_time_file = 'results_{date:%m-%d-%Y_%H:%M:%S}.txt'.format(date=START_TIME)
graph_time_name = str('graph_time_{time:%H}_{time:%M}_{time:%S}.txt'.format(time=START_TIME))
OUTPUT_FILE = "../results/" + current_time_file
GRAPH_OUT_FILE = "../graphs/"+ graph_time_name

final_population_file = 'population_{date:%m-%d-%Y_%H:%M:%S}.json'.format(date=START_TIME)
OUTPUT_POPULATION_FILE = "../populations/" + final_population_file 

STARTING_POPULATION = "../populations/population_12-12-2018_15:28:08.json"

TERMINATE = False                            
file_out = None
last_five_best = []
iteration = 0

def signal_handling(signum, frame):           
    global TERMINATE                         
    TERMINATE = True
    print("Preparing to exit...")

def savePopulation(population):
    with open(OUTPUT_POPULATION_FILE, 'w') as out:
        temp = json.dumps(population, cls=RuleSetEncoder)
        json.dump(temp, out)
        out.close()

def print_record(string):
    print(string)
    file_out.write(string + "\n")

""" index 0, check len 1"""
def getSysArgIndex(index):
    if(len(sys.argv) >= index + 1):
        return sys.argv[index]
    return None

def setStartingPopulation(preset_pop):
    if(not preset_pop):
        return None

    with open(preset_pop, 'r') as f:
        d = json.load(f)
        d = json.loads(d)
    
    pop = [getRuleSetFromDict(entry) for entry in d]
    return pop

"""
python main.py GOODFILE.txt BADFILE.txt STARTINGPOPULATION.json
 """
if __name__ == "__main__":
    #create directories if they dont exist yet
    if not os.path.exists("../graphs/"):
        os.makedirs("../graphs/")
    if not os.path.exists("../results/"):
        os.makedirs("../results/")
    if not os.path.exists("../populations/"):
        os.makedirs("../populations/")
    
    file_out = open(OUTPUT_FILE, "w")
    graph_out = open(GRAPH_OUT_FILE,"w")
    random.seed()

    fitness.GOODFILE = getSysArgIndex(1)
    fitness.BADFILE = getSysArgIndex(2)
    STARTING_POPULATION = getSysArgIndex(3)

    print_record("Initial Conditions:")
    print_record("MIN_RULES:         " + str(MIN_RULES))
    print_record("MAX_RULES:         " + str(MAX_RULES))
    print_record("POPULATION_SIZE:   " + str(POPULATION_SIZE))
    print_record("GENERATIONS:       " + str(GENERATIONS))
    print_record("MUTATION_RATE:     " + str(MUTATION_RATE))
    print_record("SKEW_EXPONENT:     " + str(SKEW_EXPONENT))
    print_record("DISCOUNT_FACTOR:   " + str(DISCOUNT_FACTOR))
    print_record("POS_WEIGHT:        " + str(POS_WEIGHT))
    print_record("NEG_WEIGHT:        " + str(NEG_WEIGHT) + "\n")

    print_record("GOODFILE: " + str(fitness.GOODFILE if fitness.GOODFILE != None else fitness.DEFAULT_GOODFILE) + "\n")
    print_record("BADFILE:  " + str(fitness.BADFILE if fitness.GOODFILE != None else fitness.DEFAULT_BADFILE) + "\n")

    if(STARTING_POPULATION):
        population = setStartingPopulation(STARTING_POPULATION)
    else:
        population = generateInitialPopulation(POPULATION_SIZE)

    print_record("Generated initial population.\n")

    signal.signal(signal.SIGINT, signal_handling) 

    while not TERMINATE: 
        #REQUIRED: population must be sorted (also updates fitness values) before next gen
        oldSorted = sortByFit(population)
        reverseSort = oldSorted[::-1]

        best = getBestIndividual(oldSorted)
        worst = getBestIndividual(reverseSort)
        upper = getUpperQuartile(oldSorted)
        print_record("Generation " + str(iteration) + ": ")
        print_record("Worst:          " + str(worst[1]))
        print_record("Lower Quartile: " + str(getUpperQuartile(reverseSort)))
        print_record("Mean:           " + str((getMeanPopulationFitness(oldSorted))))
        print_record("Upper Quartile: " + str(upper))
        print_record("Best:           " + str(best[1]))
        print_record(str(best[0]))

        last_five_best.append(best[1])
        last_five_best.append(worst[1])
        if(len(last_five_best) > 10):
            last_five_best.pop(0)
            last_five_best.pop(0)
            assert(len(last_five_best) <= 10)

        if(len(last_five_best) == 10 and all(record <= 0 for record in last_five_best)):
            population = generateInitialPopulation(POPULATION_SIZE)
            print_record("\n*Reset initial population due to failed past 5 generations.*\n")
            last_five_best = []
        else:
            population = createNextPopulation(oldSorted)
        graph_out.writelines([str(best[1])+","+ str(upper)+"\n"])
        iteration += 1

    print("Saving...")
    savePopulation(population)
    print_record("FINISHED. Best grammar found: "+ str(best[1]))
    print_record(str(best[0]))
    file_out.close()
    graph_out.close()
