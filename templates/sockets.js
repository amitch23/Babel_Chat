    // var in_room = null;
    

    $(document).ready(function(){


        namespace = '/chat';

        var socket = io.connect('http://' + document.domain + ':' + location.port + namespace);

        console.log("sockets fired");

        var game_content_list = []; 
        var room_name = "{{ room_name }}";
        var counter = 0;
        var placeholder_txt = "It's not your turn now. Listen to your partner and guess the word."
        var turn = false;
        var in_room = [];




        //1.upon socket connection, emit the message "you're connected" to the client and send message "join" to server with room name
        socket.on('connect', function() {

            in_room.push("{{user.name}}");
            socket.emit("waiting_room", {inroom: "in the waiting room: " + in_room, name: "{{user.name}}"});

            //when user connects, send message with name (?) to the server to broadcast message back and jquery html the names to the div 'waiting_room' in html file. This will show all the entering users in the waiting room who is in the waiting room.

            //if a user starts a game via the link on the profile page, they get added to the in_room array, a link is displayed to all users in the waiting room (but not that user). If one person clicks, they enter the room, their name is added to the in_room list. 

            //if the other user tries to enter room via the button, they can't get in. If length of in-room is 2, don't add 3rd user. Give them a 'can't enter' message and ask if they want to create their own room

            $('#log').append("<br>You're connected");

            // socket.emit("waiting_room", {})

            $("#in_room").html("{{ user.name }}" + "in waiting room");
           
            //if initiating usr, join room in server and invite others to join
            {% if room_name %}
                //populate input box with room name if in room
                //upon connect of initiating, join room
                socket.emit('join', {start: 1, room: "{{ room_name }}" });
                
                // in_room.push("{{user.name}}");
                // console.log(in_room);

            {% endif %}

            //if room_name==none, then join user to a room called waiting room.
            });


        socket.on("show_ppl_waiting", function(msg) {
            console.log("waiting room!!");
            $("#waiting_room_list").append("<li>" + msg.in_room + "</li>");


        });

        //5. put a button on the page for jose when 1st client starts room to join the room and pass the room name and maybe his name?)
        socket.on('invite_to_join', function(msg) {
            //invites usr in waiting room to join room via btn click
            console.log(msg);

            {% if room_name==None %}
                $("#join_room").removeClass('hidden');
                $("#join_room").html("Join " + msg.room_name);
                $("#join_room").click(function(evt){
                    socket.emit('join', {start: 2, room: msg.room_name});
                    room_name = msg.room_name;
                    //socket.emit('makebtndisappearforallotherusersinwaitingroom')
                    //broadcast, new func in server to get Addclass('hidden') to the join room button
                });
                $("#navbar").addClass("hidden");
                // in_room.push("{{user.name}}");
                // console.log(in_room);
            {% endif %}



            //append received message to log div
            $('#log').append('<br>Received #' + msg.count + ': ' + msg.data);
        });

//-----------handles starting conversation game-----------------------


        //msg 'start_game' to server to get game content
        socket.on("start_game", function(msg) {
            console.log(in_room);
            console.log("game started");
            $('#join_room').addClass("hidden");
            room_name=msg.room_name; 
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


        //debugging, print to browser
        socket.on('output to log', function(msg) {
            console.log(msg);
            $('#log').append('<br>Received: ' + msg.data);
        });
    
});

