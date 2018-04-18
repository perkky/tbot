class Position:
    #bos - buy or sell
    #initial price
    #amount
    def __init__(self, bos, price, amount):
        self.bos = bos
        self.price = price
        self.amount = amount

    def getProfit(self, price):
        profit = (price - self.price) *self.amount
        if self.bos == "Sell":
            profit = -profit

        return profit

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

class Tbot:
    #initalise variables
    def __init__(self, num, ema1, ema2):
        self.candleHeap = CandleHeap(num)
        self.bos = ""                               #Buy or sell variable
        self.amount = 10000                         #Total ammount
        self.pos = Position("Buy", 100, 0)          #Current position
        self.totalTraded = 0                        #Total value traded
        self.emaNum1 = ema1                         #1st ema days
        self.emaNum2= ema2                          #2nd ema days
        self.ema1 = 0                               #1st ema
        self.ema2 = 0                               #2nd ema
        self.numCandles = 0                         #num candles that have been added - used for crossing ema
        self.first = 0                              #the first candles time
        self.elapsedTime = 0                        #time minutes of last candle - first candle
        self.totalCandles = 0                       #total amount of candles

    def fourCandleStrat(self, min, max):
        if self.candleHeap.getNum() == self.candleHeap.numCandles:
            if self.pos.bos == "Buy":
                #if a new low is set from last four candles, close long and start a short
                if min < self.candleHeap.getMin():
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()-1) - 0.0015*self.amount
                    self.totalTraded += self.amount
                    print "closed for " + str(self.pos.getProfit(self.candleHeap.getMin()-1)) + " profit\nAmount: " + str(self.amount)
                    self.pos = Position("Sell", self.candleHeap.getMin()-1, self.amount/(self.candleHeap.getMin()-1))
            elif self.pos.bos == "Sell":
                #else if a new high is set, close shorts and open a long
                if max > self.candleHeap.getMax():
                    self.totalTraded += self.amount
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()+1) - 0.0015*self.amount
                    print "closed for " + str(self.pos.getProfit(self.candleHeap.getMin()+1)) + " profit\nAmount: " + str(self.amount)
                    self.pos = Position("Sell",self.candleHeap.getMin()+1, self.amount/(self.candleHeap.getMin()+1))

        self.candleHeap.add(min, max)


    def crossingEMAStrat(self, close):
        #set to either self.amount for compounded or a flat number
        tradingAmount = 10000

        self.ema1 = (close-self.ema1)*2/(float(self.emaNum1)+1) + self.ema1
        self.ema2 = (close-self.ema2)*2/(float(self.emaNum2)+1) + self.ema2
        change = self.ema1 - self.ema2
        delta = 0.004*close  #how far the emas need to be after crossing before chaging position
                    #can be a flat value or a % - 50 flat works well for btc
        fees = 0.002*tradingAmount#*0
        #makes sure sufficient data has been provided to allow for proper ema base calculation
        if self.numCandles > 100:
            diff = self.ema1 - self.ema2 #faster one take slower one - +ve is bullish, -ve is bearish

            if self.pos.bos == "Sell" and change >= delta:
                #closes the position, adds the profit to the amount and then opens up an opposite position
                self.amount += self.pos.getProfit(close) - fees
                self.totalTraded += tradingAmount
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)
                self.pos = Position("Buy", close, tradingAmount/(close))
            elif self.pos.bos == "Buy" and change <= -delta:
                #closes the position, adds the profit to the amount and then opens up an opposite position
                self.amount += self.pos.getProfit(close) - fees
                self.totalTraded += tradingAmount
                #print "closed for " + str(self.pos.getProfit(close)) + " profit\nAmount: " + str(self.amount)
                self.pos = Position("Sell", close, tradingAmount/(close))
        else:
            self.numCandles = self.numCandles + 1

    def update(self, time, open, close, min, max):
        if self.first == 0:
            self.first = time

        self.crossingEMAStrat(close)

        self.elapsedTime = (time - self.first)/60000    #as it is in miliseconds
        self.totalCandles += 1
