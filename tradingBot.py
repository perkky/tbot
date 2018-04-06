class lastFour:
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

class tbot:

    #initalise these variables
    #float max[] - last 4
    def __init__(self):
        self.yes = 10
