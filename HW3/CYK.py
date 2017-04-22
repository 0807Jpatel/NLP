import sys
from collections import defaultdict
from math import log
from tree import Node
from tree import Tree

grammer = defaultdict(lambda: defaultdict(int))

class Cell:
    def __init__(self, rulelist):
        self.rulelist = rulelist

    def addRule(self, j, rule):
        self.rulelist[j] = rule

class Rule:
    def __init__(self, leftside, rightside, prob):
        self.leftside = leftside
        self.rightside = rightside
        self.prob = prob

    def addbacktrack(self, x, y, x2, y2):
        self.x1 = x
        self.y1 = y
        self.x2 = x2
        self.y2 = y2


def main(argv):
    ruleFile = open("pcfg.rules", 'r')

    # read in file generated by grammergen.py
    for rule in ruleFile:
        leftside = rule.split(' ', 1)
        prob = leftside[1].rsplit(' ', 1)
        rightside = prob[0]
        (grammer[str(rightside)])[str(leftside[0])] = float(prob[1])

    test = open(argv[0], 'r')
    output = open(argv[1], 'w')
    for line in test:
        output.write(parseSentence(line) + '\n')


def parseSentence(inputsentence):
    inputsentence = inputsentence.split()
    matrix = [[0] * len(inputsentence) for i in range(len(inputsentence))]

    # #initialize
    i = 0
    for x in inputsentence:
        cell = Cell({})

        for r in grammer[x]:
            rule = Rule(r, x, (grammer[x][r]))
            rule.addbacktrack(-1, -1, -1, -1)
            cell.rulelist[r] = rule

        matrix[i][i] = cell
        i += 1

    for x in range(0, len(inputsentence)):
        for i in range(x, -1, -1):
            if x == i:
                continue
            cell = Cell({})
            matrix[i][x] = cell
            addrules(matrix, i, x, cell)

    node = backtrack(matrix, 0, len(matrix)-1, 'TOP')
    if node != -1:
        tree = Tree(node)
        return str(tree).replace('\"', '')
    else:
        return "TOP()"


def backtrack(matrix, x, y, rule):
    finalspot = matrix[x][y]
    if rule not in finalspot.rulelist:
        return -1
    rightside = finalspot.rulelist[rule].rightside.split()
    if len(rightside) == 2:
        child = [backtrack(matrix, finalspot.rulelist[rule].x1, finalspot.rulelist[rule].y1, rightside[0]),
                 backtrack(matrix, finalspot.rulelist[rule].x2, finalspot.rulelist[rule].y2, rightside[1])]
        node = Node(rule, child)
        return node
    else:
        cnode = [Node(finalspot.rulelist[rule].rightside, [])]
        node = Node(rule, cnode)
        return node


def addrules(matrix, x, i, cell):
    for a in range(x, i):
        for rule1 in (matrix[x][a]).rulelist:
            for rule2 in (matrix[a + 1][i]).rulelist:
                if rule1 + ' ' + rule2 in grammer:
                    b = grammer[rule1 + ' ' + rule2]
                    for j in b:
                        leftside = j
                        rightside = rule1 + ' ' + rule2

                        leftprob = float(matrix[x][a].rulelist[rule1].prob)
                        rightprob = float((matrix[a + 1][i]).rulelist[rule2].prob)
                        w = float(b[j])
                        prob = (w * leftprob * rightprob)
                        rule = Rule(leftside, rightside, prob)
                        rule.addbacktrack(x, a, a+1, i)
                        if j in cell.rulelist:
                            if cell.rulelist[j].prob <= prob:
                                cell.addRule(j, rule)
                        else:
                            cell.addRule(j, rule)


def printMatrix(matrix):
    for x in range(len(matrix)):
        for y in range(len(matrix[x])):
            if matrix[x][y] != 0:
                for j in (matrix[x][y]).rulelist:
                    print(j, matrix[x][y].rulelist[j].prob, end=' ')
                print('|', end=' ')
            else:
                print(matrix[x][y], end=' ')
        print()


if __name__ == "__main__":
    main(sys.argv[1:])