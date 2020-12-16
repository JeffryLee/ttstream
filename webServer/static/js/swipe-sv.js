var player = dashjs.SuperPlayer().create();

var view = document.getElementById('example-video');

// var view;

// // superplayer = dashjs.SuperPlayer().create();
// var videoContainer = document.getElementById('starter-template');
// if (!view) {
//     view = document.createElement('example-video');
//     view.controls = true;
//     videoContainer.appendChild(view);
// }


var cdnaddress = 'http://172.29.114.202:8080/dash/data/';


var thisVideo = '6836783718552636678';

var nextVideo = '';
var preVideo = '';
var swaptmp = '';




$.getJSON('/getNeighbour', {
    vid: thisVideo}, function(data) {
    preVideo = data.uidPre;
    nextVideo = data.uidNext;
});


// for (var i=0; i<7; i++) {


//     // await new Promise(r => setTimeout(r, 500));

    
// }

var intervalID = setInterval(
    function(){
        var url = cdnaddress + thisVideo + '/manifest.mpd';
        
        
        var ret = player.attachSource(url);

        console.log("attach source");

        if (ret == 0) {

            thisVideo = nextVideo;
        
            $.getJSON('/getNeighbour', {
                vid: thisVideo}, function(data) {
                preVideo = data.uidPre;
                nextVideo = data.uidNext;

                console.log("preVideo: "+ preVideo+"; nextVideo: "+nextVideo);
            });
        }
    }, 500);


player.attachView(view);




// player.ready(function() {
//     player.src({
//         src: cdnaddress + thisVideo + '/manifest.mpd',
//         type: 'application/dash+xml'
//     });
//     player.play();
// });


var start = null;


window.addEventListener("touchstart",function(event){

    if (event.touches.length === 1) {
        //just one finger touched
        start = event.touches.item(0).clientX;
    } else {
        //a second finger hit the screen, abort the touch
        start = null;
    }
});

window.addEventListener("touchend",function(event){

    var offset = 100;//at least 100px are a swipe

    if (start) {
        //the only finger that hit the screen left it
        var end = event.changedTouches.item(0).clientX;

        if(end > start + offset){
            // alert("left -> right");

            // thisVideo = preVideo;

            // player.src({
            //     src: cdnaddress + thisVideo + '/manifest.mpd',
            //     type: 'application/dash+xml'
            // });


            // player.play();


            // $.getJSON('/getNeighbour', {
            //     vid: thisVideo}, function(data) {
            //     preVideo = data.uidPre;
            //     nextVideo = data.uidNext;
            // });

            // does not process pre video

        }


        if(end < start - offset ){

            player.playNext();

            // var url = cdnaddress + thisVideo + '/manifest.mpd';
            // player.attachSource(url);
        
            // thisVideo = nextVideo;
        
        
            // $.getJSON('/getNeighbour', {
            //     vid: thisVideo}, function(data) {
            //     preVideo = data.uidPre;
            //     nextVideo = data.uidNext;
            // });


            // thisVideo = nextVideo;

            // player.src({
            //     src: cdnaddress + thisVideo + '/manifest.mpd',
            //     type: 'application/dash+xml'
            // });

            // player.play();

            // $.getJSON('/getNeighbour', {
            //     vid: thisVideo}, function(data) {
            //     preVideo = data.uidPre;
            //     nextVideo = data.uidNext;
            // });
        }
    }

});

