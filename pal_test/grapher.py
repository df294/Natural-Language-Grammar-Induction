import sys
import matplotlib.pyplot as plt
import csv

def graph_file(arg):
    y = []
    x = []
    m = []
    file = open('../graphs/'+arg, 'r')
    with file as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        gens = 0
        for row in plots:
            y.append(float(row[0]))
            m.append(float(row[1]))
            gens+=1
        x = range(gens)

    plt.plot(x,y, label="best fit individual")
    plt.plot(x,m, label="upper quartile")
    plt.xlabel('generations')
    plt.ylabel('fitness')
    plt.title('Genetic algo improvement')
    plt.legend()
    plt.show()
    file.close()

if __name__ == "__main__":
	graph_file(sys.argv[1])