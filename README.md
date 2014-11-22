Babel Chat
========
Babel Chat is a video chat web app that allows language learners to connect with native speakers of their target language and engage in guided, interactive chat sessions.

Providing an internationally convenient, entirely browser-hosted video language exchange, Babel Chat users can play games that cater to various learning styles while strengthening vocabulary, grammar, and communication skills. Users may also choose to discuss common themes by responding to questions in the chatbox, all in real time.

Babel Chat is built in Python with a Flask framework, uses a SQLite database, and integrates the FlaskSocketio and OpenTok APIs for websocket functionality.

![picture](https://github.com/amitch23/Babel_chat/blob/master/static/Babel_chat_index.png)

Getting started:
--------------------
First, clone this directory to your computer. Then
- Create and activate a new, empty virtual environment.
- Install the packages listed in requirements.txt (pip install -r requirements)
- Start the application by running 'python babel.py' in your terminal.
- Head to 'localhost:5000' in Chrome or Firefox, and open another browser in incognito/private mode to see the sockets in action. (Create a new profile and enter the chat room!)


The Breakdown:
--------------------
-	babel.py: runs the program, and contains all of the Flask app routes and socket handlers.

-	model.py: creates the database and classes.

-	babelchat.db: database that stores user, language, and game information

- Templates directory: 
  Html templates that implement Jinja to render pages in the browser, as well as sockets.js, which creates and handles websocket connection with the server for multiple-client functionality.


- Static directory:
  - Images: html visual elements, including the logo, background, icons, and game content.
  - Jquery and Bootstrap libraries with custom CSS stylesheets.
 


Contact information
------------------------
Email: andrealeemitchell@gmail.com
