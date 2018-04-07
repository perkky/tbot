#Author  : Nhan Dao
#Purpose : Extract HTML from "Bitfinex' Trade Candle" cUrl, format the data and output to a specify file.
#          Multiple html request may be sent until enough data is extracted.

import urllib2
import re
import time

def fetchData(timeFrame, coinCode, outputFile, targetLength):
    regex = re.compile(r"\[([0-9]+,(?:[0-9]+\.?[0-9]+,?){5})]") #Regex for [[MTS,OPEN,CLOSE,HIGH,LOW,VOLUME],...]
    data = []
    numEntries = 0
    urlPost = ""

    while numEntries < targetLength:
        url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=1000{z}'.format(x=timeFrame, y=coinCode, z=urlPost)

        try:
            response = urllib2.urlopen(url)
            html = response.read()
            rawData = regex.findall(html)
            tmpData = [item.split(",") for item in rawData]
            urlPost = "&end={MTS}".format(MTS=tmpData.pop(len(tmpData) - 1)[0]) #Last entry is deleted, otherwise it will be repeated.
            data.append(tmpData)
            numEntries += len(tmpData)

        except urllib2.HTTPError as err:
            print err
            print "Trying again in 60 seconds"
            time.sleep(60)

    print "Successfully fetch data, {x} number of entries.".format(x=numEntries)

    return data

def writeToFile(data, outputFile):
    f = open(outputFile, 'a')


timeFrame = "15m"
coinCode = "tBTCUSD"
outputFile = "5 Bitfinex 15m data.txt"
targetLength = 20000
writeToFile(fetchData(timeFrame, coinCode, outputFile, targetLength), outputFile)
