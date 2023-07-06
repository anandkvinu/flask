from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
from random import random
from threading import Lock
thread = None
thread_lock = Lock()
app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')





def background_thread():
        print("Generating random sensor values")
        while True:
            @socketio.on('message')
            def on_message(messages):
                 print(messages)
                 consumption = messages#round(random() * 100, 3)
# Emit the consumption value to connected clients
                 socketio.emit('consumption', {'consumption': consumption})
                 socketio.sleep(1)
                 print("emitted")

def process_message(message):
    # Example function to process the message and retrieve the consumption value
    # Modify this function according to your data format and processing logic

    return message['consumption']

@app.route('/toggle', methods=['POST'])
def handle_toggle():
    data = request.get_json()
    switch_id = data['switchId']
    state = data['state']
    print(f'Switch {switch_id} state: {state}')
    # Process the switch state as desired

    # For demonstration purposes, we will emit the switch state to connected clients
    socketio.emit('switch_state', {'switchId': switch_id, 'state': state}, broadcast=True)

    return 'OK'
@socketio.on('connect')
def on_connect():
    print('Client connected')
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='localhost', port=8000, allow_unsafe_werkzeug=True)
