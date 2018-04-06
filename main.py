from tradingBot import Position
from tradingBot import CandleHeap
from tradingBot import Tbot
import csv

tbot = Tbot(4)

print "Initial amount: " + str(tbot.amount)

with open('1 Bitfinex 15m data.txt', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\n')

    for row in reversed(list(reader)):
        #print row[0].split(',')[3] + " " + row[0].split(',')[4]
        tbot.update(float(row[0].split(',')[4]), float(row[0].split(',')[3]))

print "Final amount: " + str(tbot.amount)
