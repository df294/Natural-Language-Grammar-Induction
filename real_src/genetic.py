import random
from ruleset import *
from multiprocessing import Pool

TERMINALS = ["N", "V", "J", "A", "R", "T", "O", "P"]
MIN_RULES = 5
MAX_RULES = 35
POPULATION_SIZE = 300
GENERATIONS = 1000
MUTATION_RATE = 0.02
SKEW_EXPONENT = 1 #now if this goes below 1, it causes error

DISCOUNT_FACTOR = 0.98
POS_WEIGHT = 0.8
NEG_WEIGHT = 0.999

def generateNonTerminalFrom(ruleSet):
    nonterms = ruleSet.getNonterminals()
    return str(nonterms.keys()[random.randint(0, len(nonterms) - 1)])

def generateRandomNonTerminal():
    return str(random.randint(0,9))

def generateTokenFrom(ruleSet):
    nonterms = ruleSet.getNonterminals().keys() + TERMINALS
    r = random.randint(0, len(nonterms) - 1)
    return nonterms[r]

def generateRandomToken():
    r = random.randint(0, 9 + len(TERMINALS))
    if(r < 10):
        return str(r)
    else:
        return TERMINALS[r - 10]

#allows (x -> a) where x is a random non-term and a is a random Nonterm or term
#also allows a 50% chance to the result to look like (x -> ab) instead of just (x -> a)
def generateRandomRuleSet():
    #random.seed()
    num_rules = 10
    ruleset = RuleSet()

    for i in range(num_rules):
        second = generateRandomToken() + generateRandomToken()
        key = str(i) if i < 10 else generateRandomNonTerminal()
        ruleset.addRule(key, second)
    return ruleset

def generateInitialPopulation(populationSize):
    assert type(populationSize) == int and populationSize > 0
    return [generateRandomRuleSet() for x in range(populationSize)]

# get upper quartile of all rulesets (top 25%)
# REQUIRES: POPULATION ALREADY SORTED BY BEST FIT
def getUpperQuartile(population):
    assert type(population) == list and len(population) > 0
    assert isinstance(population[0], RuleSet)
    fitnessSum = 0
    for p in population[:int(len(population)/4)]:
        fitnessSum += p.getFitness()
    return fitnessSum / float(int(len(population)/4))

# gets mean fitness of all rulesets
# REQUIRES: POPULATION ALREADY SORTED BY BEST FIT
def getMeanPopulationFitness(population):
    assert type(population) == list and len(population) > 0
    assert isinstance(population[0], RuleSet)
    fitnessSum = 0
    for p in population:
        fitnessSum += p.getFitness()
    return fitnessSum / float(len(population))

'''Sorts by best fit and writes the newly evaluated fitness into each RuleSet'''
def sortByFit(currentPop):
    for r in currentPop:
        r.evalFitness(POS_WEIGHT, NEG_WEIGHT, DISCOUNT_FACTOR)
    return sorted(currentPop, key=lambda ruleSet: ruleSet.getFitness(), reverse=True)

'''[numBest]... int of number of individuals chosen for best fitness
    [numlucky]... int of number of individuals chosen randomly from lower fitness.
    the rest are chosen by
    *both combined must be less than currentPop
    REQUIRES: POPULATION ALREADY SORTED BY BEST FIT'''
def selectIndividuals(currentPop, numBest, numLucky):
    assert type(numBest) == int and type(numLucky) == int
    assert type(currentPop) == list and len(currentPop) > 0
    assert isinstance(currentPop[0], RuleSet)
    assert numLucky+numBest < len(currentPop)
    bestFit = currentPop[:numBest]
    lowerFit =  currentPop[numBest:]
    lowerChosen = []
    #random.seed()
    while (len(lowerChosen) < numLucky):
        lowerChosen.append(lowerFit.pop(random.randint(0, len(lowerFit) - 1)))
    selected = bestFit + lowerChosen
    assert len(selected) > 0 and len(selected) < len(currentPop)
    return selected

