var apiKey = "45939862";
window.resizeTo(528,396);
var sessionId = "2_MX40NTkzOTg2Mn5-MTUwNDEwMzMwMTkyNn5XR2dwbTVNTjk2SFZScU9zZFBMM2hTOUV-fg";
var token = "T1==cGFydG5lcl9pZD00NTkzOTg2MiZzaWc9Y2RiZWQwMWUzNTgwY2JkMzk0ZDE1M2Q2OWZjOTI2ZmMwNmVmYmVjYjpzZXNzaW9uX2lkPTJfTVg0ME5Ua3pPVGcyTW41LU1UVXdOREV3TXpNd01Ua3lObjVYUjJkd2JUVk5UamsyU0ZaU2NVOXpaRkJNTTJoVE9VVi1mZyZjcmVhdGVfdGltZT0xNTA0MTAzMzE1Jm5vbmNlPTAuMTgyNzA2MDAzOTc5MTc2NTgmcm9sZT1wdWJsaXNoZXImZXhwaXJlX3RpbWU9MTUwNjY5NTI5OCZpbml0aWFsX2xheW91dF9jbGFzc19saXN0PQ";
$(document).ready(function(){
        console.log ("starting...");

        initializeSession();
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
        var subscriber = session.subscribe(event.stream, 'subscriber', {
            insertMode: 'append',
            width: '100%',
            height: '100%',
            style: { nameDisplayMode: "auto" }
        }, handleError);
        SpeakerDetection(subscriber, function() {
            console.log('started talking');
        }, function() {
            console.log('stopped talking');
        });
    });

    var publisher = OT.initPublisher('publisher', {
        insertMode: 'append',
        width: '100%',
        height: '100%',
        style: { nameDisplayMode: "auto" }
    }, handleError);

    session.connect(token, function(error) {
        if (error) {
          handleError(error);
        } else {
          session.publish(publisher, handleError);
        }
    });
}



var SpeakerDetection = function(subscriber, startTalking, stopTalking) {
  var activity = null;
  subscriber.on('audioLevelUpdated', function(event) {
    var now = Date.now();
    console.log ("Audio Levels: " + event.audioLevel);
    if (event.audioLevel > 0.2) {
      if (!activity) {
        activity = {timestamp: now, talking: false};
      } else if (activity.talking) {
        activity.timestamp = now;
      } else if (now- activity.timestamp > 1000) {
        // detected audio activity for more than 1s
        // for the first time.
        activity.talking = true;
        if (typeof(startTalking) === 'function') {
          startTalking();
        }
      }
    } else if (activity && now - activity.timestamp > 3000) {
      // detected low audio activity for more than 3s
      if (activity.talking) {
        if (typeof(stopTalking) === 'function') {
          stopTalking();
        }
      }
      activity = null;
    }
  });
};