from eventlet import wsgi
import eventlet
eventlet.monkey_patch()
from siaskynet import SkynetClient
from flask.json import jsonify
from flask import request, Flask, make_response
from uuid import uuid4
import wavy
from airtable import Airtable
import os

import time

app = Flask(__name__)

PORTAL_URL = 'https://skynet.cloudloop.io'

def get_wav_data(filename):
    print(f'Opening wav file: {filename}')
    data = {}
    f = wavy.info(filename)
    data['channels'] = f.n_channels
    data['samplewidth'] = f.sample_width
    data['samplerate'] = f.framerate
    data['samples'] = f.n_frames
    print(f'Got wav data from {filename}')
    return data



def get_upload_options():
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

@app.route('/upload', methods=['post'])
def upload():
    """
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    # upload
    start = time.time()
    data_to_upload = request.get_data()
    creator = request.headers.get("CloudLoop-Loop-Creator")
    session = request.headers.get("CloudLoop-Loop-Session")
    print(f'Got {len(data_to_upload)} bytes to upload - creator: {creator}, session: {session}')
    filename = f'/tmp/cloudloop-file-{uuid4()}.wav'
    with open(filename, 'wb') as f:
        f.write(data_to_upload)
    finish = time.time()
    print(f'Wrote {filename} in {finish-start}')
    file_data = get_wav_data(filename)
    print(f'Uploading file {filename} : {file_data}')
    begin_upload = time.time()
    skylink = client.upload_file(filename, get_upload_options())
    finish_upload = time.time()
    print(f'Finished uploading {filename} to skynet in {finish_upload-begin_upload}')
    airtable_records =  {'link': skylink,
                         'samples': file_data['samples'],
                         'sample_rate': file_data['samplerate'],
                         'bit_depth': file_data['samplewidth'],
                         'channels': file_data['channels'],
                         'creator': creator,
                         'session': session}
    print(f'Analyzed file {filename} : {airtable_records}')
    start_airtable = time.time()
    airtable = Airtable('appHcObTX28Vj70uM', 'Loops', api_key=os.environ['AIRTABLE_KEY'])
    airtable.insert(airtable_records)
    end_airtable = time.time()
    print(f'Processed airtable record in {end_airtable-start_airtable}')
    print("Upload successful, skylink: " + skylink)
    return jsonify(skylink)

wsgi.server(eventlet.listen(('', 56001)), app)
