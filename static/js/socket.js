
$(document).ready(function(){
    alert("test");
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');

    //receive details from server
    socket.on('getNewData', function(msg) {
        console.log("Received data");
        //maintain a list of ten numbers
        document.getElementById("nomSensor").innerHTML=msg.name;
        document.getElementById("idSensor").innerHTML=msg.ID;
        document.getElementById("macAdresse").innerHTML=msg.Mac;
        document.getElementById("batterie").innerHTML=msg.battery;
        document.getElementById("humidite").innerHTML=msg.humidity;
        document.getElementById("temperature").innerHTML=msg.temperature;
    });

});