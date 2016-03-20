$(document).ready(function(){
  namespace ='';

  var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

  // Below is the socket logic for each button
  // Would be much nicer to do something creative
  // on the server end as they are all so similar
  // but time is of the essence. Should
  // refactor later. 

  $('#txfrequp').click(function(){
    socket.emit('inc tx freq');
  });

  $('#txfreqdown').click(function(){
  	socket.emit('dec tx freq');
  });

  $('#rxfrequp').click(function(){
  	socket.emit('inc rx freq');
  });

  $('#rxfreqdown').click(function(){
  	socket.emit('dec rx freq');
  });

  $('#txgainup').click(function(){
  	socket.emit('inc tx gain');
  });

  $('#txgaindown').click(function(){
  	socket.emit('dec tx gain');
  });

  $('#rxgainup').click(function(){
  	socket.emit('inc rx gain');
  });

  $('#rxgaindown').click(function(){
  	socket.emit('dec rx gain');
  });

  // Now we listen to hear back from the
  // server and/or radio

  socket.on('confirm tx freq', function(msg){
    $('#txfreq').text(msg.txfreq);
  });

  socket.on('confirm rx freq', function(msg){
  	$('#rxfreq').text(msg.rxfreq);
  });

  socket.on('confirm tx gain', function(msg){
  	$('#txgain').text(msg.txgain);
  });

  socket.on('confirm rx gain', function(msg){
  	$('#rxgain').text(msg.rxgain);
  });

});