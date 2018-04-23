from websocket import create_connection
from tradingBot import Position
import json
import base64
import hashlib
import hmac
import os
import time
import FinexAPI

#***********************depriciated***************************
#used finexAPI instead


class BFXConnection:
    def _nonce(self):
        return str(int(round(time.time()*10000)))
    def _authPayload(self):
        return "AUTH" + str(self._nonce())
    def _authSig(self, secret):
        return hmac.new(secret, msg=self._authPayload(),digestmod=hashlib.sha384).hexdigest()
    def __init__(self, url, key, secret):
        self.on = True
        self.positions = [] #list to hold the current positions
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

    #not anything, delete l8r
    def getPositions(self):
        #nothing, get rid when finished
        msg = json.dumps({ 'event':'subscribe', 'channel': "ticker", 'pair': 'BTCUSD'})

        self.ws.send(msg)

    def closeCurrentPosition(self):
        for pos in self.positions:
            msg = str([0,'on',None,json.dumps({"cid": 12345, "type": "LIMIT", "symbol": "tBTCUSD", "amount": "0.1", "price": "8000"})])
            self.ws.send(msg)

    #internally updates the positions
    def updatePosition(self, coin, status, amount, price):
        #if active, check if the order exists and only add if it does not


        if status == 'ACTIVE':
            exists = False
            for pos in self.positions:
                if pos.price == price and pos.amount == amount:
                    exists = True
            if exists == False:
                self.positions.append(Position(price, amount))
        elif status == 'CLOSED':
            for pos in self.positions:
                if pos.price == price and pos.amount == amount:
                    self.positions.remove(pos)

        print "Positions are: "
        for pos in self.positions:
            print "%.2f, %.2f" %(pos.getAmount(), pos.getPrice())

    def getResponse(self):
        #waits for the response and then updates the needed fields
        #codes are in the codes.txt file
        response = self.ws.recv()
        jsonData = json.loads(response)

        print response

        #checks that the server is connected
        #need to make sure it closes all positions before it shutsoff
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
                print "Last Message was wrong"
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

        try:
            if jsonData['event'] == "error":
                print "Error: " + jsonData['msg']
        except TypeError as err:
            #do nothing
            pass
        except KeyError as err:
            #do nothing
            pass

        #check for update from server
        try:
            if jsonData[1] =="ps":
                if len(jsonData[2][0]) > 0:
                    self.updatePosition(jsonData[2][0][0], jsonData[2][0][1], jsonData[2][0][2], jsonData[2][0][3])
            elif jsonData[1] =="ws":
                print jsonData[2]
            elif jsonData[1] =="pu":
                self.updatePosition(jsonData[2][0], jsonData[2][1], jsonData[2][2], jsonData[2][3])
            elif jsonData[1] =="pc":
                self.updatePosition(jsonData[2][0], jsonData[2][1], jsonData[2][2], jsonData[2][3])
        except KeyError as err:
            #do nothing
            pass


FinexAPI.place_order("0.01", "500.0", "buy", "limit")

"""con = BFXConnection("wss://api.bitfinex.com/ws/2", "ykVwqMBQOZJXwxfI0Qb4cGJVEa446ra83dWzJmsCt4d", "wm9oagLDmutvDlu2Ka9cWPtW7k5g8NLzv146LS28VgI")
#con.getPositions()

while True:

    num = input("Enter input: ")
    if num == 1:
        con.getResponse()
    if num == 2:
        con.closeCurrentPosition()"""
