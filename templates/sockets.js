    $(document).ready(function(){
        namespace = '/chat';
        var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

        console.log("sockets fired!");

        var game_content_list = []; 
        var room_name = "{{ room_name }}";
        var counter = 0;
        var placeholder_txt = "It's not your turn now. Listen to your partner and guess the word."
        var turn = false;
        //values assigned @ socket.on(start game)
        var starter = false;
        var joiner = false;

        socket.on('connect', function() {
            //on socket connect, if client started the room, send msg to server.

            {% if room_name %}
                socket.emit('join', {start: 1, room: "{{ room_name }}" });
            {% endif %}
            $('#log').append("<br>You're connected");
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
                $("#game_wrapper_label").append("You're in " + msg.room + "with " + msg.starter)              
             {% elif room_name!=None %}
                 $("#game_wrapper_label").append("You're in " + msg.room + "with " + msg.joiner)
            {% endif %}       
        });

//-----------handles starting conversation game-----------------------


        //msg 'start_game' to server to get game content
        socket.on("start_game", function(msg) {
            console.log("game started");

            $('#join_room').addClass("hidden");

            starter=msg.starter;
            joiner=msg.joiner;

            socket.emit("display_to_room", {starter: starter, joiner: joiner,room: msg.room_name});

            socket.emit('get_game_content', {room: msg.room_name});
        });


        //display 1st game element to both clients
        socket.on("display_convo_content", function(msg) {
            
            //save content as list in game_content_list (global var) 
            for (var i = 0; i < msg.game_content.length; i++) {
                game_content_list.push(msg.game_content[i]);
            };
            counter = 0;
            //display instructions for game

            //display first question
            $('#game_content').append(msg.game_content[counter]);
           //remove hidden class on 'next' button
           $('#nxt_q').removeClass('hidden');
        });

        //event listener for nxt-question button
        $('#nxt_q').click(function(evt){
            socket.emit("request_nxt_q", {counter:counter+1, room: room_name});
        });

        //displays next q by updated counter #
        socket.on("display_nxt_q", function(msg) {
            //get next item in list by counter
            counter = msg.counter;
            console.log(" this is the room: {{ room_name}} ");
            //if 

            $('#game_content').html(game_content_list[msg.counter]);
        });

//-------------------handles card games and game moves-----------------------

        socket.on("display_card_content", function(msg) {

            for (var i = 0; i < msg.card_content.length; i++) {
                    game_content_list.push(msg.card_content[i]);
                };
                console.log(msg.game_content_list);
           
            counter = 0;
           $('#nxt_card').removeClass('hidden');

            {% if room_name==None %}
                 $('#card_wrapper').html('<img src="' + game_content_list[counter] + '" id="card"></img>');
                turn = true;
            {% elif room_name!=None %}
                $('#nxt_card').addClass('hidden');
                $('#game_content').html(placeholder_txt);
                turn = false;
           {% endif %}

        });

 
        //event listener for next card button
        $("#nxt_card").click(function(evt) {
            //request next card from server and increase counter by 1
            socket.emit("request_nxt_q", {counter:counter+1, room: room_name, game_type:"cards", });
        });

        

        // displays next card by updated counter #
        socket.on("display_nxt_card", function(msg) {
            //get next item in list by counter
            
            if (counter < game_content_list.length){
                //switch values for turn for each player
                turn = !turn;
                counter = msg.counter;
                //put placeholder txt, clear img src, hide nxt btn
                if (turn==false) {
                    $('#game_content').html(placeholder_txt);
                    $('#card_wrapper').html('');

                    // $('#card').attr('src', '');
                    $('#nxt_card').addClass('hidden');
                }
                //clear txt area, add next card img, unhide nxt btn
                else {
                    $('#game_content').html('');
                    // $('#card').attr('src', game_content_list[msg.counter]);
                    $('#card_wrapper').html('<img src="' + game_content_list[msg.counter] + '" id="card"></img>');
                    $('#nxt_card').removeClass('hidden');
                }
            }

            else {
                //clear button and image
                //call another function to play again or end session
            }
        });

     socket.on('output to log', function(msg) {
            console.log(msg);
            $('#log').append('<br>Received: ' + msg.);
        });
    

        //debugging, print to browser
      
    
});

