from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
from gpiozero import Button
from signal import pause
import json
import serial

green = Button(3)
red   = Button(2)
bio = Button(4)
regio = Button(5)
foo   = Button(6)
bar   = Button(7)
#s = serial.Serial("/dev/ttyUSB0", baudrate=9600, timeout=0.1)

class SimpleEcho(WebSocket):
    def handleMessage(self):
        # echo message back to client
        self.sendMessage(self.data)

    def handleConnected(self):
        print(self.address, 'connected', end=" ")
        green.when_pressed = lambda: self.sendMessage(json.dumps({"type": "rightButtonClick"}))
        red.when_pressed   = lambda: self.sendMessage(json.dumps({"type": "leftButtonClick"}))
        bio.when_pressed   = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "bio", 
                "state": True
                }
            }))
        bio.when_released   = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "bio", 
                "state": False
                }
            }));
        regio.when_pressed   = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "regio", 
                "state": True
                }
            }))
        foo.when_pressed   = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "foo", 
                "state": True
                }
            }))
        bar.when_pressed   = lambda: self.sendMessage(json.dumps({
            "type": "prioritySwitch", 
            "params": {
                "priority": "bar", 
                "state": True
                }
            }))
        print('Success')

    def handleClose(self):
        print(self.address, 'closed')

server = SimpleWebSocketServer('', 7000, SimpleEcho)

print("Init Done")

while True:
    server.serveonce()
#    if s.inWaiting():
#        server.sendMessage(json.dumps({
#            "type": "rfidRead", 
#            "params": {
#                "id": int(s.readall()[1:-3], 16)
#                }
#            }))

#{"type": "rfidRead", "params": {"id": %i}}
#{"type": "rightButtonClick"}
#{"type": "leftButtonClick"}
#{"type": "prioritySwitch", "params": {"priority": "regional", "state": True}}
