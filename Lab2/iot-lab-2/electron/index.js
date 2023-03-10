document.onkeydown = updateKey;
document.onkeyup = resetKey;

var server_port = 65433;
var server_addr = "10.0.0.191";   // the IP address of your Raspberry PI

function client(sendData="garbage"){
    
    const net = require('net');
    var input = sendData

    const client = net.createConnection({ port: server_port, host: server_addr }, () => {
        // 'connect' listener.
        console.log('connected to server!');
        // send the message
        client.write(`${input}\r\n`);
        // client.write(encodeURIComponent(data))
    });
    
    // get the data from the server
    client.on('data', (data) => {
        data = decodeURIComponent(data)
        json_data = JSON.parse(data)
        document.getElementById("direction").innerHTML = json_data.direction;
        document.getElementById("bluetooth").innerHTML = json_data.echo_data;
        document.getElementById("speed").innerHTML = json_data.speed;
        document.getElementById("temperature").innerHTML = json_data.temperature;
        client.end();
        client.destroy();
    });

    client.on('end', () => {
        console.log('disconnected from server');
    });
}

// send arrow key data
function send_data(data) {
    client(data)
}

// for detecting which key is been pressed w,a,s,d
function updateKey(e) {

    e = e || window.event;

    if (e.keyCode == '87') {
        // up (w)
        document.getElementById("upArrow").style.color = "green";
        send_data("87");
    }
    else if (e.keyCode == '83') {
        // down (s)
        document.getElementById("downArrow").style.color = "green";
        send_data("83");
    }
    else if (e.keyCode == '65') {
        // left (a)
        document.getElementById("leftArrow").style.color = "green";
        send_data("65");
    }
    else if (e.keyCode == '68') {
        // right (d)
        document.getElementById("rightArrow").style.color = "green";
        send_data("68");
    }
    else if (e.keyCode == '52') {
        // speed up
        document.getElementById("slowDown").style.color = "green";
        send_data("52");
    }
    else if (e.keyCode == '54') {
        // slow down
        document.getElementById("speedUp").style.color = "green";
        send_data("54");
    }
    else if (e.keyCode == '32') {
        // slow down
        document.getElementById("halt").style.color = "green";
        send_data("32");
    }
}

// reset the key to the start state 
function resetKey(e) {

    e = e || window.event;

    document.getElementById("upArrow").style.color = "grey";
    document.getElementById("downArrow").style.color = "grey";
    document.getElementById("leftArrow").style.color = "grey";
    document.getElementById("rightArrow").style.color = "grey";
    document.getElementById("speedUp").style.color = "grey";
    document.getElementById("slowDown").style.color = "grey";
    document.getElementById("halt").style.color = "grey";

}

// update data for every 100ms
function update_data(){
    setInterval(function(){
        // get image from python server
        client();
    }, 100);
}
