from Clay import Clay
from datetime import datetime
import urllib2
import re
import time

clay = Clay(500, "ethusd", "1h", 7, 20)

#catch the bot up with the past 105 candles
regex = re.compile(r"\[([0-9]+,(?:[0-9]+\.?[0-9]+,?){5})]") #Regex for [[MTS,OPEN,CLOSE,HIGH,LOW,VOLUME],...]
url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=105'.format(x="1h", y="tETHUSD",)
latestTime= 0
try:
    response = urllib2.urlopen(url)
    html = response.read()
    data = [item.split(",") for item in regex.findall(html)]
    latestTime = data[0][0]

    for entry in reversed(data[1:]):
            clay.calcEMA(float(entry[2]))

    print "%.2f, %.2f" % (clay.ema1, clay.ema2)

except urllib2.HTTPError as err:
    clay.writeToLog("HTTP Error: Error with reading initial candles")

#decide which way the emas are oriented
if (clay.ema1 - clay.ema2) > 0:
    clay.positionType = "Buy"
    inp = raw_input("Do you want to continue from long pos? (y/n)")
    if inp == "n":
        clay.positionType = "Sell"
        clay.writeToLog("Resuming from short position")
    else:
        clay.writeToLog("Resuming from long position")
else:
    clay.positionType = "Sell"
    inp = input("Do you want to continue from short pos? (y/n)")
    if inp == "n":
        clay.positionType = "Buy"
        clay.writeToLog("Resuming from long position")
    else:
        clay.writeToLog("Resuming from short position")

#run the while loop
url = 'https://api.bitfinex.com/v2/candles/trade:{x}:{y}/hist?limit=2'.format(x="1h", y="tETHUSD",)
while True:
    #sleep two seconds to make sure you are into the next minute
    time.sleep(2)
    seconds = datetime.now().minute*60 + datetime.now().second
    time.sleep(3604-seconds)

    while True:
        try:
            response = urllib2.urlopen(url)
            html = response.read()
            data = [item.split(",") for item in regex.findall(html)]

            if latestTime == data[1][0]:
                latestTime = data[0][0]

                clay.writeToLog("Adding close of "+data[1][2]+" to the bot.")
                clay.update(float(data[1][2]))

                clay.writeToLog(str(clay.ema1) + str(clay.ema2))
                break
            else:
                time.sleep(5)

        except urllib2.HTTPError as err:
            clay.writeToLog("HTTP Error: Error with reading initial candles")
