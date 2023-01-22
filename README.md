# Graph Generator

Scripts to create one or more random graphs with a custom data structure (see section "format").

## Authors
matteobertolino1992@gmail.com

## Scope of the scripts

main.py: it creates one random graph

generateInputs.py: it uses main.py to generate a set of random graphs 

## Usage

MAIN.PY

python -s main.py numberOfTasks breadhtRecommended filename --fpga

where:

- numberOfTasks: number of tasks of the graph

- breadhtRecommended: maximum breadht of the graph (i.e., maximum number of topologically parallel tasks)

- filename: name of the graph (the graph will be create in the directory in which the script is located)

- fpga: option. In this moment, only fpga option is implemented.

Note: resources generation (i.e., CLBs, DSPs, EMBs, HET) are pseudo-randomly generated from boundaries which are hard-coded.

GENERATEINPUTS.PY

python -s generateInputs.py nbOfGraphs nbOfTasks maximumParallelism offsetForGraphName

where:

- nbOfGraphs: number of generated graphs

- numberOfTasks: number of tasks of each graph

- maximumParallelism: maximum breadht of each graph (i.e., maximum number of topologically parallel tasks)

- offsetForGraphName: all the graphs have a name which is "graphX.txt". offsetForGraphName represents the initial value X. X will be increased according to the number of graphs generated

NOTE 1: generateInputs.py will never generate two graphs which are topologically identical

NOTE 2: generated graphs will be created in folder "graphsFolder". Create it, if it does not exist!!

NOTE 3: it is not possible, for instance, putting offsetForGraphName equal to 3 whether "graphsFolder" does not contain "graph0.txt", "graph1.txt" and "graph2.txt"

## Examples
MAIN.PY
python -s main.py 10 5 "testGraph.txt" --fpga

GENERATEINPUTS.PY
python -s generateInputs.py 10 12 4 0

10 graphs will be created, from "graph0.txt" to "graph9.txt". Each graph has 12 tasks and there will be at most 4 tasks in parallel.
It is assured that no one of such graphs have the same topology.

## Graph formats
A graph is logically composed of two parts:

1- List of tasks with their consumptions, such as:

a0 --> name (string)

9279 --> clbs consumption (integer)

9 --> dsps consumption (integer)

268 --> bram memory consumption (integer)

230 --> hardware execution time (integer)

BLANK LINE

a1

3182

29

322

103

BLANK LINE

ecc.

2- A list of tasks with their direct dependencies (in the direction parent -> child)

a0 - a1

a1 - a2 a3

a2 - a4

a4 - a5

a3 - a6

a5 - a7

a6 - a8

a7 - a8

a8 - a9

a9 - a10
