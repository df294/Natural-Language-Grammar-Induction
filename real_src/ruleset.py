import random
from fitness import *
from json import JSONEncoder

TERMINALS = ["N", "V", "J", "A", "R", "T", "O", "P"]

""" of form
{u'_size': 6,
u'_nonterminals': {u'1': 1, u'0': 1, u'3': 1, u'2': 1, u'5': 1, u'4': 1},
u'_fitness': 0.0,
u'_rules': [[u'0', u'NN'], [u'1', u'JN'], [u'3', u'TT'], [u'5', u'13'], [u'2', u'VP'], [u'4', u'0V']]}
"""
def getRuleSetFromDict(dict):
    rules = []
    for r in dict['_rules']:
        k = str(r[0])
        v = str(r[1])
        rules.append((k,v))

    nonterminals = {}
    for k in dict['_nonterminals'].keys():
        nonterminals[str(k)] = dict['_nonterminals'][k]
    size = dict['_size']
    fitness = dict['_fitness']
    return RuleSet(rules = rules, nonterminals=nonterminals, size=size, fitness=fitness)

class RuleSetEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class RuleSet():
    '''RuleSet contains a list of tuples of strings representing a context-free
    grammar. The first element of a tuple is a non-terminal (0,9) and the second
    element is two symbols which can be either terminal or non-terminal.
    The possible terminals are ["N", "V", "J", "A", "R", "T", "O"].
    For example, [("1", "AN"),("1","2V"),("2","RT")] represents the following grammar:
    1 -> A N
    1 -> 2 V
    2 -> R T
    which could also be thought of as
    1 -> A & N || 2 & V
    2 -> R & T
    '''

    def __init__(self, rules=[], nonterminals={}, size=0, fitness=0.0):
        self._rules = rules[:]; #list of tuples (input, output_string)
        self._size = size
        self._fitness = fitness
        self._nonterminals = nonterminals.copy()

    def evalFitness(self, pos_weight, neg_weight, discount_factor):
        self._fitness = checkFitness(self.formatCYK(),pos_weight, neg_weight, discount_factor)
        return self._fitness

    def getSize(self):
        return self._size

    def getRules(self):
        return self._rules[:]

    def getFitness(self):
        return self._fitness

    def getNonterminals(self):
        return self._nonterminals

    def addNonterminal(self, nt):
        self._nonterminals[nt] = 1

    def addRule(self, nt, mapping):
        assert type(nt)==str and type(mapping)==str
        assert len(nt)==1 and len(mapping)==2
        if nt not in self._nonterminals:
            self._nonterminals[nt] = 1
        else:
            self._nonterminals[nt] += 1
        keys = self._nonterminals.keys() + TERMINALS
        newMap = list(mapping)
        for i in range(len(mapping)):
            if mapping[i] not in keys:
                newMap[i] = str(keys[random.randint(0, len(keys) - len(TERMINALS) - 1)])
        self._rules.append((nt, ''.join(newMap)))
        self._size += 1

    '''Removes a tuple from the RuleSet'''
    def deleteRule(self, i):
        assert type(i)==int and i >= 0 and i < self._size
        self._nonterminals[str(self._rules[i][0])] -= 1
        self._rules.pop(i)
        self._size -=1

    '''Picks a tuple at random and returns it, but it stays in the RuleSet.'''
    def getRandomRule(self):
        random.seed()
        i = random.randint(0, self._size-1)
        return self._rules[i]

    '''Picks a tuple at random and pops it.'''
    def popRandomRule(self):
        random.seed()
        i = random.randint(0, self._size - 1) if (self._size - 1 > 0) else 0
        self._nonterminals[str(self._rules[i][0])] -= 1
        self._size -= 1
        return self._rules.pop(i)

    '''Returns a deep copy of a RuleSet'''
    def copySet(self):
        return RuleSet(self._rules[:], self._nonterminals, self._size, self._fitness)

    def formatCYK(self):
        grammar = ""
        for key, val in self.getRules():
            grammar += key + " -> " + " ".join(val) + "\n"
        #print("Testing with grammar: \n" + grammar)
        return grammar

    def __str__(self):
        return self.formatCYK()

    def __eq__(self, obj):
        return (isinstance(obj, RuleSet) and
        obj.getRules() == self.getRules() and obj.getSize() == self.getSize())

    def __ne__(self, obj):
        return isinstance(obj, RuleSet) and obj.getRules() != self.getRules()
