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
    #initalise these variables
    #float max[] - last 4
    def __init__(self, num):
        self.candleHeap = CandleHeap(num)
        self.bos = ""
        self.amount = 10000
        self.pos = Position("Buy", 100, 0)
        self.totalTraded = 0

    def update(self, min, max):
        if self.candleHeap.getNum() == self.candleHeap.numCandles:
            if self.pos.bos == "Buy":
                #if a new low is set from last four candles, close long and start a short
                if min < self.candleHeap.getMin():
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()-1) - 0.001*self.amount
                    self.totalTraded += self.amount
                    print "closed for " + str(self.pos.getProfit(self.candleHeap.getMin()-1)) + " profit\nAmount: " + str(self.amount)
                    self.pos = Position("Sell", self.candleHeap.getMin()-1, self.amount/(self.candleHeap.getMin()-1))
            elif self.pos.bos == "Sell":
                #else if a new high is set, close shorts and open a long
                if max > self.candleHeap.getMax():
                    self.totalTraded += self.amount
                    self.amount += self.pos.getProfit(self.candleHeap.getMin()+1) - 0.001*self.amount
                    print "closed for " + str(self.pos.getProfit(self.candleHeap.getMin()+1)) + " profit\nAmount: " + str(self.amount)
                    self.pos = Position("Sell",self.candleHeap.getMin()+1, self.amount/(self.candleHeap.getMin()+1))

        self.candleHeap.add(min, max)
