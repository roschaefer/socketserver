from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from gpiozero import Button
from signal import pause
import json
import serial
import binascii
from subprocess import Popen

green = Button(3)
red   = Button(2)
regio = Button(4)
bio   = Button(5)
sugar = Button(6)
price = Button(7)
s = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.1)
s.readall()

class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected')
        green.when_pressed = lambda: print("Green") or self.sendMessage(json.dumps({"type": "rightButtonClick"}))
        red.when_pressed   = lambda: print("Red") or self.sendMessage(json.dumps({"type": "leftButtonClick"}))
        regio.when_pressed = lambda: print("Regio Off") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "regional", 
                "state": False
                }
            }))
        regio.when_released = lambda: print("Regio On") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "regional", 
                "state": True
                }
            }));
        bio.when_pressed = lambda: print("Bio Off") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "organic", 
                "state": False
                }
            }))
        bio.when_released = lambda: print("Bio On") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "organic", 
                "state": True
                }
            }));
        sugar.when_pressed = lambda: print("Sugar Off") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "sugar", 
                "state": False
                }
            }))
        sugar.when_released = lambda: print("Sugar On") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "sugar", 
                "state": True
                }
            }));
        price.when_pressed = lambda: print("Price Off") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "price", 
                "state": False
                }
            }))
        price.when_released = lambda: print("Price On") or self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "price", 
                "state": True
                }
            }));
            
        #Init Status
        self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "regional", 
                "state": not regio.value
                }
            }));
        self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "organic", 
                "state": not bio.value
                }
            }));
        self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "sugar", 
                "state": not sugar.value
                }
            }));
        self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "price", 
                "state": not price.value
                }
            }));
        print('Success')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 7000, SimpleEcho)

print("Init Done")

while True:
    server.serveonce()
    if s.inWaiting():
        rawdata = s.readall()[1:-3]
        print(rawdata)
        data = binascii.unhexlify(rawdata)
        if data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] == 0:
            # data = int(rawdata[:-2], 16) #Without CRC
            data = int(rawdata[:], 16) #With CRC
            
            if rawdata == b"4C00B2F3E8E5" or rawdata == b"4C00B2F47F75":
                Popen(["killall", "chromium-browser"])
                print("Reset")
                Popen(["chromium-browser", 'http://localhost:8000/', "--start-fullscreen"], env={"DISPLAY": ":0"})
            elif len(server.connections):
                for con in server.connections.values():
                    con.sendMessage(json.dumps({
                        "type": "rfidRead", 
                        "params": {
                            "id": rawdata.decode("utf-8")
                            }
                        }))
                print(json.dumps({
                        "type": "rfidRead", 
                        "params": {
                            "id": rawdata.decode("utf-8")
                            }
                        }))
        else:
            print("Bad Tag")

#{"type": "rfidRead", "params": {"id": %i}}
#{"type": "rightButtonClick"}
#{"type": "leftButtonClick"}
#{"type": "prioritySwitch", "params": {"priority": "regional", "state": True}}
