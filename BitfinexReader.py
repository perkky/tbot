#Author  : Nhan Dao
#Purpose : Extract HTML from "Bitfinex' Trade Candle" cUrl, format the data and output to a specify file.
#          Multiple html request may be sent until enough data is extracted.

import urllib2
import re
import time

def fetchData(timeFrame, coinCode, outputFile, targetLength=1000):

    f = open(outputFile, 'a')
    regex = re.compile(r"\[([0-9]+,(?:[0-9]+\.?[0-9]+,?){5})]") #Regex for [[MTS,OPEN,CLOSE,HIGH,LOW,VOLUME],...]
    numEntries = 0
    urlPost = ""

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

        except urllib2.HTTPError as err:
            print err
            print "Trying again in 60 seconds"
            time.sleep(60)

    f.close()
    print "Finished with " + str(numEntries) + " number of entries"
