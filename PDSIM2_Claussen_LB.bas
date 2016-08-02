'PLEASE READ THESE DIRECTIONS BEFORE CHANGING ANYTHING.
'Change simulation parameters in the first few sections.
'Then press shift-F5 to run.

'Enter the game utilities (from ROW's perspective):
dc = 5 'Temptation for defection
cc = 3 'Reward for cooperation
dd = 1 'Punishment for defection
cd = 0 'Sucker's payoff

'Enter the number of agents and initial distribution of types:
ALLC =  50  'Always cooperate
TFT =    0   'Tit for Tat
TFTd =   0  'Tester Tit for Tat (defect, then Tit for Tat)
GRIM =   0  'Cooperate, but always defect if opponent defects
GRIMd =  0 'Tester Grim (defect, then Grim)
ALLD =  50  'Always defect

'Enter the culling threshold (the number cut after each period):
cull = 6

'Enter the iteration parameters:
t = 10  'The number of times each agent interactions with one another.
p = 15  'The number of periods that the simulation will run.

'Enter the re-seeding parameters.
'0 = proportional to initial distribution;
'1 = proportional to end-of-period distribution.
seed = 1













'DO NOT CHANGE ANY FURTHER CODE BELOW THIS POINT! <- Too late! -Jacob
RANDOMIZE 0.5
N = ALLC + TFT + TFTd + GRIM + GRIMd + ALLD

'The program will check that the game is a Prisoner's Dilemma.
CLS
IF dc > cc AND cc > dd AND dd > cd THEN
        PRINT , "Prisoner's Dilemma verified."
        ELSE
        INPUT "The game is NOT a Prisoner's Dilemma.  Continue anyway? (y/N) "; ans$
        ans$ = UPPER$(ans$)
        IF ans$ <> "Y" THEN END
END IF
'The culling threshold must be less than the total number of agents:
IF cull > N THEN
        PRINT "The culling threshold must be less than the total number of agents."
        END
END IF
'This next part sets up arrays (sets of parameters) for each agent:
DIM agent(N, 5)
'The first part of the array (where the N is) is the ID number of the agent.
'The second part of the array allows different parameters, with six
'slots' all together:
'agent(N,0): The agent's type; 0 = All C, 1 = TFT, 2 = TFTd, 3 = GRIM, 4 = GRIMd, 5 = All D.
'agent(N,1): The agent's initial move; 0 = defect, 1 = cooperate.
'agent(N,2): The agent's move after observing a defection; as above.
'agent(N,3): The agent's move after observing cooperation; as above.
'agent(N,4): The agent's cumulative score for a period.
'agent(N,5): The agent's rank, calculated at the end of the period.

'This next part puts values into the arrays based on the initial distribution.
FOR i = 1 TO N
        IF i < ALLC + 1 THEN GOSUB [labelALLC]
        IF i > ALLC AND i < ALLC + TFT + 1 THEN GOSUB [labelTFT]
        IF i > ALLC + TFT AND i < ALLC + TFT + TFTd + 1 THEN GOSUB [labelTFTd]
        IF i > ALLC + TFT + TFTd AND i < ALLC + TFT + TFTd + GRIM + 1 THEN GOSUB [labelGRIM]
        IF i > ALLC + TFT + TFTd + GRIM AND i < ALLC + TFT + TFTd + GRIM + GRIMd + 1 THEN GOSUB [labelGRIMd]
        IF i > ALLC + TFT + TFTd + GRIM + GRIMd THEN GOSUB [labelALLD]
NEXT i

'This array keeps track of the history of a pair of agents
'over their interactions.  This is only a short-term history.
DIM h(t, 1)

'Arrays that keep track of summary information over time:
DIM dist(p, 5)
'The 'p' part means for each period.
'dist(p,0): The number of All C agents.
'dist(p,1): The number of TFT agents.
'dist(p,2): The number of TFTd agents.
'dist(p,3): The number of GRIM agents.
'dist(p,4): The number of GRIMd agents.
'dist(p,5): The number of All D agents.
DIM score(p, 5)
'score(p,0): The total score of All C agents.
'score(p,1): The total score of TFT agents.
'score(p,2): The total score of TFTd agents.
'score(p,3): The total score of GRIM agents.
'score(p,4): The total score of GRIMd agents.
'score(p,5): The total score of All D agents.

