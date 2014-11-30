$(document).ready(function() {
  // Connect to the node.js server. Change the IP address to the actual node server location.
  var socket = io.connect('http://localhost');
  // When I've received 'server connected' message from the socket.io server...
  socket.on('server connected', function (data) {
    console.log("Server connected");
  });
  // When I've received 'server command' message from this connection...
  socket.on('server command', function (data) {
    console.log(data);
    var command = data.command;
    if(command == "button1"){
      console.log("button1 hit! ");
      $(".button-number").text("1 (RED)");
    }
    else if(command == "button2"){
      console.log("button2 hit!");
      $(".button-number").text("2 (YELLOW)");
    }
  });
});