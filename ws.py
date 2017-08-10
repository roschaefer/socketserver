from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from gpiozero import Button
from signal import pause
import json
import serial
import binascii

green = Button(3)
red   = Button(2)
regio = Button(4)
bio   = Button(5)
sugar = Button(6)
price = Button(7)
s = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.1)

class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected', end=" ")
        green.when_pressed = lambda: self.sendMessage(json.dumps({"type": "rightButtonClick"}))
        red.when_pressed   = lambda: self.sendMessage(json.dumps({"type": "leftButtonClick"}))
        regio.when_pressed = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "regional", 
                "state": True
                }
            }))
        regio.when_released = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "regional", 
                "state": False
                }
            }));
        bio.when_pressed = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "organic", 
                "state": True
                }
            }))
        bio.when_released = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "organic", 
                "state": False
                }
            }));
        sugar.when_pressed = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "sugar", 
                "state": True
                }
            }))
        sugar.when_released = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "sugar", 
                "state": False
                }
            }));
        price.when_pressed = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "price", 
                "state": True
                }
            }))
        price.when_released = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "price", 
                "state": False
                }
            }));
        print('Success')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 7000, SimpleEcho)

print("Init Done")

while True:
    server.serveonce()
    if len(server.connections) and s.inWaiting():
        rawdata = s.readall()[1:-3]
        data = binascii.unhexlify(rawdata)
        if data[0] ^ data[1] ^ data[2] ^ data[3] ^ data[4] ^ data[5] == 0:
            data = int(rawdata[:-2], 16)
            for con in server.connections.values():
                con.sendMessage(json.dumps({
                    "type": "rfidRead", 
                    "params": {
                        "id": data
                        }
                    }))
        else:
            print("Bad Tag")

#{"type": "rfidRead", "params": {"id": %i}}
#{"type": "rightButtonClick"}
#{"type": "leftButtonClick"}
#{"type": "prioritySwitch", "params": {"priority": "regional", "state": True}}