def norm(values):
    n = [float(i)/sum(values) for i in values]
    s = sum(n)
    if(s != 1):
        n[1] += (1 - s)
    return n

# """ Returns a list of probabilites based on each element's fitness """
# def calculateProbabilitesList_old(currentPop):
#     total = sum([(max(0, rs.getFitness()) ** (SKEW_EXPONENT)) for rs in currentPop])
#     if total == 0:
#         probs = [1.0 / len(currentPop) for rs in currentPop]
#     else:
#         probs = [(max(0, rs.getFitness()) ** (SKEW_EXPONENT)) / total for rs in currentPop]

#     s = sum(probs)
#     if(s != 1.0):
#         print("Sum was " + str(s))
#     assert abs(s - 1.0) < 0.0000000001

#     return probs

""" Returns a list of probabilites based on each element's fitness """
def calculateProbabilitesList(currentPop):
    fitnesses = [(rs.getFitness() ** SKEW_EXPONENT) for rs in currentPop]
    if(sum(fitnesses) == 0):
        probs = [1.0 / len(currentPop) for rs in currentPop]
    else:
        probs = norm(fitnesses)

    s = sum(probs)
    if(not abs(s - 1.0) < 0.0000000001):
        print("Sum was " + str(s))
    assert abs(s - 1.0) < 0.0000000001

    return probs

""" Returns tuple of parents to use from the population based on """
def selectParentsIndex(probs_list):
    first_parent_index = getIndexFromProbabilities(probs_list)
    second_parent_index = getIndexFromProbabilities(probs_list)
    # print(first_parent_index, second_parent_index)
    # here lies a bug
    # while(second_parent_index == first_parent_index):
    #     print("stuck")
    #     second_parent_index = getIndexFromProbabilities(probs_list)

    #assure they aren't the same
    if(second_parent_index == first_parent_index):
        if(second_parent_index + 1 < len(probs_list)):
            second_parent_index += 1
        else:
            second_parent_index -= 1
    return(first_parent_index, second_parent_index)

"""Requires a list of probabilities where each element x0 + x1 +...+ xn sum to 1 """
def getIndexFromProbabilities(probs):
    assert len(probs) > 0
    s = sum(probs)
    if(not abs(s - 1.0) < 0.0000000001):
        print("Sum was " + str(s))
        print(abs(s - 1.0) < 0.0000000001)
    assert abs(s - 1.0) < 0.0000000001

    r = random.random()
    index = 0
    while(r >= 0 and index < len(probs)):
        r -= probs[index]
        index += 1
    return index - 1



# REQUIRES: POPULATION ALREADY SORTED BY BEST FIT
def getBestIndividual(currentPop):
    return (currentPop[0], currentPop[0].getFitness())

#Crossover: n is number of crossovers to perform
def crossover(parent1, parent2, n):
    #pops a rule to cross from parents
    assert isinstance(parent1, RuleSet) and isinstance(parent2, RuleSet)
    assert parent1.getSize() > 0 and parent2.getSize() > 0
    assert type(n) == int and n >= 0

    parent1save = parent1.copySet()
    parent2save = parent2.copySet()
    child1 = parent1.copySet()
    child2 = parent2.copySet()
    crosses = n

    # random.seed()
    #perform crossover n times
    while (crosses > 0):
        chosen1 = child1.popRandomRule()
        chosen2 = child2.popRandomRule()
        #random.seed()
        #choose crossover point
        crossPoint = random.randint(1, 2)
        tmp1 = chosen1[1]
        tmp2 = chosen2[1]
        if (crossPoint == 1): #swap the entire thing
            new1 = tmp1[0:crossPoint]+tmp2[crossPoint:]
            new2 = tmp2[0:crossPoint]+tmp1[crossPoint:]
        else: #randomly pick one to swap from each
            pick1 = random.randint(0, 1)
            pick2 = random.randint(0, 1)
            new1 = tmp1[pick1]+tmp2[pick2]
            new2 = tmp1[abs(1-pick1)]+tmp2[abs(1-pick2)]
        child1.addRule(chosen1[0], new1)
        child2.addRule(chosen2[0], new2)
        crosses -= 1

    # with some probability, randomly duplicate an entire rule from one child
    # to another so that there is variable size
    addNew = random.randint(0, 99)
    if (addNew == 0):
        pair = child2.getRandomRule()
        child1.addRule(pair[0], pair[1])
    elif (addNew == 1):
        pair = child1.getRandomRule()
        child2.addRule(pair[0], pair[1])
    # with some probability, randomly delete an entire rule from one child
    deleteRule = random.randint(0, 200)
    if (deleteRule == 0 and child2.getSize()>2):
        child2.popRandomRule()
    elif (deleteRule == 1 and child1.getSize()>2):
        child1.popRandomRule()

    assert parent1save == parent1 and parent2save == parent2
    return [child1, child2]

