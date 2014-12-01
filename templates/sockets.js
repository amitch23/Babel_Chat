    $(document).ready(function(){
        namespace = '/chat';
        var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

        //game variables
        var game_content_list = []; 
        var room_name = "{{ room_name }}";
        var counter = 0;
        var placeholder_txt = "<p>It's not your turn now. Listen to your partner and guess the word.</p>"
        var turn = false;

        //values assigned @ function: start game
        var starter = false;
        var joiner = false;

        //on socket connect, if client started the room, send msg to server.
        socket.on('connect', function() {
            
            {% if room_name %}
                socket.emit('join', {start: 1, room: "{{ room_name }}" });
            {% endif %}
            $('#log').append("<br>You are in the waiting room.");
            });

        //invites usr in waiting room to join room via btn click
        socket.on('invite_to_join', function(msg) {
            {% if room_name==None %}
                $("#join_room").removeClass('hidden');
                $("#join_room").html("Join " + msg.room_name);
                $("#join_room").click(function(evt){
                    socket.emit('join', {start: 2, room: msg.room_name});
                    room_name = msg.room_name;     
                });
                $("#navbar").addClass("hidden");
            {% endif %}
        });

        //once usrs in room, display msg to both re: who's in room with whom and display text chat box
        socket.on('room_message', function(msg) {
            starter=msg.starter;
            joiner=msg.joiner;
            $("#chatbox_wrapper").removeClass("hidden");

             {% if room_name==None %}
                $("#game_wrapper_label").removeClass('hidden');
                $("#game_wrapper_label").append("<p>You're in " + msg.room + " with " + msg.starter + "</p>")  
   
             {% elif room_name!=None %}
                 $("#game_wrapper_label").removeClass('hidden');
                 $("#game_wrapper_label").append("<p>You're in " + msg.room + " with " + msg.joiner + "</p>")

            {% endif %}       
        });

//--------handles starting conversation game-----------------------


        //receives and displays starter and joiner values from server 
        //and fetches game content from server
        socket.on("start_game", function(msg) {
            $('#join_room').addClass("hidden");
            socket.emit("display_to_room", {starter: msg.starter, joiner: msg.joiner, room: msg.room_name});
            socket.emit('get_game_content', {room: msg.room_name});
        });


        socket.on('full_room', function(msg) {
            $("#join_room").addClass('hidden');
        });

        //save content as list in global var 'game_content_list' 
        socket.on('send_convo_inx', function(msg) {
            for (var i = 0; i < msg.game_content.length; i++) {
                    game_content_list.push(msg.game_content[i]);
                };
            socket.emit("show_inx", {room: room_name, game: msg.game});
        });

        //displays conversation instructions to both clients
        socket.on('show_convo_inx', function(msg) {
              $('#game_title').removeClass("hidden");
              $("#log").html('');
              $("#game_title").html("<h5>" + msg.game + "</h5>");
              $('#inx').html('<p>' + msg.inx + '</p');
              $('#start_convo_btn').removeClass('hidden');
          });

        //send msg to server to show 1st card
        $("#start_convo_btn").click(function(evt) {
            socket.emit("send_1st_item", {room: room_name, topic:"convo"});
            
        });

        //displays 1st conversation question to both clients
        socket.on("display_first_q", function(msg) {
            $('#inx').html('');
            $('#start_convo_btn').addClass('hidden');
            counter = 0;
            $('#game_content').append(game_content_list[counter]);
            $('#nxt_q').removeClass('hidden');
        });

        // send data to server to request next card for both clients.
        $('#nxt_q').click(function(evt){
            socket.emit("request_nxt_q", {counter:counter+1, room: room_name});
        });

        //displays next q by updated counter number
        socket.on("display_nxt_q", function(msg) {
            counter = msg.counter;
            if (counter < (game_content_list.length)) {
                $('#game_content').html(game_content_list[msg.counter]);
            }
            else {
                $('#nxt_q').addClass('hidden');
                $("#gold_stars").removeClass('hidden');

                $("#game_content").html("<h2>Great job!</h2>");
                $("#end_of_game").removeClass("hidden");
            }                
            
        });

//---------handles card games and game moves-----------------------

        //receives game content from server and appends content to global var. Sends data to sever to show instructions to both clients.
        socket.on('send_inx', function(msg) {
            for (var i = 0; i < msg.card_content.length; i++) {
                    game_content_list.push(msg.card_content[i]);
                };
            socket.emit("show_inx", {room: room_name, game: msg.game});
        });

        //displays game instructions to both clients.
        socket.on('show_game_inx', function(msg) {
            $("#log").html('');
            $('#game_title').removeClass("hidden");
            $("#game_title").html("<h5>" + msg.game + "</h5>");
            $('#inx').html('<p>' + msg.inx + '</p');
            $('#start_btn').removeClass('hidden');
        });

        //sends msg to server to show first card
        $("#start_btn").click(function(evt) {
            socket.emit("send_1st_item", {room: room_name, topic:"game"});
            
        });

        //displays first game card
        socket.on("display_1st_card", function(msg) {
            $('#inx').html('');
            $('#start_btn').addClass('hidden');
        
            counter = 0;
            {% if room_name==None %}
                 $('#card_wrapper').html('<img src="' + game_content_list[counter] + '" id="card"></img>');
                timer = 10
                $("#timer").html("<img src='../static/img/timer.png'><h5>" + timer + "</h5>");

                 //'Next card' function called every 10 seconds
                timeout = setTimeout('$("#card_wrapper").click()', 10000);

                //when timer hits 0, call above function
                timer_interval = setInterval(function() {
                timer -= 1;
                $("#timer").html("<img src='../static/img/timer.png'><h5>" + timer + "</h5>");
                if (timer == 0){
                clearInterval(timer_interval);
                $("#timer").html('');
                }
                }, 1000);
                turn = true;

            {% elif room_name!=None %}
                $('#game_content').html(placeholder_txt);
                turn = false;
           {% endif %}
        });


        //request next card from server and increase counter by 1
        $("#card_wrapper").click(function(evt) {
            evt.preventDefault();
            socket.emit("request_nxt_q", {counter:counter+1, room: room_name, game_type:"cards"});

            clearInterval(timer_interval);
            clearTimeout(timeout);
            $("#timer").html('');
        });

        
        //displays next card by updated counter number
        socket.on("display_nxt_card", function(msg) {            

            if (counter < (game_content_list.length - 1)) {    
                turn = !turn;
                counter = msg.counter;

                if (turn==false) {
                    $('#game_content').html(placeholder_txt);
                    $('#card_wrapper').html('');
                }

                else {                               
                    $('#game_content').html('');
                    $('#card_wrapper').html('<img src="' + game_content_list[msg.counter] + '" id="card"></img>');

                    timer = 10
                    $("#timer").html("<img src='../static/img/timer.png'><h5>" + timer + "</h5>");

                    //'Next card' function called every 10 seconds
                    timeout = setTimeout('$("#card_wrapper").click()', 10000);
          
                    timer_interval = setInterval(function() 
                    {
                    timer -= 1;
                    $("#timer").html("<img src='../static/img/timer.png'><h5>" + timer + "</h5>");
                    if (timer == 0){
                    clearInterval(timer_interval);
                    $("#timer").html('');
                    }
                    }, 1000);

                }
            }

            //end of game - display congratulatory message to both clients.
            else {
                if (turn==false) {
                    $("#gold_stars").removeClass('hidden');
                    $("#game_content").html("<h2>Great job!</h2>");
                    $("#end_of_game").removeClass("hidden");
                }
                else {
                    $('#card_wrapper').html('');
                    $("#gold_stars").removeClass('hidden');
                    $("#game_content").html("<h2>Great job!</h2>");
                    $("#end_of_game").removeClass("hidden");
                }
            }

        });

//-----------ever-present btn handlers/misc.-----------------------

        //debugging display - no real use for clients
        socket.on('output to log', function(msg) {
                $('#log').append('<br>Received: ');
            });


        $("#end_session_btn").click(function(evt) {
            alert("Are you sure you want to leave?");
            socket.emit('leave', {room: room_name});        
            window.location = "/";
            });


        socket.on('display_disconnect_alert', function(msg) {
            alert(msg.leaving_usr + " has left the room. Thanks for chatting!");
            socket.emit('leave', {room: room_name});        
            window.location = "/";    
        });

//-----------chat box handlers-----------------------

//send message and txt sender to server when user clicks button
        $('#send_txt_btn').click(function(event) {

            {% if room_name!= None %}
                socket.emit('send_txt', {room: room_name, sender: starter, txt: $('#text_message').val()});
                $("#text_message").val('');

            {% elif room_name==None %}
                socket.emit('send_txt', {room: room_name, sender: joiner, txt: $('#text_message').val()});
                $("#text_message").val('');
            {% endif %}
        });

        //if user hits enter, run above function
        $('#text_message').keypress(function(evt) {
            if (evt.which === 13) {
                $('#send_txt_btn').click();
            }
        });

        //display txt message to users in room
        socket.on('display_txt_msg', function(msg) {
            $('#txt_msgs').append('<p><b>' + msg.sender+ "</b>: " + msg.txt + '</p>');
            $("#txt_msgs").prop('scrollTop', $("#txt_msgs").prop('scrollHeight'));
        });


        //end_session_btn shows on hover of subscriber wrapper
        $( "#subscriber_wrapper").hover(
          function() {
            $('#end_session_btn').removeClass('hidden');
          }, function() {
            $('#end_session_btn').addClass('hidden');
          }
        );


});

