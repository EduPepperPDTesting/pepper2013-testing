var apiKey = "45939862";
var sessionId = "2_MX40NTkzOTg2Mn5-MTUwNDEwMzMwMTkyNn5XR2dwbTVNTjk2SFZScU9zZFBMM2hTOUV-fg";
var token = "T1==cGFydG5lcl9pZD00NTkzOTg2MiZzaWc9Y2RiZWQwMWUzNTgwY2JkMzk0ZDE1M2Q2OWZjOTI2ZmMwNmVmYmVjYjpzZXNzaW9uX2lkPTJfTVg0ME5Ua3pPVGcyTW41LU1UVXdOREV3TXpNd01Ua3lObjVYUjJkd2JUVk5UamsyU0ZaU2NVOXpaRkJNTTJoVE9VVi1mZyZjcmVhdGVfdGltZT0xNTA0MTAzMzE1Jm5vbmNlPTAuMTgyNzA2MDAzOTc5MTc2NTgmcm9sZT1wdWJsaXNoZXImZXhwaXJlX3RpbWU9MTUwNjY5NTI5OCZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ";
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