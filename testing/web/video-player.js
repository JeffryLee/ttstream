(function () {
  'use strict';

  // Does the browser actually support the video element?
  var supportsVideo = !!document.createElement('video').canPlayType;

  if (supportsVideo) {
  	// Obtain handles to main elements
  	var videoContainer = document.getElementById('videoContainer');
   	var video = document.getElementById('video');
   	var videoControls = document.getElementById('video-controls');

   	// Hide the default controls
   	video.controls = false;

   	// Display the user defined video controls
   	videoControls.style.display = 'block';

   	// Obtain handles to buttons and other elements
   	var playpause = document.getElementById('playpause');
   	var stop = document.getElementById('stop');
   	var progress = document.getElementById('progress');
    var progressBar = document.getElementById('progress-bar');

   	// Only add the events if addEventListener is supported (IE8 and less don't support it, but that will use Flash anyway)
   	if (document.addEventListener) {
   		// Wait for the video's meta data to be loaded, then set the progress bar's max value to the duration of the video
   		video.addEventListener('loadedmetadata', function() {
   			progress.setAttribute('max', video.duration);
   		});

   		// Add events for all buttons
   		playpause.addEventListener('click', function(e) {
   			if (video.paused || video.ended) video.play();
   			else video.pause();
   		});

   		// The Media API has no 'stop()' function, so pause the video and reset its time and the progress bar
   		stop.addEventListener('click', function(e) {
   			video.pause();
   			video.currentTime = 0;
   			progress.value = 0;
   		});

   		// As the video is playing, update the progress bar
   		video.addEventListener('timeupdate', function() {
        // For mobile browsers, ensure that the progress element's max attribute is set
        if (!progress.getAttribute('max')) progress.setAttribute('max', video.duration);
        progress.value = video.currentTime;
        progressBar.style.width = Math.floor((video.currentTime / video.duration) * 100) + '%';
   		});

      // React to the user clicking within the progress bar
      progress.addEventListener('click', function(e) {
        var pos = (e.pageX  - this.offsetLeft) / this.offsetWidth;
        video.currentTime = pos * video.duration;
      });

   	}
  }

})();