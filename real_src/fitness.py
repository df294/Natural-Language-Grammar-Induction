import os.path
from CYKParser.Parser import Parser
import time

# class Fitness:

"""
GOODFILE and BADFILE are both test data sets of tagged sentences with each
tag being 1 character and sentences deliminated by spaces.
"""
#GOODFILE = t"../text_files/basic_tagged_simple.txt"
#BADFILE = "../text_files/B5179_simple.txt"

GOODFILE = None
BADFILE = None

DEFAULT_GOODFILE =  "../text_files/pal.txt"
DEFAULT_BADFILE = "../text_files/ungram_pal.txt"

TERMINALSMAP = """N -> 'N'
V -> 'V'
J -> 'J'
R -> 'R'
P -> 'P'
T -> 'T'
O -> 'O'"""

def checkFile(grammar, file):
    """
    Returns the percentage of sentences of the full text file that the
    grammar correctly parses by the CYK algorithm.
    :param grammar: the grammar to test with, including terminal node mappings
    :param file: the text file to check if fits grammar
    :param grammatical: if file is grammatical or not
    """
    correct = 0.0
    text = open(file).read()
    for str in text.split():
        str = " ".join(str)
        parser = Parser(grammar, str)

        if parser.print_tree(False):
            # successfully parsed
            correct += 1

    return correct / len(text.split())

def checkFitness(grammar, weight1, weight2, discount_factor):
    """
    Returns a correctness percentage of the grammar in parsing
        both the grammatical and ungrammatical the test data.
    :param grammar: the correctly formatted grammar file or string.
    :param weight: the decimal in which to weigh the correctness against
        the grammatical text.
    grammar must be provided in the following format, which each rule on
        a new line:
        A -> B C
        B -> C D
        C -> C
    """
    # print_tree with false argument returns None if not parsed
    if os.path.isfile(grammar):
        grammar = open(grammar).read()

    modGrammar = grammar + TERMINALSMAP

    # test grammatical file

    grammatical = checkFile(modGrammar, GOODFILE if GOODFILE != None else DEFAULT_GOODFILE)
    ungrammatical = checkFile(modGrammar, BADFILE if GOODFILE != None else DEFAULT_BADFILE)

    #if grammatical > 0 :
    #    print(grammatical, ungrammatical
    t = []
    for rule in grammar.splitlines():
        if rule[0] not in t:
            t.append(rule[0])

    g = discount_factor ** (max(0, (len(grammar) - len(t))))
    return g * (grammatical * weight1) - (ungrammatical * weight2)
