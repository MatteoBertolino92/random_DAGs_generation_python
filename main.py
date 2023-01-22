import random
import sys

class Task:
  def __init__(self, name):
    self.name = name
  def __str__(self):
     return self.name
  def __repr__(self):
     return self.name
  def setTiming(self, timing):
     self.timing = timing
  def setCLB(self, clb):
     self.clb = clb
  def setDSP(self, dsp):
     self.dsp = dsp
  def setMem(self, mem):
     self.mem = mem

def create_normal_int_distribution(max):
    min = 1
    avg = int((min+max)/2)
    #print(avg)
    special_counter = 1
    container = []
    i=0
    while (special_counter <= avg):
        while(i<special_counter):
            container.append(min)
            if min!=max:
                container.append(max)
            i += 1
        special_counter += 1;
        min += 1
        max -= 1
        i = 0
    #print(container)
    return container

if len(sys.argv)<2:
    print("Usage: program_name numberOfTasks breadhtRecommended filename fpga/tomato")
else:
    nt = int(sys.argv[1])
    mp = int(sys.argv[2])
    filename = sys.argv[3]

index=0
baseName = "a"

source = Task("a"+str(index))
index = index+1
currentSinks = [source]
graph = {}
flag = True

while flag:
    #print('Sinks: ', currentSinks)
    randomindex = random.randrange(0, len(currentSinks), 1)
    sink = currentSinks[randomindex]
    #print('Current sink: ', sink.name)
    pf = float(mp - len(currentSinks))
    pf /= (mp-1)
    #print('Probability of a fork: ', pf)
    sliceR = random.random()
    #print('Slice:', sliceR)

    if nt == len(graph)-1:
        sliceR = 1.1
	
    if pf >= sliceR:
        #print('Fork')
        maxP = mp - len(currentSinks)+1 #
        #print("Max // - current Sinks +1: ", maxP)
        #print(
        if (nt - len(graph) - len(currentSinks) -1) < maxP:
            maxP = nt - len(graph) - len(currentSinks) -1
        #print('Max: ', maxP)
        ndistribution = create_normal_int_distribution(maxP)
        randomindex = random.randrange(0, len(ndistribution), 1)
        #print(randomindex)
        nbforks = ndistribution[randomindex]
        #print("Nb of forks for the current sink: ", nbforks)
        c = 0

        while (c < nbforks):
            c+=1
            randomtime = random.randrange(1, 301, 1)
            forktask = Task("a"+str(index))
            #print('New fork task generated: ', forktask)
            index+=1
            if sink in graph:
                graph[sink].append(forktask)
            else:
                graph[sink] = [forktask]
            currentSinks.append(forktask)
        #print('Current sink: ', sink)
        #print('Current sinks before removing: ', currentSinks)
        currentSinks.remove(sink)
        #print('Current sinks: ', currentSinks)
        #print('Restart')

    else:
        #print('Join')
        maxT = len(currentSinks)
        #print('Max nb of tasks I can connect: ', maxT)
        tmpSet = currentSinks
        #print(tmpSet)

        #randomtime = random.randrange(1, 301, 1)
        jointask = Task("a"+str(index))
        #print('New join task generated: ', jointask)
        index+=1
        nbjoins = random.randrange(1, maxT+1, 1)
        #print("I join " + str(nbjoins) +" random sinks.")
        randomindexes = random.sample(range(0, len(currentSinks)), nbjoins)
        toRemove = []
        for i in randomindexes:
            #print('Index: ', i)
            #print(tmpSet)
            #print(len(tmpSet))
            candidate = tmpSet[i]
            #print('Candidate to the join: ', candidate)
            if candidate in graph:
                graph[candidate].append(jointask)
            else:
                graph[candidate] = [jointask]
            toRemove.append(candidate)
            #print("Add to toRemove: ", candidate)
        #print("To Remove: ", toRemove)
        #print('Current sinks before modifications: ', currentSinks)
        for element in toRemove:
            currentSinks.remove(element)
        currentSinks.append(jointask)
        #print('Current sinks: ', currentSinks)

    if (len(graph)+len(currentSinks)>=nt-1):
        #print('Max n of tasks reached')
        randomtime = random.randrange(1, 301, 1)
        finaljointask = Task("a"+str(index))
        index+=1
        #print('Final join task generated: ', finaljointask)
        for task in currentSinks:
            if task in graph:
                graph[task].append(finaljointask)
            else:
                graph[task] = [finaljointask]
        flag = False
    #print(graph)

#print(graph)

if sys.argv[4] == "--fpga":
    listoftask = []
    for keyz in graph:
        listoftask.append(keyz)
    listoftask.append(finaljointask)
    f = open(filename, "w")

    for task in listoftask:
        sliceR = random.random()
        if sliceR > 0.75:
            randomtime = random.randrange(40, 301, 1)
        else:
            randomtime = random.randrange(40, 501, 1)
        task.setTiming(randomtime)

        sliceR = random.random()
        if sliceR > 0.75:
            randomclb = random.randrange(2101, 11501, 1)
        else:
            randomclb = random.randrange(2101, 7201, 1)
        task.setCLB(randomclb)

        sliceR = random.random()
        if sliceR > 0.75:
            randomdsp = random.randrange(8, 40, 1)
        else:
            randomdsp = random.randrange(8, 28, 1)
        task.setDSP(randomdsp)

        sliceR = random.random()
        if sliceR > 0.75:
            randommem = random.randrange(150, 900, 1)
        else:
            randommem = random.randrange(150, 601, 1)
        task.setMem(randommem)

        f.write(task.name+"\n")
        f.write(str(task.clb)+"\n")
        f.write(str(task.dsp)+"\n")
        f.write(str(task.mem)+"\n")
        f.write(str(task.timing)+"\n")
        f.write("\n")

    for keyz in graph:
        f.write(str(keyz))
        f.write(" - ")
        for element in graph[keyz]:
            f.write(str(element))
            f.write(" ")
        f.write("\n")
    f.close()
