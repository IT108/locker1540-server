var appName = "icebebpcncnjfggpajldhickffdipnok";
var onMessage = function (data) {
    switch (data.action) {
        case 'scanner': {
            chrome.tabs.query({url: "*://admin.pfc-online.xyz/*"}, function (tab) {
                for (var i = 0; i < tab.length; i++) {
                    chrome.tabs.sendMessage(tab[i].id, data);
                    console.log(data)
                }
            });
        }
            break;
    }
};

var onPageMessage = function (data) {
    switch (data.action) {
        case 'test': {
            console.log(data.data.barcode);
        }
            break;
        case 'scan': {
            console.log('scanning');
            chrome.management.launchApp(appName, function () {
                if (chrome.runtime.lastError) console.error(chrome.runtime.lastError);
                else console.log("App launched");
                chrome.runtime.sendMessage(appName, 'HI there');
            });
        }
    }
};

chrome.runtime.onMessageExternal.addListener(onMessage);
chrome.runtime.onMessage.addListener(onPageMessage);
