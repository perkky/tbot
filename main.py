from tradingBot import Position
from tradingBot import CandleHeap
from tradingBot import Tbot
import csv
import random

def testData(fileLocation):
    # 14 and 24
    # 4 and 21
    # 13 and 21
    tbot = Tbot(4, 8, 21)

    print "Initial amount: " + str(tbot.amount)

    with open(fileLocation, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')

        for row in reversed(list(reader)):
            #print row[0].split(',')[3] + " " + row[0].split(',')[4]
            tbot.update(int(row[0].split(',')[0]), float(row[0].split(',')[1]), float(row[0].split(',')[2]), float(row[0].split(',')[4]), float(row[0].split(',')[3]))

    print "\nOriginal amount:\t10000"
    print "Final amount:\t\t%.2f" % tbot.amount
    print "Profit percentage:\t%.2f %%" % (100*tbot.amount/10000 - 100)
    print "Time elapsed:\t%d days, %.2f hours and %.2f minutes (%d candles)" % (int(tbot.elapsedTime/ 1440), int((tbot.elapsedTime % 1440)/ 60), (tbot.elapsedTime % 1440 % 60), tbot.totalCandles)
    print "Total amount traded:\t" + str(tbot.totalTraded)

def testRandomRange(fileLocation, numTimes, upper):
    num = 1
    profit = 0
    profitPercent = 0
    print "Initial: 10000"
    print "Number\t\tLower\t\tUpper\t\tTotal\t\tProfit Percentage"
    with open(fileLocation, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter='\n')

        rowList = list(reader)

        for i in range(1, numTimes+1):
            tbot = Tbot(4, 8, 21)

            low = random.randrange(0, upper - 100)
            high = random.randrange(low, upper)

            for row in reversed(rowList[low:high]):
                #print row[0].split(',')[3] + " " + row[0].split(',')[4]
                tbot.update(int(row[0].split(',')[0]), float(row[0].split(',')[1]), float(row[0].split(',')[2]), float(row[0].split(',')[4]), float(row[0].split(',')[3]))

            amount += tbot.amount
            profitPercent += (100*tbot.amount/10000 - 100)
            print "%d\t\t%d\t\t%d\t\t%.2f\t\t%.4f" % (num, low, high, tbot.amount, (100*tbot.amount/10000 - 100))
            num += 1


    print "Average final amount:\t%.2f" % amount/numTimes
    print "Average profit percent:\t%.2f" % profitPercent/numTimes
#testData('Data/BTC/1hr/2018-2014.csv')
testRandomRange('Data/BTC/1hr/2018-2014.csv', 10, 30000)
