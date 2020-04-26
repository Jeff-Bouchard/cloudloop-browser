from flask import Flask, render_template, request, abort
from flask.json import jsonify
from flask_socketio import SocketIO
from siaskynet import Skynet
from uuid import uuid4
#import redis
import logging

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


_log = logging.getLogger()

sessions = {}

@app.route('/create', methods=['POST'])
def create():
    if not request.json or not 'username' in request.json or not 'session_name' in request.json:
        abort(400)
    else:
        session_name = request.json['session_name']
        username = request.json['username']
        if session_name in sessions:
            abort(403)
        else:
            sessions[session_name] = {
                "session_name":session_name,
                "generation":0,
                "users":[username],
                "loops":{}
            }
            return jsonify(sessions[session_name])

@app.route('/add_loop', methods=['POST'])
def add_loop():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        wav_link = request.json['wav_link']
        tag = request.json['tag']
    except Exception as e:
        _log.error(e)
        abort(400)
    try:
        session = sessions[session_name]
    except Exception as e:
        _log.error(e)
        abort(404)
    if len(session['loops']) > 0:
        new_loop_id = max(session['loops']) + 1
        if wav_link in [session['loops'][loop]['link'] for loop in session['loops']]:
            abort(403)
    else:
        new_loop_id = 0
    session['loops'][new_loop_id] = {"link":wav_link,"creator":username,"tag":tag}
    session['generation']+=1
    #broadcast socket update
    return jsonify(sessions[session_name])

@app.route('/update_loop', methods=['POST'])
def update_loop():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        loop_id = request.json['loop_id']
        wav_link = request.json['wav_link']
    except Exception as e:
        _log.error(e)
        abort(400)
    try:
        session = sessions[session_name]
        loop = session[session_name]['loops'][loop_id]
    except Exception as e:
        _log.error(e)
        abort(404)
    creator = session[session_name]['loops'][loop_id]['creator']
    if creator != username:
        _log.warning(f'Unauthorized: {username} attempted update of {creator}\'s loop {loop_id}.')
        abort(403)
    else:
        session[session_name]['loops'][loop_id]['link'] = wav_link
        _log.info(f'{session_name} {loop_id} updated: {wav_link}')
        return jsonify(sessions[session_name])

@app.route('/delete_loop', methods=['POST'])
def delete_loop():
    try:
        username = request.json['username']
        session_name = request.json['session_name']
        loop_id = request.json['loop_id']
    except Exception as e:
        _log.error(e)
        abort(400)
    try:
        session = sessions[session_name]
        loop = session[session_name]['loops'][loop_id]
    except Exception as e:
        _log.error(e)
        abort(404)
    creator = session[session_name]['loops'][loop_id]['creator']
    if creator != username:
        _log.warning(f'Unauthorized: {username} attempted delete of {creator}\'s loop {loop_id}.')
        abort(403)
    else:
        del session[session_name]['loops'][loop_id]
        _log.info(f'Deleted loop {loop_id} from {session_name}')
        return jsonify(sessions[session_name])
"""
THIS RUNS ON GCP - https://us-central1-cloudloop-175221.cloudfunctions.net/upload-to-skynet
@app.route('/skynet', methods=['POST'])
def upload_to_skynet():
    data_to_upload = request.get_data()
    filename = f'cloudloop-file-{uuid4()}.wav'
    with open(filename, 'wb') as f:
        f.write(data_to_upload)
    skylink = Skynet.upload_file(filename)
    print("Upload successful, skylink: " + skylink)
    return jsonify(skylink)
"""

@app.route('/links', methods=['GET'])
def links():
    try:
        session_name = request.args.get('session')
        wav_links = [loop['link'] for loop in sessions[session_name]['loops']]
    except Exception as e:
        _log.error(e)
    render_template("links.html", wav_links=wav_links)

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
