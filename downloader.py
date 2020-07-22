from siaskynet import Skynet
from flask.json import jsonify
from flask import Flask, request, send_file
from uuid import uuid4
import io
import os
from airtable import Airtable

app = Flask(__name__)

def get_download_options():
        return type('obj', (object,), {
            'portal_url': 'https://skynet.cloudloop.io',
            'portal_upload_path': 'skynet/skyfile',
            'portal_file_fieldname': 'file',
            'portal_directory_file_fieldname': 'files[]',
            'custom_filename': ''
        })

@app.route('/', methods=['GET'])
def download():
    request_args = request.args
    skylink = request_args['skylink']
    print(f"Received request for skylink {skylink}")
    filename = f'/tmp/cloudloop-file-{uuid4()}.wav'

    Skynet.download_file(filename, skylink, get_download_options())
    print("Download successful from skylink: " + skylink)
    with open(filename, 'rb') as bites:
        return send_file(
                     io.BytesIO(bites.read()),
                     attachment_filename='cloudloop-sound.wav',
                     mimetype='audio/wav'
               )