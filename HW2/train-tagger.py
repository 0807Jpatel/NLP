import sys
from collections import defaultdict


def main(args):
    file = open(args[0])
    binaryTagCount = defaultdict(int)
    tagWordCount = defaultdict(int)
    wordUnigram = defaultdict(int)
    unigramTagCount = defaultdict(int)
    counter = 0
    for line in file:
        line = line.strip()
        line = line.split(' ')
        tag = line[0].split('/')[-1]
        binaryTagCount['<s> ' + tag] += 1
        unigramTagCount['<s>'] += 1
        lengthofline = len(line)

        for x in range (0, lengthofline):
            taga = line[x].rsplit('/', 1)
            taga[0] = taga[0].strip()
            unigramTagCount[taga[1]] += 1
            if(x != lengthofline-1):
                binaryTagCount[taga[1] + ' ' + line[x+1].rsplit('/', 1)[1]] += 1
                tagWordCount[taga[0] + ' ' + taga[1]] += 1
            wordUnigram[taga[0]] += 1

        tag = line[-1].rsplit('/', 1)
        unigramTagCount[tag[1]] += 1
        binaryTagCount[tag[1] + ' </s>'] += 1
        tagWordCount[tag[0] + ' ' + tag[1]] += 1
        unigramTagCount['</s>'] += 1
    transitions(binaryTagCount, unigramTagCount, args[1])
    emissions(tagWordCount, unigramTagCount, wordUnigram, args[2])
    laplaceunigram(unigramTagCount, args[3])


def transitions(bigarmtag, unigramtag, file):
    file = open(file, 'w')
    for x in bigarmtag:
        MLEprob = bigarmtag[x] / unigramtag[x.split(' ')[0]]
        file.write('%-30s %s \n' % (x, str(MLEprob)))


def emissions(wordtaggram, unigramtag, wordUnigram, file):
    file = open(file, 'w')
    unigramtaglen = len(unigramtag)
    unigramWordlen = len(wordUnigram)
    for x in wordtaggram:
        MLEprob1 = wordtaggram[x] / unigramtag[x.split(' ')[1]]
        lapprob1 = (wordtaggram[x] + 1) / (unigramtag[x.split(' ')[1]] + unigramWordlen + 1)
        MLEprob2 = wordtaggram[x] / wordUnigram[x.split(' ')[0]]
        lapprob2 = (wordtaggram[x] + 1) / (wordUnigram[x.split(' ')[0]] + unigramtaglen + 1)
        file.write('%-30s %-30s %-30s %-30s %s \n' % (x, str(MLEprob1), str(lapprob1), str(MLEprob2), lapprob2))
    file.write('%-30s %-30s %-30s %-30s %s \n' % ('<s> <s>', 1, 1, 1, 1))
    file.write('%-30s %-30s %-30s %-30s %s\n' % ('</s> </s>', 1, 1, 1, 1))

    for x in unigramtag:
        lapprob1 = 1 / (unigramtag[x] + unigramWordlen + 1)
        file.write('%-30s %-30s %-30s %-30s %s \n' % ('unk ' + x, 0, lapprob1, 0, 0))


def laplaceunigram(unigramtag, file):
    file = open(file, 'w')
    totaltag = sum(unigramtag.values())
    for x in unigramtag:
        lapprob = (unigramtag[x] + 1) / (totaltag + len(unigramtag) + 1)
        file.write('%-30s %s \n' % (x, str(lapprob)))


if __name__ == "__main__":
    main(sys.argv[1:])