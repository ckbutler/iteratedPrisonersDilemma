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

# Read argv:


# If argv==1, use default values for payoffs, initial distribution of
# strategies, culling threshold, iteration parameters, and re-seeding method:
# Default payoffs:
dc = 5 # Temptation for defection
cc = 3 # Reward for cooperation
dd = 1 # Punishment for defection
cd = 0 # Sucker's payoff
# Default initial distribution of strategies:
numberOf_allC  =  50   # Always cooperate
numberOf_TFT   =   0   # Tit for Tat
numberOf_TFTd  =   0   # Simple Tester Tit for Tat (defect, then Tit for Tat)
numberOf_TFTdc =   0   # Tester TFT (defect, cooperate, then Tit for Tat)
numberOf_GRIM  =   0   # Cooperate, but always defect if opponent defects
numberOf_allD  =  50   # Always defect
# Default culling amount:
cull = 6
# Default iteration parameters:
t = 10  # The number of times each agent interactions with one another.
p = 15  # The number of periods that the simulation will run.
# Default re-seeding method:
# 0 = proportional to initial distribution;
# 1 = proportional to end-of-period distribution.
seed = 1

# Error checking (PD preferences, culling amount, anything else?):
if dc > cc and cc > dd and dd > cd:
    print("Prisoner's Dilemma verified.")
# If not PD preferences, need user response...
N = numberOf_allC + numberOf_TFT + numberOf_TFTd + numberOf_TFTdc +
  numberOf_GRIM + numberOf_allD
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
  'firstMove': 'C',
  'react_C':   'C',
  'react_D':   'C'
  }
allD = {
  'name':      'Always defect',
  'firstMove': 'D',
  'react_C':   'D',
  'react_D':   'D'
  }
TFT = {
  'name':      'Tit-for-Tat',
  'firstMove': 'C',
  'react_C':   'C',
  'react_D':   'D'
  }
TFTd = {
  'name':      'Simple tester Tit-for-Tat',
  'firstMove': 'D',
  'react_C':   'C',
  'react_D':   'D'
  }
# Create more nuanced strategies:
TFTdc = {
  'name':      'Tester Tit-for-Tat',
  'firstMove': 'D',
  'react_C':   'C',
  'react_D':   'D',
  'secondMove':'C'
  }
GRIM = {
  'name':      'Grim Trigger',
  'firstMove': 'C',
  'react_C':   'C',
  'react_D':   'D',
  'reactEverD':'D'    # If the opponent ever played D, GRIM always plays D.
}
# These dictionaries can then be assigned to agents, perhaps with other
# attributes such as initial score:
# agents = []
# for i in range(numberOf_allC):
#   agents.append( ( allC, 0 ) )
# agents[i][0] would represent agent i's strategy;
# agents[i][1] would represent agent i's cumulative score.




# Create structures for tracking play:


############################### FUNCTIONS BEGIN ###############################
# One play of the PD game, returning useful information:


# Culling and seeding at the end of a period:


################################ FUNCTIONS END ################################


############################ CORE SIMULATION BEGINS ############################
# 1 - Pair each agent i with each *other* agent j to play the stage game t times


# 2 - Once all loops for (1) are complete, sort by score, cull and seed


# 3 - Do (1) and (2) over p periods, outputing changed distribution of
#     strategies for each period


############################# CORE SIMULATION ENDS #############################


################################################################################
# HISTORY:
#
# Date       Name        Reason
# ---------- ----------- -------------------------------------------------------
# 08-02-2016 CK Butler   Created file with commented outline of components
#                        Added strategy dictionaries and some error checking
