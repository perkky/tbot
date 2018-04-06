from tradingBot import Position
from tradingBot import LastFour
from tradingBot import Tbot
import csv

tbot = Tbot()

print "Initial amount: " + str(tbot.amount)

with open('Bitfinex 1day data.txt') as csvfile:
    reader = csv.reader(csvfile, delimiter='\n')
    print list(reader)

    for row in reversed(reader):
        print '\n'.join(row)
        print row[0].split(',')[3] + " " + row[0].split(',')[4]

print "Final amount: " + str(tbot.amount)
