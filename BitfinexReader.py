#Author  : Nhan Dao
#Purpose : Extract HTML from "Bitfinex' Trade Candle" cUrl, format the data and output to a specify file.
#          Multiple html request may be sent until enough data is extracted.

#candles are saved in this format
#time, open, close, high, low, volume
import urllib2
import re
import time

def fetchData(timeFrame, coinCode, outputFile, targetLength=1000, limit=1000, end=""):

    f = open(outputFile, 'a')
    regex = re.compile(r"\[([0-9]+,(?:[0-9]+\.?[0-9]+,?){5})]") #Regex for [[MTS,OPEN,CLOSE,HIGH,LOW,VOLUME],...]
    numEntries = 0
    urlPost = "&end=" + str(end)
    tooManyRequest = False

    while numEntries < targetLength:
        url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=1000{z}'.format(x=timeFrame, y=coinCode, z=urlPost)

        try:
            response = urllib2.urlopen(url)
            html = response.read()
            data = [item.split(",") for item in regex.findall(html)]
            urlPost = "&end={MTS}".format(MTS=data.pop(len(data) - 1)[0]) #Last entry is deleted, otherwise it will be repeated.

            for entry in data:
                    f.write(','.join(entry) + "\n")

            numEntries += len(data)
            print "Added " + str(len(data)) + " entries, total: " + str(numEntries)
            tooManyRequest = False

        except urllib2.HTTPError as err:
            if err.reason == "Too Many Requests":
                if tooManyRequest == False:
                    tooManyRequest = True
                    print err.reason
                    print "Retrying until successful..."
            else:
                raise

    f.close()
    print "Finished with " + str(numEntries) + " number of entries"

fetchData('1h','tBTCUSD','Data/BTC/1hr/2000 21-4.csv',targetLength=1989)
