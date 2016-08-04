# ipdsim.py copyright by:
#             Christopher K. Butler (CK Butler)
#
# DESCRIPTION
#   <- Add description of what the script does and how to use it.
#
# SYNTAX
#   python ipdsim.py
#   python ipdsim.py -p dc cc dd cd
#   python ipdsim.py -s allC allD TFT TFTd TFTdc GRIM
#   python ipdsim.py -c cull
#   python ipdsim.py -i iterations
#   python ipdsim.py -r rounds
#
# EXAMPLES
#   <- If appropriate, add example syntax with notes.
#   python ipdsim.py                 # Runs simulation with default parameters.

################################################################################

from sys import argv
from random import choice
import networkx as nx

VERBOSE = False

# Default values for payoffs, initial distribution of strategies,
# culling threshold, iteration parameters, and re-seeding method:
# Default payoffs:
dc = 5 # Temptation for defection
cc = 3 # Reward for cooperation
dd = 1 # Punishment for defection
cd = 0 # Sucker's payoff
# Default initial distribution of strategies:
numberOf_allC  =  16   # Always cooperate
numberOf_allD  =  20   # Always defect
numberOf_TFT   =  16   # Tit for Tat
numberOf_TFTd  =  16   # Simple Tester Tit for Tat (defect, then Tit for Tat)
numberOf_TFTdc =  16   # Tester TFT (defect, cooperate, then Tit for Tat)
numberOf_GRIM  =  16   # Cooperate, but always defect if opponent defects
# Default culling amount:
cull = 5
# Default iteration parameters:
iterations = 10  # The number of times each agent interacts with one another.
rounds     = 42  # The number of rounds that the simulation will run.

# Read argv, change default values accordingly:
#print(argv)
if '-p' in argv:
    payoffList = argv[argv.index('-p')+1:argv.index('-p')+5]
    dc = int(payoffList[0])
    cc = int(payoffList[1])
    dd = int(payoffList[2])
    cd = int(payoffList[3])
if '-s' in argv:
    strategyDistribution = argv[argv.index('-s')+1:argv.index('-s')+7]
    numberOf_allC  = int(strategyDistribution[0])
    numberOf_allD  = int(strategyDistribution[1])
    numberOf_TFT   = int(strategyDistribution[2])
    numberOf_TFTd  = int(strategyDistribution[3])
    numberOf_TFTdc = int(strategyDistribution[4])
    numberOf_GRIM  = int(strategyDistribution[5])
if '-c' in argv:
    cull = int(argv[argv.index('-c')+1])
if '-i' in argv:
    iterations = int(argv[argv.index('-i')+1])
if '-r' in argv:
    rounds = int(argv[argv.index('-r')+1])

# Error checking (PD preferences, culling amount, anything else?):
if dc > cc and cc > dd and dd > cd:
    if VERBOSE: print("Prisoner's Dilemma preferences verified.")
# If not PD preferences, need user response...
N = (numberOf_allC + numberOf_TFT + numberOf_TFTd + numberOf_TFTdc +
     numberOf_GRIM + numberOf_allD)
if cull > N/2:
    print("The culling amount must be less than half the total number of agents.")
    exit()

# Set up attributes for each agent and create agents according to initial
# distribution of strategies:
# An IPD strategy is defined by (1) its initial move {C/D}, (2) whether it
# is contingent or not, and [branching]...
# If it's contingent, what it's current move is given the history of play.
# If it's not contingent, what it's current move is given its non-contingent
# pattern of moves.
# A strategy can also be programmed to do non-contingent moves beyond the first
# move and then become contingent. E.G., TFTdc could defect on the first move,
# cooperate on the second move, and then play normal TFT.
# Simple non-contingent strategies of allC and allD can be programmed as if
# they are reacting to the last move (react_C and react_D).
# Create simple strategy-type dictionaries:
allC = {
  'name':      'Naive cooperator',
  'abbr':      'allC',
  'firstMove': 'C',
  'react_C':   'C',
  'react_D':   'C'
  }
allD = {
  'name':      'Always defect',
  'abbr':      'allD',
  'firstMove': 'D',
  'react_C':   'D',
  'react_D':   'D'
  }
TFT = {
  'name':      'Tit-for-Tat',
  'abbr':      'TFT',
  'firstMove': 'C',
  'react_C':   'C',
  'react_D':   'D'
  }
TFTd = {
  'name':      'Simple tester Tit-for-Tat',
  'abbr':      'TFTd',
  'firstMove': 'D',
  'react_C':   'C',
  'react_D':   'D'
  }
