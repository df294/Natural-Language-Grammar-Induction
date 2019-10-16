import sys

simple_dict = {
	'NN': 'N',
	'NNP': 'N',
	'NNPS': 'N', 
	'NNS': 'N', 
	'PRP': 'N',
	'WP': 'N',
	'MD': 'V', 
	'VB': 'V', 
	'VBD': 'V', 
	'VBG': 'V', 
	'VBN': 'V', 
	'VBP': 'V', 
	'VBZ': 'V',
	'CD': 'J', 
	'JJ': 'J', 
	'JJR': 'J', 
	'JJS': 'J', 
	'PRP$': 'J',
	'WP$': 'J',
	'RB' : 'R',
	'RBR': 'R',
	'RBS': 'R',
	'WRB': 'R',
	'IN': 'P',
	'RP': 'P',
	'TO': 'P',
	'CC': 'T',
	'DT': 'T',
	'EX': 'T',
	'PDT': 'T',
	'WDT': 'T',
	'FW': 'O',
	'SYM': 'O',
	'UH': 'O',
	'POS': 'S'
}

def simplify_tags(args):


	in_file = open(args[0])
	out_file = open(args[1],'w')

	line = in_file.readlines() #reads whole text file (there is only 1 line)
	
	sentences = line[0].split('._.') #creates a list of sentences
	simple_sentences = ''
	for s in sentences:
		stripped = s.strip()
		if stripped != '\n':
			s_list = stripped.split(' ')
			simple_s = ''
			for word in s_list: #for each word in a sentence
				tmp = word.split('_')
				pos = tmp[len(tmp)-1]
				if pos != '' and pos.isalpha():
					simple_s += simple_dict[pos] #get the simplified POS
			if simple_s != '':
				simple_sentences += simple_s + ' ' #separate sentences by spaces
	out_file.writelines(simple_sentences)

	in_file.close()
	out_file.close()

if __name__ == "__main__":
	simplify_tags(sys.argv[1:])

