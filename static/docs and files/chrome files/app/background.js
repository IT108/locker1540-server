var extName = "mbjbpcfbkejffkccefpdooheiijlooaf";
var onGetDevices = function (ports) {
    console.log("device number: " + ports.length);
    for (var i = 0; i < ports.length; i++) {
        console.log(ports[i].path);
    }
    if (ports.length === 1) {
        currentDevice = ports[0].path;
        console.log("current device: " + currentDevice)
    } else if (ports.length < 1){
        console.log("no devices found")
    } else{
        currentDevice = ports[0].path;
        console.log("multiple device found, current device is: " + currentDevice)
    }
};

var currentDevice = "";

var onMessage = function (data) {
    console.log(data)
};

chrome.serial.getDevices(onGetDevices);
chrome.runtime.onMessageExternal.addListener(onMessage);
chrome.runtime.onMessage.addListener(onMessage);

chrome.app.runtime.onLaunched.addListener(function () {
    console.log("OnLaunch");
    chrome.serial.connect(currentDevice, {bitrate: 9600}, onConnect);
});
var stringReceived = '';

var onConnect = function (connectionInfo) {
    var connectionId = connectionInfo.connectionId;
    console.log("connect");
    var onReceiveCallback = function (info) {
        if (info.connectionId == connectionId) {
            var str = arrayBufferToString(info.data);
            if (str.charAt(str.length - 1) === '\n') {
                stringReceived += str.substring(0, str.length - 1);
                stringReceived = checkPattern(stringReceived);
                console.log(stringReceived);
                chrome.runtime.sendMessage(extName, {
                    action: 'scanner', data: {
                        barcode: stringReceived
                    }
                });
                close();
                stringReceived = '';
            } else {
                stringReceived += str;
            }
        }
    };

    chrome.serial.onReceive.addListener(onReceiveCallback);
};

function arrayBufferToString(buffer) {
    var string = '';
    var bytes = new Uint8Array(buffer);
    var len = bytes.byteLength;
    for (var i = 0; i < len; i++) {
        string += String.fromCharCode(bytes[i]);
    }
    return string;
}

function checkPattern(p) {
    var i = 0;
    var t = p.length;
    var res = '';
    while (i < t) {
        var s = p.charCodeAt(i);
        if ((47 < s && s < 58) || (64 < s && s < 71)) {
            res += String.fromCharCode(s);
        }
        i += 1;
    }
    return res;
}

function getPorts() {
    
}


