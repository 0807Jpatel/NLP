import sys
from collections import defaultdict
from collections import OrderedDict
from operator import itemgetter


def main(args):
    emission = open(args[1])
    MLEbigram = defaultdict(lambda: defaultdict(int))
    for line in emission:
        line = line.split()
        (MLEbigram[line[0]])[line[1]] = line[4]

    unigramTag = defaultdict(int)
    laplacefile = open("laplaceUnigram.txt")
    for line in laplacefile:
        line = line.split()
        unigramTag[line[0]] = float(line[1])

    mostFreqTag = max(unigramTag, key=unigramTag.get)
    testfile = open(args[0])
    writefile = open(args[2], 'w')
    for word in testfile:
        word = word.split()
        for x in word:
            x = x.rsplit('/', 1)
            x = x[0]
            if x in MLEbigram:
                writefile.write(x + '/' + findMaxProbTag(MLEbigram[x], unigramTag) + ' ')
            else:
                writefile.write(x + '/' + mostFreqTag + ' ')
        writefile.write('\n')


def findMaxProbTag(tags, unigramTag):
    lengthofarray = len(tags)
    if lengthofarray == 1:
        return list(tags.keys())[0]
    sortedtags = OrderedDict(sorted(tags.items(), key=itemgetter(1), reverse=True))
    sortedtagsKeys = list(sortedtags.keys())
    x = 0
    y = 1
    while x < lengthofarray and y < lengthofarray and sortedtags[sortedtagsKeys[x]] == sortedtags[sortedtagsKeys[y]]:
        if unigramTag[sortedtagsKeys[x]] < unigramTag[sortedtagsKeys[y]]:
            x = y
        y += 1

    return sortedtagsKeys[x]


if __name__ == "__main__":
    main(sys.argv[1:])
