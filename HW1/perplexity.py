import re, sys
import math

totalword = 0

def main(argv):
    unifile = open(argv[1], 'r')
    bifile = open(argv[0], 'r')
    testfile = open(argv[2], 'r')
    list = []
    unigram = {}
    bigram = {}
    global totalword
    filetolist(testfile, list)
    totalword = len(list)
    readbifile(bifile, bigram)
    readunifile(unifile, unigram)
    getnumbers(list, unigram, bigram)


def filetolist(inputFile, list):
    list.append('<s>')
    for lines in inputFile:
        lines = lines.replace('.', ' </s> <s> ')
        sentence = re.split('[\t\n ]', lines)
        for n in sentence:
            if (n == ''):
                continue
            n = n.lower()
            list.append(n)
    del list[len(list) -1]


def readbifile(filebi, bigram):
    for line in filebi:
        spl = line.split()
        word = spl[0] + ' ' + spl[1]
        bigram[word] = (float((spl[2])), float(spl[4]), float(spl[5]))


def readunifile(fileuni, unigram):
    for line in fileuni:
        spl = line.split()
        unigram[spl[0]] = int(spl[1])


def getnumbers(list, unigram, bigram):
    laplaceprex = 0
    interperx = 0
    uniperx = 0
    for words in range(0, len(list)-2):
        temp = list[words] + ' ' + list[words+1]
        if temp in bigram:
            laplaceprex += math.log((bigram[temp])[1], 2)
            interperx += math.log((bigram[temp])[2], 2)
        else:
            laplaceprex += math.log(laplacesmoothing(list[words], list[words+1], bigram, unigram), 2)
            interperx += math.log(interpolation(list[words], list[words+1], bigram, unigram, .3), 2)
        uniperx += math.log(laplaceUnigram(list[words], unigram), 2)

    uniperx += math.log(laplaceUnigram(list[len(list)-1], unigram), 2)
    constant = -1/float(len(list))
    n = laplaceprex * constant
    print("Laplace bigram: ", math.pow(2, n))
    n = interperx * constant
    print("Interpolated bigram: ", math.pow(2, n))
    n = uniperx * constant
    print("Laplace unigram: ", math.pow(2, n))



def laplaceUnigram(word1, uniGram):
    if word1 in uniGram:
        return float(1 + uniGram[word1]) / (totalword + len(uniGram) + 1)
    else:
        return float(1) / (totalword + len(uniGram) + 1)


def laplacesmoothing(word1, word2, biGram, uniGram):
    x = word1 + ' ' + word2
    n = 1
    if x in biGram:
        n += (biGram[x])[0]
    y = len(uniGram) + 1
    if word1 in uniGram:
        y += uniGram[word1]
    s = float(n)/float(y)
    return s


def interpolation(word1, word2, biGram, uniGram, lamda):
    mle = bigramfortwowords(word1, word2, biGram, uniGram)
    lap = laplaceUnigram(word2, uniGram)
    rt = (lamda * mle) + ((1-lamda) * lap)
    return rt


def bigramfortwowords(word1, word2, biGram, uniGram):
    x = word1 + ' ' + word2
    n = 0
    if(x in biGram):
        n = (biGram[x])[0]
    else:
        return 0
    y = 0
    if(word1 in uniGram):
        y = uniGram[word1]
    else:
        return 0
    s = float(n)/float(y)
    return s




if __name__ == "__main__":
    main(sys.argv[1:])
