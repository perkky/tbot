class Position:
    #bos - buy or sell
    #initial price
    #amount
    def __init__(self, bos, price, amount):
        self.bos = bos
        self.price = price
        self.amount = amount

    def getProfit(self, price):
        profit = (price - self.price) *amount
        if self.bos == "Sell":
            profit = -profit

        return profit

class LastFour:
    #num is number of candles (should be 4 after the first 4 are added)
    #max is a list of the latest 4 maxs
    #min is a list of the latest 4 mins
    def __init__(self):
        self.num = 0
        self.max = []
        self.min = []

    def add(self, min, max):
        if not num == 4:
            self.max[self.num] = max
            self.min[self.num] = min
            self.num += 1
        else:
            'ripple them down'
            'then add it to the end'
            self.max[0] = self.max[1]
            self.min[0] = self.min[1]
            self.max[1] = self.max[2]
            self.min[1] = self.min[2]
            self.max[2] = self.max[3]
            self.min[2] = self.min[3]
            self.max[3] = max
            self.min[3] = min

    def getMax(self):
        return max(self.max)

    def getMin(self):
        return min(self.min)

    def getNum(self):
        return self.num

class Tbot:
    #initalise these variables
    #float max[] - last 4
    def __init__(self):
        self.lastFour = LastFour()
        self.bos = ""
        self.amount = 10000
        self.pos = Position("Buy", 100, 0)

    def update(self, min, max):
        if lastFour.getNum() == 4:
            if self.pos.bos == "Buy":
                #if a new low is set from last four candles, close long and start a short
                if min < lastFour.getMin():
                    self.amount += self.pos.getProfit(lastFour.getMin()-1)
                    self.pos = Position("Sell",lastFour.getMin()-1, self.amount/(lastFour.getMin()-1))
            elif self.pos.bos == "Sell":
                #else if a new high is set, close shorts and open a long
                if max > lastFour.getMax():
                    self.amount += self.pos.getProfit(lastFour.getMin()+1)
                    self.pos = Position("Sell",lastFour.getMin()+1, self.amount/(lastFour.getMin()+1))

        self.lastFour.add(min, max)
