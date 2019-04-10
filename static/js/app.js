// require("../socket.js");

var idCapteur1 = 0;
var idCapteur2 = 0;

document.addEventListener("DOMContentLoaded", function (event) {

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/getNewDataSensor');

    //receive details from server
    socket.on('getNewData', function (msg) {
        //maintain a list of ten numbers
        if (msg.id_sensor != idCapteur1 && msg.id_sensor != null) {

            idCapteur1 = msg.id_sensor;
            document.getElementById("sensor1").setAttribute("href", "/sensor/" + idCapteur1);
            document.getElementById("nomSensor").innerHTML = msg.name;
            document.getElementById("idSensor").innerHTML = msg.ID;
            document.getElementById("macAdresse").innerHTML = msg.Mac;
            document.getElementById("date").innerHTML = msg.date;

            if (msg.battery >= 90) {
                document.getElementById("batterie-full").removeAttribute("style");
                document.getElementById("batterie-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie-half").setAttribute("style", "display:none");
                document.getElementById("batterie-quarter").setAttribute("style", "display:none");
                document.getElementById("batterie-empty").setAttribute("style", "display:none");
            } else if (msg.battery >= 60 && msg.battery < 90) {
                document.getElementById("batterie-three-quarters").removeAttribute("style");
                document.getElementById("batterie-full").setAttribute("style", "display:none");
                document.getElementById("batterie-half").setAttribute("style", "display:none");
                document.getElementById("batterie-quarter").setAttribute("style", "display:none");
                document.getElementById("batterie-empty").setAttribute("style", "display:none");
            } else if (msg.battery >= 40 && msg.battery < 60) {
                document.getElementById("batterie-half").removeAttribute("style");
                document.getElementById("batterie-full").setAttribute("style", "display:none");
                document.getElementById("batterie-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie-quarter").setAttribute("style", "display:none");
                document.getElementById("batterie-empty").setAttribute("style", "display:none");
            } else if (msg.battery >= 10 && msg.battery < 40) {
                document.getElementById("batterie-quarter").removeAttribute("style");
                document.getElementById("batterie-full").setAttribute("style", "display:none");
                document.getElementById("batterie-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie-half").setAttribute("style", "display:none");
                document.getElementById("batterie-empty").setAttribute("style", "display:none");
            } else {
                document.getElementById("batterie-empty").removeAttribute("style");
                document.getElementById("batterie-full").setAttribute("style", "display:none");
                document.getElementById("batterie-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie-half").setAttribute("style", "display:none");
                document.getElementById("batterie-quarter").setAttribute("style", "display:none");
            }
            document.getElementById("batterie").innerHTML = msg.battery;
            document.getElementById("humidite").innerHTML = msg.humidity;
            document.getElementById("temperature").innerHTML = msg.temperature;
        }

        if (msg.id_sensor2 != idCapteur2 && msg.id_sensor2 != null) {

            idCapteur2 = msg.id_sensor2;
            document.getElementById("sensor2").setAttribute("href", "/sensor/" + idCapteur2);
            document.getElementById("nomSensor2").innerHTML = msg.name2;
            document.getElementById("idSensor2").innerHTML = msg.ID2;
            document.getElementById("macAdresse2").innerHTML = msg.Mac2;
            document.getElementById("date2").innerHTML = msg.date2;

            if (msg.battery2 >= 90) {
                document.getElementById("batterie2-full").removeAttribute("style");
                document.getElementById("batterie2-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie2-half").setAttribute("style", "display:none");
                document.getElementById("batterie2-quarter").setAttribute("style", "display:none");
                document.getElementById("batterie2-empty").setAttribute("style", "display:none");
            } else if (msg.battery2 >= 60 && msg.battery2 < 90) {
                document.getElementById("batterie2-three-quarters").removeAttribute("style");
                document.getElementById("batterie2-full").setAttribute("style", "display:none");
                document.getElementById("batterie2-half").setAttribute("style", "display:none");
                document.getElementById("batterie2-quarter").setAttribute("style", "display:none");
                document.getElementById("batterie2-empty").setAttribute("style", "display:none");
            } else if (msg.battery2 >= 40 && msg.battery2 < 60) {
                document.getElementById("batterie2-half").removeAttribute("style");
                document.getElementById("batterie2-full").setAttribute("style", "display:none");
                document.getElementById("batterie2-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie2-quarter").setAttribute("style", "display:none");
                document.getElementById("batterie2-empty").setAttribute("style", "display:none");
            } else if (msg.battery2 >= 10 && msg.battery2 < 40) {
                document.getElementById("batterie2-quarter").removeAttribute("style");
                document.getElementById("batterie2-full").setAttribute("style", "display:none");
                document.getElementById("batterie2-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie2-half").setAttribute("style", "display:none");
                document.getElementById("batterie2-empty").setAttribute("style", "display:none");
            } else {
                document.getElementById("batterie2-empty").removeAttribute("style");
                document.getElementById("batterie2-full").setAttribute("style", "display:none");
                document.getElementById("batterie2-three-quarters").setAttribute("style", "display:none");
                document.getElementById("batterie2-half").setAttribute("style", "display:none");
                document.getElementById("batterie2-quarter").setAttribute("style", "display:none");
            }
            document.getElementById("batterie2").innerHTML = msg.battery2;
            document.getElementById("humidite2").innerHTML = msg.humidity2;
            document.getElementById("temperature2").innerHTML = msg.temperature2;
        }
    });
});