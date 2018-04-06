#Reads data from the bitfinex website and output it to a csv file
import urllib2
import re

def fetchData(url):
    response = urllib2.urlopen(url)
    html = response.read() #Raw HTML data
    html = html[1:len(html) - 1]
    data = re.findall(r'\[(\d{13}),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{4}.[0-9]+)|(?:\d{4})),((?:\d{3}.[0-9]+)|(?:\d{4}))],?',html)
    data = list(data)

    return data


timeFrame = "15m"
coinCode = "tBTCUSD"
outputFile = "5 Bitfinex 15m data.txt"
targetDataSet = 5000

url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=1000'.format(x=timeFrame, y=coinCode)


f = open(outputFile, 'w')
response = urllib2.urlopen(url)
html = response.read() #Raw HTML data
html = html[1:len(html) - 1]
data = fetchData(url)
for entry in data:
    f.write(str(entry) + "\n")
