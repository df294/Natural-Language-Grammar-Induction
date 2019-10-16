import sys
from ruleset import *
from genetic import *
import time
import datetime
import sys
import signal
import json
from collections import namedtuple

current_time_file = 'results_{date:%m-%d-%Y_%H:%M:%S}.txt'.format(date=datetime.datetime.now())
OUTPUT_FILE = "../results/" + current_time_file
graph_time_name = str('graph_time_{time:%H}_{time:%M}.txt'.format(time=datetime.datetime.now()))
GRAPH_OUT_FILE = "../graphs/"+ graph_time_name



final_population_file = 'population_{date:%m-%d-%Y_%H:%M:%S}.json'.format(date=datetime.datetime.now())
OUTPUT_POPULATION_FILE = "../populations/" + final_population_file 

STARTING_POPULATION = "../populations/population_12-12-2018_15:28:08.json"

TERMINATE = False                            
file_out = None
last_five_best = []
iteration = 0

def signal_handling(signum, frame):           
    global TERMINATE                         
    TERMINATE = True  

def savePopulation(population):
    with open(OUTPUT_POPULATION_FILE, 'w') as out:
        temp = json.dumps(population, cls=RuleSetEncoder)
        json.dump(temp, out)
        out.close()

def print_record(string):
    print(string)
    file_out.write(string + "\n")

def _json_object_hook(d):
    return namedtuple('X', d.keys())(*d.values())
        
def json2obj(data): 
    return json.loads(data, object_hook=_json_object_hook)

def setStartingPopulation(preset_pop):
    if(not preset_pop):
        return None

    with open(preset_pop, 'r') as f:
        d = json.load(f)
        d = json.loads(d)
    
    # e = d[0]['_rules']
    # print(type(e))
    # for i in e:
    #     i = [str(i[0]), str(i[1])]
    # print(e)
    # print(type(e))
    pop = [getRuleSetFromDict(entry) for entry in d]
    return pop

if __name__ == "__main__":
    file_out = open(OUTPUT_FILE, "w")
    graph_out = open(GRAPH_OUT_FILE, "w")
    random.seed()

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

    print_record("GOODFILE:        " + str(GOODFILE) + "\n")
    print_record("BADFILE:        " + str(BADFILE) + "\n")

    #population = setStartingPopulation(STARTING_POPULATION)
    population = generateInitialPopulation(POPULATION_SIZE)
    if(not population):
        population = generateInitialPopulation(POPULATION_SIZE)

    print_record("Generated initial population.\n")

    signal.signal(signal.SIGINT, signal_handling) 

    while not TERMINATE: 
        #REQUIRED: population must be sorted (also updates fitness values) before next gen
        oldSorted = sortByFit(population)

        best = getBestIndividual(oldSorted)
        upper = str(getUpperQuartile(oldSorted))
        print_record("Generation " + str(iteration) + ": ")
        print_record("Mean:           " + str((getMeanPopulationFitness(oldSorted))))
        print_record("Upper Quartile: " + upper)
        print_record("Best:           " + str(best[1]))
        print_record(str(best[0]))
        # if (best[1] >= 0.80):
        #     break

        population = createNextPopulation(oldSorted)
        graph_out.writelines([str(best[1])+","+upper+"\n"])
        iteration += 1

    print_record("FINISHED. Best grammar found: "+ str(best[1]))
    print_record(str(best[0]))

    savePopulation(population)
    file_out.close()
    graph_out.close()
