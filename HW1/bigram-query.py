import sys

unigramLength = 0
bigramLength = 0
listLength = 0

def main(argv):
    fileuni = open(argv[1], 'r')
    filebi = open(argv[0], 'r')
    word1 = argv[2]
    word2 = argv[3]
    smoothing = argv[4]
    unigram = {}
    bigram = {}
    smoothingmethod = {'M': 3, 'L': 4, 'I': 5, 'K': 6}
    updatedlist = {}
    global listLength
    global unigramLength
    global bigramLength
    listLength = readunifile(fileuni, unigram)
    readbifile(filebi, bigram, smoothingmethod[smoothing])
    unigramLength = len(unigram)
    bigramLength = len(bigram)
    # updateunigram(unigram, bigram, word1, updatedlist, smoothingmethod[smoothing])
    # top10 = sorted(updatedlist, key=updatedlist.get, reverse=True)[:50]
    # x = 0
    # y = 0
    # while(y < 10):
    #     if '<s>' in top10[x]:
    #         x+=1
    #         continue
    #     else:
    #         print '{:30}{:20f}'.format(top10[x], updatedlist[top10[x]])
    #         x+=1
    #         y+=1
    print valueoftwoword(unigram, bigram, word1, word2, smoothingmethod[smoothing])



def valueoftwoword(unigram, bigram, word1,word2, typeofcomp):
    x = word1 + ' ' + word2
    if x in bigram:
        return (bigram[x])[1]
    else:
        return computevalue(unigram, bigram, word1, word2, typeofcomp)



def updateunigram(unigram, bigram, inputword, updatedlist, typeofcomp):
    for word in unigram:
        x = inputword + ' ' + word
        if x in bigram:
            updatedlist[word] = (bigram[x])[1]
        else:
            updatedlist[word] = computevalue(unigram, bigram, inputword, word, typeofcomp)


def computevalue(unigram, bigram, word1, word2, typeofcomp):
    if typeofcomp == 3:
        return bigramfortwowords(word1, word2, bigram, unigram)
    elif typeofcomp == 4:
        return laplacesmoothing(word1, word2, bigram, unigram)
    elif typeofcomp == 5:
        return interpolation(word1, word2, bigram, unigram, .1)
    elif typeofcomp == 6:
        return katzoff(word1, word2, bigram, unigram, .5)


def katzBackAD(word1, word2, biGram, uniGram, D):
    x = word1 + ' ' + word2
    n = 0 - D
    if x in biGram:
        n += (biGram[x])[0]
    else:
        return 0
    y = 0
    if word1 in uniGram:
        y = uniGram[word1]
    s = float(n) / float(y)
    return s


def katzoff(word1, word2, biGram, uniGram, D):
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
            beta += laplaceUnigram( key, uniGram)
    beta = float(laplaceUnigram(word2, uniGram)) / beta
    return alpa * beta




def interpolation(word1, word2, biGram, uniGram, lamda):
    mle = bigramfortwowords(word1, word2, biGram, uniGram)
    lap = laplaceUnigram(word2, uniGram)
    rt = (lamda * mle) + ((1-lamda) * lap)
    return rt


def laplaceUnigram(word2, uniGram):
    if word2 in uniGram:
        return float(1 + uniGram[word2]) / (listLength + unigramLength + 1)
    else:
        return float(1) / (listLength + unigramLength + 1)


def laplacesmoothing(word1, word2, biGram, uniGram):
    x = word1 + ' ' + word2
    n = 1
    if x in biGram:
        n += (biGram[x])[0]
    y = len(uniGram) + 1
    if word1 in uniGram:
        y += uniGram[word1]
    s = float(n) / float(y)
    return s


def bigramfortwowords(word1, word2, biGram, uniGram):
    x = word1 + ' ' + word2
    n = 0
    if (x in biGram):
        n = (biGram[x])[0]
    else:
        return 0
    y = uniGram[word1]
    s = float(n) / float(y)
    return s

def readbifile(filebi, bigram, ind):
    for line in filebi:
        spl = line.split()
        word = spl[0] + ' ' + spl[1]
        bigram[word] = (float((spl[2])), float(spl[ind]))

def readunifile(fileuni, unigram):
    totalwords = 0
    for line in fileuni:
        spl = line.split()
        unigram[spl[0]] = int(spl[1])
        totalwords += int(spl[1])
    return totalwords




if __name__ == "__main__":
    main(sys.argv[1:])
