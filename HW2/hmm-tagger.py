import sys
import re
from collections import defaultdict
from math import log2



def main(args):
    emission = open(args[2])
    transitions = open(args[1])
    MLEbigram = defaultdict(int)
    unigramTag = set([])
    bigramTag = defaultdict(int)
    loadcolume = 3
    if(args[3] == 'M' or args[3] == 'm'):
        loadcolume = 2
    for line in emission:
        line = line.split()
        MLEbigram[line[0] + ' ' + line[1]] = float(line[loadcolume])
        unigramTag.add(line[1])

    for line in transitions:
        line = re.split(r'\s{2,}', line)
        bigramTag[line[0]] = float(line[1])

    test = open(args[0])
    Tagsize = len(unigramTag)
    unigramTag = sorted(unigramTag)
    testfbtagger = open(args[4], 'w')
    if(loadcolume == 2):
        for line in test:
            ViterbiAlgo(line, unigramTag, MLEbigram, bigramTag, Tagsize, testfbtagger, False)
    else:
        for line in test:
            ViterbiAlgo(line, unigramTag, MLEbigram, bigramTag, Tagsize, testfbtagger, True)



def ViterbiAlgo(line, unigramTag, MLEbigram, bigramTag, Tagsize, testfbtagger, mlelap):

    line = line.split()
    sizeofsen = len(line)
    scoreInfo = [[0 for row in range(sizeofsen)] for col in range(Tagsize)]
    backtrackInfo = [[0 for x in range(sizeofsen)] for y in range(Tagsize)]
    # print(unigramTag)
    out = ((line[0]).rsplit("/", 1))
    line[0] = out[0]
    actualTag = []
    actualTag.append(out[1])

    for x in range(Tagsize):
        bigram2 = bigramTag['<s> ' + unigramTag[x]]
        if (bigram2 != 0):
            bigram2 = log2(bigram2)
        else:
            bigram2 = log2(.000000000000000000000000000001)

        bigram1 = MLEbigram[line[0] + ' ' + unigramTag[x]]
        if (bigram1 != 0):
            bigram1 = log2(bigram1)
        else:
            if(mlelap):
                bigram1 = log2(MLEbigram['unk ' + unigramTag[x]])
            else:
                bigram1 = log2(.000000000000000000000000000001)

        scoreInfo[x][0] = bigram2 + bigram1
        backtrackInfo[x][0] = 0

    for word in range(1, sizeofsen):
        out = ((line[word]).rsplit("/", 1))
        line[word] = out[0]
        actualTag.append(out[1])
        for tag in range(Tagsize):
            max = float('-inf')
            maxarg = 0

            bigram2 = MLEbigram[line[word] + ' ' + unigramTag[tag]]

            if (bigram2 != 0):
                bigram2 = log2(bigram2)
            else:
                if (mlelap):
                    bigram2 = log2(MLEbigram['unk ' + unigramTag[tag]])
                else:
                    bigram2 = log2(.000000000000000000000000000001)

            for x in range(Tagsize):
                prevtagscore = scoreInfo[x][word-1]

                bigram1 = bigramTag[unigramTag[x] + ' ' + unigramTag[tag]]
                if(bigram1 != 0):
                    bigram1 = log2(bigram1)
                else:
                    bigram1 = log2(.000000000000000000000000000001)

                score = bigram1 + bigram2 + prevtagscore

                if(score > max):
                    max = score
                    maxarg = x

            scoreInfo[tag][word] = max
            backtrackInfo[tag][word] = maxarg

    max = float('-inf')
    maxarg = 0
    for x in range(Tagsize):
        score = scoreInfo[x][sizeofsen - 1]
        if(max < score):
            max = score
            maxarg = x

    tagrev = []
    for x in range(sizeofsen-1, -1, -1):
        tagrev.append(unigramTag[maxarg])
        maxarg = backtrackInfo[maxarg][x]

    max = pow(2, max)
    testfbtagger.write(str(max) + ' ')

    for x in range(sizeofsen):
        testfbtagger.write(line[x] + '/' + actualTag[x] + '/' + tagrev[sizeofsen-x-1] + ' ')

    testfbtagger.write('\n')








if __name__ == "__main__":
    main(sys.argv[1:])
