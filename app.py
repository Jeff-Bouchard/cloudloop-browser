import eventlet
eventlet.monkey_patch()
from flask import Flask, render_template, request, make_response
from flask.json import jsonify
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from http import HTTPStatus
from userstore import UserStore
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp

import json

from loop import Loop
from sessionstore import SessionStore, SessionAlreadyExistsException, SessionNotFoundException, SessionActionNotPermittedException
from serde import CloudLoopDecoder, CloudLoopEncoder

import logging

#SECRET
JWT_SECRET_KEY=b'|\xc7\xf6E9&\xf9vf`N(\xe3x.\xd4R\xc1|<_\xddJ\xa7'

app = Flask(__name__)

#SECRET
app.config['SECRET_KEY'] = 'secret!'

#SECRET (defined above)
app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.json_decoder = CloudLoopDecoder
app.json_encoder = CloudLoopEncoder
app.config['REDIS_HOST'] = 'redis'

print(app.config['REDIS_HOST'])

socketio = SocketIO(app, cors_allowed_origins="*", message_queue=f'redis://{app.config["REDIS_HOST"]}:6379', async_mode="eventlet")


_log = logging.getLogger()

sessions = SessionStore(flush=False)
users = UserStore(flush=False)

def authenticate(username, password):
    if users.check_password(username, password):
        return users.get_user(username)

def identity(payload):
    username = payload['sub']
    return users.get_user(username)

jwt = JWT(app, authenticate, identity)

def build_response(status, message, data=None):
    if data is None:
        data = {}
    return make_response(jsonify({'status': status, 'message': message, 'data': {'results': data}}), status)


def not_permitted_response(message='Operation not permitted.'):
    return build_response(HTTPStatus.FORBIDDEN, message=message)

@app.route('/healthz/ready/', methods=['GET'])
def healthz():
    result = sessions.healthz_check()
    if result:
        return build_response(HTTPStatus.OK, message="Session server communicating with memstore")
    else:
        return build_response(HTTPStatus.INTERNAL_SERVER_ERROR, message="Session server cannot communicate with memstore.")

@app.route('/auth/login', methods=['POST'])
def login_user():
    try:
        username = request.json['username']
        password = request.json['password']
        user = users.get_user(username)
        if user and users.check_password(username, password):
            auth_token = user.encode_auth_token(user.username)
            return build_response(HTTPStatus.OK, f'User {username} logged in.', auth_token.decode())
        else:
            return build_response(HTTPStatus.UNAUTHORIZED, f'Incorrect login details.')
    except Exception as e:
        _log.error(e)
        return build_response(HTTPStatus.BAD_REQUEST, f'Bad Request. {e}')


@app.route('/register_user', methods=['POST'])
def register_user():
    try:
        username = request.json['username']
        email = request.json['email']
        password = request.json['password']
        if not users.get_user(username):
            users.create_user(username=username, email=email, password=password)
            new_user = users.get_user(username)
            token = new_user.encode_auth_token(username)
            print("success registering")
            return build_response(HTTPStatus.OK, f'User {username} created.', token.decode())
        else:
            return build_response(HTTPStatus.CONFLICT, f'{username} already exists.')
    except KeyError as e:
        print("error Creating user: " + str(e))
        return build_response(HTTPStatus.BAD_REQUEST, 'Keys username, email, password not present in request exist.')
    except TypeError as e:
        print(f'typeerror: {str(e)}')
        return build_response(HTTPStatus.NOT_ACCEPTABLE, 'Content type not acceptable.')
    except Exception as e:
        return build_response(status=HTTPStatus.NOT_ACCEPTABLE,
                              message='Other error: ' + str(e))

@app.route('/user', methods=['GET'])
@jwt_required()
def get_user():
    try:
        params = request.args
        username = params['username']
        user = users[username]
        if user is not None:
            return build_response(status=HTTPStatus.OK,
                                message=f'Got user {username}.',
                                data=user)
        else:
            return build_response(status=HTTPStatus.NOT_FOUND,
                                  message=f'User {username} not found.')
    except Exception as e:
        print("error " + str(e))
        return build_response(HTTPStatus.BAD_REQUEST, message=str(e))


