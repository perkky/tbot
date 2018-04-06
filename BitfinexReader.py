#Reads data from the bitfinex website and output it to a csv file
import urllib2
import re

def fetchData(timeFrame, coinCode, outputFile, targetLength):
    data = []
    length = 0

    while length < targetLength:
        urlPost = ""
        url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=1000{z}'.format(x=timeFrame, y=coinCode, z=urlPost)

        response = urllib2.urlopen(url)
        html = response.read()
        tmpData = re.findall(r'(\d{13}),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{3}.[0-9]+)|(?:\d{4})),?',html)
        urlPost = "&end={MTS}".format(MTS=str(tmpData.pop(len(tmpData)-1))[0])
        data.append(tmpData)

        length = length + len(tmpData)

    return data

def writeToFile(data):
    f = open(outputFile, 'a')
    for entry in data:
        for item in entry:
            f.write("{MTS},{OPEN},{CLOSE},{HIGH},{LOW},{VOLUME}\n".format(MTS=item[0],OPEN=item[1],CLOSE=item[2],HIGH=item[3],LOW=item[4],VOLUME=item[5]))


timeFrame = "15m"
coinCode = "tBTCUSD"
outputFile = "5 Bitfinex 15m data.txt"
targetLength = 1
writeToFile(fetchData(timeFrame, coinCode, outputFile, targetLength))
