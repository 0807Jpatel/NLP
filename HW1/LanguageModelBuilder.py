import sys, getopt
import re

list = []

def main(argv):
    inputFile = parseinput(argv)
    list = []
    biGram = {}
    uniGram = {}
    filetolist(inputFile, list, uniGram)
    listtobigram(list, biGram)
    bigramlm(biGram, uniGram, .3, .5, list)
    unigramlm(uniGram)
    topbigramtxt(biGram)

def parseinput(argv):
    inputFile = ''
    try:
        opts, arg = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('LanguageModelBuilder.py -i <inputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputFile = arg
    f = open(inputFile, 'r')
    return f


def filetolist(inputFile, list, uniGram):
    list.append('<s>')
    for lines in inputFile:
        lines = lines.replace('.', ' </s> <s> ')
        # lines = re.sub('[\t\n,.;_\"*!?:]+', '', lines)
        sentence = re.split('[\t\n ]', lines)
        for n in sentence:
            if (n == ''):
                continue
            n = n.lower()
            list.append(n)
            if(n in uniGram):
                uniGram[n]+=1
            else:
                uniGram[n] = 1


def listtobigram(list, biGram):
    for x in range(0, len(list)-1):
        strinBi = list[x] + ' '+ list[x+1]
        if(strinBi in biGram):
            biGram[strinBi]+=1
        else:
            biGram[strinBi]=1


def bigramfortwowords(word1, word2, biGram, uniGram):
    x = word1 + ' ' + word2
    n = 0
    if(x in biGram):
        n = biGram[x]
    else:
        return 0
    y = 0
    if(word1 in uniGram):
        y = uniGram[word1]
    else:
        return 0
    s = float(n)/float(y)
    return s


def laplacesmoothing(word1, word2, biGram, uniGram):
    x = word1 + ' ' + word2
    n = 1
    if x in biGram:
        n += biGram[x]
    y = len(uniGram) + 1
    if word1 in uniGram:
        y += uniGram[word1]
    s = float(n)/float(y)
    return s


def interpolation(word1, word2, biGram, uniGram, lamda, list):
    mle = bigramfortwowords(word1, word2, biGram, uniGram)
    lap = laplaceUnigram(list, word2, uniGram)
    rt = (lamda * mle) + ((1-lamda) * lap)
    return rt


def laplaceUnigram(list, word1, uniGram):
    if word1 in uniGram:
        return float(1 + uniGram[word1]) / (len(list) + len(uniGram) + 1)
    else:
        return float(1) / (len(list) + len(uniGram) + 1)


def katzBackAD(word1, word2, biGram, uniGram, D):
    x = word1 + ' ' + word2
    n = 0 - D
    if x in biGram:
        n += biGram[x]
    else:
        return 0
    y = 0
    if word1 in uniGram:
        y = uniGram[word1]
    s = float(n) / float(y)
    return s


def katzoff(word1, word2, biGram, uniGram, D, list):
    x = katzBackAD(word1, word2, biGram, uniGram, D)
    if x == 0:
        alpa = 0
        for key, value in uniGram.items():
            x = word1 + ' ' + key
            if x in biGram:
                alpa += float(katzBackAD(word1, key, biGram, uniGram, D))
        alpa = 1 - alpa
        beta = 0
        for key, value in uniGram.items():
            x = word1 + ' ' + key
            if x not in biGram:
                beta += laplaceUnigram(list, key, uniGram)
        beta = float(laplaceUnigram(list, word2, uniGram)) / beta
        return alpa * beta

    return x


def unigramlm(unigram):
    file = open('unigram.lm', 'w')
    for key, value in unigram.items():
        file.write('{:30} {}\n'.format(key, value))

def bigramlm(biGram, uniGram, lamda, D, list):
    file = open('bigram.lm', 'w')
    for key, value in biGram.items():
        word = key.split(" ")
        word1 = word[0]
        word2 = word[1]
        b = bigramfortwowords(word1, word2, biGram, uniGram)
        l = laplacesmoothing(word1, word2, biGram, uniGram)
        i = interpolation(word1, word2, biGram, uniGram, lamda, list)
        k = katzoff(word1, word2, biGram, uniGram, D, list)
        biGram[key] = l
        file.write('{:20}{:20}{:8.2f}{:20.10f}{:20.10f}{:20.10f}{:20.10f}\n'.format(word1, word2, value, b, l, i, k))


def topbigramtxt(biGram):
    sorted(biGram)
    file = open('top-bigram.txt', 'w')
    # print(biGram)
    sortedtop20 = sorted(biGram, key=biGram.get, reverse=True)
    x = 0
    y = 0
    while(y < 20):
        if '<s>' in sortedtop20[x] or '</s>' in sortedtop20[x]:
            x+=1
            continue
        else:
            file.write('{:30}{:20f}\n'.format(sortedtop20[x], biGram[sortedtop20[x]]))
            x+=1
            y+=1


if __name__ == "__main__":
    main(sys.argv[1:])

