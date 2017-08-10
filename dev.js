let WebSocketServer = require('ws').Server,
  wss = new WebSocketServer({port: 7000});
let ws = null;
wss.on('connection', function(connection) {
  ws = connection;
});
