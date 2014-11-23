    $(document).ready(function(){
        namespace = '/chat';
        var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

        console.log("sockets fired!");

        var game_content_list = []; 
        var room_name = "{{ room_name }}";
        var counter = 0;
        var placeholder_txt = "It's not your turn now. Listen to your partner and guess the word."
        var turn = false;
        //values assigned @ function: start game
        var starter = false;
        var joiner = false;

        socket.on('connect', function() {
            //on socket connect, if client started the room, send msg to server.

            {% if room_name %}
                socket.emit('join', {start: 1, room: "{{ room_name }}" });
            {% endif %}
            // $('#log').append("<br>You're connected.");
            });

        
        socket.on('invite_to_join', function(msg) {
            //invites usr in waiting room to join room via btn click
            {% if room_name==None %}
                console.log("{{ user.name }}");
                $("#join_room").removeClass('hidden');
                $("#join_room").html("Join " + msg.room_name);
                $("#join_room").click(function(evt){
                    socket.emit('join', {start: 2, room: msg.room_name});
                    room_name = msg.room_name;
                    //socket.emit('makebtndisappearforallotherusersinwaitingroom')
                    //broadcast, new func in server to get Addclass('hidden') to the join room button
                });
                $("#navbar").addClass("hidden");
            {% endif %}
        });

        //once usrs in room, display msg to both re: who's in room with whom
        socket.on('room_message', function(msg) {
             {% if room_name==None %}
                $("#game_wrapper_label").append("<p>You're in " + msg.room + " with " + msg.starter + "</p>")  
                $("#end_session_btn").removeClass('hidden')
   
             {% elif room_name!=None %}
                 $("#game_wrapper_label").append("<p>You're in " + msg.room + " with " + msg.joiner + "</p>")
                 $("#end_session_btn").removeClass('hidden')

            {% endif %}       
        });

//--------handles starting conversation game-----------------------


        //msg 'start_game' to server to get game content
        socket.on("start_game", function(msg) {
            console.log("game started");
            $('#join_room').addClass("hidden");
            starter=msg.starter;
            joiner=msg.joiner;
            socket.emit("display_to_room", {starter: starter, joiner: joiner, room: msg.room_name});

            socket.emit('get_game_content', {room: msg.room_name});
        });


        //display 1st convo question to both clients
        socket.on("display_convo_content", function(msg) {
            //save content as list in game_content_list 
            for (var i = 0; i < msg.game_content.length; i++) {
                game_content_list.push(msg.game_content[i]);
            };
            counter = 0;
            //need to display instructions for convo
            $('#game_content').append(msg.game_content[counter]);
            $('#nxt_q').removeClass('hidden');
        });

        $('#nxt_q').click(function(evt){
            socket.emit("request_nxt_q", {counter:counter+1, room: room_name});
        });

        //displays next q by updated counter #
        socket.on("display_nxt_q", function(msg) {
            //get next item in list by counter
            counter = msg.counter;
            $('#game_content').html(game_content_list[msg.counter]);
        });

//---------handles card games and game moves-----------------------

        socket.on('send_inx', function(msg) {
            for (var i = 0; i < msg.card_content.length; i++) {
                    game_content_list.push(msg.card_content[i]);
                };
            socket.emit("show_inx", {room: room_name, game: msg.game});
        });


      socket.on('show_inx', function(msg) {
            $('#game_title').removeClass("hidden");
            $("#game_title").html("<h5>You're playing: " + msg.game + "</h5>");
            $('#inx').html('<p>' + msg.inx + '</p');
            $('#start_btn').removeClass('hidden');
        });


      $("#start_btn").click(function(evt) {
        //send msg to server to show 1st card
          socket.emit("send_1st_card", {room: room_name});
          
      });


        socket.on("display_1st_card", function(msg) {
            // $("#game_title").html('');
            $('#inx').html('');
            $('#start_btn').addClass('hidden');
        
            counter = 0;
           $('#nxt_card').removeClass('hidden');
            {% if room_name==None %}
                 $('#card_wrapper').html('<img src="' + game_content_list[counter] + '" id="card"></img>');
                 timer = 3
                 $("#timer").html("<h5>Timer:" + timer + "</h5");

                 //when this function is called, every x seconds, the click event will fire
                 timeout = setTimeout('$("#nxt_card").click()', 3000);

                 //displays timer in browser for player whose turn it is
                 timer_interval = setInterval(function() 
                 {
                  timer -= 1;
                  $("#timer").html("<h5>Timer:" + timer + "</h5");
                  if (timer == 0){
                   clearInterval(timer_interval);
                   $("#timer").html('');
                  }
                 }, 1000);

                turn = true;


            {% elif room_name!=None %}
                $('#nxt_card').addClass('hidden');
                $('#game_content').html(placeholder_txt);

                turn = false;
           {% endif %}
        });


        $("#nxt_card").click(function(evt) {
            //request next card from server and increase counter by 1
            socket.emit("request_nxt_q", {counter:counter+1, room: room_name, game_type:"cards"});
            //clear timer and interval
            clearInterval(timer_interval);
            clearTimeout(timeout);
            $("#timer").html('');
        });

        
        // displays next card by updated counter #
        socket.on("display_nxt_card", function(msg) {            
            //get next item in list by counter    
            if (counter < (game_content_list.length - 1)) {    
                turn = !turn;
                counter = msg.counter;

                if (turn==false) {
                    console.log("turn=false");
                    $('#game_content').html(placeholder_txt);
                    $('#card_wrapper').html('');
                    $('#nxt_card').addClass('hidden');               
                }

                else {
                    console.log("counter: " + counter);
                    console.log(game_content_list.length);
                    console.log(game_content_list[counter]);
                    
                    $('#game_content').html('');
                    $('#card_wrapper').html('<img src="' + game_content_list[msg.counter] + '" id="card"></img>');
                    $('#nxt_card').removeClass('hidden');

                    timer = 3
                    $("#timer").html("<h5>Timer:" + timer + "</h5");

                    //when this function is called, every x seconds, the click event will fire
                    timeout = setTimeout('$("#nxt_card").click()', 3000);

                    //displays timer in browser for player whose turn it is              
                    timer_interval = setInterval(function() 
                    {
                     timer -= 1;
                     $("#timer").html("<h5>Timer:" + timer + "</h5");
                     if (timer == 0){
                      clearInterval(timer_interval);
                      $("#timer").html('');
                     }
                    }, 1000);

                }
            }
            else {
                console.log("counter is more than length of game content");

                //clear all button and images for both clients with if statements targeting turn=true/false
                //($("#game_title").html('');

                //call another function to play again or end session
                //redirect to profile page?
                //OR display 2 btns to play another game or keep chatting without games...
            }
        });

//-----------ever-present btn handlers/misc.-----------------------

     // socket.on('output to log', function(msg) {
     //    console.log(msg);
     //        $('#log').append('<br>Received: ');
     //    });

     $("#end_session_btn").click(function(evt) {
        console.log("end session");
        //alert pops up before function fires: on person who clicked, "are you sure you want to leave this session?"

            //have user leave room (flasksocketio method)
            //send socket msg to server to remove that user from global room dictionary
            
            //send msg to other person: 'your partner has ended the session.'
        //redirect both to profile pages or home page

     });
          
    
});

