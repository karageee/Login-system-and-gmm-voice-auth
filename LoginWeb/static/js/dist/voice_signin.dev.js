"use strict";

//webkitURL is deprecated but nevertheless
URL = window.URL || window.webkitURL;
var gumStream; //stream from getUserMedia()

var rec; //Recorder.js object

var input; //MediaStreamAudioSourceNode we'll be recording
// shim for AudioContext when it's not avb. 

var AudioContext = window.AudioContext || window.webkitAudioContext;
var audioContext; //audio context to help us record

var recordButton = document.getElementById("recordButton");
var resetButton = document.getElementById("resetButton");
var data = new FormData(); //add events to those 2 buttons

recordButton.addEventListener("click", startRecording);
resetButton.addEventListener("click", reset);
var filename = 0;

function startRecording() {
  console.log("recordButton clicked");
  /*
      Simple constraints object, for more advanced audio features see
      https://addpipe.com/blog/audio-constraints-getusermedia/
  */

  var constraints = {
    audio: true,
    video: false
  };
  /*
      Disable the record button until we get a success or fail from getUserMedia() 
  */

  recordButton.disabled = true;
  /*
      We're using the standard promise based getUserMedia() 
      https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices/getUserMedia
  */

  navigator.mediaDevices.getUserMedia(constraints).then(function (stream) {
    console.log("getUserMedia() success, stream created, initializing Recorder.js ...");
    /*
        create an audio context after getUserMedia is called
        sampleRate might change after getUserMedia is called, like it does on macOS when recording through AirPods
        the sampleRate defaults to the one set in your OS for your playback device
      */

    audioContext = new AudioContext(); //update the format 

    document.getElementById("formats").innerHTML = "Format: 1 channel pcm @ " + audioContext.sampleRate / 1000 + "kHz";
    /*  assign to gumStream for later use  */

    gumStream = stream;
    /* use the stream */

    input = audioContext.createMediaStreamSource(stream);
    /* 
        Create the Recorder object and configure to record mono sound (1 channel)
        Recording 2 channels  will double the file size
    */

    rec = new Recorder(input, {
      numChannels: 1
    }); //start the recording process

    rec.record();
    console.log("Recording started");
    setTimeout(function () {
      stopRecording();
    }, 5000);
  })["catch"](function (err) {
    //enable the record button if getUserMedia() fails
    recordButton.disabled = false;
  });
}

function stopRecording() {
  console.log("stopButton clicked"); //disable the stop button, enable the record too allow for new recordings

  recordButton.disabled = false; //tell the recorder to stop the recording

  rec.stop(); //stop microphone access

  gumStream.getAudioTracks()[0].stop(); //create the wav blob and pass it on to createDownloadLink

  rec.exportWAV(createDownloadLink);
}

function reset() {
  console.log("Reset button clicked");

  while (recordingsList.hasChildNodes()) {
    recordingsList.removeChild(recordingsList.firstChild);
  }

  filename = 0;
  recordButton.disabled = false;
}

function createDownloadLink(blob) {
  var url = URL.createObjectURL(blob);
  var au = document.createElement('audio');
  var li = document.createElement('li');
  var link = document.createElement('a'); //name of .wav file to use during upload and download (without extension)

  filename = filename + 1; //add controls to the <audio> element

  au.controls = true;
  au.src = url; //save to disk link

  link.href = url;
  link.download = filename + ".wav"; //download forces the browser to donwload the file using the  filename

  link.innerHTML = "Save to disk"; //add the new audio element to li

  li.appendChild(au); //add the filename to the li

  li.appendChild(document.createTextNode(filename + ".wav "));
  data.append("voice", blob, filename + ".wav"); //add the save to disk link to li

  li.appendChild(link);
  li.appendChild(document.createTextNode(" ")); //add a space in between
  // li.appendChild(upload)//add the upload link to li
  //add the li element to the ol

  recordingsList.appendChild(li);
  recordButton.disabled = true;
} //upload


$('form[name=voice_signup').submit(function (e) {
  var $form = $(this);
  var $error = $form.find(".error");
  $.ajax({
    url: '/user/voice_signin',
    type: 'POST',
    data: data,
    processData: false,
    contentType: false,
    success: function success(resp) {
      console.log(resp);

      if (resp.error == "There's no voice yet") {
        window.location.href = "/voice_signup/";
      } else {
        window.location.href = "/dashboard/";
      }
    },
    error: function error(resp) {
      console.log(resp);
      $error.text(resp.responseJSON.error).removeClass("error--hidden");
      recordingsList.removeChild(recordingsList.firstChild);
      recordButton.disabled = false;
    }
  });
  e.preventDefault();
});