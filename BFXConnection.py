from websocket import create_connection
import json
import base64
import hashlib
import hmac
import os
import time

class BFXConnection:
    def _nonce(self):
        return str(int(round(time.time()*10000)))
    def _authPayload(self):
        return "AUTH" + str(self._nonce())
    def _authSig(self, secret):
        return hmac.new(secret, msg=self._authPayload(),digestmod=hashlib.sha384).hexdigest()
    def __init__(self, url, key, secret):
        self.ws = create_connection(url)

        authNonce = self._nonce()
        authPayload = self._authPayload()
        authSig = self._authSig(secret)

        msg = json.dumps( {"apiKey": key, "authSig": authSig, "authNonce": authNonce, "authPayload": authPayload, 'event': 'auth'}, separators=(',',':') )
        self.ws.send(msg)

        result = self.ws.recv()
        print "Recieved %s" % result
        result = self.ws.recv()
        print "Recieved %s" % result



con = BFXConnection("wss://api.bitfinex.com/ws/2", "ykVwqMBQOZJXwxfI0Qb4cGJVEa446ra83dWzJmsCt4d", "wm9oagLDmutvDlu2Ka9cWPtW7k5g8NLzv146LS28VgI")

"""
ws = create_connection("wss://api.bitfinex.com/ws/2")
msg = json.dumps({
  'event': 'subscribe',
  'channel': 'ticker',
  'symbol': 'tBTCUSD'
}, separators=(',',':'))
print msg
ws.send(msg)

result = ws.recv()
print "Recieved %s" % result
result = ws.recv()
print "Recieved %s" % result
result = ws.recv()
print "Recieved %s" % result"""
