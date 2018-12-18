var extName = "mbjbpcfbkejffkccefpdooheiijlooaf";
chrome.runtime.onMessage.addListener(
    function(data) {
        var event = new CustomEvent(data.action, {detail: data.data});
        document.dispatchEvent(event);
    }
);
console.log('HI!');
window.addEventListener("message", function(event) {
    var data = event.data;
    console.log(data);
    chrome.runtime.sendMessage(extName, data);
});