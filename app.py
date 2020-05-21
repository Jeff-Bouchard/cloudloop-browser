import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request
from flask.json import jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from http import HTTPStatus
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp


import json



from loop import Loop, LoopEncoder, LoopDecoder
from sessionstore import SessionStore, SessionAlreadyExistsException, SessionNotFoundException, SessionActionNotPermittedException

import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.json_decoder = LoopDecoder
app.json_encoder = LoopEncoder
app.config['REDIS_HOST'] = 'cloudloop-rejson'
socketio = SocketIO(app, cors_allowed_origins="*", message_queue=f'redis://{app.config["REDIS_HOST"]}:6379')


_log = logging.getLogger()

sessions = SessionStore(flush=True)

def build_response(status, message, data={}):
    return jsonify({'status':status, 'message':message, 'data':{'results':data}})

def not_permitted_response(message='Operation not permitted.'):
    return build_response(HTTPStatus.FORBIDDEN, message=message)

"""
@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        userstore.create_user(username, email, password)
"""

@app.route('/session', methods=['POST'])
def create_session():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        private = request.json['private_session']
        sessions.create_session(session_name, username, private)
        return build_response(status=HTTPStatus.OK,
                              message=f'Session {session_name} created',
                              data=sessions[session_name])
    except KeyError as e:
        return build_response(status=HTTPStatus.OK,
                              message=f'Missing parameter {e}')
    except SessionAlreadyExistsException as e:
        return build_response(status=HTTPStatus.FORBIDDEN,
                              message=f'Session already exists.')

@app.route('/join', methods=['POST'])
def join():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        inviter = request.json['inviter']
        if sessions.join_session(session_name, username, inviter):
            return build_response(status=HTTPStatus.OK,
                                  message=f'{username} has joined session {session_name}',
                                  data=sessions[session_name])
        else:
            return build_response(status=HTTPStatus.NOT_ACCEPTABLE,
                                  message=f'{username} failed to join session {session_name}')
    except KeyError as e:
        return build_response(status=HTTPStatus.BAD_REQUEST,
                              message=f'Missing parameter {e}') # TODO Test this
    except SessionActionNotPermittedException as e:
        return build_response(status=HTTPStatus.FORBIDDEN,
                              message='Operation not permitted.')

@app.route('/sessionNames', methods=['GET'])
def get_session_names():
    session_names = sessions.get_session_names()
    return build_response(status=HTTPStatus.OK,
                          message=f'Got {len(session_names)} session names.',
                          data=session_names)

@app.route('/session', methods=['GET'])
def get_session():
    try:
        params = request.args
        session_name = params['session_name']
        session = sessions[session_name]
        return build_response(status=HTTPStatus.OK,
                              message=f'Got session {session_name}.',
                              data=session)
    except KeyError as e:
        return build_response(status=HTTPStatus.BAD_REQUEST,
                              message='Please specify a session_name.')
    except SessionNotFoundException as e:
        return build_response(status=HTTPStatus.NOT_FOUND,
                              message='Session not found.')

@app.route('/add_loop', methods=['POST'])
def add_loop():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        wav_link = request.json['wav_link']
        hash = request.json['hash']
        # Do some sort of hashing on the contents... sia does this for us so maybe just retrieve
        loop = Loop(creator=username, link=wav_link, hash=hash)
        sessions.add_loop(session_name, username, loop)
        session_data = sessions[session_name]
        session_json = json.dumps(session_data, cls=LoopEncoder)
        socketio.emit("state_update", session_json, broadcast=True)
        _log.info(session_data)
        return build_response(status=HTTPStatus.OK,
                              message=f'Loop {session_name}/{loop.link} created',
                              data=session_data)
    except KeyError as e:
        return build_response(status=HTTPStatus.BAD_REQUEST,
                              message=f'Missing parameters in request.')
    except SessionActionNotPermittedException as e:
        return build_response(status=HTTPStatus.FORBIDDEN,
                              message=f'Operation forbidden: {e}')
    except SessionNotFoundException as e:
        return build_response(status=HTTPStatus.NOT_FOUND,
                              message=f'Session {session_name} not found.')


@app.route('/add_slot', methods=['POST'])
def add_slot():
    try:
        session_name = request.json['session_name']
        username = request.json['username']
        slot = sessions.add_slot(session_name, username)
        return build_response(HTTPStatus.OK,
                       message=f'Slot {slot} created.',
                       data=jsonify(sessions[session_name]))
    except KeyError as e:
        return build_response(HTTPStatus.NOT_FOUND,
                       message=f'Missing parameter {e}')
    except SessionActionNotPermittedException as e:
        return build_response(HTTPStatus.FORBIDDEN,
                       message=f'Operation forbidden {e}')
    except SessionNotFoundException:
        return build_response(status=HTTPStatus.NOT_FOUND,
                              message=f'Session {session_name} not found.')


