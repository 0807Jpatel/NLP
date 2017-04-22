import sys
from collections import defaultdict


def main(args):
   test = 'test.txt'
   fbtagger = "test-fbtagger.txt"
   error = 0
   total = 0
   totalTAGPredict = defaultdict(int)
   totalTAGCorrectPredict = defaultdict(int)
   totalTAGintest = defaultdict(int)
   unigueTAGS = set()

   with open(test) as f1, open(fbtagger) as f2:
       for x, y in zip(f1, f2):
           line1 = x.split()
           line2 = y.split()
           for x in range(len(line1)):
               if line1[x] != line2[x]:
                   error += 1
               total += 1
               testTAG = line1[x].rsplit('/', 1)[-1]
               predictTAG = line2[x].rsplit('/', 1)[-1]
               totalTAGPredict[predictTAG] += 1
               totalTAGintest[testTAG] += 1
               unigueTAGS.add(predictTAG)
               unigueTAGS.add(testTAG)
               if(testTAG == predictTAG):
                   totalTAGCorrectPredict[predictTAG] += 1


   writefile = open('accuracy.txt', 'w')
   writefile.write("correct Prediction %d\n" %(total-error))
   writefile.write("Prediction %d\n" % total)
   writefile.write("%-10s %-10s %-10s %-10s %-10s %-10s %-10s\n" % ("TAGS", "SCPT", "SPT", "TKT", "P", "R", "F1"))
   for tag in unigueTAGS:
       p = 0
       r = 0
       f1 = 0
       if(totalTAGPredict[tag] != 0):
           p = totalTAGCorrectPredict[tag] / totalTAGPredict[tag]
       if(totalTAGintest[tag] != 0):
           r = totalTAGCorrectPredict[tag] / totalTAGintest[tag]
       if((p+r) != 0):
           f1 = (2 * p * r) / (p + r)

       writefile.write("%-10s %-10s %-10s %-10s %-2.5f  %-2.5f  %-2.5f\n" % (tag, totalTAGCorrectPredict[tag], totalTAGPredict[tag], totalTAGintest[tag]
                                                                        , p
                                                                        , r
                                                                        , f1))




if __name__ == "__main__":
    main(sys.argv[1:])