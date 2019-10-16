import sys
from nltk.parse.generate import generate
from nltk import CFG

def generate_sentences(args):

    in_file = open(args[1])
    out_file = open(args[2],'w')

    gram = in_file.read()

    grammar = CFG.fromstring(gram)
    print(grammar)
    sentences = ""

    for s in generate(grammar, depth=int(args[0])):
        sentences += ''.join(s) + '\n'

    out_file.writelines(sentences)

    in_file.close()
    out_file.close()

if __name__ == "__main__":
	generate_sentences(sys.argv[1:])