# Create more nuanced strategies:
TFTdc = {
  'name':      'Tester Tit-for-Tat',
  'abbr':      'TFTdc',
  'firstMove': 'D',
  'react_C':   'C',
  'react_D':   'D',
  'secondMove':'C'
  }
GRIM = {
  'name':      'Grim Trigger',
  'abbr':      'GRIM',
  'firstMove': 'C',
  'react_C':   'C',
  'react_D':   'D',
  'reactEverD':'D'    # If the opponent ever played D, GRIM always plays D.
}                     # So, the history structure should track this.
# These dictionaries can then be assigned to agents, with other
# attributes such as initial score:
agents = []
for i in range(numberOf_allC):
  agent = {'score':0}
  agent.update(allC)
  agents.append(agent)
for i in range(numberOf_allD):
  agent = {'score':0}
  agent.update(allD)
  agents.append(agent)
for i in range(numberOf_TFT):
  agent = {'score':0}
  agent.update(TFT)
  agents.append(agent)
for i in range(numberOf_TFTd):
  agent = {'score':0}
  agent.update(TFTd)
  agents.append(agent)
for i in range(numberOf_TFTdc):
  agent = {'score':0}
  agent.update(TFTdc)
  agents.append(agent)
for i in range(numberOf_GRIM):
  agent = {'score':0}
  agent.update(GRIM)
  agents.append(agent)
G = nx.complete_graph(len(agents))
for i,agent in enumerate(agents):
    G.node[i] = agent

# Create structures for tracking play:
distribution = [
  (
  (allC , numberOf_allC),
  (allD , numberOf_allD),
  (TFT  , numberOf_TFT),
  (TFTd , numberOf_TFTd),
  (TFTdc, numberOf_TFTdc),
  (GRIM , numberOf_GRIM)
  ),
]
averageScore = []

############################### FUNCTIONS BEGIN ###############################
# Count strategy types in agents list:
def updateDistribution():
    count_allC  = 0
    count_allD  = 0
    count_TFT   = 0
    count_TFTd  = 0
    count_TFTdc = 0
    count_GRIM  = 0
    for n in G:
        if G.node[n]['abbr'] == 'allC' : count_allC  += 1
        if G.node[n]['abbr'] == 'allD' : count_allD  += 1
        if G.node[n]['abbr'] == 'TFT'  : count_TFT   += 1
        if G.node[n]['abbr'] == 'TFTd' : count_TFTd  += 1
        if G.node[n]['abbr'] == 'TFTdc': count_TFTdc += 1
        if G.node[n]['abbr'] == 'GRIM' : count_GRIM  += 1
    tuple = (
        (allC , count_allC),
        (allD , count_allD),
        (TFT  , count_TFT),
        (TFTd , count_TFTd),
        (TFTdc, count_TFTdc),
        (GRIM , count_GRIM)
    )
    return(tuple)

# Print current distribution to screen as whole table:
def printCurrentDistributionAsWholeTable():
    currentDistribution = distribution[-1]
    print('\nEnd of round distribution of strategies:')
    for type,count in currentDistribution:
        print("%25s : %5d" % (type['name'],count) )

# Print history of strategy distributions with average score:
def printDistributionHistory():
    header='Round: --- allC  allD   TFT  TFTd TFTdc  GRIM --- Average Score'
    print(header)
    for i in range(r):
        print(
            '%5d:    %5d %5d %5d %5d %5d %5d     %13d'
            %
            (i,
            distribution[i][0][1],
            distribution[i][1][1],
            distribution[i][2][1],
            distribution[i][3][1],
            distribution[i][4][1],
            distribution[i][5][1],
            averageScore[i])
        )

# Play iterations of the PD game, updating score of agents:
def playIPDgame(node_A,node_B):
    history_A = []  # History of A's actions
    history_B = []  # History of B's actions
    for i in range(iterations):
        action_A=action_B=''
        if i == 0:
            action_A = G.node[node_A]['firstMove']
            action_B = G.node[node_B]['firstMove']
        if i == 1:
            if history_B[-1] == 'C':
                action_A = G.node[node_A]['react_C']
            else:
                action_A = G.node[node_A]['react_D']
            if history_A[-1] == 'C':
                action_B = G.node[node_B]['react_C']
            else:
                action_B = G.node[node_B]['react_D']
            if 'reactEverD' in G.node[node_A] and 'D' in history_B:
                action_A = G.node[node_A]['reactEverD']
            if 'reactEverD' in G.node[node_B] and 'D' in history_A:
                action_B = G.node[node_B]['reactEverD']
            if 'secondMove' in G.node[node_A]:
                action_A = G.node[node_A]['secondMove']
            if 'secondMove' in G.node[node_B]:
                action_B = G.node[node_B]['secondMove']
        if i>1:
            if history_B[-1] == 'C':
                action_A = G.node[node_A]['react_C']
            else:
                action_A = G.node[node_A]['react_D']
            if history_A[-1] == 'C':
                action_B = G.node[node_B]['react_C']
            else:
                action_B = G.node[node_B]['react_D']
            if 'reactEverD' in G.node[node_A] and 'D' in history_B:
                action_A = G.node[node_A]['reactEverD']
            if 'reactEverD' in G.node[node_B] and 'D' in history_A:
                action_B = G.node[node_B]['reactEverD']
        history_A.append(action_A)
        history_B.append(action_B)
        (score_A,score_B) = stageGamePayoffs(action_A,action_B)
        G.node[node_A]['score']+=score_A
        G.node[node_B]['score']+=score_B
    return(0)

