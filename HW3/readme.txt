Jaykumar Patel
110255934



grammergen.py is the program that will generate PCFG grammer, it will create
pcfg.rule file which will be used by CYK.py. it will also print out top 10
rules.
		python3 grammergen.py <train.tree>


CYK will parse sentences into prase trees.
		python3 CYK.py <test.txt> <output.trees>

evalb.py was edited to print F1, recall and precision. this program only runs with python 2.7

TOP 10 PCFG for test.txt file 
'PUNC->.', 383
'TO->to', 268
'PP->IN NP_NNP', 263
'IN->from', 243
'PP->IN NP', 222
'PP->TO NP_NNP', 175
'NNS->flights', 169
'NP->NNP NNP', 151
'PUNC->?', 144
'DT->the', 137


Precision before smoothing was about 84, but this would cause some none parsable trees, 
used Laplace smoothing to address this issue, Precision went down to 77. After smoothing
the data it was able to parse every single sentence.


I did not use the psedo-code provided, just used slides for guide line. Each cell in matrix 
is Cell object, and each Cell object holds list of Rules, each Rules hold following info:
Backtrack Cells, Leftside of rule, Rightside of rule, prob.


