from Clay import Clay
from datetime import datetime
import urllib2
import re
import time
import DatabaseLog

clay = Clay(300, "ethusd", "1h", 7, 20)

#decide which way the emas are oriented
if clay.positionType == "None":
    if (clay.ema1 - clay.ema2) > 0:
        clay.positionType = "Long"
        inp = raw_input("Do you want to continue from long pos? (y/n)")
        if inp == "n":
            clay.positionType = "Short"
            clay.writeToLog("Resuming from short position")
        else:
            clay.writeToLog("Resuming from long position")
    else:
        clay.positionType = "Short"
        inp = raw_input("Do you want to continue from short pos? (y/n)")
        if inp == "n":
            clay.positionType = "Long"
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
                errcode, dec = DatabaseLog.write_ClayLog(datetime.now(), data[1][2], clay.ema1 , clay.ema2)
                clay.writeToLog("Error code: " +str(errcode) + ", Description: " + str(dec))
                break
            else:
                time.sleep(5)

        except urllib2.HTTPError as err:
            clay.writeToLog("HTTP Error: Error with reading initial candles")
        except urllib2.URLError as err:
            clay.reset()
            break
