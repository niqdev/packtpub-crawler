/*
  // setup project
  npm init
  npm install connect serve-static --save
  npm install

  // run dev
  node server.js
*/

var connect = require('connect');
var serveStatic = require('serve-static');

var PATH = __dirname + '/public';
var PORT = 8080;

connect().use(serveStatic(PATH)).listen(PORT, function() {
  console.log("listening on port " + PORT);
});
