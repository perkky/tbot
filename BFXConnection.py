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
        self.on = True

        self.ws = create_connection(url)

        authNonce = self._nonce()
        authPayload = self._authPayload()
        authSig = self._authSig(secret)

        msg = json.dumps( {"apiKey": key, "authSig": authSig, "authNonce": authNonce, "authPayload": authPayload, 'event': 'auth'}, separators=(',',':') )
        self.ws.send(msg)

        result = self.ws.recv()
        jsonData = json.loads(result)

        while not jsonData['event'] == "auth":
            result = self.ws.recv()
            jsonData = json.loads(result)

        if jsonData['status'] == "OK":
            print result
            print "Connection successful!"
        else:
            print "Could not connect."

    def getPositions(self):
        #nothing, get rid when finished
        #msg = json.dumps({ 'event':'subscribe', 'channel': "Candles", 'key': 'trade:15m:tBTCUSD'})
        msg = json.dumps({ 'event':'subscribe', 'channel': "positions"})
        self.ws.send(msg)

    def getResponse(self):
        #waits for the response and then updates the needed fields
        #codes are in the codes.txt file
        response = self.ws.recv()
        jsonData = json.loads(response)

        #checks that the server is connected\
        #make sure it closes all positions before it shutsoff
        try:
            if jsonData['status'] == "FAIL":
                print "Connection has fail"
                print "Bot shutting off..."
                self.on = False
            #checks the error codes
        except TypeError as err:
            #do nothing
            pass
        except KeyError as err:
            #do nothing
            pass

        #check for error codes
        try:
            if jsonData['code'] == 10300:
                print "Message was wrong"
            elif jsonData['code'] == 10000:
                print "Unkown Error"
                print "Bot shutting off..."
                self.on = false
            #checks the error codes
        except TypeError as err:
            #do nothing
            pass
        except KeyError as err:
            #do nothing
            pass

        #check for update from server
        try:
            if jsonData[1] =="ps":
                print jsonData[2]
            elif jsonData[1] =="ws":
                print jsonData[2]
        except KeyError as err:
            #do nothing
            pass


con.getPositions()
while True:
    con.getResponse()
