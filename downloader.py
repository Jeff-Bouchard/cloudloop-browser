from eventlet import wsgi
import eventlet
eventlet.monkey_patch()
from siaskynet import SkynetClient
from flask.json import jsonify
from flask import Flask, make_response, request, send_file
from uuid import uuid4
import io
import os
from airtable import Airtable
from time import time

app = Flask(__name__)
PORTAL_URL = 'https://skynet.cloudloop.io'

def get_download_options():
        return {
            'portal_url': PORTAL_URL,
            'portal_upload_path': 'skynet/skyfile',
            'portal_file_fieldname': 'file',
            'portal_directory_file_fieldname': 'files[]',
            'custom_filename': ''
        }

client = SkynetClient(portal_url=PORTAL_URL)

@app.route('/healthz/ready/', methods=['GET'])
def healthz_ready():
    return make_response(jsonify({'status': 'ok', 'message': 'ok', 'data': {'results': 'ok'}}), 200)

@app.route('/download', methods=['GET'])
def download():
    request_args = request.args
    skylink = request_args['skylink']
    filename = f'/tmp/cloudloop-file-{uuid4()}.wav'    
    print(f"Received request for skylink {skylink} --> {filename}")
    start_time = time()
    client.download_file(filename, skylink, get_download_options())
    end_time = time()
    print(f"Download successful from skylink: {skylink} in {str(end_time-start_time)}")
    with open(filename, 'rb') as bites:
        return send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='cloudloop-sound.wav',
                     mimetype='audio/wav'
               )

wsgi.server(eventlet.listen(('', 56002)), app)
