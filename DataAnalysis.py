class Candle:
    def __init__(self, time, open, close, min, max, volume):
        setTime(time)
        setOpen(open)
        setClose(close)
        setMin(min)
        setMax(max)
        setVol(volume)

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

    def getTime(self, time):
        return self.time
    def getOpen(self, open):
        return self.open
    def getClose(self, close):
        return self.close
    def getMin(self, min):
        return self.min
    def getMax(self, max):
        return self.max
    def getVol(self, volume):
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
        for candle in self.Data:
            if candle.getTime() > time:
                break
            elif candle.getTime() == time:
                index =-1
                break
            else:
                index += 1

        if index >= 0:
            self.data.insert(Candle(time,open,close,min,max,volume), index)
        else:
            print "Candle time already exists"
