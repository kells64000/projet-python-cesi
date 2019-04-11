var idDataSensor1 = 0;
var idDataSensor2 = 0;
var idDataSensor3 = 0;

document.addEventListener("DOMContentLoaded", function (event) {

    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/getNewDataSensor');

    //receive details from server
    socket.on('getNewData', function (msg) {
        //maintain a list of ten numbers
        if (msg.id_data_sensor !== idDataSensor1 && msg.id_sensor !== null) {

            idDataSensor1 = msg.id_data_sensor;
            document.getElementById("sensor1").setAttribute("href", "/sensor/" + msg.id_sensor);
            document.getElementById("nomSensor").innerHTML = msg.name;
            document.getElementById("idSensor").innerHTML = msg.ID;
            document.getElementById("macAdresse").innerHTML = msg.Mac;
            document.getElementById("date").innerHTML = msg.date;

            checkSignal(msg.signal, 1);
            checkBatterie(msg.battery, 1);
            document.getElementById("batterie").innerHTML = msg.battery;
            document.getElementById("humidite").innerHTML = msg.humidity;
            document.getElementById("temperature").innerHTML = msg.temperature;
        }

        if (msg.id_data_sensor2 !== idDataSensor2 && msg.id_sensor2 !== null) {

            idDataSensor2 = msg.id_data_sensor2;
            document.getElementById("sensor2").setAttribute("href", "/sensor/" + msg.id_sensor2);
            document.getElementById("nomSensor2").innerHTML = msg.name2;
            document.getElementById("idSensor2").innerHTML = msg.ID2;
            document.getElementById("macAdresse2").innerHTML = msg.Mac2;
            document.getElementById("date2").innerHTML = msg.date2;

            checkSignal(msg.signal2, 2);
            checkBatterie(msg.battery2, 2);
            document.getElementById("batterie2").innerHTML = msg.battery2;
            document.getElementById("humidite2").innerHTML = msg.humidity2;
            document.getElementById("temperature2").innerHTML = msg.temperature2;
        }

        if (msg.id_data_sensor3 !== idDataSensor3 && msg.id_sensor3 !== null) {

            idDataSensor3 = msg.id_data_sensor3;
            // document.getElementById("sensor3").setAttribute("href", "/sensor/3");
            document.getElementById("nomSensor3").innerHTML = msg.name3;
            document.getElementById("date3").innerHTML = msg.date3;

            checkSignal(msg.signal3, 3);
            document.getElementById("humidite3").innerHTML = msg.humidity3;
            document.getElementById("temperature3").innerHTML = msg.temperature3;
        }
    });

    function checkBatterie(battery, id) {

        let batteryName = "";

        if (id === 1) {
            batteryName = "batterie";
        } else {
            batteryName = "batterie2";
        }

        if (battery >= 90) {
                document.getElementById(batteryName + "-full").removeAttribute("style");
                document.getElementById(batteryName + "-three-quarters").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-half").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-quarter").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-empty").setAttribute("style", "display:none");
            } else if (battery >= 60 && battery < 90) {
                document.getElementById(batteryName + "-three-quarters").removeAttribute("style");
                document.getElementById(batteryName + "-full").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-half").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-quarter").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-empty").setAttribute("style", "display:none");
            } else if (battery >= 40 && battery < 60) {
                document.getElementById(batteryName + "-half").removeAttribute("style");
                document.getElementById(batteryName + "-full").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-three-quarters").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-quarter").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-empty").setAttribute("style", "display:none");
            } else if (battery >= 10 && battery < 40) {
                document.getElementById(batteryName + "-quarter").removeAttribute("style");
                document.getElementById(batteryName + "-full").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-three-quarters").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-half").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-empty").setAttribute("style", "display:none");
            } else {
                document.getElementById(batteryName + "-empty").removeAttribute("style");
                document.getElementById(batteryName + "-full").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-three-quarters").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-half").setAttribute("style", "display:none");
                document.getElementById(batteryName + "-quarter").setAttribute("style", "display:none");
            }
    }

    function checkSignal(signal, id) {

        let signalName = "";
        let signalText = "";

        if (id === 1) {
            signalName = "signal";
        } else if (id === 2) {
            signalName = "signal2";
        }
        else {
            signalName = "signal3";
        }

        let signalHtml = document.getElementById(signalName);

        if (signal === 0) {
            signalHtml .classList.remove('has-background-success');
            signalHtml .classList.add('has-background-danger');

            signalText = document.createTextNode(' Déconnecté');
            signalHtml.parentNode.insertBefore(signalText, signalHtml.nextSibling);

        } else {
            signalHtml.classList.remove('has-background-danger');
            signalHtml.classList.add('has-background-success');

            signalText = document.createTextNode(' Connecté');
            signalHtml.parentNode.insertBefore(signalText, signalHtml.nextSibling);
        }
    }
});