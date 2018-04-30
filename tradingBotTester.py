class Position:
    #initial price
    #amount - positive if long, -ve if short
    def __init__(self, price, amount):
        self.price = price
        self.amount = amount

    def getProfit(self, price):
        profit = (price - self.price) *self.amount

        return profit

    def getAmount(self):
        return self.amount
    def getPrice(self):
        return self.price

pos = Position(10, 1)

class CandleHeap:
    #num is number of candles you want to take into account
    #numCandles is the amount of candles to take into account
    #max is a list of the latest 4 maxs
    #min is a list of the latest 4 mins
    def __init__(self, numCandles):
        self.num = 0
        self.max = []
        self.min = []
        self.numCandles = numCandles

    def add(self, min, max):
        if not self.num == self.numCandles:
            self.max.append(max)
            self.min.append(min)
            self.num += 1
        else:
            #ripple them down'
            #then add it to the end'
            for i in range(0, self.numCandles-1):
                self.max[i] = self.max[i+1]
                self.min[i] = self.min[i+1]

            self.max[self.numCandles-1] = max
            self.min[self.numCandles-1] = min

    def getMax(self):
        return max(self.max)

    def getMin(self):
        return min(self.min)

    def getNum(self):
        return self.num

    #for debugging
    def printHeap(self):
        print "Max: %.2f %.2f %.2f %.2f" % (self.max[0], self.max[1], self.max[2], self.max[3])
        print "Min: %.2f %.2f %.2f %.2f" % (self.min[0], self.min[1], self.min[2], self.min[3])

