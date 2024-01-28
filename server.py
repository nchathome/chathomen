
from flask import Flask, render_template
from flask import request
from flask_socketio import SocketIO, emit
from flask import Flask, redirect
from flask import Flask,session
import os


app = Flask(__name__)
sims = []

socketio = SocketIO(app)


@app.route('/')
def login():
  return """

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>チャットサイトログイン画面（デモ版）</title>

    <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.0/socket.io.js"></script> -->
</head>
<body>

    <p class="fsize">sysの担任は</p>

    <footer>
        <form method="post" action="/chat">
            <input type="passw" name="passw" class="passw" placeholder="passw">
        </form>
    </footer>


</body>
</html>


"""




@app.route('/chat', methods=['GET', 'POST'])
def index():
  password = request.form["passw"]
  print(password)

  if password == "システム":
    return """

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
  　<meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>チャットサイト（デモ版）</title>
    <style type="text/css">


    .midasi{
      font-size: 5em;
    }
    P{
      text-align: center;
    }


    *{margin: 0;padding: 0;list-style: none;}

    .wrap{
        width: 600px;
        margin: 0 auto;
        padding: 20px 0 150px 0;
        background: #7c7c8b;
        min-height: 100vh;
    }
    li{
        position: relative;
        padding: 10px 20px;
        margin: 0 10px 10px 10px;
        background-color: #fff;
        border-radius: 5px;
    }
    span{
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        right: 10px;
        font-size: 12px;
        color: #ccc;
    }

    .wrapper{
        height: 100%;
        min-height: 100vh;
        position: relative;
        padding-bottom: 120px;
        box-sizing: border-box;
    }

    footer{

        width: 300px;
        margin: 0 auto;
        background-color: #7c7c8b;
        border-radius: 5px;
        position: absolute;/*←絶対位置*/
        bottom: 0; 
    }

    input{

        width: 80%;
        margin: 10px;
        border: none;
        border-radius: 5px;
        padding: 10px;
        position: fixed;
        bottom: -10; 
        right: 35%;
        width:550px; 
        display: block;
        margin:0 auto 30px;
    }
    .name-1 {
      outline:solid 5px #333;
      width:550px;
      bottom: 0;
    }

    .name-2 {
      outline:solid 5px #333;
      bottom: 50px; 
    }

      
    .fixed_btn { 
    position: fixed;
    bottom: 10px;
    right: 10px;
    padding: 6px 40px;

    display: block;
    text-align: center;
    vertical-align: middle;
    text-decoration: none;
    width: 120px;
    margin: auto;
    padding: 1rem 0rem;
    font-weight: bold;
    border: 2px solid #27acd9;
    background: #27acd9;
    color: #fff;
    border-radius: 100vh;
    transition: 0.5s;
    }
    .fixed_btn:hover {
      color: #27acd9;
      background: #fff;
    }


      
    .fixed_btn2 { 
    position: fixed;
    bottom: 70px;
    right: 10px;
    padding: 6px 40px;

    display: block;
    text-align: center;
    vertical-align: middle;
    text-decoration: none;
    width: 120px;
    margin: auto;
    padding: 1rem 0rem;
    font-weight: bold;
    border: 2px solid #27acd9;
    background: #27acd9;
    color: #fff;
    border-radius: 100vh;
    transition: 0.5s;
    }
    .fixed_btn2:hover {
      color: #27acd9;
      background: #fff;
    }

      


    @media screen and (max-width: 768px) {
      .wrap {
        width: 90%;
      }
      .midasi {
        font-size: 3em;
      }
      input {
        width: 90%;
      }
      .name-1, .name-2 {
        width: 60%; 
        right: 30%; 
      }
      .fixed_btn, .fixed_btn2{
        width: 50px;
        padding: 0.5rem;
      }
    }

    </style>


  

    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.4.0/socket.io.js"></script>
</head>
<body>

<div class = "midasi">
  <p>chathome</p>
  
</div>

<div class="wrap">
    <ul id="messages">
    </ul>

</div>
<footer>
    <form  id="form1">
        <input type="text" name="name" class="name-2" placeholder="名前（ID）" autocomplete="off">
    </form>
  
    <form id="form">
        <input type="text" name="message" class="name-1" placeholder="message" autocomplete="off">
    </form>
    <button class="fixed_btn2" id="boto" onclick="buttonclick2()">↑</button>
  
    <button class="fixed_btn" id="boto" onclick="buttonclick()">↓</button>




</footer>
<script>
  var socket = io();
  window.scroll(0,0);
  function buttonclick(){
      let button_var = document.getElementById("Button");
      window.scroll(0,document.documentElement.scrollHeight);
  }

  
  function buttonclick2(){
      let button_var = document.getElementById("Button");
      window.scroll(0,0);
  }


  
  

  var form = document.getElementById('form');
  var form1 = document.getElementById('form1');



  form.addEventListener('submit', function(event) {

    event.preventDefault();
    var message = form.message.value;
    var name = form1.name.value;
    if (name == "") {
      var name = "匿名";
    }
    if (message) {
      socket.send(name + " : " +message);
      form.message.value = '';


    }
  });

  
  form1.addEventListener('submit', function(event){
    event.preventDefault();
  });


  var messages = document.getElementById('messages');
  var count = 0;
  socket.on('message', function(data) {
    console.log(data)
    count = count + 1
    var li = document.createElement('li');
    li.textContent = count + " | " + data;



    
    function isBottom() {
      let windowHeight = window.innerHeight;
      let scrollY = window.scrollY;
      let documentHeight = document.documentElement.scrollHeight;
      return (windowHeight + scrollY) >= documentHeight;
    }
    window.addEventListener("scroll", function() {
      if (isBottom()) {
           console.log("top");
      }
    });
    
    if(isBottom()){
      console.log(isBottom());
      messages.appendChild(li);
      window.scroll(0,document.documentElement.scrollHeight);
    }else{
      messages.appendChild(li);
    }
    



    
  });
  
  

</script>
</body>
</html>


"""
  else:
    return redirect('/')









@socketio.on('connect')
def on_connect():
  print('Client connected ' + request.sid)
  sid = request.sid
  with open("message.txt", "r") as f:
    for line in f:
      line = line.strip()
      emit("message", line, room=sid, broadcast=True)
  f.close()



@socketio.on('message')
def on_message(data):

  print('Received message: ' + data)

  emit('message', data, broadcast=True)
  with open("message.txt", 'a') as f:
    f.write(data + '\n')



@socketio.on('disconnect')
def on_disconnect():
  print('Client disconnected')



if __name__ == '__main__':
  if not os.path.exists("message.txt"):
    open("message.txt", 'w').close()
  socketio.run(app, debug=True, host='0.0.0.0', port=5000)
