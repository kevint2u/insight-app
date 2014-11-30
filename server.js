// Initialize express and server
var path = require('path')
var express = require('express')
var app = express()
  , server = require('http').createServer(app);

// Access server through port 80
server.listen(80);

// Set '/public' as the static folder. Any files there will be directly sent to the viewer
//app.use(express.static(__dirname + '/public'));
app.use(express.static(path.join(__dirname, 'public')));

// Set index.html as the base file
app.get('/', function (req, res) {
  res.sendfile(__dirname + '/index.html');
});


// Link socket.io to the previously created server
var io = require('socket.io').listen(server);

// When someone has connected to me...
io.sockets.on('connection', function (socket) {
  // Send out a message (only to the one who connected)
  socket.emit('server connected', { data: 'Connected' });

	var five = require("johnny-five"), button1, button2, led1, led2;
	five.Board().on("ready", function() {
	  button1 = new five.Button(2);

	  button2 = new five.Button(3);

	  led1 = new five.Led(13);
	  led2 = new five.Led(12);

	  button1.on("down", function(value){
	    led2.on();
	    led1.off();
	    console.log('button1');
	    socket.emit('server command', { command: 'button1' });
	  });

	  button2.on("down", function(){
	    led2.off();
	    led1.on();
	    console.log("button2");
	    socket.emit('server command', { command: 'button2' });
	  });

	});


});