class Tbot:
    #initalise variables
    def __init__(self, num, ema1, ema2):
        self.candleHeap = CandleHeap(num)
        self.bos = ""                               #Buy or sell variable
        self.amount = 10000                         #Total ammount
        self.pos = Position( 100, 0.01)          #Current position
        self.totalTraded = 0                        #Total value traded
        self.emaNum1 = ema1                         #1st ema days
        self.emaNum2= ema2                          #2nd ema days
        self.ema1 = 0                               #1st ema
        self.ema2 = 0                               #2nd ema
        self.numCandles = 0                         #num candles that have been added - used for crossing ema
        self.first = 0                              #the first candles time
        self.elapsedTime = 0                        #time minutes of last candle - first candle
        self.totalCandles = 0                       #total amount of candles
        self.marginCalled = False                   #flag to see if you were margin called
        self.lastTrade = "None"                     #the last trade - None, Long, Short

        self.ema12 = 0                               #2nd 1st ema
        self.ema22 = 0                               #2nd 2nd ema

    def fourCandleStrat(self, min, max):
        amount = 10000
        fee = 0.0015*amount

        if self.candleHeap.getNum() == self.candleHeap.numCandles:

            #if positive = long position
            if self.pos.getAmount() > 0:
                #if a new low is set from last four candles, close long and start a short
                if min < self.candleHeap.getMin():
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()-1) - fee
                    self.totalTraded += amount

                    print "\nClosed a long position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMin()-1)
                    print "Opened up a short position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMin()-1), self.candleHeap.getMin()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMin()-1) - fee)

                    self.pos = Position( self.candleHeap.getMin()-1, -amount/(self.candleHeap.getMin()-1))
            elif self.pos.getAmount() < 0:
                #else if a new high is set, close shorts and open a long
                if max > self.candleHeap.getMax():
                    self.totalTraded += amount
                    self.amount += self.pos.getProfit(self.candleHeap.getMax()+1) - fee

                    print "\nClosed a short position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMax()-1)
                    print "Opened up a long position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMax()-1), self.candleHeap.getMax()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMax()-1) - fee)

                    self.pos = Position(self.candleHeap.getMax()+1, amount/(self.candleHeap.getMax()+1))

        self.candleHeap.add(min, max)

    def fourCandleStratReversed(self, min, max):
        amount = 10000
        fee = 0.0015*amount

        if self.candleHeap.getNum() == self.candleHeap.numCandles:

            #if positive = long position
            if self.pos.getAmount() < 0:
                #if a new low is set from last four candles, close long and start a short
                if min < self.candleHeap.getMin():
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()-1) - fee
                    self.totalTraded += amount

                    """print "\nClosed a long position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMin()-1)
                    print "Opened up a short position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMin()-1), self.candleHeap.getMin()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMin()-1) - fee)
                    """
                    self.pos = Position( self.candleHeap.getMin()-1, amount/(self.candleHeap.getMin()-1))
            elif self.pos.getAmount() > 0:
                #else if a new high is set, close shorts and open a long
                if max > self.candleHeap.getMax():
                    self.totalTraded += amount
                    self.amount += self.pos.getProfit(self.candleHeap.getMax()+1) - fee

                    """print "\nClosed a short position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMax()-1)
                    print "Opened up a long position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMax()-1), self.candleHeap.getMax()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMax()-1) - fee)
                    """
                    self.pos = Position(self.candleHeap.getMax()+1, -amount/(self.candleHeap.getMax()+1))

        self.candleHeap.add(min, max)

    def combinedStrat(self, min, max):
        amount = 10000
        fee = 0.0015*amount

        change = self.ema1 - self.ema2

        if self.candleHeap.getNum() == self.candleHeap.numCandles:

            #if positive = long position
            if self.pos.getAmount() > 0 and change < 0:
                #if a new low is set from last four candles, close long and start a short
                if min < self.candleHeap.getMin():
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()-1) - fee
                    self.totalTraded += amount

                    """print "\nClosed a long position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMin()-1)
                    print "Opened up a short position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMin()-1), self.candleHeap.getMin()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMin()-1) - fee)
                    """
                    self.pos = Position( self.candleHeap.getMin()-1, -amount/(self.candleHeap.getMin()-1))
            elif self.pos.getAmount() < 0 and change > 0:
                #else if a new high is set, close shorts and open a long
                if max > self.candleHeap.getMax():
                    self.totalTraded += amount
                    self.amount += self.pos.getProfit(self.candleHeap.getMax()+1) - fee

                    """print "\nClosed a short position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMax()-1)
                    print "Opened up a long position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMax()-1), self.candleHeap.getMax()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMax()-1) - fee)
                    """
                    self.pos = Position(self.candleHeap.getMax()+1, amount/(self.candleHeap.getMax()+1))

        self.candleHeap.add(min, max)

    def combinedStratReversed(self, min, max):
        amount = 10000
        fee = 0.0015*amount

        change = self.ema1 - self.ema2

        if self.candleHeap.getNum() == self.candleHeap.numCandles:

            #if positive = long position
            if self.pos.getAmount() < 0 and change > 0:
                #if a new low is set from last four candles, close long and start a short
                if min < self.candleHeap.getMin():
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()-1) - fee
                    self.totalTraded += amount

                    """print "\nClosed a long position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMin()-1)
                    print "Opened up a short position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMin()-1), self.candleHeap.getMin()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMin()-1) - fee)
                    """
                    self.pos = Position( self.candleHeap.getMin()-1, amount/(self.candleHeap.getMin()-1))
            elif self.pos.getAmount() > 0 and change < 0:
                #else if a new high is set, close shorts and open a long
                if max > self.candleHeap.getMax():
                    self.totalTraded += amount
                    self.amount += self.pos.getProfit(self.candleHeap.getMax()+1) - fee

                    """print "\nClosed a short position of %.2f units at $%.2f " % (self.pos.getAmount(), self.candleHeap.getMax()-1)
                    print "Opened up a long position of %.2f units at $%.2f" % (-amount/(self.candleHeap.getMax()-1), self.candleHeap.getMax()-1)
                    print "Profit for last trade: %.2f" % (self.pos.getProfit(self.candleHeap.getMax()-1) - fee)
                    """
                    self.pos = Position(self.candleHeap.getMax()+1, -amount/(self.candleHeap.getMax()+1))

        self.candleHeap.add(min, max)



    def calcEMA(self, close):
        self.ema1 = (close-self.ema1)*2/(float(self.emaNum1)+1) + self.ema1
        self.ema2 = (close-self.ema2)*2/(float(self.emaNum2)+1) + self.ema2

    def crossingEMAStrat(self, close):
        #set to either self.amount for compounded or a flat number
        tradingAmount = 10000

        #+ve means faster is above the slower
        change = self.ema1 - self.ema2
        delta = 0.004*close  #how far the emas need to be after crossing before chaging position
                    #can be a flat value or a % - 50 flat works well for btc
        fees = 0.004*tradingAmount#*0
        #makes sure sufficient data has been provided to allow for proper ema base calculation
        if self.numCandles > 100:
            diff = self.ema1 - self.ema2 #faster one take slower one - +ve is bullish, -ve is bearish

            if self.pos.getAmount() < 0 and change >= delta:
                #closes the position, adds the profit to the amount and then opens up an opposite position
                self.amount += self.pos.getProfit(close) - fees
                self.totalTraded += tradingAmount
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)
                self.pos = Position(close, tradingAmount/(close))
            elif self.pos.getAmount() > 0 and change <= -delta:
                #closes the position, adds the profit to the amount and then opens up an opposite position
                self.amount += self.pos.getProfit(close) - fees
                self.totalTraded += tradingAmount
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)
                self.pos = Position(close, -tradingAmount/(close))

            if self.pos.getProfit(close) < -1500:
                print "You've been margin called! (%d lost)" % self.pos.getProfit(close)
                self.marginCalled = True


    #Similar to the crossing ema strat however will always close the position at x% profit
    def takeProfitStrat(self, close):
        #set to either self.amount for compounded or a flat number
        tradingAmount = 10000

        #+ve means faster is above the slower
        change = self.ema1 - self.ema2
        delta = 0.004*close  #how far the emas need to be after crossing before chaging position
                    #can be a flat value or a % - 50 flat works well for btc
        fees = 0.002*tradingAmount#*0
        #makes sure sufficient data has been provided to allow for proper ema base calculation
        if self.numCandles > 100:
            diff = self.ema1 - self.ema2 #faster one take slower one - +ve is bullish, -ve is bearish

            if change >= delta:
                #closes the position, adds the profit to the amount and then opens up an opposite position
                if self.pos.getAmount() < 0:
                    self.amount += self.pos.getProfit(close) - fees
                    self.totalTraded += tradingAmount
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)
                if self.pos.getAmount() <= 0:
                    self.pos = Position(close, tradingAmount/(close))
                    self.lastTrade = "Long"
            elif change <= -delta:
                #closes the position, adds the profit to the amount and then opens up an opposite position
                if self.pos.getAmount() > 0:
                    self.amount += self.pos.getProfit(close) - fees
                    self.totalTraded += tradingAmount
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)
                if self.pos.getAmount() >= 0:
                    self.pos = Position(close, -tradingAmount/(close))
                    self.lastTrade = "Short"

            if self.pos.getProfit(close) < -1500:
                print "You've been margin called! (%d lost)" % self.pos.getProfit(close)
                self.marginCalled = True
            elif self.pos.getProfit(close)*self.pos.getProfit(close) > 500*500:
                self.amount += self.pos.getProfit(close) - fees
                self.totalTraded += tradingAmount
                self.pos.amount = 0


    #******************Depreciated*********************
    #similar to the crossing ema strat, except it will only trade with the trend
    #if the larger ema is sloping down it will only short and vice versa
    #depriciated - need to update how the positions work if you want to use it
    def crossingEMATrend(self, close):
        #set to either self.amount for compounded or a flat number
        tradingAmount = 10000

        self.ema12 = self.ema1
        self.ema22 = self.ema2

        self.ema1 = (close-self.ema1)*2/(float(self.emaNum1)+1) + self.ema1
        self.ema2 = (close-self.ema2)*2/(float(self.emaNum2)+1) + self.ema2
        change = self.ema1 - self.ema2
        delta = 0.004*close  #how far the emas need to be after crossing before chaging position
                    #can be a flat value or a % - 50 flat works well for btc
        fees = 0.002*tradingAmount#*0
        #makes sure sufficient data has been provided to allow for proper ema base calculation
        if self.numCandles > 100:
            diff = self.ema1 - self.ema2 #faster one take slower one - +ve is bullish, -ve is bearish

            if change >= delta:
                if self.pos.bos == "Sell":
                    #closes the position, adds the profit to the amount and then opens up an opposite position
                    self.amount += self.pos.getProfit(close) - fees
                    self.totalTraded += tradingAmount
                    self.pos = Position("Empty", close, 0) #make it no trade
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)

                #only open a long position if the bigger ema is trending up
                if self.pos.bos == "Empty" and (self.ema1 - self.ema12) > 0:
                    self.pos = Position("Buy", close, tradingAmount/(close))


            elif change <= -delta:
                if self.pos.bos == "Buy":
                    #closes the position, adds the profit to the amount and then opens up an opposite position
                    self.amount += self.pos.getProfit(close) - fees
                    self.totalTraded += tradingAmount
                    self.pos = Position("Empty", close, 0) #make it no trade
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)

                #only open a short position if the bigger ema is trending down
                if self.pos.bos == "Empty" and (self.ema1 - self.ema12) < 0:
                    self.pos = Position("Sell", close, tradingAmount/(close))

            if self.pos.getProfit(close) < -1500:
                print "You've been margin called! (%d lost)" % self.pos.getProfit(close)
                self.marginCalled = True

        else:
            self.numCandles = self.numCandles + 1


    def update(self, time, open, close, min, max):
        if self.first == 0:
            self.first = time

        self.calcEMA(close)

        #self.takeProfitStrat(close)
        self.crossingEMAStrat(close)
        #self.fourCandleStratReversed(min, max)
        #self.combinedStratReversed(min,max)
        #self.combinedStrat(min, max)

        if self.numCandles < 250:
            self.numCandles = self.numCandles + 1

        self.elapsedTime = (time - self.first)/60000    #as it is in miliseconds
        self.totalCandles += 1
