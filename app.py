from flask import Flask, render_template, request, abort
from flask.json import jsonify
from flask_socketio import SocketIO, send, emit
import datetime
import flask_apispec

from sessionstore import SessionStore, Loop, SessionAlreadyExistsException, SessionNotFoundException, SessionActionNotPermittedException

import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['ENABLE_SKYNET_UPLOAD'] = False
socketio = SocketIO(app)


_log = logging.getLogger()

sessions = SessionStore()

@app.route('/session', methods=['POST'])
def create_session():
    try:
        print(request.json)
        username = request.json['username']
        session_name = request.json['session_name']
        private = request.json['private_session']
        sessions.create_session(session_name, username, private)
        return jsonify(sessions[session_name])
    except KeyError as e:
        _log.error(f'{e}')
        abort(400)
    except SessionAlreadyExistsException as e:
        _log.error(e)
        abort(403)

@app.route('/join', methods=['POST'])
def join():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        inviter = request.json['inviter']
        sessions.join_session(session_name, username, inviter)
        return jsonify(sessions['session_name'])
    except KeyError as e:
        abort(400)
    except SessionActionNotPermittedException as e:
        abort(403)

@app.route('/sessions', methods=['GET'])
def get_sessions():
    return jsonify(sessions.get_session_names())

@app.route('/session', methods=['GET'])
def get_session():
    try:
        session_name = request.json['session_name']
        return jsonify(sessions.get_session(session_name))
    except KeyError as e:
        abort(404)
    except SessionNotFoundException as e:
        abort(404)

@app.route('/add_loop', methods=['POST'])
def add_loop():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        wav_link = request.json['wav_link']
        # Do some sort of hashing on the contents... sia does this for us so maybe just retrieve
        loop = Loop(creator=username, session_name=session_name, link=wav_link, hash=None)
        sessions.add_loop(session_name, username, loop)
        return jsonify(sessions['session_name'])
    except KeyError as e:
        abort(400)
    except SessionActionNotPermittedException as e:
        abort(403)
    except SessionNotFoundException as e:
        abort(404)


@app.route('/add_slot', methods=['POST'])
def add_slot():
    try:
        session_name = request.json['session_name']
        username = request.json['username']
        sessions.add_slot(session_name, username)
        return jsonify(sessions['session_name'])
    except KeyError as e:
        abort(400)
    except SessionActionNotPermittedException as e:
        abort(403)
    except SessionNotFoundException:
        abort(404)


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
        return jsonify(sessions['session_name'])
    except KeyError as e:
        _log.error(e)
        abort(400)
    except SessionActionNotPermittedException as e:
        _log.error(e)
        abort(403)
    except SessionNotFoundException as e:
        abort(404)



@app.route('/delete_slot', methods=['POST'])
def delete_slot():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        slot_number = request.json['slot_number']
        sessions.delete_slot(session_name, username, slot_number)
        return jsonify(sessions['session_name'])
    except KeyError as e:
        _log.error(e)
        abort(400)
    except SessionActionNotPermittedException as e:
        _log.error(e)
        abort(403)
    except SessionNotFoundException as e:
        _log.error(e)
        abort(404)

@app.route('/links', methods=['GET'])
def links():
    try:
        session_name = request.args.get('session_name')
        links = sessions[session_name]['loops']['library']
        return render_template("links.html", wav_links=links)
    except Exception as e:
        _log.error(e)

@socketio.on('connect', namespace='/test')
def test_connect():
    emit('my response', {'data': 'Connected'})

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if app.config['ENABLE_SKYNET_UPLOAD']:
    import skynet

if __name__ == '__main__':
    socketio.run(app)

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
