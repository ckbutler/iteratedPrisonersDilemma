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
cd = 0 # Sucker# s payoff
# Default initial distribution of strategies:
ALLC  =  50   # Always cooperate
TFT   =   0   # Tit for Tat
TFTd  =   0   # Tester Tit for Tat (defect, then Tit for Tat)
GRIM  =   0   # Cooperate, but always defect if opponent defects
GRIMd =   0   # Tester Grim (defect, then Grim)
ALLD  =  50   # Always defect
# Default culling threshold:
cull = 6
# Default iteration parameters:
t = 10  # The number of times each agent interactions with one another.
p = 15  # The number of periods that the simulation will run.
# Default re-seeding method:
# 0 = proportional to initial distribution;
# 1 = proportional to end-of-period distribution.
seed = 1

# Error checking (PD preferences, culling threshold, anything else?):


# Set up attributes for each agent and create agents according to initial
# distribution of strategies:


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

