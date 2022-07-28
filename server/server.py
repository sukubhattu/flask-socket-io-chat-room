from flask import Flask,jsonify
from flask_socketio import SocketIO, join_room, leave_room
from flask_cors import CORS

app = Flask(__name__)
CORS(app,resources={r"/*":{"origins":"*"}})
socketio = SocketIO(app, cors_allowed_origins="*")


@app.route("/")
def index():
    data = {'data':'Server is running'}
    return jsonify(data)

# Join room
@socketio.on('join_room')
def join_chat_room(data):
    join_room(data['room'])
    socketio.emit('join_room_announcement', data, room=data['room'])
    
# leave room
@socketio.on('leave_room')
def leave_chat_room(data):
    leave_room(data['room'], data['username'])
    socketio.emit('leave_room_announcement', data, room=data['room'])

@socketio.on('send_message')
def send_message(data):
    socketio.emit('receive_message', data, room=data['room'])

if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)