# Return score from stage game given actions:
def stageGamePayoffs(action_A,action_B):
    score_A=0
    score_B=0
    if action_A == 'D' and action_B == 'C':
        score_A = dc
        score_B = cd
    if action_A == 'C' and action_B == 'C':
        score_A = cc
        score_B = cc
    if action_A == 'D' and action_B == 'D':
        score_A = dd
        score_B = dd
    if action_A == 'C' and action_B == 'D':
        score_A = cd
        score_B = dc
    return(score_A,score_B)

# Record average score:
def calculateAverageScore():
    scores = []
    for n in G:
        scores.append(G.node[n]['score'])
    return(sum(scores)/len(scores))

# Culling and seeding at the end of a round:
def cullingAndSeeding():
    # This culling method has two random components.
    # First, if there are ties wrt bestLowScore, all agents with that
    # bestLowScore are susceptible to culling.
    # Second, all agents with a score greater than the bestLowScore have an
    # equal chance of re-seeding for the culled agents.
    # Final note: if changing the graph from a complete graph, this culling
    # method should be adjusted for the number of edges each node has.
    scoreList = []
    for n in G:
        scoreList.append( (n,G.node[n]['score'],G.node[n]['abbr']) )
    scoreList = sorted(scoreList, key=lambda x: x[1])
    cullList = scoreList[:cull]
    seedList = scoreList[cull:]
    bestLowScore = cullList[-1][1]
    for x in scoreList[cull:]:
        if x[1] == bestLowScore:
            cullList.append(x)
            seedList.remove(x)
    for n in G:
        G.node[n]['score'] = 0
    if len(seedList) == 0: # All agents have the same score; don't cull
        return(0)
    for i in range(len(cullList)-cull):
        cullList.remove(choice(cullList))
    for i in range(len(seedList)-cull):
        seedList.remove(choice(seedList))
    if len(seedList) < len(cullList):
        for i in range(len(cullList)-len(seedList)):
            seedList.append(choice(cullList))
    for i,(n,score,type) in enumerate(cullList):
        agent = {'score':0}
        if seedList[i][2] == 'allC' : agent.update(allC)
        if seedList[i][2] == 'allD' : agent.update(allD)
        if seedList[i][2] == 'TFT'  : agent.update(TFT)
        if seedList[i][2] == 'TFTd' : agent.update(TFTd)
        if seedList[i][2] == 'TFTdc': agent.update(TFTdc)
        if seedList[i][2] == 'GRIM' : agent.update(GRIM)
        G.node[n] = agent
    return(0)
################################ FUNCTIONS END ################################


############################ CORE SIMULATION BEGINS ############################
r = 0
while r < rounds:
    for (node_A,node_B) in G.edges():
        playIPDgame(node_A,node_B)
    if VERBOSE:
        print("\nEnd of round scores:")
        for n in G:
            print("Node %3d (%5s): %5d" %
            (n,G.node[n]['abbr'],G.node[n]['score']) )
    averageScore.append(calculateAverageScore())
    cullingAndSeeding()
    distribution.append(updateDistribution())
    r += 1
printDistributionHistory()


# For error checking:
if VERBOSE:
    printCurrentDistributionAsWholeTable()
############################# CORE SIMULATION ENDS #############################


################################################################################
# HISTORY:
#
# Date       Name        Reason
# ---------- ----------- -------------------------------------------------------
# 08-02-2016 CK Butler   Created file with commented outline of components
#                        Added strategy dictionaries and some error checking
# 08-03-2016 CK Butler   Created agents' list & function for counting strategies
#                        Changed agents' structure to be dictionaries
#                        Created function for appropriate pairings per round
# 08-04-2016 CK Butler   Changed structure from lists to networkx
#                        Iterating over edges, agents play IPD & tally scores
#                        Added command-line functionality
#                        Added cullingAndSeeding function, finishing main prog
#                        Added output for main prog. Fully functional!
