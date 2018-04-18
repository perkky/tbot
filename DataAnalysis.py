import csv

class Candle:
    def __init__(self, time, open, close, min, max, volume):
        self.setTime(time)
        self.setOpen(open)
        self.setClose(close)
        self.setMin(min)
        self.setMax(max)
        self.setVol(volume)

    def setTime(self, time):
        if time >= 0:
            self.time = time
        else:
            print "Error setting time for candle"
    def setOpen(self, open):
        if open >= 0:
            self.open = open
        else:
            print "Error setting open for candle"
    def setClose(self, close):
        if close >= 0:
            self.close = close
        else:
            print "Error setting close for candle"
    def setMin(self, min):
        if min >= 0:
            self.min = min
        else:
            print "Error setting min for candle"
    def setMax(self, max):
        if max >= 0:
            self.max = max
        else:
            print "Error setting max for candle"
    def setVol(self, volume):
        if volume >= 0:
            self.volume = volume
        else:
            print "Error setting volume for candle"

    def getTime(self):
        return self.time
    def getOpen(self):
        return self.open
    def getClose(self):
        return self.close
    def getMin(self):
        return self.min
    def getMax(self):
        return self.max
    def getVol(self):
        return self.volume

class Data:
    #Initialise the class with:
    #time frame in minutes
    #an empty data list which will hold all the candles
    def __init__(self, timeFrame):
        self.timeFrame = timeFrame
        self.data = []

    def addCandle(self, time, open, close, min, max, volume):
        index = 0
        for candle in self.data:
            if candle.getTime() > time:
                break
            elif candle.getTime() == time:
                index =-1
                break
            else:
                index += 1

        if index >= 0:
            self.data.insert(index, Candle(time,open,close,min,max,volume))
        else:
            print "Candle time already exists"

    def calcEMA(self, days):
        multiplier = 2/(float(days)+1)
        ema = 0.0

        for candle in self.data:
            ema = (candle.getClose()-ema)*multiplier + ema

        return ema

data = Data("15m")
with open('Data/8 Bitfinex 15m data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter='\n')

    for row in reader:
        data.addCandle(int(row[0].split(',')[0]), float(row[0].split(',')[1]), float(row[0].split(',')[2]), float(row[0].split(',')[3]), float(row[0].split(',')[4]), float(row[0].split(',')[5]))

print str(data.calcEMA(55))