#Mutation
def mutateChildrenPool(childPop, mutationRate):
    assert type(mutationRate)==float and mutationRate >= 0.0
    assert type(childPop) == list and len(childPop) > 0
    assert isinstance(childPop[0], RuleSet)

    return [mutateChild(child, mutationRate) for child in childPop]

def mutateChild(child, mutationRate):
    assert isinstance(child, RuleSet)
    assert type(mutationRate)==float and mutationRate >= 0.0

    new_child = RuleSet()
    for (key, val) in child.getRules():
        res = random.randint(0, 100) / 100.0
        if (res <= mutationRate):
            #mutate
            key = generateRandomNonTerminal()
            if key not in child.getNonterminals():
                child.addNonterminal(key)

        res = random.randint(0, 100) / 100.0
        if(res <= mutationRate):
            new = generateTokenFrom(child)
            val = new + ("" if len(val) < 2 else val[1])

        res = random.randint(0, 100) / 100.0
        if(res <= mutationRate):
            new = generateTokenFrom(child)
            val = val[0] + new
        new_child.addRule(key, val)
    add = random.randint(0, 70) / 100.0
    if (add <= mutationRate):
        addKey = generateRandomNonTerminal()
        type1 = random.randint(0, 1)
        type2 = random.randint(0, 1)
        if type1 == 0:
            val1 = generateRandomNonTerminal()
        else: 
            val1 = generateTokenFrom(child)
        if type2 == 0:
            val2 = generateRandomNonTerminal()
        else:
            val2 = generateTokenFrom(child)
        new_child.addRule(addKey, val1+val2)
    return new_child

'''REQUIRES: the current pop is sorted in order of best fit'''
def createNextPopulation(currentPop):
    # random.seed()
    assert type(currentPop) == list and len(currentPop) > 0
    assert isinstance(currentPop[0], RuleSet)

    probabilities = calculateProbabilitesList(currentPop)
    popSize = len(currentPop)
    newPop = []
    while(len(newPop) < popSize):
        parents_indexes = selectParentsIndex(probabilities)
        parent1 = currentPop[parents_indexes[0]]
        parent2 = currentPop[parents_indexes[1]]

        newPop += crossover(parent1, parent2, 2)
    return mutateChildrenPool(newPop, MUTATION_RATE)

    # popSize = len(currentPop)
    # parentPool = selectIndividuals(currentPop, int(popSize/3), int(popSize/6)) #TODO: decide on percent of best and lucky
    # poolSize = len(parentPool)
    # newPop = []
    # while (len(newPop) < popSize):
    #     parent1 = parentPool[random.randint(0, poolSize-1)]
    #     parent2 = parentPool[random.randint(0, poolSize-1)]
    #     newPop += crossover(parent1, parent2, 2)
    #return mutateChildrenPool(newPop, 0.01)
