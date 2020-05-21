#THIS RUNS ON GCP - https://us-central1-cloudloop-175221.cloudfunctions.net/upload-to-skynet
# (c) Zip Technologies LLC 2020
from siaskynet import Skynet
from uuid import uuid4
from flask.json import jsonify
from flask import request

from app import app

def get_skynet_upload_options():
    return type('obj', (object,), {
        'portal_url': 'https://skynet.cloudloop.io',
        'portal_upload_path': 'skynet/skyfile',
        'portal_file_fieldname': 'file',
        'portal_directory_file_fieldname': 'files[]',
        'custom_filename': ''
    })


@app.route('/skynet', methods=['POST'])
def upload_to_skynet():
    data_to_upload = request.get_data()
    opts = get_skynet_upload_options()
    filename = f'cloudloop-file-{uuid4()}.wav'
    with open(filename, 'wb') as f:
        f.write(data_to_upload)
    skylink = Skynet.upload_file(filename, opts)
    print("Upload successful, skylink: " + skylink)
    return jsonify(skylink)