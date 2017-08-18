var apiKey = "45939862";
var sessionId = "2_MX40NTkzOTg2Mn5-MTUwMjkwNTYwNzEwNH5yd0FxS2tWZVA4czBzQ1VOL0hGQXdjaE1-fg";
var token = "T1==cGFydG5lcl9pZD00NTkzOTg2MiZzaWc9MTFjYjIzOWIwZGYwMTczYzdmNGI2ZDU1YmU3YmJlZWFmNTlmZmU5NTpzZXNzaW9uX2lkPTJfTVg0ME5Ua3pPVGcyTW41LU1UVXdNamt3TlRZd056RXdOSDV5ZDBGeFMydFdaVkE0Y3pCelExVk9MMGhHUVhkamFFMS1mZyZjcmVhdGVfdGltZT0xNTAzMDY4NDE5Jm5vbmNlPTAuNTIwNjkwMDcwNzQ0MTczMSZyb2xlPXB1Ymxpc2hlciZleHBpcmVfdGltZT0xNTAzNjczMjEwJmluaXRpYWxfbGF5b3V0X2NsYXNzX2xpc3Q9";
$(document).ready(function(){
    $("#start-session").click(function() {
        initializeSession();
    });
    $("#webchat > .close-modal").click(function () {
        disconnectSession();
    })
});

function handleError(error) {
  if (error) {
    alert(error.message);
  }
}

function disconnectSession () {
    var session = OT.initSession(apiKey, sessionId);
    session.disconnect();
}

function initializeSession() {
    var session = OT.initSession(apiKey, sessionId);

    session.on('streamCreated', function(event) {
        session.subscribe(event.stream, 'subscriber', {
            insertMode: 'append',
            width: '100%',
            height: '100%'
        }, handleError);
    });

    var publisher = OT.initPublisher('publisher', {
        insertMode: 'append',
        width: '100%',
        height: '100%'
    }, handleError);

    session.connect(token, function(error) {
        if (error) {
          handleError(error);
        } else {
          session.publish(publisher, handleError);
        }
    });
}