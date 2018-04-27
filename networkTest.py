import FinexAPI
import json
from datetime import datetime
import time

print FinexAPI.balances()
print str(datetime.now().minute*60 + datetime.now().second)
print str(datetime.now().second)

while True:
    time.sleep(2)
    seconds = datetime.now().second
    time.sleep(60-seconds)
    print "poo"

"""
result = str(FinexAPI.active_positions()[0])

result = json.loads(makeJSONReadable(result))

print result['id']
new = FinexAPI.close_position(result['id'])
new = json.loads(makeJSONReadable(str(new)))
"""
