# ipdsim.py copyright by:
#             Christopher K. Butler (CK Butler)
#
# DESCRIPTION
#   <- Add description of what the script does and how to use it.
#
# SYNTAX
#   <- Add generic syntax, including optional arguments.
#   python ipdsim.py
#
# EXAMPLES
#   <- If appropriate, add example syntax with notes.
#   python ipdsim.py                 # Runs simulation with default parameters.

################################################################################

import sys
import random
import networkx as nx

VERBOSE = True

# Read argv:  #Perhaps move reading of command-line arguments after defaults.


# If argv==1, use default values for payoffs, initial distribution of
# strategies, culling threshold, iteration parameters, and re-seeding method:
# Default payoffs:
dc = 5 # Temptation for defection
cc = 3 # Reward for cooperation
dd = 1 # Punishment for defection
cd = 0 # Sucker's payoff
# Default initial distribution of strategies:
numberOf_allC  =  20   # Always cooperate
numberOf_allD  =  10   # Always defect
numberOf_TFT   =  10   # Tit for Tat
numberOf_TFTd  =  10   # Simple Tester Tit for Tat (defect, then Tit for Tat)
numberOf_TFTdc =   0   # Tester TFT (defect, cooperate, then Tit for Tat)
numberOf_GRIM  =   0   # Cooperate, but always defect if opponent defects
# Default culling amount:
cull = 6
# Default iteration parameters:
iterations = 10  # The number of times each agent interactions with one another.
periods    = 15  # The number of periods that the simulation will run.
# Default re-seeding method:
# 0 = proportional to initial distribution;
# 1 = proportional to end-of-period distribution.
seed = 1

# Error checking (PD preferences, culling amount, anything else?):
if dc > cc and cc > dd and dd > cd:
    print("Prisoner's Dilemma verified.")
# If not PD preferences, need user response...
N = (numberOf_allC + numberOf_TFT + numberOf_TFTd + numberOf_TFTdc +
     numberOf_GRIM + numberOf_allD)
if cull > N:
    print("The culling amount must be less than the total number of agents.")
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
H = nx.complete_graph(len(agents))
G = nx.Graph()
for i,agent in enumerate(agents):
    G.add_node(i,agent)
G.add_edges_from(H.edges())



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
    for type,count in currentDistribution:
        print("%25s : %5d" % (type['name'],count) )


# Play iterations of the PD game, updating score of agents:
def playIPDgame():
    return(0)


# Culling and seeding at the end of a period:


################################ FUNCTIONS END ################################


############################ CORE SIMULATION BEGINS ############################
# 1 - Pair each agent i with each *other* agent j to play the stage game t times
for

# 2 - Once all loops for (1) are complete, sort by score, cull and seed


# 3 - Do (1) and (2) over p periods, outputing changed distribution of
#     strategies for each period
distribution.append(updateDistribution())

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
#                        Created function for appropriate pairings per period
# 08-04-2016 CK Butler   Changed structure from lists to networkx