@app.route('/session', methods=['POST'])
@jwt_required()
def create_session():
    try:
        username = request.json['username'] # deprecate username
        session_name = request.json['session_name']
        private = request.json['private_session']
        identity = current_identity.username
        sessions.create_session(session_name, identity, private)
        users.join_session(identity, session_name)
        return build_response(status=HTTPStatus.OK,
                              message=f'Session {session_name} created.',
                              data=sessions[session_name])
    except KeyError as e:
        return build_response(status=HTTPStatus.NOT_ACCEPTABLE,
                              message=f'Missing parameter {e}')
    except SessionAlreadyExistsException as e:
        return build_response(status=HTTPStatus.FORBIDDEN,
                              message=f'Session already exists.')

@app.route('/deleteSession', methods=['POST'])
@jwt_required()
def delete_session():
    try:
        username = current_identity.username
        session_name = request.json['session_name']
        res = sessions.delete_session(session_name, username)
        return build_response(status=HTTPStatus.OK,
                              message=f'Session {session_name} deleted.',
                              data=res)
    except KeyError as e:
        return build_response(status=HTTPStatus.NOT_ACCEPTABLE,
                              message=f'Missing parameter {e}')
    except Exception as e:
        _log.error(f'{e}')
        return build_response(status=HTTPStatus.BAD_REQUEST,
                              message=f'Bad Request!')



@app.route('/join', methods=['POST'])
@jwt_required()
def join():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        inviter = current_identity.username
        if sessions.join_session(session_name, username, inviter):
            users.join_session(username, session_name)
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


@app.route('/publicSessionHeaders', methods=['GET'])
@jwt_required()
def get_public_session_headers():
    session_headers = sessions.get_public_session_headers()
    return build_response(status=HTTPStatus.OK,
                          message=f'Got {len(session_headers)} public session headers.',
                          data=session_headers)


@app.route('/friends_sessions', methods=['GET'])
@jwt_required()
def get_friends_sessions():
    try:
        username = current_identity.username
        friends = users.get_friends(username)
        session_names = []
        for friend in friends:
            session_names.extend(users.get_user_sessions(friend))
        friend_session_headers = sessions.get_sessions_headers(session_names)
        return build_response(status=HTTPStatus.OK,
                              message=f'Got {len(friend_session_headers)} friends sessions.',
                              data=friend_session_headers)
    except Exception as e:
        msg = f'An unknown error occurred while getting friends sessions: {e}'
        _log.error(msg)
        return build_response(HTTPStatus.NOT_ACCEPTABLE, msg, [])


@app.route('/sessions', methods=['GET'])
@jwt_required()
def get_sessions_for_user():
    try:
        username = current_identity.username
        session_names = users.get_user_sessions(username)
        if len(session_names) == 0:
            valid_sessions = []
        else:
            sessions_map = sessions.get_sessions_data(session_names)
            valid_sessions = list(filter(lambda p: p is not None, sessions_map))
        msg = f'Retrieved {len(valid_sessions)} sessions for user {username}'
        _log.info(msg)
        return build_response(status=HTTPStatus.OK,
                          message=msg,
                          data={'sessions': valid_sessions})
    except Exception as e:
        _log.error(f"Error retrieving user: {e}")



@app.route('/session', methods=['GET'])
@jwt_required()
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
@jwt_required()
def add_loop():
    try:
        username = current_identity.username
        session_name = request.json['session_name']
        wav_link = request.json['wav_link']
        hash = request.json['hash']
        # Do some sort of hashing on the contents... sia does this for us so maybe just retrieve
        loop = Loop(creator=username, link=wav_link, hash=hash)
        sessions.add_loop(session_name, username, loop)
        session_data = sessions[session_name]
        session_json = json.dumps(session_data, cls=CloudLoopEncoder)
        socketio.emit("state_update", session_json, room=session_name, broadcast=True)
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


