var player = videojs('example-video');

            player.ready(function() {

                player.src({
                // src: 'https://s3.amazonaws.com/_bc_dml/example-content/sintel_dash/sintel_vod.mpd',
                src: 'https://bitmovin-a.akamaihd.net/content/playhouse-vr/mpds/105560.mpd',
                type: 'application/dash+xml'
                });

                player.play();
            });


            var start = null;


            // $(function(){
            //     // Bind the swipeleftHandler callback function to the swipe event on div.box
            //     $("div.bg").on( "swipeleft", swipeleftHandler );
            //
            //     // Callback function references the event target and adds the 'swipeleft' class to it
            //     function swipeleftHandler( event ){
            //         // $( event.target ).addClass( "swipeleft" );
            //         alert("left");
            //     }
            // });


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

                        player.src({
                            src: 'https://bitmovin-a.akamaihd.net/content/playhouse-vr/mpds/105560.mpd',
                            // src: '/manifest.mpd',
                            type: 'application/dash+xml'
                        });

                        player.play();

                        $.getJSON('/postmethod', {
                            vid: "123"}, function(data) {
                            // $("#result").text(data.result);
                            alert(data.result)
                        });
                    }



                    if(end < start - offset ){
                        // alert("right -> left");

                        player.src({
                            src: 'https://s3.amazonaws.com/_bc_dml/example-content/sintel_dash/sintel_vod.mpd',
                            // src: '/manifest.mpd',
                            type: 'application/dash+xml'
                        });

                        player.play();
                    }
                }

            });