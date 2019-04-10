// require("../socket.js");

var idCapteur1 = 0;
var idCapteur2 = 0;

$(document).ready(function(){

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/getNewDataSensor');

    //receive details from server
    socket.on('getNewData', function(msg) {
        console.log("Received data");
        //maintain a list of ten numbers
        if(msg.id_sensor != idCapteur1 && msg.id_sensor != null ){
            //alert(msg.id_sensor +"  != " + idCapteur1)
            idCapteur1 = msg.id_sensor;
            document.getElementById("nomSensor").innerHTML=msg.name;
            document.getElementById("idSensor").innerHTML=msg.ID;
            document.getElementById("macAdresse").innerHTML=msg.Mac;
            document.getElementById("batterie").innerHTML=msg.battery;
            document.getElementById("humidite").innerHTML=msg.humidity;
            document.getElementById("temperature").innerHTML=msg.temperature;
        }

         if(msg.id_sensor2 != idCapteur2 && msg.id_sensor2 != null){
            //alert(msg.id_sensor2 +"  != " + idCapteur2)
            idCapteur2 = msg.id_sensor2;
            document.getElementById("nomSensor2").innerHTML=msg.name2;
            document.getElementById("idSensor2").innerHTML=msg.ID2;
            document.getElementById("macAdresse2").innerHTML=msg.Mac2;
            document.getElementById("batterie2").innerHTML=msg.battery2;
            document.getElementById("humidite2").innerHTML=msg.humidity2;
            document.getElementById("temperature2").innerHTML=msg.temperature2;
        }
    });

});