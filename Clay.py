#Author  : Ryan Pyrc
#Purpose : Contains the Clay bot which trades any coin using a crossing ema strategy

from datetime import datetime
import FinexAPI
import json
import time
import urllib2
import re


def makeJSONReadable(result):
    newResult = ""
    i = 0
    while i < len(result):
        if result[i] == chr(39):
            if result[i-1] == "u" and (result[i-2] == " " or i == 2):
                newResult = newResult[:-1]
            newResult += chr(34)
        elif result[i] != " ":
            newResult += result[i]
        i += 1

    return newResult

class Clay:
    #initalise variables
    def __init__(self, tradeableAmount, coinCode, timeFrame, ema1, ema2):
        self.tradeableAmount = tradeableAmount      #The amount in $ you want the bot to trade with
        self.coinCode = coinCode                    #The code of the coin being traded eg BTCUSD etc
        self.timeFrame = timeFrame                  #the timeframe eg 1h, 15m etc
        self.emaNum1 = ema1                         #1st ema days
        self.emaNum2= ema2                          #2nd ema days
        self.ema1 = 0                               #1st ema
        self.ema2 = 0                               #2nd ema
        self.numCandles = 0                         #num of candles that have been loaded in
        self.positionType = "None"                  #The position type - Long, Short, None
        self.f = open("ClayLog.txt", 'a')
        self.latestTime = 0
        self.writeToLog("Starting bot...")
        self.getPosition()
        self.catchUp()

    #resets the bot completely cand catches it back up
    def reset(self):
        self.ema1 = 0
        self.ema2 = 0
        self.numCandles = 0
        self.positionType = "None"
        self.latestTime = 0
        self.writeToLog("Restarting bot...")
        self.getPosition()
        self.catchUp()

    #catches the bot up with the last 500 candles
    def catchUp(self):
        regex = re.compile(r"\[([0-9]+,(?:[0-9]+\.?[0-9]+,?){5})]") #Regex for [[MTS,OPEN,CLOSE,HIGH,LOW,VOLUME],...]
        url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=500'.format(x="1h", y="tETHUSD",)

        while True:
            try:
                response = urllib2.urlopen(url)
                html = response.read()
                data = [item.split(",") for item in regex.findall(html)]
                self.latestTime = data[0][0]

                for entry in reversed(data[1:]):
                        self.calcEMA(float(entry[2]))
                        if self.numCandles < 100:
                            self.numCandles += 1

                print "%.2f, %.2f" % (self.ema1, self.ema2)
                break

            except urllib2.HTTPError as err:
                self.writeToLog("HTTP Error: Error with reading initial candles")
                time.sleep(5)
            except urllib2.URLError as err:
                self.writeToLog("URL Error: Cant reach the url")
                time.sleep(5)


    def writeToLog(self, string):
        self.f.write(str(datetime.now())+": " +str(string)+"\n")
        self.f.close()
        self.f = open("ClayLog.txt", 'a')

    #this function gets the current position and sets in
    def getPosition(self):

        try:
            pos = makeJSONReadable(str(FinexAPI.active_positions()[0]))
            self.writeToLog(pos)
            pos = json.loads(pos)
            print pos['amount']
            if float(pos['amount']) > 0.0000001:
                self.positionType = "Long"
            elif float(pos['amount']) < -0.0000001:
                self.positionType = "Short"
        except:
            None

    #this function will close all positions that are currently active on bitfinex
    def closeAllPositions(self):
        #Get current open positions
        self.writeToLog("Closing all positions...")
        openPositions = FinexAPI.active_positions()
        self.writeToLog(openPositions)

        for pos in openPositions:
            id = json.loads(makeJSONReadable(str(pos)))['id']
            self.writeToLog(FinexAPI.close_position(id))

        self.writeToLog("All positions closed.")

    def openPositionMarket(self, type, price):
        amount = (self.tradeableAmount/price)*0.995  #<--- gives a 0.5% buffer in case of price difference

        self.writeToLog(FinexAPI.place_order(str(amount), "500", type, "market", symbol = self.coinCode))
        self.writeToLog("Opened position of " + str(amount) + " at approx " + str(price))

    #This function calculates the ema
    #continually feed close values into this to catch up to current values
    def calcEMA(self, close):
        self.ema1 = (close-self.ema1)*2/(float(self.emaNum1)+1) + self.ema1
        self.ema2 = (close-self.ema2)*2/(float(self.emaNum2)+1) + self.ema2

    def crossingEMAStrat(self, close):
        if self.numCandles < 100:
            self.writeToLog("Error: not enough candles for reliable EMA values, skiping this candle... ")
        else:
            #+ve means faster is above the slower
            diff = self.ema1 - self.ema2
            delta = 0.004*close  #how far the emas need to be after crossing before chaging position
                        #can be a flat value or a % - 50 flat works well for btc

            #If you are currently in a short position and the ema's have now crossed,
            #close your position and open a long position
            if self.positionType == "Short" and diff >= delta:
                self.closeAllPositions()
                self.openPositionMarket("buy", close)

                self.positionType = "Long"

            #If you are currently in a long position and the ema's have now crossed,
            #close your position and open a short position
            elif self.positionType == "Long" and diff <= -delta:
                self.closeAllPositions()
                self.openPositionMarket("sell", close)

                self.positionType = "Short"


    def update(self, close,):
        self.calcEMA(close)
        self.crossingEMAStrat(close)

        if self.numCandles < 100:
            self.numCandles += 1