'Records the initial distribution:
dist(0, 0) = ALLC
dist(0, 1) = TFT
dist(0, 2) = TFTd
dist(0, 3) = GRIM
dist(0, 4) = GRIMd
dist(0, 5) = ALLD
CLS
IF seed = 0 THEN seed$ = "Re-Seeding Proportional to Initial Distribution"
IF seed = 1 THEN seed$ = "Re-Seeding Proportional to End-of-Period Distribution"
PRINT , seed$: PRINT , , t; "trials per pairing": PRINT : PRINT "Period"; TAB(11); "All C"; TAB(21); "TFT"; TAB(29); "TFTd"; TAB(38); "GRIM"; TAB(47); "GRIMd"; TAB(57); "All D"; TAB(67); "Elapsed Time": PRINT period; TAB(11); dist(0, 0); TAB(21); dist(0, 1); TAB(29); dist(0, 2); TAB(38); dist(0, 3); TAB(47); dist(0, 4); TAB(57); dist(0, 5)

'The simulation begins:
FOR period = 1 TO p
        time0 = time$("seconds")
'The set of interactions:
FOR i = 1 TO N
        FOR j = 1 TO N
        IF i = j GOTO [nexti]
                REDIM h(t, 1)
                FOR k = 1 TO t
                        GOSUB [playgame]
                NEXT k
        NEXT j
[nexti]
NEXT i
GOSUB [dist]
GOSUB [rank]
GOSUB [CULLandSEED]
NEXT period

END


'SUBROUTINES:

'A subroutine calculates the score for each agent in the stage game:
[playgame]
IF k = 1 THEN
        movei = agent(i, 1)
        movej = agent(j, 1)
ELSE
        IF h(k - 1, 1) = 0 THEN movei = agent(i, 2) 'if j's last move was d, then this move for i is post-d move
        IF h(k - 1, 1) = 1 THEN movei = agent(i, 3) 'if j's last move was c, then this move for i is post-c move
        IF h(k - 1, 0) = 0 THEN movej = agent(j, 2) 'same for i/j reversed
        IF h(k - 1, 0) = 1 THEN movej = agent(j, 3) 'same
END IF
IF h(k - 1, 1) = 0 AND (agent(i, 0) = 3 OR agent(i, 0) = 4) THEN agent(i, 3) = 0 'Handle Grim players: if opponent's previous move was d, then make all of
IF h(k - 1, 0) = 0 AND (agent(j, 0) = 3 OR agent(j, 0) = 4) THEN agent(i, 3) = 0 'Grim's subsequent moves d - only requires changing behavior following c
IF movei = 0 AND movej = 0 THEN
        agent(i, 4) = agent(i, 4) + dd: agent(j, 4) = agent(j, 4) + dd
        h(k, 0) = 0: h(k, 1) = 0
        RETURN
END IF
IF movei = 0 AND movej = 1 THEN
        agent(i, 4) = agent(i, 4) + dc: agent(j, 4) = agent(j, 4) + cd
        h(k, 0) = 0: h(k, 1) = 1
        RETURN
END IF
IF movei = 1 AND movej = 0 THEN
        agent(i, 4) = agent(i, 4) + cd: agent(j, 4) = agent(j, 4) + dc
        h(k, 0) = 1: h(k, 1) = 0
        RETURN
END IF
IF movei = 1 AND movej = 1 THEN
        agent(i, 4) = agent(i, 4) + cc: agent(j, 4) = agent(j, 4) + cc
        h(k, 0) = 1: h(k, 1) = 1
        RETURN
END IF
IF k = t THEN
    IF agent(i, 0) = 3 OR agent(i, 0) = 4 THEN agent(i, 3) = 1 'end of final iteration for this pair so return
        IF agent(j, 0) = 3 OR agent(j, 0) = 4 THEN agent(j, 3) = 1 'Grim to original behavior in case changed above
END IF
RETURN

[dist]
FOR i = 1 TO N
        IF agent(i, 0) = 0 THEN
                dist(period, 0) = dist(period, 0) + 1
                score(period, 0) = score(period, 0) + agent(i, 4)
        END IF
        IF agent(i, 0) = 1 THEN
                dist(period, 1) = dist(period, 1) + 1
                score(period, 1) = score(period, 1) + agent(i, 4)
        END IF
        IF agent(i, 0) = 2 THEN
                dist(period, 2) = dist(period, 2) + 1
                score(period, 2) = score(period, 2) + agent(i, 4)
        END IF
        IF agent(i, 0) = 3 THEN
                dist(period, 3) = dist(period, 3) + 1
                score(period, 3) = score(period, 3) + agent(i, 4)
        END IF
        IF agent(i, 0) = 4 THEN
                dist(period, 4) = dist(period, 4) + 1
                score(period, 4) = score(period, 4) + agent(i, 4)
        END IF
        IF agent(i, 0) = 5 THEN
                dist(period, 5) = dist(period, 5) + 1
                score(period, 5) = score(period, 5) + agent(i, 4)
        END IF