@app.route('/reserve_slot', methods=['POST'])
@jwt_required()
def reserve_slot():
    try:
        session_name = request.json['session_name']
        new_id = request.json['new_id']
        username = current_identity.username
        slot = sessions.reserve_slot(session_name, username, new_id)
        session_data = sessions[session_name]
        session_json = json.dumps(session_data, cls=CloudLoopEncoder)
        socketio.emit("state_update", session_json, room=session_name, broadcast=True)
        return build_response(HTTPStatus.OK,
                       message=f'Slot {slot} in {session_name} reserved by {username}',
                       data=slot)
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
@jwt_required()
def update_slot():
    try:
        username = current_identity.username
        session_name = request.json['session_name']
        wav_link = request.json['wav_link'] #wav_link for now
        slot_number = request.json['slot_number']
        hash = request.json['hash']
        loop = sessions.get_loop_from_library(session_name, wav_link)
        if loop is None:
            loop = Loop(creator=username, link=wav_link, hash=hash)
            sessions.add_loop(session_name=session_name, username=username, loop=loop)
        sessions.update_slot(session_name, username, slot_number, loop=loop)
        session_data = sessions[session_name]
        session_json = json.dumps(session_data, cls=CloudLoopEncoder)
        socketio.emit("state_update", session_json, room=session_name, broadcast=True)
        return build_response(status=HTTPStatus.OK,
                              message=f'Slot updated',
                              data=session_data)
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
@jwt_required()
def delete_slot():
    try:
        username = current_identity.username
        session_name = request.json['session_name']
        slot_number = request.json['slot_number']
        sessions.delete_slot(session_name, username, slot_number)
        session_data = sessions[session_name]
        session_json = json.dumps(session_data, cls=CloudLoopEncoder)
        socketio.emit("state_update", session_json, room=session_name, broadcast=True)
        return build_response(status=HTTPStatus.OK,
                              message=f'Slot {session_name}/{slot_number} deleted.',
                              data=session_data)
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
        links = [loop.link for loop in sessions[session_name]['library']]
        return render_template("links.html", session=session_name, links=links)
    except Exception as e:
        _log.error(e)

@app.route('/add_friend', methods=['POST'])
@jwt_required()
def add_friend():
    try:
        username = current_identity.username
        friend_username = request.json['friend_username']
        result = users.add_friend_mutual(username, friend_username)
        friends = users.get_friends(username)
        if result:
            msg = f'{username} added {friend_username} as friend successfully.'
            return build_response(HTTPStatus.OK, msg, friends)
        else:
            msg = f'{username} could not add {friend_username} as friend - You are probably already friends!'
            return build_response(HTTPStatus.NOT_ACCEPTABLE, msg, friends)
    except Exception as e:
        msg = f'An unknown error occurred: {e}'
        return build_response(HTTPStatus.BAD_REQUEST, msg, {})

@app.route('/search_users', methods=['GET'])
@jwt_required()
def search_users():
    try:
        query = request.args.get('search_query')
        result = users.search_users(query)
        msg = f'Found {len(result)} keys for user search query: {query}'
        _log.info(msg)
        return build_response(HTTPStatus.OK, msg, result)
    except KeyError as e:
        msg = f'Error issuing search. Invalid query: {e}'
        return build_response(HTTPStatus.BAD_REQUEST, msg, [])
    except Exception as e:
        msg = f'Error in search: {e}'
        _log.error(msg)
        return build_response(HTTPStatus.BAD_REQUEST, msg, [])

@app.route('/friends', methods=['GET'])
@jwt_required()
def get_friends():
    try:
        username = current_identity.username
        result = users.get_friends(username)
        msg = f'Got {len(result)} friends for user {username}'
        return build_response(HTTPStatus.OK, msg, result)
    except Exception as e:
        msg = f'An unknown error occurred while getting friends: {e}'
        _log.error(msg)
        return build_response(HTTPStatus.NOT_ACCEPTABLE, msg, [])


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


@socketio.on('joinSession')
def on_join(data):
    try:
        print(f"JOIN SESSION {data}")
        username = data['username']
        session_name = data['session_name']
        join_room(session_name)
        sessions.user_connect(username=username, session_name=session_name)
        jsondata = json.dumps(sessions[session_name], cls=CloudLoopEncoder)
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
        jsondata = json.dumps(sessions[session_name], cls=CloudLoopEncoder)
        emit("state_update", jsondata, room=session_name, broadcast=True)
        emit('message', username + ' has left the session ' + session_name, room=session_name)
    except KeyError as e:
        _log.info("username and room not found.")


@socketio.on('disconnect')
def test_disconnect():
    print('Client disconnected')


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=56000, log_output=True)

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
