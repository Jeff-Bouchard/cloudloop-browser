from eventlet import wsgi
import eventlet
eventlet.monkey_patch()
from siaskynet import SkynetClient
from flask.json import jsonify
from flask import Flask, make_response, request, send_file
from http import HTTPStatus

from uuid import uuid4
import io
import os
from airtable import Airtable
from time import time

app = Flask(__name__)

airtable = Airtable('appHcObTX28Vj70uM', 'Loops', api_key=os.environ['AIRTABLE_KEY'])


def build_response(status, message, data=None):
    if data is None:
        data = {}
    return make_response(jsonify({'status': status, 'message': message, 'data': {'results': data}}), status)

@app.route('/healthz/ready/', methods=['GET'])
def healthz_ready():
    return make_response(jsonify({'status': 'ok', 'message': 'ok', 'data': {'results': 'ok'}}), 200)

@app.route('/loops', methods=['GET'])
def loop_browser():
    try:
        request_args = request.args
        session = request_args['session']
        loops = airtable.get_all(formula=f"{{session}}='{session}'")
        return build_response(status=HTTPStatus.OK, message=f"Got loops for session {session}", data=loops)
    except KeyError as e:
        return build_response(status=HTTPStatus.NOT_ACCEPTABLE,
                              message=f'Missing parameter {e}')


wsgi.server(eventlet.listen(('', 56003)), app)
