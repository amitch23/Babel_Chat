Babel Chat
========
Babel Chat is a video chat web app that allows language learners to connect with native speakers of their target language and engage in guided, interactive chat sessions.

Providing an internationally convenient, entirely browser-hosted video language exchange, Babel Chat users can play games that cater to various learning styles while strengthening vocabulary, grammar, and communication skills. Users may also choose to discuss common themes by responding to questions in the chatbox, all in real time.

Babel Chat is built in Python with a Flask framework, uses a SQLite database, and integrates the FlaskSocketio and OpenTok APIs for websocket functionality.

![picture](https://github.com/amitch23/Babel_chat/blob/master/static/Babel_chat_index.png)

Getting started:
--------------------
1) First, clone this directory to your computer.

<pre><code>$ git clone https://github.com/amitch23/Babel_Chat.git</code></pre>

2) Create and activate a virtual environment in the same directory: 

<pre><code>$ pip install virtualenv
$ virtualenv env
$ . env/bin/activate 
</code></pre>

3) Install the required packages using pip:

<pre><code>(env)$ pip install -r requirements.txt
</code></pre>


4) In Chrome or Firefox, open 2 browser windows - one in 'normal' mode and another in incognito or private mode:

<pre><code>http://localhost:5000/</code></pre> 

Create new profiles and enter the chat room!



The Breakdown:
--------------------
-	babel.py: runs the program, and contains all of the Flask app routes and socket handlers.

-	model.py: creates the database and classes.

-	babelchat.db: database that stores user, language, and game information

- Templates directory: 
 html templates that implement Jinja to render pages in the browser, as well as sockets.js, which creates and handles websocket connectivity with the server for multiple-client functionality.


- Static directory:
  - Images: html visual elements, including the logo, background, icons, and game content.
  - Jquery and Bootstrap libraries with custom CSS stylesheets.
 


Contact information
------------------------
Email: andrealeemitchell@gmail.com
