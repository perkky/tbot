from tradingBotTester import Position
from tradingBotTester import CandleHeap
from tradingBotTester import Tbot
import csv
import random
import heapq

def testData(fileLocation, ema1=8, ema2=21):
    # 14 and 24
    # 4 and 21
    # 13 and 21
    #8 and 21 is the main one
    #21 and 55
    tbot = Tbot(4, ema1, ema2)

    print "Initial amount: " + str(tbot.amount)

    with open(fileLocation, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')

        for row in reversed(list(reader)):
            #print row[0].split(',')[3] + " " + row[0].split(',')[4]
            tbot.update(int(row[0].split(',')[0]), float(row[0].split(',')[1]), float(row[0].split(',')[2]), float(row[0].split(',')[4]), float(row[0].split(',')[3]))


    print "\nOriginal value:\t10000"
    print "Final value:\t\t%.2f" % tbot.amount
    print "Profit percentage:\t%.2f %%" % (100*tbot.amount/10000 - 100)
    print "Time elapsed:\t\t%d days, %.2f hours and %.2f minutes (%d candles)" % (int(tbot.elapsedTime/ 1440), int((tbot.elapsedTime % 1440)/ 60), (tbot.elapsedTime % 1440 % 60), tbot.totalCandles)
    print "Total volume traded:\t" + str(tbot.totalTraded)

    return (100*tbot.amount/10000 - 100)
#Test numTimes random data sets from the file fileLocation
#upper is the upper number of data
#displays results to the user as well as average ending amount, days and average profit percentage

def testRandomRange(fileLocation, numTimes, upper, ema1=8, ema2=21):
    num = 1
    amount = 0
    days = 0
    profitPercent = 0
    marginCalled = 0
    best = -100
    worst = 100
    print "Initial: 10000"
    print "Number\t\tLower\t\tUpper\t\tRange (days)\t\tTotal\t\tProfit Percentage"
    with open(fileLocation, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')

        rowList = list(reader)

        for i in range(1, numTimes+1):
            tbot = Tbot(4, ema1, ema2)

            low = random.randrange(0, upper - 100)
            high = random.randrange(low, upper)

            for row in reversed(rowList[low:high]):
                #print row[0].split(',')[3] + " " + row[0].split(',')[4]
                tbot.update(int(row[0].split(',')[0]), float(row[0].split(',')[1]), float(row[0].split(',')[2]), float(row[0].split(',')[4]), float(row[0].split(',')[3]))

            amount += tbot.amount
            profitPercent += (100*tbot.amount/10000 - 100)
            if (100*tbot.amount/10000 - 100) > best:
                best = (100*tbot.amount/10000 - 100)
            elif (100*tbot.amount/10000 - 100) < worst:
                worst = (100*tbot.amount/10000 - 100)

            days += tbot.elapsedTime/ 1440
            #print "%d\t\t%d\t\t%d\t\t%.2f\t\t%.2f\t\t%.4f" % (num, low, high, tbot.elapsedTime/ 1440, tbot.amount, (100*tbot.amount/10000 - 100))
            num += 1
            if tbot.marginCalled == True:
                marginCalled += 1


    print "Average final amount:\t%.2f" % (amount/numTimes)
    print "Average profit percent:\t%.2f" % (profitPercent/numTimes)
    print "Average time:\t\t%.2f days" % (days/numTimes)
    print "You were margin called:\t%d times (%.2f%%)" % (marginCalled, float(marginCalled)*100/numTimes)
    print "Best:%.2f\tWorst:%.2f" % (best, worst)

    return (profitPercent/numTimes)

#main loop


testData('Data/BTC/1hr/2018-2014.csv', 7, 20)
testRandomRange('Data/BTC/1hr/2018-2014.csv', 1000, 30600, 7, 20)



"""
highest = 0
ema1 = 0
ema2 = 0
f = open("log 3hr.csv", 'a')
for i in range(5, 55):
    for j in range (i, 56):
        sample = testData('Data/BTC/3hr/2018-2014.csv', ema1=i, ema2=j)
        f.write(str(sample)+","+str(i)+","+str(j)+"\n ")

f.close()
print "The highest was %.2f%% with and ema of %d and %d" % (highest, ema1, ema2)"""
