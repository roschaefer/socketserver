let argv = require('minimist')(process.argv.slice(2), {
  default: {
    serverPort: 7000,
    clientPort: 8000,
  }
});
let path = require('path');
let http = require('http');
let finalhandler = require('finalhandler');
let serveStatic = require('serve-static');

if (!argv.client) {
  console.log(`Usage: ${path.basename(__filename)} --client path/to/trolley/client/dist`);
  process.exit();
}




let serve = serveStatic(argv.client);

let server = http.createServer(function(req, res) {
  let done = finalhandler(req, res);
  serve(req, res, done);
});

server.listen(argv.clientPort);

let WebSocketServer = require('ws').Server,
  wss = new WebSocketServer({port: argv.serverPort});
let ws = null;
wss.on('connection', function(connection) {
  ws = connection;
});


let SerialPort = require('serialport');
let port = new SerialPort('/dev/ttyUSB0', {
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

