from collections import defaultdict
import sys
from tree import Tree
import operator

grammer = defaultdict(lambda: defaultdict(int))
singleRule = defaultdict(int)
singleword = defaultdict(int)


def main(argv):
    trainTree = open(argv[0])
    printPCFG = open("pcfg.rules", 'w')
    for line in trainTree:
        x = Tree.from_str(line)
        add_rules(x.root)
    printTopTen()
    for leftside in grammer:
        for rightside in grammer[leftside]:
            MLE = getMLE(leftside, rightside)
            printPCFG.write(leftside + ' ' + rightside + ' ' + str(MLE) + '\n')

    for x in singleRule:
        for word in singleword:
            if (x + ' ' + word) not in grammer:
                # MLE = 1.0 / float(singleRule[x] + len(singleword) + 1)
                MLE = getMLE(x, word)
                printPCFG.write(x + ' ' + word + ' ' + str(MLE) + '\n')


def add_rules(x):
    singleRule[str(x)] += 1
    child1 = str(x.children[0])
    if len(x.children) > 1:
        child2 = str(x.children[1])
        st = child1 + ' ' + child2
        (grammer[str(x)])[st] += 1
        add_rules(x.children[0])
        add_rules(x.children[1])
        return
    else:
        st = child1
        singleword[child1] += 1
        (grammer[str(x)])[st] += 1
        return


def getMLE(leftside, rightside):
    num = (grammer[leftside])[rightside]
    deno = singleRule[leftside]
    if ' ' not in rightside:  # unirule
        num += 1
        deno += (len(singleword) + 1)

    return float(num) / float(deno)


def printTopTen():
    topofeach = []
    for x in grammer:
        sortedrule = sorted(grammer[x].items(), key=operator.itemgetter(1))
        for y in sortedrule:
            rule = str(x) + '->' + str(y[0])
            count = y[1]
            topofeach.append((rule, count))

    for x in sorted(topofeach, key=operator.itemgetter(1), reverse=True)[:10]:
        print(x)


if __name__ == "__main__":
    main(sys.argv[1:])
