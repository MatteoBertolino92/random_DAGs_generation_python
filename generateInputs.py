from progress.bar import Bar
import os
import sys
from time import sleep

def takeGraph(stringFile, nbOfActors):
	f= open(stringFile,"r")
	content = []
	if f.mode == 'r':
		lines = f.readlines()
		i = 0
		for line in lines:
			i+=1
			if i<=nbOfActors*6:
				continue
			content.append(line)
		f.close()
		return content
		


listOfGraph = []

if len(sys.argv) < 5:
	print("Usage: programName nbOfGraphs nbOfTasks maximumParallelism offsetForGraphName\n")
	print("For example, if the arguments are: 10 12 4 0, 10 graphs will be created, from graph0 to graph 9. Each graph has 12 tasks and there will be at most 4 tasks in parallel. If I already have 10 graphs in my folder, I can create other X graphs by changing offset parameter in 10: in this ways, graph generation will start by creating graph10 until graph(10+X-1)")
	exit()

var = int(sys.argv[1])
nbOfActors = int(sys.argv[2])
avgPvalue = int(sys.argv[3])
offset = int(sys.argv[4])
bar = Bar('Processing', max=var)
i = offset 
j = 0
counter = 0

for j in range(offset):
	path = "graphsFolder/graph"+str(j)+".txt"
	graph = takeGraph(path, nbOfActors)
	listOfGraph.append(graph)

print('Start: ', str(offset), ' end: ', str(var+offset))

while i<var+offset:
	path = "graphsFolder/graph"+str(i)+".txt"
	os.system("python3 -s main.py "+ str(nbOfActors) + " "+ str(avgPvalue) + " " + path+ " --fpga")
	graph = takeGraph(path, nbOfActors)
	while graph in listOfGraph:
		os.system("rm "+path)
		os.system("python3 -s main.py "+ str(nbOfActors) + " "+ str(avgPvalue) + " " + path+ " --fpga")
		graph = takeGraph(path, nbOfActors)
		counter += 1
	else:
		listOfGraph.append(graph)	
		bar.next()
	i+=1
bar.finish()
print('Avoided ', str(counter), ' duplicata topologies')
