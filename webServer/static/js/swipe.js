var player = videojs('example-video');



var cdnaddress = 'http://172.29.114.202:8080/dash/data/';


var thisVideo = '6836783718552636678';

var nextVideo = '';
var preVideo = '';


$.getJSON('/getpre', {
    vid: thisVideo}, function(data) {
    preVideo = data.result
});


$.getJSON('/getnext', {
    vid: thisVideo}, function(data) {
    nextVideo = data.result
});

player.ready(function() {

    player.src({
        // src: 'https://s3.amazonaws.com/_bc_dml/example-content/sintel_dash/sintel_vod.mpd',
        // src: 'https://bitmovin-a.akamaihd.net/content/playhouse-vr/mpds/105560.mpd',
        src: cdnaddress + thisVideo + '/manifest.mpd',
        type: 'application/dash+xml'
    });

    player.play();
});


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


            thisVideo = preVideo;


            player.src({
                // src: 'https://bitmovin-a.akamaihd.net/content/playhouse-vr/mpds/105560.mpd',
                // src: '/manifest.mpd',
                src: cdnaddress + thisVideo + '/manifest.mpd',
                type: 'application/dash+xml'
            });


            $.getJSON('/getpre', {
                vid: thisVideo}, function(data) {
                preVideo = data.result
            });


            $.getJSON('/getnext', {
                vid: thisVideo}, function(data) {
                nextVideo = data.result
            });

            player.play();


        }



        if(end < start - offset ){
            // alert("right -> left");

            // $.getJSON('/getnext', {
            //     vid: thisVideo}, function(data) {
            //     // $("#result").text(data.result);
            //     thisVideo = data.result
            // });

            thisVideo = nextVideo;

            player.src({
                // src: 'https://s3.amazonaws.com/_bc_dml/example-content/sintel_dash/sintel_vod.mpd',
                // src: '/manifest.mpd',
                src: cdnaddress + thisVideo + '/manifest.mpd',
                type: 'application/dash+xml'
            });

            player.play();


            $.getJSON('/getpre', {
                vid: thisVideo}, function(data) {
                preVideo = data.result
            });


            $.getJSON('/getnext', {
                vid: thisVideo}, function(data) {
                nextVideo = data.result
            });
        }
    }

});

