var WebSocketServer = require('ws').Server,
    wss = new WebSocketServer({port: 7000});
let ws = null;
wss.on('connection', function(connection) {
    ws = connection;
});


var SerialPort = require('serialport');
var port = new SerialPort('/dev/ttyUSB0', {
  baudRate: 115200
});


port.on('data', function (data) {
  let id = data.toString();
  console.log('Data:', id);
  ws.send(JSON.stringify({type: 'rfidRead', params: {'id': id}}));
});

// Read data that is available but keep the stream from entering "flowing mode"
port.on('readable', function () {
  console.log('Readable:', port.read());
});
