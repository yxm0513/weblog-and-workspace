var express = require('express');
var http    = require('http');
var path    = require('path');
var _       = require('underscore');
var child   = require('child_process');
var s       = require('socket.io');
var carrier = require('carrier');


var app = express();

app.configure(function(){
  app.set('port', process.env.PORT || 8080);
  app.set('views', __dirname + '/views');
  app.set('view engine', 'jade');
  app.use(express.logger('dev'));
  app.use(express.bodyParser());
  app.use(express.methodOverride());
  app.use(app.router);  
  app.use(express.static(path.join(__dirname, 'public')));
});

app.configure('development', function(){
  app.use(express.errorHandler());
});

app.get('/', function(req, res) {
	res.render('log');
});
app.get('/pxe', function(req, res) {
	res.render('pxe');
});

app.get('/about', function(req, res) {
	res.render('about');
});

var http = http.createServer(app).listen(app.get('port'), function(){
  console.log("Express server listening on port " + app.get('port'));
});

io = s.listen(http);
var socket;
io.sockets.on('connection', function (socket) {
  socket.on('disconnect', function() {
    socket = null;
  });
  socket.on('log', function (data) {
     console.log("Hostname: " + data.hostname);
     console.log("AR: " + data.ar);
     com = child.spawn('/home/simon/public/weblog1/log.pl',[data.hostname, data.ar]);
     com.stdout.on('data', function(data){
         if(socket){
             var lines = data.toString().split(/\r?\n/);
             for (var l = 0; l < lines.length; l++){
                 if(lines[l]){
                     socket.emit('output', lines[l]);
                 }
             }
         }
     });
     com.on('exit', function(code, signal){
         if(socket){
             socket.emit('end', code);
         } else{
             console.log("socket has closed.");
         }
     });
  });
  socket.on('pxe', function (data) {
     console.log("Hostname: " + data.hostname);
     com = child.spawn('/home/simon/public/weblog1/pxe.pl',[data.hostname]);
     com.stdout.on('data', function(data){
         if(socket){
             var lines = data.toString().split(/\r?\n/);
             for (var l = 0; l < lines.length; l++){
                 if(lines[l]){
                     socket.emit('output', lines[l]);
                 }
             }
         }
     });
     com.on('exit', function(code, signal){
         if(socket){
             socket.emit('end', code);
         } else{
             console.log("socket has closed.");
         }
     });
  });

});