@app.route('/update_slot', methods=['POST'])
def update_slot():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        loop_id = request.json['loop_id'] #wav_link for now
        slot_number = request.json['slot_number']
        loop = sessions.get_loop_from_library(session_name, loop_id)
        if loop is None:
            sessions.add_loop(session_name, username,)
        sessions.update_slot(session_name, username, slot_number, loop=loop)
        return build_response(status=HTTPStatus.OK,
                              message=f'Slot updated',
                              data=jsonify(sessions[session_name]))
    except KeyError as e:
        _log.error(e)
        return build_response(status=HTTPStatus.BAD_REQUEST,
                              message=f'Missing parameter {e}')
    except SessionActionNotPermittedException as e:
        _log.error(e)
        return build_response(status=HTTPStatus.FORBIDDEN,
                              message=f'Operation not permitted {e}')
    except SessionNotFoundException as e:
        return build_response(status=HTTPStatus.NOT_FOUND,
                              message=f'Session {session_name} not found.')



@app.route('/delete_slot', methods=['POST'])
def delete_slot():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        slot_number = request.json['slot_number']
        sessions.delete_slot(session_name, username, slot_number)
        return build_response(status=HTTPStatus.OK,
                              message=f'Slot {session_name}/{slot_number} deleted.',
                              data=jsonify(sessions[session_name]))
    except KeyError as e:
        _log.error(e)
        return build_response(status=HTTPStatus.BAD_REQUEST,
                              message=f'Parameter missing: {e}')
    except SessionActionNotPermittedException as e:
        _log.error(e)
        return build_response(status=HTTPStatus.FORBIDDEN,
                              message='Operation not permitted.')
    except SessionNotFoundException as e:
        _log.error(e)
        return build_response(status=HTTPStatus.NOT_FOUND,
                              message=f'Session {session_name} not found.')

@app.route('/links', methods=['GET'])
def links():
    try:
        session_name = request.args.get('session_name')
        links = sessions[session_name]['loops']['library']
        return render_template("links.html", wav_links=links)
    except Exception as e:
        _log.error(e)



@socketio.on('message')
def handle_message(msg):
    print('Message: ' + msg)
    send(msg, broadcast=True)

@socketio.on('json')
def handle_json(json):
    print('Message: ' + json)

@socketio.on('ack')
def handle_ack(ack):
    print('Got it: ' + ack)

@socketio.on('connect')
def send_ack():
    print("client connect")
    emit("message", "Connected Successfully.")

@socketio.on('joinSession')
def on_join(data):
    try:
        print(f"JOIN SESSION {data}")
        username = data['username']
        session_name = data['session_name']
        join_room(session_name)
        sessions.user_connect(username=username, session_name=session_name)
        jsondata = json.dumps(sessions[session_name], cls=LoopEncoder)
        emit("state_update", jsondata, room=session_name, broadcast=True)
        emit('message', username + ' has joined the session ' + session_name, room=session_name)
    except KeyError as e:
        _log.info("username and room not found.")

@socketio.on('leaveSession')
def on_leave(data):
    try:
        username = data['username']
        session_name = data['session_name']
        leave_room(session_name)
        sessions.user_disconnect(username=username, session_name=session_name)
        send(username + ' has left the session ' + session_name, room=session_name)
    except KeyError as e:
        _log.info("username and room not found.")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, log_output=True)

"""
FROM CLIENT:
LOOP_ADD
{"loop_add": {
    "session_id":"my_session",
    "wav_link: "wav_link1",
}

FROM SERVER:
INIT:
{
    "session_id":"my_session"
    "generation":0,
    "users":['user1'],
    "loops":[]
}

RECORDING:
{   "session_id":"my_session",
    "generation":3,
    "users": ["username1", "username2"],
    "loops": {1:{"link":"wav_link1","creator":"username1"},
              2:{"link":"wav_link2","creator":"username2"},
              3:{"link":None, "creator":"username3"}}
}
LOOP ADDED:
{   "session_id":"my_session",
    "generation":3,
    "users": ["username1", "username2"],
    "loops": {1:{"link":"wav_link1","creator":"username1"},
              2:{"link":"wav_link2","creator":"username2"},
              3:{"link":"wav_link3", "creator":"username3"}}
}



@socketio.on('loop_add', namespace=)
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username = ' has entered the session.', session=session)
"""