NEXT i
IF period > (screentimes + 1) * 43 THEN
        WAIT
        CLS : PRINT , seed$: PRINT , , t; "trials per pairing": PRINT : PRINT "Period"; TAB(11); "All C"; TAB(21); "TFT"; TAB(29); "TFTd"; TAB(38); "GRIM"; TAB(47); "GRIMd"; TAB(57); "All D"; TAB(67); "Elapsed Time"
        screentimes = screentimes + 1
END IF
timeELAPSED = INT((time$("seconds") - time0) * 10) / 10
PRINT period; TAB(11); dist(period, 0); TAB(21); dist(period, 1); TAB(29); dist(period, 2); TAB(38); dist(period, 3); TAB(47); dist(period, 4); TAB(57); dist(period, 5); TAB(67); timeELAPSED

FOR i = 0 TO 5
        IF seed = 1 AND dist(period, i) = N THEN
                PRINT , , "Population bottle-neck reached."
                WAIT
                END
        END IF
NEXT i
RETURN

[rank]
FOR rank = 1 TO cull
        minscore = t * dc * (N - 1)
        FOR i = 1 TO N
                IF agent(i, 5) = 0 AND agent(i, 4) < minscore THEN
                        minscore = agent(i, 4)
                        minagent = i
                END IF
        NEXT i
        agent(minagent, 5) = rank
NEXT rank
RETURN

[CULLandSEED]
FOR i = 1 TO N
        IF agent(i, 5) > 0 THEN
                x = RND
                IF seed = 0 THEN
                        IF x < ALLC / N THEN GOSUB [labelALLC]
                        IF x > ALLC / N AND x < (ALLC + TFT) / N THEN GOSUB [labelTFT]
                        IF x > (ALLC + TFT) / N AND x < (ALLC + TFT + TFTd) / N THEN GOSUB [labelTFTd]
                        IF x > (ALLC + TFT + TFTd) / N AND x < (ALLC + TFT + TFTd + GRIM) / N THEN GOSUB [labelGRIM]
                        IF x > (ALLC + TFT + TFTd + GRIM) / N AND x < (ALLC + TFT + TFTd + GRIM + GRIMd) / N THEN GOSUB [labelGRIMd]
                        IF x > (ALLC + TFT + TFTd + GRIM + GRIMd) / N THEN GOSUB [labelALLD]
                END IF
                IF seed = 1 THEN
                        IF x < dist(period, 0) / N THEN GOSUB [labelALLC]
                        IF x > dist(period, 0) / N AND x < (dist(period, 0) + dist(period, 1)) / N THEN GOSUB [labelTFT]
                        IF x > (dist(period, 0) + dist(period, 1)) / N AND x < (dist(period, 0) + dist(period, 1) + dist(period, 2)) / N THEN GOSUB [labelTFTd]
                        IF x > (dist(period, 0) + dist(period, 1) + dist(period, 2)) / N AND x < (dist(period, 0) + dist(period, 1) + dist(period, 2) + dist(period, 3)) / N THEN GOSUB [labelGRIM]
                        IF x > (dist(period, 0) + dist(period, 1) + dist(period, 2) + dist(period, 3)) / N AND x < (dist(period, 0) + dist(period, 1) + dist(period, 2) + dist(period, 3) + dist(period, 4)) / N THEN GOSUB [labelGRIMd]
                        IF x > (dist(period, 0) + dist(period, 1) + dist(period, 2) + dist(period, 3) + dist(period, 4)) / N THEN GOSUB [labelALLD]
                END IF
        END IF
        agent(i, 4) = 0
        agent(i, 5) = 0
NEXT i
RETURN

[labelALLC]
agent(i, 0) = 0
agent(i, 1) = 1
agent(i, 2) = 1
agent(i, 3) = 1
RETURN

[labelTFT]
agent(i, 0) = 1
agent(i, 1) = 1
agent(i, 2) = 0
agent(i, 3) = 1
RETURN

[labelTFTd]
agent(i, 0) = 2
agent(i, 1) = 0
agent(i, 2) = 0
agent(i, 3) = 1
RETURN

[labelGRIM]
agent(i, 0) = 3
agent(i, 1) = 1
agent(i, 2) = 0
agent(i, 3) = 1
RETURN

[labelGRIMd]
agent(i, 0) = 4
agent(i, 1) = 0
agent(i, 2) = 0
agent(i, 3) = 1
RETURN

[labelALLD]
agent(i, 0) = 5
agent(i, 1) = 0
agent(i, 2) = 0
agent(i, 3) = 0
RETURN

